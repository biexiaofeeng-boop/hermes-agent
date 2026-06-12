# 03-TaskPackage-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08

## 任务定位

本任务包属于 S10.C，目标是在 `chimera-core` 中完成一轮真正结构性的交互层收束：

- 统一 `Input Triage`
- 统一 `Submit Gate`
- 规范 `Task Packet`
- 规范 `Result Packet`
- 补齐双时钟与可见 receipt 策略

本轮不是继续做零散对话修修补补，而是把前面多轮修复中反复出现的入口/提交/收口问题抽成稳定结构。

## 为什么现在做这件事

过去多轮迭代已经反复修过：

- Lobby 阻塞
- 对话去噪
- ACK / FinalReport 强收口
- 非执行回合误判
- 确认过期与 cron 误拦截
- runtime bridge fail-open

这些问题说明当前主要缺口不再是单点功能，而是 `interaction shell -> submission -> control plane` 这条链还没有被稳定建模。

## 本轮边界

### In Scope

- 统一 triage / submit 决策
- control-plane handoff packet 强化
- control-plane result packet 归一化
- dual-clock policy
- Telegram 等对话面 compact receipt / trace 策略
- focused tests 与文档回填

### Out Of Scope

- 完整 task tree / assignment 系统
- durable truth 回迁到 `chimera-core`
- 完整 skills/capabilities 治理重做
- Cherry Studio 改造
- specialist runtime 整合改造

## 关键设计点

### 1. Input Triage

每轮输入拆成：

- `reply_part`
- `task_candidate`
- `clarification_part`

目的：让“聊天”和“任务候选”先解耦，而不是一进入主循环就混成执行态。

### 2. Submit Gate

统一决定：

- `reply_only`
- `local_fast_exec`
- `handoff_to_control_plane`
- `plan_or_confirm_first`

目的：不再让多个下游位置各自重复判断这轮到底是不是任务。

### 3. Task Packet

发给 `chimera-iceclaw` 的包应更规范，至少强化：

- `goal`
- `constraints`
- `source_summary`
- `requested_mode`
- `evidence_expectation`
- `observed_at_utc`
- `observed_at_local`
- `timezone`
- `thread_id/project_id/node_id`

### 4. Result Packet

从 `chimera-iceclaw` 回来后的结果应归一化后再叙事。

至少包括：

- `status`
- `summary`
- `what_was_done`
- `evidence`
- `artifacts`
- `next_actions`
- `risk_or_blockers`
- `task_id/receipt_id/correlation_id`

### 5. Dual Clock Policy

采用双时钟：

- `UTC` 继续做系统排序真相
- `Asia/Shanghai` 做对话语义时间

作用：避免模型在本地白天按 UTC 深夜语义提醒休息，同时不破坏跨节点时间对齐。

### 6. Visible Receipt Policy

默认保留：

- 简短 ACK
- compact receipt
- compact trace（必要时）
- final summary

默认不外显：

- 原始事件洪流
- 低价值内部调度噪音

## 上游资料包

- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/00-README.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/01-iteration-review.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/02-cross-compare.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/03-task-pack-chimera-core-s10c.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/04-task-cards-chimera-core-s10c.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/05-checks-chimera-core-s10c.md`

## 下一步衔接建议

本轮完成后，下一阶段更适合推进：

1. `chimera-iceclaw` 轻任务树骨架
2. 再之后才是 skills/capabilities 的统一治理升级
