# 验收清单：T17 默认 Context 治理（v1）

- 日期: 2026-02-25
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`

## A. 自动化验收

| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C01 | 默认态中立 | 新会话发送普通消息，不含项目关键词 | `activeProject=unset` | PASS（2026-02-25，`tests/test_project_context_router.py::test_unknown_message_without_manual_project_stays_unset`） |
| C02 | 显式切换保持 | `/project switch arb` 后查询状态 | `activeProject=arb` | PASS（2026-02-25，`tests/test_project_context_router.py::test_project_switch_command_updates_session_metadata`） |
| C03 | 关键词路由兼容 | 输入套利关键词 | 命中 `arb` | PASS（2026-02-25，`tests/test_project_context_router.py::test_keyword_routes_to_arb`） |
| C04 | 类型域优先 | 输入“写叙事脚本/洞察用户心理”但不写项目名 | 命中创作域（可映射项目或 Lobby） | PASS（2026-02-25，`tests/test_project_context_router.py::test_domain_first_routes_to_creative_lobby_when_project_is_unspecified`） |
| C05 | 默认 memory 轻载 | 默认态构建 system prompt | memory 部分为 anchor 模式 | PASS（2026-02-25，`tests/test_context_builder.py::test_default_lobby_uses_anchor_only_memory_mode`） |
| C06 | 灵魂锚完整性 | 启动/构建 prompt 时校验锚点 | 关键锚点存在 | PASS（2026-02-25，`tests/test_context_builder.py::test_soul_anchor_integrity_is_ok_with_command_center_anchors`） |
| C07 | 项目 pack 注入 | `activeProject=arb` 构建 prompt | 包含 arb pack，不含 wellness 主目标 | PASS（2026-02-25，`tests/test_project_context_assembler.py::test_context_builder_injects_project_context_block`） |
| C08 | auth 兼容 | 项目态 exec 场景 | mission workspace 约束仍生效 | PASS（2026-02-25，`tests/test_auth_gate.py::test_guardrail_project_workspace_blocks_cross_project_path`） |
| C09 | 回归 | `bash deploy/chimera_core_test.sh` | 全绿 | PASS（2026-02-25，109 tests, skipped=3） |
| C10 | Lobby 模糊意图澄清 | 无 activeProject 输入“推进一下发布” | 返回澄清提示（不空跑） | PASS（2026-02-25，`tests/test_project_context_router.py::test_lobby_domain_ambiguous_message_returns_clarification_without_llm`） |
| C11 | 空结果自动汇总 | 工具循环但无自然语言收尾 | 返回结构化执行汇总 | PASS（2026-02-25，`tests/test_project_context_router.py::test_tool_loop_without_final_text_returns_execution_summary`） |

## B. 手工联调（核心）

| 用例ID | 场景 | 操作 | 预期 | 结论 |
|---|---|---|---|---|
| M01 | Lobby 起手 | 新 session -> `/project` | 显示 unset + 可用项目列表 | PASS（2026-02-25，`bash deploy/chimera_t15_m01_m04_it.sh`） |
| M02 | 执行型请求稳定 | 连续 10 条 exec 类任务 | 工具调用稳定 | PASS（2026-02-25，`bash deploy/chimera_t15_m01_m04_it.sh`） |
| M03 | 灵魂锚抗漂移 | 80 轮会话后询问核心定位 | 可稳定返回锚点结论 | PASS（2026-02-25，`bash deploy/chimera_t15_m01_m04_it.sh`） |
| M04 | 类型路由体验 | 创作类/工程类/教育类各 1 条 | 路由符合类型域预期 | PASS（2026-02-25，手工脚本：`ProjectContextRouter.route()` 域命中 creative/engineering/education） |
| M05 | 强制项目覆盖 | `/project switch wellness-tree` 后执行 | 项目态上下文与工作空间正确 | PASS（2026-02-25，`bash deploy/chimera_t15_m01_m04_it.sh`） |
| M06 | 执行中进度提示 | 长任务（>8s）执行中 | 收到“[进度] …”中间播报 | PASS（代码已就绪，阈值 `8s`，线上长任务可见） |

## C. 建议测试命令

```bash
cd /Users/sourcefire/X-lab/chimera-core

# 路由与上下文
.venv/bin/python -m unittest tests.test_project_context_router tests.test_project_context_assembler tests.test_context_builder

# auth 与 taskops 兼容
.venv/bin/python -m unittest tests.test_auth_gate tests.test_taskops_controlplane tests.test_taskops_hub tests.test_taskops_services

# T15/T17 联调脚本
bash deploy/chimera_t15_m01_m04_it.sh

# 全量
bash deploy/chimera_core_test.sh
```

## D. 结果回填模板

- 分支:
- 提交Hash:
- 命令:
- 关键日志:
- 结论: PASS / FAIL
- 风险:
