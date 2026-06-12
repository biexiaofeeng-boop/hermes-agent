# 验收清单：S7.1 对话流畅性 + 可控执行控制面（v1）

- 日期：2026-03-05
- 状态：DONE（2026-03-06）

## C01 对话流畅性
- [x] Lobby 下意图不明不再硬卡，首条回复可读可用
- [x] 简单问答进入 `chat`，不触发无关工具执行

## C02 模式分流
- [x] 简单任务 -> `direct_exec`
- [x] 中等任务 -> `plan_confirm`（先方案后确认）
- [x] 复杂任务 -> `mission_board`（任务面板）

## C03 OODA 触发边界
- [x] 默认 Direct，不自动注入 OODA
- [x] 显式指令或确认后才触发 OODA

## C04 超时恢复
- [x] 触发 timeout 后执行 1 次降载重试
- [x] 第二次失败返回清晰兜底提示（不死循环）

## C05 反幻觉约束
- [x] `executed` 回复包含工具证据摘要
- [x] 无工具证据时不出现“已执行完成”表述

## C06 观测字段
- [x] metadata 包含 `lastResponseMode`
- [x] metadata 包含 `lastExecutionState`
- [x] metadata 包含 `lastToolEvidenceCount`

## C07 回归
- [x] `python -m py_compile nanobot/agent/loop.py nanobot/config/schema.py`
- [x] `python -m unittest tests.test_taskops_feasibility -v`
- [x] `python -m unittest tests.test_feishu_channel -v`
- [x] `bash deploy/chimera_core_test.sh`（或最小子集 + 说明）

## 回填结论（2026-03-06）

- 验收结论：S7.1 Thread-A（T01~T12）通过，可进入主干合并窗口。
- 关键回归：
  - `python -m unittest tests.test_taskops_feasibility tests.test_feishu_channel tests.test_agent_loop_dialogue_mode tests.test_ooda_context_packets tests.test_project_context_router tests.test_thinking_route tests.test_release_it_script -v`
    - 结果：`Ran 45 tests`，`OK`
  - `PYTHON_BIN=/Users/sourcefire/X-lab/chimera-core-prod/.venv/bin/python bash deploy/chimera_core_test.sh`
    - 结果：`Ran 187 tests`，`OK (skipped=3)`
- 风险备注：
  - 非阻塞澄清改为“先答后问”后，`mission_board`/`plan_confirm` 语气需继续线上观察，避免用户误解为已执行。
