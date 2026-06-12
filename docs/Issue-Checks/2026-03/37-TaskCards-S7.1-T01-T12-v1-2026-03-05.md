# 任务卡：S7.1（T01 ~ T12）

- 日期：2026-03-05
- 状态：DONE（2026-03-06）

## S7.1-A 对话优先分流

### T01 新增响应模式判定器
- 文件：`nanobot/agent/loop.py`
- 目标：新增 `resolve_response_mode(...)`，输出 `chat|direct_exec|plan_confirm|mission_board`。
- DoD：不增加额外 LLM 调用；同一输入模式稳定。

### T02 Lobby 澄清改非阻塞
- 文件：`nanobot/agent/loop.py`
- 目标：替换 `_should_request_lobby_clarification` 的阻塞返回逻辑为“先答后问”。
- DoD：意图不明时仍有主回复，不再中断。

### T03 中等复杂任务默认先方案确认
- 文件：`nanobot/agent/loop.py`
- 目标：`plan_confirm` 下输出简版执行清单+确认语句，不直接跑长链工具。
- DoD：中等复杂输入不会直接进入长执行。

### T04 高复杂任务导向任务面板
- 文件：`nanobot/agent/loop.py`
- 目标：`mission_board` 下输出任务拆解（目标/步骤/风险/资源），建议分线程。
- DoD：复杂任务首轮输出结构化计划，不刷工具日志。

## S7.1-B OODA 与执行节奏

### T05 OODA 改显式触发
- 文件：`nanobot/agent/loop.py`
- 目标：仅显式触发或确认后触发 `_build_ooda_prompt`。
- DoD：普通对话与简单执行不再注入 OODA 模板。

### T06 进度播报降噪
- 文件：`nanobot/agent/loop.py`
- 目标：提高进度播报阈值（时间+步数双门槛），避免高频刷屏。
- DoD：同等任务下消息数量明显减少。

## S7.1-C 超时恢复与上下文预算

### T07 增加超时自动降载重试
- 文件：`nanobot/agent/loop.py`
- 目标：识别 LLM timeout 后执行一次“降载重试”（缩 history / 降 thinking / 关 OODA）。
- DoD：仅重试 1 次，不造成工具重放。

### T08 配置化降载参数
- 文件：`nanobot/config/schema.py`
- 目标：新增 `agents.defaults.dialogue_guard`（enable/retry/history_shrink_ratio 等）。
- DoD：默认值可保持兼容，配置可被读取。

## S7.1-D 反幻觉与可观测

### T09 执行状态标准化
- 文件：`nanobot/agent/loop.py`
- 目标：统一 `lastExecutionState` 为 `executed|planned|blocked|chat`。
- DoD：`/status` 或会话元数据可见。

### T10 工具证据约束
- 文件：`nanobot/agent/loop.py`
- 目标：若无工具证据，禁止输出“已执行完成”语义。
- DoD：执行型回复携带 evidence 摘要。

### T11 单元测试补齐
- 文件：`tests/test_agent_loop_dialogue_mode.py`（新增）
- 目标：覆盖模式判定、非阻塞澄清、超时降载、证据约束。
- DoD：新增测试通过，旧用例不回归。

### T12 文档回填
- 文件：`docs/Issue-Checks/2026-03/38-...` + `00-INDEX-2026-03.md`
- 目标：回填结果、阻塞点、最终结论（单一事实源）。
- DoD：索引与验收一致。
