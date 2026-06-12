# 任务包：S9.1 TaskTrace Non-Exec Dialogue Fix（v1）

- 日期：2026-03-31
- 状态：READY
- 建议分支：`codex/s9-chimera-ironelf-runtime-bridge-v1`
- 目标：修复任务 trace 内“非执行回合”被误判为执行失败，从而强制输出 `[FinalReport]` / `[CollabReceipt]` 的问题，同时保持 S9 runtime bridge 主链不回退。

## 0）结论先行

1. 这次问题的主因在 `chimera-core`，不是 `ironelf`。
2. 当前误触发来自主循环中的任务态强制收口逻辑，而不只是 prompt 惯性。
3. P0 必须修 `chimera-core`：让“任务内总结/解释/解除阻塞后的直接交流”可以留在 chat/report 回合。
4. `ironelf` 只需要一个轻量护栏，不是当前发布 blocker。
5. 本包应继续留在 S9 分支上收口，和 runtime bridge 一起合并。

## 1）问题现象

1. 用户在 Telegram 中明确说“非执行任务。汇总汇报”。
2. 系统仍先输出 `[ACK]`，随后进入 `[FinalReport]`。
3. 因为本轮没有真实工具调用，`execution_state` 被打成 `blocked`。
4. 同时输出 `[CollabReceipt]`，把任务路由信息暴露到用户窗口。
5. 最终体感像“对话被执行模板劫持”。

## 2）已确认根因

## 2.1 `chimera-core` 侧控制流问题

1. 只要带 `industrial_task_id` 且本轮无工具证据，就会被强制打成 `blocked`。
2. 只要处于任务态，就可能强制进入 `FinalReport` 收口。
3. Telegram 协同回执仍会在某些任务 trace 场景可见输出。
4. 这使“任务线程中的普通总结回合”被错误等同为“执行失败回合”。

## 2.2 `ironelf` 侧现状

1. 当前问题发生在 runtime 派发之前。
2. 也就是说，即使 `ironelf` 完全不参与，本问题依然存在。
3. 但为了避免未来把“report/chat 回合”错误送入 runtime lane，协议层最好补一个轻量标识。

## 3）修复边界

## 3.1 P0：必须在 `chimera-core` 修

1. 新增“任务内非执行回合”判定。
2. 收紧“无证据即 blocked”的触发条件。
3. 收紧 `FinalReport` 强制收口条件。
4. 默认保持 `CollabReceipt` 静默，除非显式 trace/异常/长延迟场景。

## 3.2 P1：可选在 bridge / `ironelf` 补护栏

1. `ExecutionRequest` 增加可选字段：`intent_mode=execute|plan|report|chat`。
2. `ironelf` 对 `report/chat` 请求可返回 `noop/not_runnable`，而不是 `FAILED`。
3. 该项是加固，不阻塞这次 S9.1 收口。

## 4）本轮范围

1. 修复任务 trace 中“非执行总结/解释”回合的 response mode 与 terminal state 判定。
2. 确保这类回合输出自然语言总结，而不是 `[FinalReport]`。
3. 确保这类回合默认不向用户窗口输出 `[CollabReceipt]`。
4. 保持真正执行回合的 `[ACK] -> 执行 -> FinalReport` 机制不退化。
5. 视实现成本决定是否补 `intent_mode` 的可选协议字段。

## 5）明确不做

1. 不重写整个 industrial lane / TaskOps 状态机。
2. 不放松“真实执行必须有证据”的原则。
3. 不削弱 runtime bridge 的 fail-open / success-claim guard。
4. 不把自然语言总结直接当作执行成功凭据。

## 6）修复原则

1. 执行回合与报告回合分开。
2. `task trace` 不等于“本轮一定执行”。
3. 只在真正执行回合强制 `FinalReport`。
4. 用户窗口优先自然交互，trace/audit 留在系统内部。
5. 协议加固必须是 additive，不破坏现有 S9 联调结果。

## 7）风险与控制

1. 风险：把真实执行回合误降为 chat。
- 控制：仅对显式“非执行/汇总/解释/只回复”语义生效，并补回归测试。

2. 风险：`FinalReport` 覆盖率下降。
- 控制：只放宽 report/chat 回合，执行回合仍保持强制收口。

3. 风险：Telegram trace 可见性再度漂移。
- 控制：对任务 trace 下的可见 receipt 规则补定向测试。

4. 风险：bridge 与 `ironelf` 协议分叉。
- 控制：`intent_mode` 只做可选字段，先不做强依赖。

## 8）验收门槛

1. 任务 trace 内的“非执行总结回合”不再输出 `[FinalReport]`。
2. 这类回合不再因“无工具证据”被打成 `blocked`。
3. 这类回合默认不再向用户可见输出 `[CollabReceipt]`。
4. 真正执行回合的 `ACK -> FinalReport` 不回归。
5. 若补 `intent_mode`，字段为可选且不影响现有 `ironelf` 联调。
