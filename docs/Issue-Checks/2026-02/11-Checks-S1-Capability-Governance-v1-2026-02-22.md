# 验收清单：S1 核心能力治理 v1

- 任务ID: T11
- 分支: `codex/feature-capability-governance-v1`
- 验收日期: 2026-02-22（起）
- 验收人: chimera-core-codex（自动）+ sourcefire（人工）

## 验收环境
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`
- 运行方式: `bash deploy/chimera_core_deploy.sh restart`
- 关键配置: `taskops.enabled=true`，并开启 feasibility/router 对应开关（新增后记录）

## M1：能力注册统一（registry + sync）
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C01 | 汇聚能力 | 执行 `capability sync --from toolchain --from skills` | 生成统一 registry | PASS（sources=toolchain,skills；incoming=14；total=14） |
| C02 | schema 校验 | `CapabilityRegistry.ensure_files/load_registry/load_state` | 校验通过 | PASS（schema 文件存在且 load 校验通过） |
| C03 | 冲突覆盖 | 预置 `executor:codex` 冲突记录后执行 sync | 按优先级覆盖 | PASS（记录被 toolchain 源更新，`counts.updated=1`） |
| C04 | 能力列表 | `capability list --show-disabled` | 显示 type/risk/requires | PASS（CLI 输出 Capability Registry，字段完整） |

## M2：readiness 检查（check + state + audit）
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C05 | 全量检查 | 执行 `capability check --timeout 3` | 返回每项 readiness | PASS（返回 14 项，counts: ready=9 blocked=5） |
| C06 | 缺依赖阻断 | readiness 检查 `executor:codex/service:github` | 标记 `blocked` + reason | PASS（missing env: `OPENAI_API_KEY`/`GH_TOKEN`） |
| C07 | 状态落盘 | 检查 `chimera-bridge/capabilities/state.json` | 状态与时间戳更新 | PASS（`checkedAt/updatedAt/readiness/reason` 随检查更新） |
| C08 | 审计日志 | 执行 `capability runs --limit 5` | 包含 check/decision 事件 | PASS（`action=check` 已记录；M4 新增 runlog） |

## M3：Task Feasibility + Executor Router
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C09 | 不满足能力不 claim | `tests.test_taskops_feasibility::test_claim_blocks_when_required_capability_missing` | 任务被标记 blocked | PASS |
| C10 | 满足能力可 claim | `tests.test_taskops_services::test_dispatcher_completes_claimed_bot_task` | claim 成功并进入 in_progress/done | PASS |
| C11 | codex 路由 | `tests.test_taskops_feasibility` 路由路径覆盖 | 调用 codex adapter | PASS |
| C12 | claude 路由 | `tests.test_taskops_feasibility::test_dispatcher_executes_with_selected_adapter` | 调用 claude adapter | PASS |
| C13 | fallback 生效 | `tests.test_taskops_feasibility::test_guard_selects_fallback_executor` | 路由 fallbackExecutors | PASS |
| C14 | 权限一致 | `tests.test_auth_gate` 全套 + dispatcher 回归 | AuthGate 仍生效 | PASS |

## M4：控制面/API + 回归收口
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C15 | capability API | `CapabilityControlPlane.handle_rpc` + CLI `capability list/status/check/sync/runs` | 返回结构化结果 | PASS |
| C16 | task feasibility API | `tests.test_taskops_controlplane::test_feasibility_rpc_uses_guard` | 返回任务可执行性 | PASS |
| C17 | runlog 可查询 | CLI `capability runs --limit/--action/--id` + `tests.test_capability_controlplane::test_runs_support_filters` | 支持 limit 与过滤 | PASS |
| C18 | 回归测试 | `bash deploy/chimera_core_test.sh` | 全绿通过 | PASS（`Ran 66 tests ... OK (skipped=3)`） |
| C19 | 文档一致性 | 回写 taskcard/checks/backlog/index | 状态一致 | PASS（本次 M4 收口已同步） |
| C20 | 人工联调 | 真实通道 + 人机任务 | 闭环通过 | PASS（2026-02-23：Telegram 收到 `task-3977c46291`；done 后短窗口无重复；`capability.status`/`taskops.feasibility` RPC 均 `ok=true`） |

## 回归清单
- [x] `bash deploy/chimera_core_test.sh` 通过（`Ran 66 tests ... OK (skipped=3)`）
- [x] `taskops` 主路径不回归（list/add/update/board/claim/complete）
- [x] `auth` 主路径不回归（pending/approve/reject/resume）
- [x] status api `/health` + `/status` + `/rpc` 主路径可用

## 结果记录模板
- 提交Hash: `61ebcc1`, `a1ddbed`, `46338b7`, `8bbf8ca`, `ae33cad`
- 执行命令:
  - `.venv/bin/python -m unittest tests.test_cli_smoke tests.test_capability_controlplane tests.test_capability_checker tests.test_capability_sync`
  - `bash deploy/chimera_core_test.sh`
  - `.venv/bin/python -m nanobot.cli.commands capability sync --from toolchain --from skills`
  - `.venv/bin/python -m nanobot.cli.commands capability status`
  - `.venv/bin/python -m nanobot.cli.commands capability check --timeout 3`
  - `.venv/bin/python -m nanobot.cli.commands capability runs --limit 5`
  - `.venv/bin/python -m nanobot.cli.commands taskops feasibility --limit 5`
  - `TG_CHAT_ID=8464732775 bash /tmp/chimera_c20_it.sh`（实网联调）
- 结果摘要:
  - Capability 控制面新增 `status/runs` 与 runlog 过滤，CLI/API 路径可用。
  - Task feasibility 与 executor 路由链路在自动化测试通过。
  - 全量回归通过，且 C20 实网联调通过（Telegram + 冷却 + RPC）。
- 结论: DONE
- 备注: T11 C01-C20 全量完成。

## 最终结论
- 结论: DONE
- 备注: C01-C20 全量通过，T11 收口完成。
