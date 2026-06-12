# 任务包：S9.1a Execution Coherence Fix（v1）

- 日期：2026-04-04
- 状态：READY
- 建议分支：`codex/s9-1a-execution-coherence-v1`
- 目标：修复两个已在线上集成发布后暴露的执行一致性问题，同时保持 S9 / S9.1 主链能力不回退。

## 0）结论先行

1. 这次是 `chimera-core` 的执行控制流一致性问题，不是 `ironelf` 主因。
2. 问题一：内部已编排的 `cron` 任务仍被当成人类待确认任务，错误进入 `TaskConfirm`。
3. 问题二：延迟较久后再回复“确认执行”，系统仍沿用旧待确认状态，先发 `[ACK]`，随后因无执行证据强制收口为 `[FinalReport] FAILED`。
4. 两个问题都应作为 `S9.1a` 的同一跟进包处理，继续放在 runtimebridge 线收口。
5. 本包优先修执行一致性与用户体感，不改动 S9 runtime bridge 的协议主链。

## 1）线上现象

## 1.1 cron 被二次拦截

1. `cron` 任务本身已经完成内部编排。
2. 运行时却再次进入 `industrial lane -> TaskConfirm`。
3. 这会把“系统内部已安排好的执行”错误变成人类确认流程。
4. 结果是自动任务不稳定，且引入无意义的人机交互噪音。

## 1.2 延迟确认后 ACK -> FAILED

1. 用户先收到 `[TaskConfirm]`。
2. 间隔较长时间后回复“确认执行”。
3. 系统先发送 `[ACK] 已受理，进入执行状态`。
4. 随后本轮没有真实工具证据，进入 `[FinalReport]`：`terminal_state=FAILED`、`execution_state=blocked`、`evidence_steps=0`。
5. 用户体感像“确认已生效，但系统又立刻否认自己理解了任务”。

## 2）已确认根因

## 2.1 cron 根因

1. `cron` 入口通过 `process_direct()` 把任务文本当普通消息送入 agent。
2. 当前没有“内部已编排任务”标识，也没有“confirm bypass”护栏。
3. `industrial lane` 判断逻辑只看复杂度/执行意图，不区分来源是否为系统内部调度。
4. 结果：`cron` 与普通 Telegram/CLI 执行请求走了同一确认路径。

## 2.2 延迟确认根因

1. `pendingIndustrialTask` 目前只有保存/清除，没有 TTL、过期时间、版本戳。
2. 无论 2 分钟还是 2 小时后回复“确认执行”，都会被当成原待确认任务继续执行。
3. 一旦确认后本轮没有真实工具调用，会被统一降为 `execution_state=blocked`。
4. 由于 industrial task 已创建，又会被强制包装成 `[FinalReport]`。
5. 当前 ACK 发送时机过早，发生在“真正执行证据出现之前”，放大了失败体感。

## 3）修复边界

## 3.1 P0：本轮必须修

1. `cron/internal scheduled task` 默认绕过 `TaskConfirm`。
2. `pendingIndustrialTask` 增加 TTL / 过期处理。
3. 过期确认不再直接 ACK + FAILED，而是返回“确认已过期，请重新确认原议题”。
4. ACK 发送时机后移到“真正进入执行面”之后。
5. 对“确认后无证据”的终态表达从“直接 FAILED”收敛为“需要重确认 / HOLD / blocked”。

## 3.2 P1：本轮不做

1. 不重写整个 industrial lane 状态机。
2. 不改 `ironelf` 运行协议主结构。
3. 不放松“真实执行必须有证据”的原则。
4. 不把任何自然语言描述当作执行成功凭据。

## 4）设计原则

1. 内部编排任务不应再次做人类确认拦截。
2. 人类确认必须有时效语义，过期后需要回到确认态。
3. ACK 只表示“已真正进入执行面”，不表示“只是接受了文本”。
4. FAILED 只用于真正执行失败，不用于“确认过期 / 未启动执行”。
5. 证据约束继续保留，但表达方式要与用户认知一致。

## 5）建议实现

## 5.1 cron/internal 任务来源标识

1. 在 `process_direct()` / cron 入口补充 metadata：
   - `execution_origin=cron`
   - `internally_orchestrated=true`
   - `confirm_bypass=true`
2. 在 loop 层识别该标识后：
   - 不进入 `TaskConfirm`
   - 不写入 `pendingIndustrialTask`
   - 直接走执行面
3. 但仍保留：
   - 工具证据要求
   - 最终回执
   - trace / taskops 留痕

## 5.2 pendingIndustrialTask TTL

1. `pendingIndustrialTask` payload 增加：
   - `created_at`
   - `expires_at`
   - `trace_id`
   - `source_message`
   - `source_digest`
2. `load_pending_industrial_task()` 时增加过期校验。
3. 过期则清理旧 pending，并返回“确认已过期，请重新确认/重新下达任务”。

## 5.3 ACK 时机后移

1. 本地执行链：至少在第一条真实 tool event 或 runtime submit 成功后再 ACK。
2. runtime lane：在 submit 成功且 execution_id 确立后 ACK。
3. 若执行尚未真正开始，不应先对用户说“进入执行状态”。

## 5.4 终态收敛

1. “延迟确认已过期” -> 不输出 `[FinalReport] FAILED`。
2. “本轮还未触发执行” -> 返回重确认/重试提示，终态偏 `planned` 或 `blocked/HOLD`。
3. 只有真正执行回合且发生失败，才进入 `FAILED`。

## 6）风险与控制

1. 风险：错误放开了本该确认的人类高风险请求。
- 控制：仅对白名单来源 `internally_orchestrated=true` 免确认。

2. 风险：TTL 过短影响正常使用。
- 控制：TTL 配置化，默认建议 30m 或 60m，并补测试。

3. 风险：ACK 后移影响已有用例。
- 控制：验收只要求“仍有 ACK”，不要求“在当前旧位置发送 ACK”。

4. 风险：状态语义变化影响 task hub 统计。
- 控制：优先复用已有 `HOLD -> blocked` 映射，不新增复杂状态机。

## 7）验收门槛

1. cron/internal scheduled 任务不再输出 `[TaskConfirm]`。
2. cron/internal scheduled 任务仍保留证据与最终回执。
3. 过期确认回复后，不再出现“先 ACK 再 FAILED”的体验。
4. 过期确认应返回明确的“确认已过期，请重新确认原议题”。
5. 真实执行回合、runtime lane、fail-open、receipt-missing 等 S9 主链回归不退化。
