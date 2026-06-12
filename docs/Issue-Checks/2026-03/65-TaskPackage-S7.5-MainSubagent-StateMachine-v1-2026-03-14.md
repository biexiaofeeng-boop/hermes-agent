# 任务包：S7.5 主/子代理状态机与终态闭环（v1）

- 日期：2026-03-14
- 状态：DONE
- 建议分支：`codex/s7-5-main-subagent-state-machine-v1`
- 输入来源：
  - 用户运行反馈（Telegram：执行后“无后文”）
  - `docs/ops/Agent-Direct-测试记录-2026-03-10.md`
  - `docs/Issue-Checks/2026-03/61-TaskCards-S7.4.1-Dialogue-ZeroIntercept-v1-2026-03-11.md`

## 0) 结论先行

当前问题不是 prompt 文案问题，而是执行控制流没有“强终态”保障：

1. 复杂任务缺少 `ACK -> 进度 -> FinalReport` 的强约束路径。  
2. 子代理回传虽有 `ContextPacket`，但主代理没有任务级聚合闭环。  
3. 模型偶发输出伪 `<tool_call>` 文本会被当作普通回复外发，造成“像执行了但其实没执行”的体感。  

S7.5 目标：在不重构全栈前提下，做一版“轻状态机 + 强终态回执 + 可观测节流”的可靠闭环。

## 1) 问题归类

| issue_id | 等级 | 现象 | 目标 |
|---|---|---|---|
| OPS-EXEC-001 | P0 | 任务开始后缺最终回执，用户窗口“失联” | 强制 FinalReport 必达 |
| OPS-EXEC-002 | P0 | 出现 `<tool_call>` 文本但未真实执行 | 伪工具调用识别并阻断“假执行” |
| OPS-EXEC-003 | P1 | 主/子代理协同结果无统一汇总 | 子任务汇总后由主代理统一上报 |
| OPS-EXEC-004 | P1 | 进度消息噪声或缺失并存 | 进度节流并保留关键节点通知 |
| OPS-EXEC-005 | P1 | 回执规则分散，体验不稳定 | 统一 ACK/PROGRESS/FINAL 协议 |

## 2) 根因定位（代码锚点）

1. 主循环缺任务状态机实体  
- `nanobot/agent/loop.py:560`（LLM/工具迭代）
- `nanobot/agent/loop.py:685`（收尾分支）
- `nanobot/agent/loop.py:722`（直接持久化出站）

2. 回执跟进为后台 fire-and-forget，失败不影响主链  
- `nanobot/agent/loop.py:1723`（`_schedule_collab_followups`）

3. provider 只识别结构化 `tool_calls`，伪标签文本会透传  
- `nanobot/providers/litellm_provider.py:171`

4. 子代理有 packet 但缺“主代理统一 FinalReport 语义”  
- `nanobot/agent/subagent.py:280`
- `nanobot/agent/loop.py:1118`

## 3) 设计目标（本轮）

1. 复杂任务：一定有 `已受理` 和 `最终结果` 两个确定节点。  
2. 主代理对外唯一口径：子代理只上报，主代理负责面向用户汇总。  
3. 出现伪执行信号时，明确声明“未执行”。  
4. 保持 S7.4 的对话流畅，不回退到模板化拦截。  

## 4) 方案摘要（轻状态机）

新增轻量任务运行状态（可存在 session metadata + trace event）：

`RECEIVED -> ACKED -> EXECUTING -> WAIT_AUTH | WAIT_SUBTASK -> REPORTING -> DONE | FAILED | TIMEOUT`

关键规则：

1. 进入 `EXECUTING` 的任务，必须进入 `REPORTING`，再到终态。  
2. `WAIT_SUBTASK` 必须有子任务回传事件或超时事件。  
3. 终态（`DONE/FAILED/TIMEOUT`）必须写 trace，并向用户发送 FinalReport。  

## 5) 实施任务卡（摘要）

- 详见：`66-TaskCards-S7.5-T01-T14-v1-2026-03-14.md`
- 核心改动面：
  - `nanobot/agent/loop.py`
  - `nanobot/agent/subagent.py`
  - `nanobot/config/schema.py`
  - `tests/test_agent_loop_dialogue_mode.py`
  - `tests/test_ooda_context_packets.py`

## 6) 验收标准（必须全部满足）

1. 复杂执行任务，100% 出现 FinalReport（成功/失败/超时都要有）。  
2. 用户侧不再看到“伪 `<tool_call>` 执行文本”作为已执行结论。  
3. 子任务完成后，主代理统一汇总并回执，不出现“子任务完成但主线程失联”。  
4. `CollabReceipt` 继续默认静默，仅在显式 trace/异常/长延迟场景可见。  
5. 既有 S7.4 对话去噪行为不回退。  

## 7) 风险与回滚

- 风险 1：状态过多导致响应延迟增加。  
  - 规避：仅对 `execution_state in {planned, executed, blocked}` 启用任务态机。
- 风险 2：通知过多影响体感。  
  - 规避：进度节流，保持“少而关键”。
- 风险 3：兼容历史逻辑。  
  - 规避：加 feature flag，默认温和开启。

回滚策略：

1. 回滚状态机聚合逻辑（保留 S7.4 去噪）。  
2. 保留伪工具调用保护（该项不建议回滚）。  
