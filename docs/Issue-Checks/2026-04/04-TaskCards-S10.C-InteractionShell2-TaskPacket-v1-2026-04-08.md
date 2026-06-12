# 04-TaskCards-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08

## T01 Input Triage 基线

- 定义 triage 结果对象
- 区分 `reply_part / task_candidate / clarification_part`
- 保证普通交流不直接落入任务态

## T02 Submit Gate

- 建立统一提交闸门
- 固定四类结果：
  - `reply_only`
  - `local_fast_exec`
  - `handoff_to_control_plane`
  - `plan_or_confirm_first`

## T03 路由回归测试

- 纯交流不进入任务态
- 只做方案不假执行
- 简单低风险请求保持本地 fast lane
- 明确 durable 任务形成 handoff packet

## T04 Task Packet Builder

- 强化 goal / constraints / source_summary
- 强化 evidence expectation
- 强化 time/thread/project/node metadata

## T05 Result Packet Builder

- 归一化：summary / what_was_done / evidence / artifacts / next_actions / blockers
- 为 shell 侧叙事提供稳定输入

## T06 User-visible Renderer

- 稳定 ACK / compact receipt / compact trace / final summary
- 减少低价值内部噪音

## T07 Dual Clock Policy

- 注入 `utc_now`
- 注入 `local_now`
- 注入 `timezone=Asia/Shanghai`
- 保障对话时间语义使用本地时区

## T08 Dialogue Time Tests

- 本地时间注入测试
- “今天/今晚/明早”类对话语义测试
- 避免 UTC-only 误导

## T09 Backward Compatibility

- 保持 local fast lane
- 保持 control-plane fail-open
- 保持现有 handoff 基础链路不回退

## T10 Docs 回填

- 回填本目录任务包 / 验收 / 启动词
- 必要时补一条 operator note
