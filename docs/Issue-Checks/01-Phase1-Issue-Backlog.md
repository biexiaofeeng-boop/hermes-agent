# Phase1 Issue Backlog（实施任务池）

状态枚举：`TODO` / `DOING` / `CHECK` / `DONE` / `BLOCKED`

---

## T01 部署脚本生命周期补全（P0）
- 状态: DONE
- 负责人: codex
- 优先级: P0
- 目标:
  - 为 `deploy/chimera_core_deploy.sh` 增加 `stop/restart/logs/health`。
  - 增加 PID 与日志约定（`.runtime/run/chimera-gateway.pid`, `.runtime/logs/chimera-gateway.log`）。
- 现状证据:
  - `deploy/chimera_core_deploy.sh` 已支持 `deploy/start/stop/restart/logs/health/status`。
  - 已支持独立 runtime HOME 与默认隔离端口 `28790`。
  - `start/stop/restart` 已加入同项目 gateway 进程扫描与残留清理，避免重复轮询实例并发。
- 验收结果（2026-02-19）:
  - 人工验收 A 已通过（部署链路完整通过）。

## T02 Toolchain Registry（P0）
- 状态: DONE
- 负责人: codex
- 优先级: P0
- 目标:
  - 提供 `chimera-bridge/toolchain/registry.json` 与 `registry.schema.json`。
  - 提供工具链清单（Tavily/GitHub/Feishu/Codex/Claude 等）的可用性字段。
- 现状证据:
  - 注册表与 schema 已落地。
  - CLI 已支持 `nanobot toolchain status` 与 `nanobot toolchain check`。
- 验收结果（2026-02-19）:
  - 人工验收 C 已通过（`toolchain status/check --tool codex` 正常，`codex` 健康检查为 `ok`）。

## T03 Tasks Pool + Daily Board（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - 新增 `chimera-bridge/taskops/tasks.json` + schema。
  - 新增看板生成器，输出 `chimera-bridge/boards/YYYY-MM-DD.md`。
- 现状证据:
  - TaskHub 已落地，支持读取/写入/加锁/原子写入/看板生成。
  - CLI 已支持 `nanobot taskops list/add/update/board`。
- 验收结果（2026-02-19）:
  - 人工验收 D（T03）已通过（`taskops list/board` 正常，`chimera-bridge/boards/2026-02-19.md` 可用）。

## T04 Bot Dispatcher（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - 自动领取 `ownerType=bot` 且依赖满足的任务。
- 现状证据:
  - 已在 `nanobot/taskops/services.py` 实现 `TaskDispatcherService`。
  - 已接入 gateway 生命周期，按配置周期调度。
- 验收结果（2026-02-22）:
  - 在 prod profile 执行真实任务链路验证（`closure-t04`）：
    - `task-e1259ad0bd -> done`
    - `task-2f9e7c8c3e -> done`
    - `task-219ff37066 -> done`
  - 日志可见 dispatcher 自动推进记录，依赖顺序生效。

## T05 Human Notifier（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - 将 `ownerType=human` 任务推送 Telegram，并记录通知状态。
- 现状证据:
  - 已在 `nanobot/taskops/services.py` 实现 `HumanTaskNotifierService`。
  - 已支持冷却时间（`renotify_after_s`）与 `lastNotifiedAt` 去重。
- 验收结果（2026-02-22）:
  - prod profile 下通知成功到达 Telegram（含测试任务 `task-9839ae3261`）。
  - `lastNotifiedAt` 正常回写。
  - 冷却行为验证通过（10 分钟会重发），随后将 `renotifyAfterS` 调整回 4 小时并完成任务状态更新。

## T06 高风险工具权限闸门（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - 对 `exec/write/message` 增加最小权限控制（默认 deny）。
- 现状证据:
  - 已实现 `AuthGate` 执行前拦截（高风险工具默认需授权）。
  - 已实现 `execPolicy=balanced`：低风险命令白名单直通，高风险/链式命令继续审批。
  - 已实现持久化审批队列：`chimera-bridge/auth/pending_auth.json`。
  - 已实现审计日志：`chimera-bridge/auth/audit_auth.jsonl`。
  - 已新增审批命令：`nanobot auth list/approve/reject`。
  - 已支持 Telegram 内联审批命令：`/approve <request-id>`、`/reject <request-id> [reason]`、`/auth list`。
- 测试结果（2026-02-19）:
  - 自动化测试通过（`tests/test_auth_gate.py`）。
  - `bash deploy/chimera_core_test.sh` 全量通过（26 tests）。
- 验收结果（2026-02-22）:
  - strict 模式下审批闭环验证通过：
    - 默认拦截：`allowed=False` + 生成 `request_id`
    - `once` 审批：首次放行、二次回到 pending
    - `reject` 审批：状态为 rejected
  - `audit_auth.jsonl` 审计链完整（`requested/approved/consumed/rejected`）。

## T07 Status API 最小鉴权（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - `/status` 增加 token 或 loopback-only 限制。
- 现状证据:
  - 状态服务已支持 `X-Status-Token`。
  - 若未配置 token 且 host 为 `0.0.0.0/::`，gateway 启动时自动回退到 `127.0.0.1`。
- 验收结果（2026-02-19）:
  - 人工验收 B 已通过（未授权 `/status` 返回 401；携带 `X-Status-Token` 返回 200）。

## T08 测试与回归（P1）
- 状态: DONE
- 负责人: codex
- 优先级: P1
- 目标:
  - 建立最小测试集（deploy 生命周期、schema、dispatcher/notifier、status 鉴权）。
- 现状证据:
  - 已新增 `tests/` 最小回归集，覆盖 deploy/toolchain/taskops/status/dispatcher/notifier。
  - 已新增一键命令脚本 `deploy/chimera_core_test.sh`。
  - 本地执行 `bash deploy/chimera_core_test.sh`：26 tests passed。
- 验收结果（2026-02-19）:
  - 人工验收 G（T08）已通过（`Ran 14 tests ... OK`）。

## T09 AuthGate v2 设计与实施（P0/P1）
- 状态: DONE
- 负责人: chimera-core-codex
- 优先级: P0/P1
- 目标:
  - 引入分层策略（security + ask）与审批作用域（once/session/ttl/always）。
  - 支持审批后自动续跑，移动端审批链路闭环。
  - 引入 approver ACL，强化 `/approve` 安全边界。
  - 扩展 `guardrail` 模式与 `mission` 作用域，实现“主节点宽松/子节点收敛”分层策略。
- 现状证据:
  - 设计文档已完成：`docs/Issue-Checks/06-AuthGate-v2-设计方案-2026-02-20.md`。
  - 任务卡已创建：`docs/Issue-Checks/2026-02/06-TaskCard-AuthGate-v2-2026-02-20.md`。
  - 验收清单已创建：`docs/Issue-Checks/2026-02/06-Checks-AuthGate-v2-2026-02-20.md`。
  - P0 已落地：`highRiskTools` 默认收敛为 `["exec"]`，`execPolicy=balanced`，支持 `policy.json` 覆盖。
  - P1 已落地：
    - 审批作用域：`once/session/ttl/always`（CLI + Telegram）。
    - 自动续跑：审批后自动投递原始消息回队列（无需重发）。
    - 审批 ACL：`authGate.approvers` 独立校验 + 审计事件 `approver_denied`。
    - 规则持久化：`chimera-bridge/auth/rules.json`（含 `rules.schema.json`）。
  - 本轮扩展（2026-02-21）：
    - `execPolicy.mode` 新增 `guardrail`，实现默认放行 + 红线拦截。
    - `scope` 新增 `mission`，支持 `mission_id/node/workspace` 约束。
    - 新增 `auth mission-grant`，支持战役级授权直发。
    - `policy.json` 支持 `activeProfile/profiles`（`chimera_main_relaxed` / `child_node_constrained`）。
  - P0/P1 代码：`nanobot/auth/gate.py`、`nanobot/agent/loop.py`、`nanobot/cli/commands.py`、`nanobot/config/schema.py`、`chimera-bridge/auth/policy.json`、`chimera-bridge/auth/policy.schema.json`、`chimera-bridge/auth/rules.schema.json`。
  - 新增联调脚本：`deploy/chimera_auth_it.sh`（main-smoke/child-check/remote-acceptance）。
- 验收结果（2026-02-21）:
  - 自动回归：`bash deploy/chimera_core_test.sh` 通过（54 tests，含 3 条远端验收用例默认 skip）。
  - 人工联调：`bash deploy/chimera_auth_it.sh all` 输出全 PASS（main 放行与越界拦截、child strict 收敛均符合预期）。

## T10 TaskOps ControlPlane v1（P1）
- 状态: DONE
- 负责人: chimera-core-codex
- 优先级: P1
- 目标:
  - 将 TaskOps 能力控制面化：新增 `taskops.*` gateway methods（list/add/update/claim/complete）。
  - 新增 dispatcher/notifier 结构化 run log（jsonl），支持查询与裁剪。
  - 新增任务状态变化事件广播（claim/complete/notify/fail）。
- 现状证据:
  - 对比分析报告：`docs/Issue-Checks/08-ProjectMgmt-HumanCollab-Compare-Report-2026-02-21.md`。
  - 任务卡：`docs/Issue-Checks/2026-02/08-TaskCard-TaskOps-ControlPlane-v1-2026-02-21.md`。
  - 验收清单：`docs/Issue-Checks/2026-02/08-Checks-TaskOps-ControlPlane-v1-2026-02-21.md`。
  - 实施顺序脚本清单：`docs/Issue-Checks/2026-02/08-实施顺序脚本清单-TaskOps-ControlPlane-v1-2026-02-21.md`。
- 验收结果（2026-02-21）:
  - M1/M2/M3 的 C01-C12 全量通过（自动化）。
  - `taskops` CLI 兼容不回归（含空目录 bootstrap）。
  - 主分支已合并：`master@7c03c60`（后续脚本增强提交：`master@539743d`）。
  - prod profile 验收路径已打通（`chimera_profile.sh` + `chimera_core_deploy.sh`）。


## T11 S1 核心能力治理 v1（P0/P1）
- 状态: DONE
- 负责人: chimera-core-codex
- 优先级: P0/P1
- 目标:
  - 建立统一 Capability Registry（tool/skill/service/executor/channel）与 readiness 状态。
  - 打通 TaskOps feasibility guard（claim 前可执行性校验）。
  - 打通执行器路由（local-tools / executor:codex / executor:claude）。
- 现状证据:
  - 需求架构: `docs/Issue-Checks/2026-02/10-S1-核心能力治理-需求架构与实施计划-2026-02-22.md`。
  - 任务卡: `docs/Issue-Checks/2026-02/11-TaskCard-S1-Capability-Governance-v1-2026-02-22.md`。
  - 验收清单: `docs/Issue-Checks/2026-02/11-Checks-S1-Capability-Governance-v1-2026-02-22.md`。
  - 实施顺序脚本清单: `docs/Issue-Checks/2026-02/11-实施顺序脚本清单-S1-Capability-Governance-v1-2026-02-22.md`。
  - 已完成里程碑提交:
    - M1: `61ebcc1`（registry/state/schema + sync/list）。
    - M2: `a1ddbed`（readiness check + state 落盘 + `capability check`）。
    - M3: `46338b7`（feasibility + executor router + codex/claude adapters）。
    - M4: `8bbf8ca` + `ae33cad`（runlog 查询增强 + `capability status/runs` + docs 回写）。
  - 本地回归结果:
    - `bash deploy/chimera_core_test.sh` => `Ran 66 tests ... OK (skipped=3)`。
  - 人工联调结果（2026-02-23）:
    - Telegram 收到人类协同任务通知（task `task-3977c46291`）。
    - 任务 `done` 后短窗口无重复通知（冷却/状态控制正常）。
    - `/rpc`：`capability.status` 与 `taskops.feasibility` 返回 `ok=true`。

---

## 全局 DoD（Definition of Done）
- 全部 T01-T11 到达 `DONE`（2026-02-23 已完成 T11 收口）。
- 连续运行 24h 无崩溃、无僵尸进程。
- 看板每日自动更新可用。
- 人机分流任务可闭环推进。
