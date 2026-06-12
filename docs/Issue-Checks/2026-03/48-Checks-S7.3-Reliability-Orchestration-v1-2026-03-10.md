# 验收清单：S7.3 稳定性编排（v1）

- 日期：2026-03-10
- 状态：DONE

## C01 任务完成确定性
- [x] DONE 任务具备 `completion_contract`（含 evidence）
- [x] 无证据路径不会被标记 DONE
- [x] `FAILED/BLOCKED` 具备结构化 reason

## C02 子代理回报可靠性
- [x] announce 带稳定 `announce_id`
- [x] 临时故障后重试成功可见
- [x] 重复回报不重复展示（幂等）

## C03 工具环路防护
- [x] 可识别同参无进展重复调用
- [x] warn/block 双阈值可配置
- [x] 阻断时给出可执行建议，不沉默失败

## C04 上下文预算守卫
- [x] soft 阈值触发压缩摘要
- [x] hard 阈值触发轻量降级策略
- [x] 降级触发有 metadata 与日志记录

## C05 兼容性与回归
- [x] 不改变 AuthGate 语义边界
- [x] Telegram/Feishu 主链路不回退
- [x] 现有核心测试通过

## C06 最小测试命令
- [x] `python -m py_compile nanobot/agent/loop.py nanobot/agent/subagent.py nanobot/taskops/services.py nanobot/providers/litellm_provider.py nanobot/config/schema.py`
- [x] `python -m unittest tests.test_taskops_services tests.test_subagent_project_workspace tests.test_session_context_window -v`
- [x] `python -m unittest tests.test_agent_loop_dialogue_mode tests.test_taskops_controlplane tests.test_taskops_feasibility -v`
- [x] `bash deploy/chimera_core_test.sh`（以 `PYTHON_BIN=/Users/sourcefire/X-lab/chimera-core-prod/.venv/bin/python` 运行通过）

## 回填结论（待执行后更新）
- 验收结论：通过。S7.3（T01~T12）代码、测试、文档回填已完成。
- 关键验证命令与结果：
  - `python -m py_compile ...`：通过。
  - `python -m unittest tests.test_taskops_services tests.test_subagent_project_workspace tests.test_session_context_window -v`：17 通过。
  - `python -m unittest tests.test_agent_loop_dialogue_mode tests.test_taskops_controlplane tests.test_taskops_feasibility -v`：23 通过。
  - `PYTHON_BIN=/Users/sourcefire/X-lab/chimera-core-prod/.venv/bin/python bash deploy/chimera_core_test.sh`：212 通过，3 跳过。
- 残留风险：
  - 仓库内 `.venv` 当前为自引用软链；若不显式设置 `PYTHON_BIN`，`chimera_core_test.sh` 会回退到系统 Python 3.9 并产生环境性失败。
