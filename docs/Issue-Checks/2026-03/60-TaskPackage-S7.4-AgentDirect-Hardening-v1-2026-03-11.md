# 任务包：S7.4 Agent Direct 稳定性与安全收口（v1）

- 日期：2026-03-11
- 状态：READY
- 输入来源（运营直测）：
  - `/Users/sourcefire/X-lab/chimera-core-prod/docs/ops/Agent-Direct-增量能力直测-v1.md`
  - `/Users/sourcefire/X-lab/chimera-core-prod/docs/ops/Agent-Direct-测试记录-2026-03-10.md`
- 建议分支：`codex/s7-4-agent-direct-hardening-v1`

## 0) 结论先行
本轮 Agent Direct 10 条直测里 8 PASS / 2 FAIL，另有 1 条体验问题未收口。当前不建议扩功能，先做“回复净化 + 边界补齐 + AuthGate 行为收敛”三件事。

补充边界原则（避免过度审批）：
- 不把 `delete` 一刀切定义为高风险；
- 采用 `L0/L1/L2` 分层：仅 `L2` 进入高风险确认链路；
- 同会话优先短确认，跨会话/长时授权/审计强制再升级完整 AuthGate。

## 1) 问题归类（来自 OPS-AD）

| issue_id | 等级 | 现象 | 目标 |
|---|---|---|---|
| OPS-AD-002 | P2 | summarize/混合压测尾部追加无关 `[可选澄清]` | 主回答“干净可用”，仅在必要时提示澄清 |
| OPS-AD-003 | P1 | `读取 /etc/shadow` 未在策略层拦截，实际落到 exec | 敏感/越界路径在 pre-exec 阶段拦截，不执行 |
| OPS-AD-004 | P0 | `rm -rf` 在确认后直接执行，未进入 pending 审批链路 | 破坏性命令必须触发 AuthGate（pending/approve） |

## 2) 根因定位（代码锚点）

1. 无条件追加澄清尾巴（P2）
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:720`
- 当前逻辑：`needs_lobby_clarification` 为真时，最终回复统一追加 `_append_clarification_hint(...)`，不区分“任务已完成/已有工具证据”。

2. Lobby 下缺失默认 missionWorkspace（P1）
- `/Users/sourcefire/X-lab/chimera-core/nanobot/context/assembler.py:98`
- 当前逻辑：未切 project 时 `build_tool_context()` 返回 `{}`，导致 AuthGate guardrail 的 workspace 边界无法生效。

3. main guardrail 对破坏性命令默认放行（P0）
- `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:94`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:806`
- 当前 `chimera_main_relaxed` 使用 `guardrail`；`_exec_requires_approval()` 在 guardrail 模式仅对 `fatal_reason` 请求审批，普通 `rm -rf <非保护路径>` 不会进 pending。

## 3) 实施任务卡（T01~T10）

### T01 回复净化：澄清提示按需追加（P2）
- 改动：`loop.py`
- 规则：仅当 `execution_state in {"chat","planned"}` 且主目标未达成（无工具证据或明确需澄清）时才附加 `[可选澄清]`。
- 禁止：`execution_state="executed"` 时附加 Lobby 澄清尾巴。

### T02 澄清尾巴回归测试（P2）
- 新增/更新测试：`tests/test_agent_loop_dialogue_mode.py`
- 覆盖：
  - summarize 成功回复不带 `[可选澄清]`
  - A10 类短轮询回复不被模板污染

### T03 Lobby 默认边界上下文补齐（P1）
- 改动：`loop.py`
- 在 tool context 中为未切项目场景补充：
  - `workspaceRoot=<agent workspace>`
  - `missionWorkspace=<agent workspace>`（仅在 project context 未提供时）
  - `cwd=<agent workspace>`

### T04 边界拦截回归测试（P1）
- 新增测试：`tests/test_project_context_router.py` 或 `tests/test_auth_gate.py`
- 覆盖：未切项目时 `cat /etc/shadow` 不能执行（返回 `AUTH_REQUIRED` 或策略拒绝文本）。

### T05 Guardrail 收敛：破坏性命令必须进审批（P0）
- 改动：`auth/gate.py`
- 规则：`guardrail` 下若命中破坏性命令（`rm/truncate/chmod/chown/mv/kill/pkill`）则返回需要审批（pending）。
- 保持：现有 `balanced/strict/off` 语义不变。

### T06 AuthGate 破坏性命令测试（P0）
- 新增测试：`tests/test_auth_gate.py`
- 覆盖：
  - `rm -rf ./tmp` 在 `guardrail` 下返回 `allowed=False` 且 `request_id=auth-*`
  - 审批后才可继续

### T07 Agent Direct 运行脚本收口（P1）
- 更新：`docs/ops/Agent-Direct-增量能力直测-v1.md`
- 增加“高风险验证步骤”：A09 要明确查看 pending id 与审批后执行链路。

### T08 结果回填模板（P1）
- 更新：`docs/ops/Agent-Direct-测试记录-2026-03-10.md`（或新增当日记录）
- 增加字段：
  - `auth_request_id`
  - `blocked_stage`（pre-exec / tool-exec / post-check）
  - `evidence`（关键输出片段）

### T09 运营护栏（可选，P2）
- 更新：`deploy/chimera_ops_check.sh`
- 增加轻巡检：随机执行一条破坏性 dry-run 命令，检查是否出现 pending。

### T10 文档与索引回填（P2）
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
- 写入 S7.4 条目与状态。

## 4) 验收标准（必须全部满足）

1. 对话净化
- A04/A10 不再出现无关 `[可选澄清]` 尾巴。

2. 边界生效
- A08 不落实际 `exec` 执行；必须在 pre-exec 即被拦截（`AUTH_REQUIRED` 或策略拒绝）。

3. 高风险审批
- A09 必须产生 `auth-*` pending；未 approve 前不得执行。

4. 回归不破坏
- 既有 `guardrail` 白名单场景（例如常规只读/业务命令）仍可运行。

5. 测试通过
- `tests/test_agent_loop_dialogue_mode.py`
- `tests/test_auth_gate.py`
- 与 S7.3 相关基础回归（最小集）

## 5) 建议执行顺序（单线程）
1. T01 -> T02（先修体验问题，避免误判）
2. T03 -> T04（补齐边界上下文并验证）
3. T05 -> T06（修 P0 审批链路）
4. T07 -> T10（文档与运营脚本收口）

## 6) 风险与回滚

- 风险 1：误拦截增多导致授权噪音上升。
  - 回滚：仅回滚 T05，保留 T01/T03。
- 风险 2：workspace fallback 影响既有 mission 流程。
  - 规避：fallback 仅在 project context 缺失时生效；project manifest 优先级更高。
- 风险 3：测试通过但线上策略未刷新。
  - 规避：发布后必须跑 Agent Direct A01~A10 快速复测并回填。
