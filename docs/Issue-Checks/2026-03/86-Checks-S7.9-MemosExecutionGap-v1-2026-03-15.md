# 验收清单：S7.9 Memos Execution Gap（v1）

- 日期：2026-03-15
- 状态：DONE

## A. 回执与语义

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | fallback 可见回执 | 发生 `local_staged` 时，用户侧必须收到明确降级提示 |
| C02 | 禁止 silent 吞信号 | memos 失败/降级场景不允许 `TG_RECEIPT_SKIPPED` |
| C03 | 语义一致 | 用户文案、trace 字段、内部状态三者一致 |
| C04 | 成功/失败区分 | 仅 `remote_success` 可宣称“已写入远端” |

## B. 证据门禁

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | memos 宣称门禁 | 无远端证据时，不得输出“已归档/已写入” |
| C06 | claim guard 回退 | 检测到无证据宣称时自动改写为待确认或降级文案 |

## C. 回归与观测

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C07 | 单测覆盖 | fallback + receipt + claim guard 三类测试通过 |
| C08 | 运行观测 | 复测期间不再出现“远端失败但用户误判成功” |

## D. 回归命令（已执行）

```bash
python3.11 -m py_compile nanobot/agent/loop.py nanobot/integrations/memos.py nanobot/trace/store.py
python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_collab_trace_memos -v
```

## E. 验收结果回填（2026-03-15）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `tests.test_agent_loop_dialogue_mode::test_telegram_note_intent_local_staged_forces_visible_receipt`，local staged 场景强制收到 `[CollabReceipt]` |
| C02 | PASS | 同上用例校验 trace 中 `TG_RECEIPT_SENT` 存在且 `TG_RECEIPT_SKIPPED` 不存在 |
| C03 | PASS | 回执新增 `memos_state`；trace `payloadDigest=memos:local_staged`；内部状态统一为 `remote_success/local_staged` |
| C04 | PASS | `nanobot/agent/loop.py` 仅在 `memos_state=remote_success` 时标记 DONE 与远端成功语义 |
| C05 | PASS | `tests.test_agent_loop_dialogue_mode::test_no_tool_evidence_cannot_claim_memos_remote_written` |
| C06 | PASS | 无工具证据时，成功宣称自动降级为“没有工具执行证据”提示 |
| C07 | PASS | `Ran 15 tests in 0.301s, OK`（dialogue_mode + collab_trace_memos） |
| C08 | PASS | 本轮复测未出现“远端失败但用户误判成功”；fallback 统一进入可见降级回执 |
