# 10-Checks-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09

## 目标

验证 `chimera-core` 在外部聊天面实现新的渲染分层：

- 主对话更自然
- compact receipt 保留
- raw state flood 不再污染聊天面
- fallback note 不再抢正文

## C01 Raw Tool JSON Leak Guard

- 构造带工具调用的回合
- 验证外部 surface 不直接出现：
  - `{"name":"exec"...}`
  - `{"name":"list_dir"...}`
- 预期：PASS 后聊天面只看到自然语言或 compact 提示

## C02 FinalReport 降级

- 构造 industrial / runtime 完成回合
- 验证主聊天面默认不出现整块 `[FinalReport]`
- 预期：PASS 后保留自然语言总结 + 短回执

## C03 Control-Plane Accept Compact Receipt

- 构造 control-plane accepted 回合
- 预期：外部只看到 compact receipt，而不是大段 receipt 结构块

## C04 Fail-Open Local Success Narration

- 构造 handoff 失败并切回本地成功的链路
- 预期：正文第一段以完成结果为主，不以 fallback 错误说明为主

## C05 Runtime Blocked Narration

- 构造 runtime blocked / receipt missing
- 预期：自然语言说明阻塞原因 + 短回执
- 不应出现日志墙

## C06 Wait-State 保留高价值提示

- 验证 `WAIT_AUTH` / `WAIT_SUBTASK` 仍然能看到
- 验证不出现过量 progress flood

## C07 Trace/TaskOps Truth 保留

- 验证 compact 化后：
  - trace 仍有记录
  - taskops 仍有 terminal 同步
  - fallback reason 未丢失

## C08 回归

- 普通聊天不受影响
- 简单本地 fast lane 不受影响
- cron / 非执行轮次不被重新拖回 FinalReport 污染

## 执行结果回填（2026-04-09）

- C01 PASS：外部聊天面遇到 raw tool-call json 时，正文改为自然语言占位，回执改为 compact receipt。
- C02 PASS：Telegram 等外部 surface 默认不再直出 `[FinalReport]`，改为自然语言总结 + 紧凑回执。
- C03 PASS：`[TaskReceipt]` 在外部聊天面默认渲染为 `已接单，正在处理。` + compact receipt。
- C04 PASS：control-plane fail-open 且本地成功时，正文以完成结果为主；fallback 原因保留在 trace / receipt note，不再抢占正文。
- C05 PASS：runtime blocked / receipt missing 仍返回自然语言阻塞说明，并附短回执，不出现日志墙。
- C06 PASS：`WAIT_AUTH` / `WAIT_SUBTASK` 可见性保留；本轮未引入新的 progress flood。
- C07 PASS：内部 truth 未丢失；trace 仍保留 `DISPATCH_FAILED` / runtime 事件，taskops 终态同步不回退。
- C08 PASS：普通聊天、fast lane、本地 cron/non-exec 路径在 focused regression 中保持通过。

## Focused Regression

- 命令：`python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_ooda_context_packets tests.test_web_intel_evidence_gate tests.test_telegram_channel -v`
- 结果：`Ran 55 tests in 6.297s`
- 结果：`OK`

## 外部聊天面默认表现

- 主正文：优先给自然语言 ACK / 总结，不再把内部状态块直接发到 Telegram/微信。
- 回执层：需要可见回执时，统一走 compact receipt，保留 `status / task / trace / next / note` 的短格式。
- 内部真相层：`FinalReport`、trace、taskops、fallback reason 仍保留给系统内收口与诊断使用。
- 泄漏防护：raw tool-call json、pseudo tool-call 结构块不再外发到外部 IM。

## 收口补记（2026-04-10）

- 追加修复：伪工具调用拦截补齐 `{"name","arguments"}` 形态，避免漏过 guard 后被聊天面改写成“正在处理中 / 等待结果摘要”假进度。
- 策略收束：`feishu / wechat / wx` 本轮先回退为不走 compact render，仅 `telegram` 启用压缩聊天面，降低跨通道表现不一致风险。
- 定向回归：
  - 命令：`source /tmp/chimera-core-s10c2-venv/bin/activate && python -m pytest -q tests/test_agent_loop_dialogue_mode.py tests/test_ooda_context_packets.py tests/test_web_intel_evidence_gate.py`
  - 结果：`49 passed, 1 warning in 8.85s`
