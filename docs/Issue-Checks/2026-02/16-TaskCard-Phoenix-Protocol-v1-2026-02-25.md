# 任务卡：T16 Phoenix Protocol v1（赛博修狗）

- 任务ID: T16
- 标题: Watchdog Self-Heal + Release State Machine + Auto Rollback
- 日期: 2026-02-25
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`
- 优先级: P0
- 状态: DONE（2026-02-26）

## 目标

1. 引入独立 watchdog，自动检测并恢复主网关异常。
2. 建立发布状态机（preflight/cutover/verify/rollback）。
3. 发布失败时可自动回滚到最近稳定快照。
4. 输出夜间战报和可追溯审计日志。

## 实施范围

- `/Users/sourcefire/X-lab/chimera-core/deploy/chimera_watchdog.sh`（新增）
- `/Users/sourcefire/X-lab/chimera-core/deploy/chimera_release_controller.sh`（新增）
- `/Users/sourcefire/X-lab/chimera-core/deploy/chimera_snapshot.sh`（新增）
- `/Users/sourcefire/X-lab/chimera-core/deploy/chimera_core_deploy.sh`（增强）
- `/Users/sourcefire/X-lab/chimera-core/chimera-bridge/watchdog/*`（新增，状态与审计）
- `/Users/sourcefire/X-lab/chimera-core/docs/INTEGRATED_RELEASE_RUNBOOK.md`（更新）
- `/Users/sourcefire/X-lab/chimera-core/docs/OPS_QUICK_REFERENCE.md`（更新）

## 实施清单

- [x] S1: 定义 watchdog 配置与状态目录（PID/lock/last_heartbeat/restart_count）。（2026-02-25，`deploy/chimera_watchdog.sh` + `chimera-bridge/watchdog/`）
- [x] S2: 增加 health 探针聚合（进程活性 + `/health` + Telegram 连通性）。（2026-02-25，M1 先落地进程活性 + `/health`，Telegram 专项探针在 M2 补齐）
- [x] S3: 实现自愈重启与重试门限（指数退避 + 熔断窗口）。（2026-02-25，M1 已落地）
- [x] S4: 实现 release-controller 状态机（PREFLIGHT/GREEN_VERIFY/CUTOVER/POST_VERIFY/ROLLBACK）。（2026-02-25，`deploy/chimera_release_controller.sh`）
- [x] S5: 接入 snapshot 机制（发布前后打点，失败自动回滚）。（2026-02-25，`deploy/chimera_snapshot.sh` + controller 回滚链路）
- [x] S6: 输出审计日志（`chimera-bridge/watchdog/audit_watchdog.jsonl`）。（2026-02-25，新增 `chimera-bridge/watchdog/audit_release.jsonl`）
- [x] S7: 增加夜间执行脚本（dry-run + real-run）。（2026-02-25，`chimera_release_controller.sh dry-run|run|status`）
- [x] S8: 增加最小回归测试与联调脚本。（2026-02-25，新增 smoke tests，`bash deploy/chimera_core_test.sh` 100 通过）

## 里程碑拆分（执行版）

- M1（P0，自愈）: S1+S2+S3，目标是“断网/崩溃自动拉起”。
- M2（P0，发布）: S4+S5，目标是“可发布、失败自动回滚”。
- M3（P1，可观测）: S6+S7+S8，目标是“有日志、有战报、可验收”。

## 风险与回滚

1. 风险: watchdog 与主进程互相抢占。
   - 缓解: 单实例锁 + 明确 PID ownership。
2. 风险: 错误触发频繁重启。
   - 缓解: 失败阈值、退避、熔断与人工接管开关。
3. 风险: 发布状态机半途中断。
   - 缓解: 持久化状态 + 幂等恢复步骤。

## 依赖与前置

1. 已有 `deploy/chimera_core_deploy.sh`（start/stop/restart/health）可复用。
2. 已有状态接口鉴权（`X-Status-Token`）可复用。
3. 生产与测试 Telegram token 已隔离（可执行准蓝绿切换）。

## 当前结论（2026-02-25）

1. 文档阶段已收敛：方案+任务卡+验收清单已齐套。
2. M3 已实现并完成联调；T16 M1~M3 收口完成。

## M3 收口记录（2026-02-26）

1. 新增 `deploy/chimera_nightly_report.sh`（按日生成战报 markdown）。
2. 新增 `deploy/chimera_nightly_run.sh`（夜间 dry-run/run + 状态落盘）。
3. 新增回归用例：
   - `tests/test_nightly_report_smoke.py`
   - `tests/test_nightly_run_smoke.py`
4. 全量回归：`bash deploy/chimera_core_test.sh` 通过（113 tests，skipped=3）。
