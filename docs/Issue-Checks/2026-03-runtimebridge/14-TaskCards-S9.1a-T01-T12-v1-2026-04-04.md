# 任务卡：S9.1a T01-T12

- 日期：2026-04-04
- 状态：READY
- 关联：`13-TaskPackage-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md`

## A. cron/internal task 免确认（P0）

## T01

- 输出：内部编排来源标识设计
- DoD：明确 `execution_origin / internally_orchestrated / confirm_bypass` 的最小字段与默认值

## T02

- 输出：cron 入口 metadata 注入
- DoD：`cron` 任务进入 agent 时带内部编排标识，而非裸文本执行

## T03

- 输出：loop 层 confirm bypass
- DoD：`internally_orchestrated=true` 时不进入 `TaskConfirm`，也不写 pendingIndustrialTask

## T04

- 输出：cron 直执行回归测试
- DoD：覆盖“cron task 不再被二次确认拦截，但证据与最终回执仍存在”

## B. 延迟确认 TTL（P0）

## T05

- 输出：`pendingIndustrialTask` 结构扩展
- DoD：增加 `created_at/expires_at/trace_id/source_digest`

## T06

- 输出：pending 过期加载与清理逻辑
- DoD：旧 pending 超时后自动失效，不再被“确认执行”直接复用

## T07

- 输出：过期确认用户提示
- DoD：返回“确认已过期，请重新确认原议题/重新发起任务”，不输出 `[FinalReport] FAILED`

## C. ACK 与终态收敛（P0）

## T08

- 输出：ACK 后移策略
- DoD：ACK 只在真正进入执行面后发送；本地执行与 runtime lane 行为一致

## T09

- 输出：确认后无证据时的终态收敛
- DoD：未真正起执行时不直接映射为 FAILED；优先回到 re-confirm / HOLD / blocked 语义

## T10

- 输出：延迟确认回归测试
- DoD：覆盖“先 TaskConfirm，长时间后确认”场景，不再出现“ACK 后立即 FAILED”

## D. 回归与交付（P0）

## T11

- 输出：S9 / S9.1 主链回归
- DoD：runtime lane success / receipt_missing / fail-open / non-exec summary 相关既有测试继续通过

## T12

- 输出：验收清单与交接回填
- DoD：checks 文档回填、changed files、commit hash、残余风险说明完整
