# 16-方案设计：Phoenix Protocol v1（赛博修狗）

- 日期: 2026-02-25
- 适用范围: Chimera Core 夜间自动演进 + 生产平滑切换
- 目标仓路径:
  - DEV: `/Users/sourcefire/X-lab/chimera-core`
  - PROD: `/Users/sourcefire/X-lab/chimera-core-prod`

## 背景问题

近期出现网络抖动后 Telegram polling 中断，表现为“进程仍在但通信不可用”。当前恢复依赖人工重启，夜间无人值守风险较高。

## 设计目标

1. 主节点故障自动恢复（自愈）。
2. 夜间升级自动化（可门禁、可回滚）。
3. 切换失败自动回滚到 snapshot。
4. 次晨可追溯（有战报、有日志）。

## 架构组件

1. `chimera-watchdog`（赛博修狗）
   - 独立守护进程，仅负责监控与编排，不承载业务推理。
2. `release-controller`（发布控制器）
   - 负责 preflight、cutover、verify、rollback 的状态机。
3. `health probes`（健康探针）
   - 进程活性、`/health`、Telegram 连接状态、错误速率。
4. `snapshot manager`
   - 发布前后记录版本，失败自动回滚到最近稳定快照。

## 状态机

`IDLE -> PREFLIGHT -> GREEN_VERIFY -> CUTOVER -> POST_VERIFY -> DONE`

失败路径：

`ANY_STATE -> ROLLBACK -> ALERT -> IDLE`

## 发布策略（v1）

说明：由于 Telegram 同一 token polling 不能双活，v1 使用“准蓝绿”：

1. Green 预检（test bot 或离线探针）通过。
2. 切流瞬间停止 Blue（prod token）。
3. 启动 Green（prod token）并做 post-verify。
4. 失败立即回滚至上一个 snapshot。

## 监控与判定阈值（v1）

1. `health` 连续失败 >= 3 次（每次间隔 10s）触发重启。
2. Telegram 网络错误窗口（5 分钟）>= 5 次触发重建通道。
3. 连续 3 次自愈失败触发自动回滚与报警。

## 风险与控制

1. 风险: 重启风暴
   - 控制: 指数退避 + 熔断（10 分钟最多 3 次）。
2. 风险: 错误版本误发布
   - 控制: 发布门禁必须包含测试通过与快照记录。
3. 风险: 回滚失败
   - 控制: 快照前置 + 固定回滚脚本。

## 文档与脚本落点

1. 方案: 本文档
2. 任务卡: `16-TaskCard-Phoenix-Protocol-v1-2026-02-25.md`
3. 验收: `16-Checks-Phoenix-Protocol-v1-2026-02-25.md`
4. 运行手册: `/Users/sourcefire/X-lab/chimera-core/docs/INTEGRATED_RELEASE_RUNBOOK.md`

## v1 交付边界

In Scope:

1. Watchdog 监控 + 自愈重启
2. 发布状态机与自动回滚
3. 基础报警与战报输出

Out of Scope:

1. Telegram 真双活蓝绿
2. 独立消息中继总线
3. 跨机房多活
