# 09-TaskCards-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09

## 分支与目录约束

- repo: `/Users/sourcefire/X-lab/chimera-core`
- base branch: `master`
- working branch: `codex/s10c2-chat-surface-render-policy-v1`

优先修改目录：

- `nanobot/agent/loop.py`
- `nanobot/agent/interaction_shell.py`
- `tests/test_ooda_context_packets.py`

必要时允许补充：

- `nanobot/channels/telegram.py`
- `nanobot/taskops/*`
- `nanobot/trace/*`

## T01 Chat Surface 分层

- 明确三层：`dialogue` / `compact_receipt` / `trace_log`
- 约束外部 IM 默认只走 `dialogue + compact_receipt`
- 不让 raw packet 默认直出聊天面

## T02 Compact Receipt Renderer

- 为聊天面补一个简短回执 renderer
- 保留：`task_id/trace_id/status/next`
- 不保留：`evidence_digest` 全量、lane、runtime_status 大段内部字段

## T03 FinalReport 降级为内部结构

- 保留内部 `FinalReport` packet 用于 taskops / trace / durable sync
- 聊天面默认改为自然语言总结 + compact receipt
- 避免 `[FinalReport]` 大块文本直接占满主对话

## T04 Fallback Note Demotion

- `control_plane_fallback_note` 不再直接注入主正文
- `runtime_fallback_note` 不再直接注入主正文
- fallback 信息应进入：
  - trace
  - taskops log
  - compact receipt 附注（必要时）

## T05 Tool-Call Leak Guard

- 禁止 raw function-call json 发送到外部 IM
- 检测 `{"name":"exec"...}` / `{"name":"list_dir"...}` / pseudo-tool-call 文本
- 对外改为：
  - 压制
  - 或替换为用户可读阻断提示

## T06 Wait / Progress 策略收束

- 保留高价值状态：
  - `WAIT_AUTH`
  - `WAIT_SUBTASK`
  - 长任务必要 progress
- 压制低价值 flood：
  - 频繁 progress
  - lane chatter
  - 调度噪声

## T07 Control-Plane Accepted 对话面优化

- `TaskReceipt` 默认改 compact
- 避免长块结构化 receipt 挤压自然语言
- 对外表达目标：
  - `已接单，正在处理。trace: xxx`

## T08 Fail-Open 成功路径优化

- 当 handoff 失败但本地执行成功时：
  - 对外总结应以“完成了什么”为主
  - 不以“之前 handoff 失败”作为正文开头
- fallback 原因进入 log/receipt 附注

## T09 Focused Tests

至少覆盖：

- raw tool-call json 不外发
- control-plane accept 只给 compact receipt
- control-plane fail-open + local success 不输出日志墙
- runtime blocked 输出自然语言阻塞说明 + 短回执
- orchestration wait-state 仍然可见但不过量

## T10 文档回填

- 回填本目录 `Checks`
- 回填一条给运营/测试的可见行为说明
