# 验收清单：AuthGate v2

- 任务ID: T09
- 版本/提交:
  - `7c03c60`（合并到 `master`）
  - `539743d`（发布后联调脚本）
- 验收日期: 2026-02-20 ~ 2026-02-21
- 验收人: chimera-core-codex（自动）+ sourcefire（人工）

## 验收环境
- 分支: `master`（已合并）
- 运行环境: `/Users/sourcefire/X-lab/chimera-core-prod`
- 配置差异: `authGate.execPolicy`、`authGate.approvers`、`authGate.resume`、`authGate.revokeDenyTtlS`

## 自动化与基础用例清单
| 用例ID | 目标 | 步骤 | 预期 | 实际 | 结论 |
|---|---|---|---|---|---|
| C01 | 低风险 exec 免审批 | Telegram 发送 `echo/ping/ls` | 直接执行，无 pending | 用户已完成（P0） | PASS |
| C02 | 高风险 exec 触发审批 | Telegram 发送链式命令/危险命令 | 生成 pending + 通知 | 用户已完成（P0） | PASS |
| C03 | once 审批语义 | `/approve <id> once` 后重试两次 | 第一次放行、第二次再审批 | `tests/test_auth_gate.py::test_request_approve_consume_one_time` | PASS |
| C04 | session 审批语义 | `/approve <id> session` 同会话重复执行 | 会话内连续放行 | `tests/test_auth_gate.py::test_scope_session_reuses_approval_in_same_session` | PASS |
| C05 | ttl 审批语义 | `/approve <id> ttl 1m` | TTL 内放行，过期后再审批 | `tests/test_auth_gate.py::test_scope_ttl_expires_then_requires_approval_again` | PASS |
| C06 | always 审批语义 | `/approve <id> always` | 同类请求长期放行 | `tests/test_auth_gate.py::test_scope_always_matches_principal_across_sessions` | PASS |
| C07 | 自动续跑 | 命中审批后直接批准 | 无需重发，任务继续执行 | `tests/test_auth_gate.py::test_take_resume_payload_only_once` + Telegram 人工联调 | PASS |
| C08 | ACL 拒绝 | 非 approver 发 `/approve` | 拒绝并审计 | `tests/test_auth_gate.py::test_approver_acl_matching` | PASS |
| C09 | 审计完整性 | 检查 `audit_auth.jsonl` | request/resolve/consume 链完整 | `deploy/chimera_core_test.sh` 回归通过（54 tests） | PASS |

## 扩展验收（Guardrail + Mission）
| 用例ID | 目标 | 结果 | 结论 |
|---|---|---|---|
| C10 | 主节点 mission 放行 | `deploy/chimera_auth_it.sh main-smoke` 中 `ssh_sync_allow`/`remote_restart_allow` PASS | PASS |
| C11 | mission 越界拦截 | `boundary_block` 输出 `allowed=False expected=False` | PASS |
| C12 | 子节点 strict 收敛 | `deploy/chimera_auth_it.sh child-check` 输出 `allowed=False expected=False` | PASS |

## 人工联调用例（U01~U10）
| 用例ID | 目标 | 结果 | 结论 |
|---|---|---|---|
| U01~U08 | 审批触发、拒绝、always、ttl、revoke、续跑链路 | sourcefire 已完成联调并反馈通过 | PASS |
| U09 | 非 owner 越权审批（当前单用户 Telegram） | 当前场景暂不执行，后续多账号联调补测 | DEFERRED |
| U10 | TTL 到期后再次请求必须回到 pending | 已复核 `rule_expired -> requested` 事件链（2026-02-21） | PASS |

## 缺陷记录
- 本轮无阻塞缺陷。

## 最终结论
- 结论: PASS（已合并，已完成发布后联调）
- 备注:
  - 自动回归：`bash deploy/chimera_core_test.sh` -> `Ran 54 tests ... OK (skipped=3)`
  - 发布后联调：`bash deploy/chimera_auth_it.sh all` -> PASS
  - U09 已登记为延后验证，不阻塞本次版本收口。
