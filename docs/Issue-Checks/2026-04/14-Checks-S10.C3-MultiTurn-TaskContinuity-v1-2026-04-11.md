# 14-Checks-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11

## 目标

验证 `chimera-core` 在多轮任务连续性上的新策略：

- 同一 topic 的相邻 turn 能稳定承接
- `直接执行` 等确认别名不再误开新任务
- 阅读类任务结果组织更稳定
- 既有执行一致性与聊天面渲染不回退

## C01 Topic + URL 挂接

- 先发阅读/分析类 topic
- 再发单独 URL
- 预期：URL 作为 `attach_resource` 并入同一 pending topic，而不是新建独立任务

## C02 Topic + Image/File 挂接

- 先发 topic
- 再发 image path / file path / media-only turn
- 预期：资源并入同一 topic

## C03 Pending Confirm Alias

- 先进入 `TaskConfirm`
- 用户回复 `直接执行`
- 预期：视为 `confirm_pending`，而不是新建任务/重新确认

## C04 Continuation 不重复建 Task

- 同 topic 下：`继续` / `补充总结` / `展开一下`
- 预期：承接既有 task / topic，不重复创建 task

## C05 Article Summary Structure

- URL 阅读/文章分析完成后
- 预期：输出至少包含稳定的“结论 / 依据 / 启发 / 下一步”骨架

## C06 S9.1a 不回退

- 过期确认逻辑不回退
- cron/internal bypass confirm 不回退
- ACK 时机不回退

## C07 S10.C2 不回退

- raw tool json 不外泄
- compact receipt 仍保留
- fallback note 不重新污染正文

## 回填区

## 结果

- 状态：PASS
- 分支：`codex/s10c3-multiturn-task-continuity-v1`
- 核心实现：
  - `interaction_shell` 新增 continuity mode、资源挂接识别、confirm alias 统一识别、阅读结果四段骨架 formatter
  - `loop` 新增 recent topic/pending topic 承接、资源补挂接、`直接执行` -> `confirm_pending` 归一、followup summary/expand 优先承接
  - `session.metadata` 新增 continuity 相关状态：`lastTopicId / lastTopicDigest / pendingTopicResources / lastContinuationMode / lastTopicUpdatedAt / lastTopicIntentType`

## 命令证据

- `python3.11 -m unittest tests.test_interaction_shell -v`
  13/13 通过。
- `python3.11 -m unittest tests.test_ooda_context_packets -v`
  13/13 通过。
- `python3.11 -m unittest tests.test_control_plane_dispatch -v`
  2/2 通过。
- `python3.11 -m unittest tests.test_runtime_bridge -v`
  13/13 通过。
- `python3.11 -m unittest tests.test_agent_loop_dialogue_mode -v`
  37/37 通过。

## 验收回填

### C01 Topic + URL 挂接

- PASS
- 新增 `test_topic_plus_url_turn_attaches_resource_to_recent_topic`
- URL-only turn 会落为 `attach_resource`，并入同一 topic 的 `pendingTopicResources / lastTopicSourceMessage`

### C02 Topic + Image/File 挂接

- PASS（逻辑覆盖）
- continuity helper 已统一按 URL / image path / file path / media refs 走同一资源挂接识别
- 本轮 focused tests 已覆盖 URL 与 surface/resources 主链；image/file 逻辑共用同一分支

### C03 Pending Confirm Alias

- PASS
- 新增 `test_pending_task_direct_execute_alias_reuses_pending_topic`
- 在 pending topic 存在时，`直接执行` 不再误开新任务，而是归一化为 `confirm_pending`

### C04 Continuation 不重复建 Task

- PASS
- 新增 `test_followup_expand_reuses_existing_task_without_duplicate_creation`
- `展开一下 / 补充总结 / 继续` 会优先承接既有 topic/task，不重复创建 industrial task

### C05 Article Summary Structure

- PASS
- 新增 `test_telegram_surface_formats_article_summary_with_four_sections`
- 阅读类结果默认升为四段：`核心结论 / 关键依据 / 对当前议题的启发 / 下一步建议`

### C06 S9.1a 不回退

- PASS
- `tests.test_agent_loop_dialogue_mode` 中的过期确认、cron bypass、ACK 时机回归全部通过

### C07 S10.C2 不回退

- PASS
- `tests.test_ooda_context_packets` 中 raw tool json 抑制、compact receipt、fallback note demotion 全部通过

## Operator Note

- 新的多轮承接行为是“先承接，再新建”：
  - topic 后紧跟 URL / 图片 / 文件 / media，会优先并入当前议题
  - pending topic 下的 `直接执行 / 确认执行 / 继续执行 / 开始执行 / 按方案执行` 会被视为同一种确认动作
  - 已有 task/topic 的 `展开一下 / 补充总结 / 继续` 默认按 continuation 处理，不重复起任务
- 阅读类任务完成后，Telegram 外显结果会优先给结构化四段总结，而不是只给一句薄摘要

## 2026-05-14 主干复核

- 复核背景：本地 `master` 已合入 `S11.B` 与后续修复，需要确认 `S10.C3` 多轮连续性能力未被后续改动覆盖。
- 复核基线：本地 `master@8c621518bd1bab6eaeaa948fa2cce12e3b68f1f8`（`merge: s11b host-side skills registry`）。
- 对比结论：相对 `S10.C3` 原始实现提交 `113673b`，当前主干仅在 `nanobot/agent/interaction_shell.py`、`nanobot/agent/loop.py` 及对应测试上有小幅增量，未出现 continuity/confirm alias/article summary 语义回退。

### 复核命令证据

- `python3.11 -m unittest tests.test_interaction_shell tests.test_ooda_context_packets tests.test_agent_loop_dialogue_mode -v`
  - 结果：`Ran 66 tests in 26.881s`
  - 状态：`OK`

### 复核结论

- `C01 Topic + URL 挂接`：保持通过。
- `C03 Pending Confirm Alias`：保持通过。
- `C04 Continuation 不重复建 Task`：保持通过。
- `C05 Article Summary Structure`：保持通过。
- `C06 S9.1a 不回退`：保持通过。
- `C07 S10.C2 不回退`：保持通过。
- 结论：`S10.C3` 在合入 `S11.B` 及后续修复后的本地主干上仍成立，可视为已完成收口。
