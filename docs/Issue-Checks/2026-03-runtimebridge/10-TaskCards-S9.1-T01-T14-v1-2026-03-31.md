# 任务卡：S9.1 T01-T14

- 日期：2026-03-31
- 状态：READY
- 关联：`09-TaskPackage-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md`

## A. 对话态判定（P0）

## T01

- 输出：任务内非执行回合判定函数
- DoD：能识别“非执行任务/汇总汇报/先总结/只回复/恢复直接对话/跳出任务循环”等语义

## T02

- 输出：任务 trace 下的 response mode 收敛规则
- DoD：任务 trace 内允许 `chat/report` 回合，不再默认进入执行闭环

## T03

- 输出：执行意图与报告意图区分测试
- DoD：覆盖“确认执行”与“非执行总结”在同一 trace 下的分流差异

## B. FinalReport/Blocked 收口修复（P0）

## T04

- 输出：`industrial_task_id` + 无工具证据的收口条件收紧
- DoD：只有真正执行回合才因“无工具证据”进入 blocked

## T05

- 输出：`force_final_report` 触发条件收紧
- DoD：`chat/report` 回合不再自动套 `[FinalReport]`

## T06

- 输出：任务内总结回合自然语言输出
- DoD：保留自然回复，不暴露模板噪音

## C. CollabReceipt 可见性修复（P0）

## T07

- 输出：任务 trace 下 receipt 可见性规则收敛
- DoD：普通总结/解释回合默认静默，显式 trace 请求例外

## T08

- 输出：Telegram 定向测试
- DoD：复现截图中的回合后，不再收到用户可见 `[CollabReceipt]`

## D. Bridge / Ironelf 护栏（P1）

## T09

- 输出：可选 `intent_mode` 字段设计
- DoD：支持 `execute|plan|report|chat`，保持向后兼容

## T10

- 输出：`ExecutionRequest` builder 可选扩展
- DoD：若本轮实现，则仅 additive，不影响现有真实联调

## T11

- 输出：`ironelf` 兼容说明
- DoD：明确该字段当前可忽略；若后续接入则返回 `noop/not_runnable` 即可

## E. 回归与交付（P0）

## T12

- 输出：`tests.test_agent_loop_dialogue_mode` 新增回归
- DoD：至少覆盖 3 个用例：非执行总结不 FinalReport、不 blocked、receipt 静默

## T13

- 输出：验收清单回填
- DoD：`11-Checks-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md` 证据完整

## T14

- 输出：交接说明
- DoD：changed files、commit hash、是否包含 `intent_mode`、残余风险说明完整
