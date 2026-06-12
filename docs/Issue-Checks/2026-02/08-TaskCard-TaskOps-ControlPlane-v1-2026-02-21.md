# 任务卡：TaskOps ControlPlane v1

- 任务ID: T10
- 标题: TaskOps 控制面化（API + 运行日志 + 事件）
- 日期: 2026-02-21
- 负责人: chimera-core-codex
- 分支: codex/feature-taskops-controlplane-v1（已合并到 `master`）
- 优先级: P1
- 状态: DONE

## 背景
- chimera-core 已有 TaskOps（任务池/看板/人机分流），但主要通过 CLI 与本地文件驱动。
- 需要补足“控制面能力”，与 OpenClaw 的 gateway 管理模式对齐，提升可观测与远程编排能力。

## 目标
1. 给 TaskOps 增加 gateway methods（`taskops.list/add/update/claim/complete`）。
2. 给 dispatcher/notifier 增加结构化 run log（jsonl）。
3. 增加 task state change 事件广播（claim/complete/notify/fail）。

## 范围
- In Scope:
  - taskops gateway handlers + schema + 权限映射。
  - taskops run log（读写/轮转/查询接口）。
  - taskops 事件广播（最小事件集合）。
- Out of Scope:
  - Web 控制台 UI。
  - 分布式多节点任务一致性。

## 里程碑（M1/M2/M3）
- M1 API 化（3 天）
  - 新增 `taskops.*` methods + 最小鉴权。
- M2 可观测（2 天）
  - 新增 `taskops/runs/*.jsonl` + `taskops.runs` 查询。
- M3 事件化（2 天）
  - 新增 `taskops.changed` 事件与订阅消费验证。

## 实施清单
- [x] S1: 设计 `taskops` 协议 schema（方法参数/返回）
- [x] S2: 增加 gateway handlers 与 method 注册
- [x] S3: 增加 run log 模块（append/read/prune）
- [x] S4: 在 dispatcher/notifier/hub 回写点打日志与事件
- [x] S5: 增加自动化测试（handlers + runlog + 事件）
- [x] S6: 更新 Issue-Checks 文档与验收记录

## 验收标准
- [x] A1: API/CLI 双路径可完成任务生命周期操作
- [x] A2: 每次 bot/human 处理有结构化 run log 记录
- [x] A3: 关键状态变化可通过 gateway event 观察到
- [x] A4: 回归通过（含 taskops + auth + deploy 基线）

## 代码参考
- chimera-core:
  - /Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/taskops/services.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py
- OpenClaw（借鉴）:
  - /Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/cron.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/cron/run-log.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/system.ts

## 风险与回滚
- 风险:
  - 事件风暴导致广播压力上升。
  - 任务与日志写入时序不一致。
- 回滚:
  - feature flag 关闭 `taskops.gateway.enabled` / `taskops.events.enabled`。
  - 保留 CLI 原有路径作为降级通道。

## 收口记录（2026-02-21）
- 自动回归：`bash deploy/chimera_core_test.sh` 通过（54 tests，含远端验收用例默认 skip）。
- 主分支合并：`master@7c03c60`。
- 配套联调脚本：`deploy/chimera_auth_it.sh`（用于本轮 auth/taskops 联动验收）。
