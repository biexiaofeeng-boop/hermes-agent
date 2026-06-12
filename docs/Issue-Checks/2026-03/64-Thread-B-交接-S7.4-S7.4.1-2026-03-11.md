# 线程交接：S7.4 + S7.4.1 Thread-B（2026-03-11）

- 线程：B
- 分支：`codex/s7-4b-agent-direct-hardening-v1`
- 基线：`origin/master@a0f4b9b`
- 状态：DONE（本地开发 + 回归完成）

## 本线程完成项

1. 对话去噪（S7.4.1）
- 移除 Lobby 场景“模板直返”路径，模糊输入不再直接返回固定文案。
- 移除全链路尾部无条件 `[可选澄清]` 追加。
- 保留内部可观测字段：`lastLobbyClarificationNeeded`。

2. Lobby 默认边界上下文补齐（S7.4）
- 在无 active project 且缺少项目上下文时，自动补齐：
  - `missionWorkspace=<agent workspace>`
  - `workspaceRoot=<agent workspace>`
  - `cwd=<agent workspace>`
  - `missionWorkspaceSource=agent.workspace_fallback`
- 目标：确保未切项目时 AuthGate/guardrail 仍有可用边界。

3. Guardrail 审批收敛（S7.4）
- `guardrail` 模式下，破坏性命令统一进入审批链路（pending）：
  - `rm` / `truncate` / `chmod` / `chown` / `mv` / `kill` / `pkill`
- 保持既有 fatal guardrail 规则不变。

## 代码改动清单

- `nanobot/agent/loop.py`
  - 移除 Lobby 模板拦截与无条件澄清尾巴。
  - 新增 `_with_tool_context_defaults(...)` 并在消息处理/系统消息处理中使用。
- `nanobot/auth/gate.py`
  - `guardrail` 模式增加“破坏性命令 => 需要审批”判定。
  - 扩展 `_is_destructive_command(...)` 识别集合。

## 测试改动

- `tests/test_agent_loop_dialogue_mode.py`
  - 更新 Lobby 模糊输入行为预期（自然回复，不走模板直返）。
  - 新增 summarize 回复不追加 `[可选澄清]` 覆盖。
- `tests/test_project_context_router.py`
  - 更新 Lobby 模糊输入行为测试。
  - 新增 Lobby 工具上下文 fallback 覆盖（missionWorkspace/workspaceRoot/cwd）。
- `tests/test_auth_gate.py`
  - 新增 guardrail 下破坏性命令需审批测试（`rm -rf ./tmp`）。

## 回归结果

执行命令：

```bash
PYTHONPATH=/Users/sourcefire/X-lab/chimera-core-s7b \
/Users/sourcefire/X-lab/nanobot/.venv/bin/python -m unittest \
  tests.test_agent_loop_dialogue_mode \
  tests.test_project_context_router \
  tests.test_auth_gate -v
```

结果：`Ran 60 tests, OK`

## 文档回填

- `docs/ops/Agent-Direct-增量能力直测-v1.md`
  - 增加 A09 高风险验证步骤（pending id + approve 链路）
  - 增加“对话去噪黑名单”判定
- `docs/ops/Agent-Direct-测试记录-2026-03-10.md`
  - 增加 2026-03-11 复验记录
  - 关闭 OPS-AD-002/003/004
  - 状态更新为 DONE
