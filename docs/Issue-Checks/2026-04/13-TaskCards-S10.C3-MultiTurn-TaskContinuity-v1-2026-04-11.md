# 13-TaskCards-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11

## 分支与目录约束

- repo: `/Users/sourcefire/X-lab/chimera-core`
- base branch: `master`
- working branch: `codex/s10c3-multiturn-task-continuity-v1`

优先修改目录：

- `nanobot/agent/interaction_shell.py`
- `nanobot/agent/loop.py`
- `tests/test_agent_loop_dialogue_mode.py`
- `tests/test_ooda_context_packets.py`

必要时允许补充：

- `nanobot/session/*`
- `nanobot/taskops/*`

## T01 Continuity Mode 对象

- 定义 continuation mode 结果
- 至少覆盖：
  - `new_topic`
  - `attach_resource`
  - `confirm_pending`
  - `followup_expand`
  - `followup_summary`
  - `followup_non_exec`

## T02 Resource Attachment 识别

- URL-only turn
- image/file path turn
- media-only turn
- 在短窗口内自动挂接到 pending topic / pendingIndustrialTask

## T03 Confirm Alias 统一

- 在 pending task 存在时：
  - `直接执行`
  - `确认执行`
  - `继续执行`
  - `开始执行`
  - `按方案执行`
  统一视为 `confirm_pending`

## T04 Pending Topic Merge

- source_message 合并
- resource refs 合并
- digest / updated_at 刷新
- 保持原 task_id / trace continuity 不漂移

## T05 Continuation 优先级

- 承接判断优先于新任务创建
- 顺序：
  1. pending continuation
  2. attach_resource
  3. confirm_pending
  4. followup summary/expand
  5. new_topic

## T06 Article Summary 结构升级

- 阅读类任务默认输出：
  - 核心结论
  - 关键依据
  - 对当前议题的启发
  - 下一步建议
- 保持简洁，不强制长文

## T07 Focused Tests

至少覆盖：

- topic + URL -> attach_resource
- pending task + `直接执行` -> confirm_pending
- continuation 不重复建 task
- article summary 输出骨架存在
- S9.1a / S10.C2 主链不回退

## T08 Docs 回填

- 回填 Checks
- 回填启动词
- 回填 operator note
