# 方案设计：Executor Identity + Auth UX + Context Compression（v1）

- 日期: 2026-02-24
- 面向对象: chimera-core-codex
- 目标: 让 chimera-core 在长会话中保持“执行体优先”，并显著降低授权噪声

## 一、设计目标

1. **执行体优先**：默认行为是“围绕目标执行”，不是“围绕人格叙事对话”。
2. **授权可预期**：`session` 就是 session 语义，不因轻微参数变化反复授权。
3. **上下文可控**：长会话时模型仍能稳定调用工具并持续推进任务。
4. **可诊断可回滚**：每个优化点都有审计和开关，便于线上快速回退。

## 二、总体架构（本轮）

### 2.1 Prompt 层（T12）

新增“执行契约层”并放在 system prompt 最前：

- 优先级顺序：`Execution Contract > Safety/Auth Rules > Persona Narrative`。
- 约束：
  - 遇到可执行请求优先走工具；
  - 对话类请求才走纯文本；
  - 战略/创作模式仅在显式触发标签下进入（如 `#strategy_mode`, `#creative_mode`）。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/context.py`
- `/Users/sourcefire/X-lab/chimera-core/workspace/AGENTS.md`
- `/Users/sourcefire/X-lab/chimera-core/workspace/USER.md`
- 新增核心模板：`workspace/SOUL_CORE.md`、`workspace/IDENTITY_CORE.md`
- 同步部署拷贝策略：`/Users/sourcefire/X-lab/chimera-core/deploy/chimera_profile.sh`

### 2.2 授权层（T13）

- 修正 `session` scope 语义：从“session + paramsHash”调整为“session 内同工具复用”。
- `approve not found` 增强诊断：
  - 回显 pending topN + 最近过期请求；
  - 审计新增 `approve_not_found` 事件。
- 保持 `once/ttl/always/mission` 现有语义不变。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
- `/Users/sourcefire/X-lab/chimera-core/tests/test_auth_gate.py`

### 2.3 上下文层（T14）

- 历史消息采用“短窗 + 摘要”模式：
  - 短窗（例如 16-20 条）保留最新交互细节；
  - 长历史压缩为执行摘要（目标、已完成、阻塞、下一步）。
- 把“高情感长文本”从执行上下文降权，保留在 memory/归档。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/session/manager.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py`
- 新增测试（建议）：`/Users/sourcefire/X-lab/chimera-core/tests/test_session_context_window.py`

## 三、与 OpenClaw 的对比借鉴

### 借鉴点（建议参考）

1. 授权模型的“主机侧控制 + 明确决策词典”：
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/exec-approvals.md`
2. 聊天渠道 `/approve` 的规范化解析与权限校验：
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts`
3. 审批结果事件化（便于可视化与审计回放）：
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approval-forwarder.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/discord/monitor/exec-approvals.ts`

### 需谨慎借鉴（不建议照搬）

- OpenClaw 的多通道/多节点生态复杂度更高，不应把其完整控制面一次性搬入 chimera-core。  
- 本轮应坚持“最小变更收口”：先稳 prompt/auth/context，再扩展 UI 或跨节点流程。

## 四、兼容与回滚设计

- 建议新增 feature flags：
  - `agent.executionContract.enabled`
  - `authGate.sessionScope.ignoreParamsHash`
  - `agent.contextCompression.enabled`
- 回滚策略：
  - 任一特性出现异常可单独关闭；
  - 保持旧行为可回放，避免联调中断。

## 五、验收标准（总）

1. 连续 20 轮混合会话下，执行请求仍稳定触发工具调用。  
2. `session` scope 授权后，同会话同工具不同参数不再重复申请（危险命令策略不变）。  
3. `approve not found` 返回可操作提示（pending/expired/命令格式建议）。  
4. 回归：`bash deploy/chimera_core_test.sh` 全绿。
