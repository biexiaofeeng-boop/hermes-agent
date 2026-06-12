# 实施顺序脚本清单：T16 Phoenix Protocol v1

- 适用目录: `/Users/sourcefire/X-lab/chimera-core`
- 目标: 最小落地“自愈 + 发布状态机 + 回滚”闭环

## 0) 基线确认

```bash
cd /Users/sourcefire/X-lab/chimera-core
git status --short
bash deploy/chimera_core_test.sh
bash deploy/chimera_profile.sh profile-status all
```

## 1) 创建迭代分支

```bash
cd /Users/sourcefire/X-lab/chimera-core
git checkout master
git checkout -b codex/t16-phoenix-protocol-v1
```

## 2) M1（自愈 watchdog）

```bash
# 新增脚本（建议）
# - deploy/chimera_watchdog.sh
# - chimera-bridge/watchdog/.gitkeep

# 核心能力
# - watchdog start|stop|status|tick
# - 探针: 进程活性 + /health (X-Status-Token)
# - 自愈: 失败阈值触发 restart，含退避与熔断
```

建议检查命令：

```bash
bash deploy/chimera_watchdog.sh start --profile prod
bash deploy/chimera_watchdog.sh status --profile prod
bash deploy/chimera_watchdog.sh tick --profile prod
tail -n 120 chimera-bridge/watchdog/audit_watchdog.jsonl
```

## 3) M2（发布状态机 + 快照回滚）

```bash
# 新增脚本（建议）
# - deploy/chimera_release_controller.sh
# - deploy/chimera_snapshot.sh

# 状态机目标:
# IDLE -> PREFLIGHT -> GREEN_VERIFY -> CUTOVER -> POST_VERIFY -> DONE
# 失败路径:
# ANY -> ROLLBACK -> ALERT -> IDLE
```

建议检查命令：

```bash
bash deploy/chimera_release_controller.sh dry-run --profile prod
bash deploy/chimera_snapshot.sh create --profile prod --label pre-release
bash deploy/chimera_release_controller.sh run --profile prod
```

## 4) M3（可观测与文档）

```bash
# 新增脚本（建议）
# - deploy/chimera_nightly_report.sh
# - deploy/chimera_nightly_run.sh

# 文档回填
# - docs/INTEGRATED_RELEASE_RUNBOOK.md
# - docs/OPS_QUICK_REFERENCE.md
# - docs/Issue-Checks/2026-02/16-Checks-Phoenix-Protocol-v1-2026-02-25.md
```

建议检查命令：

```bash
RUN_TESTS=0 RUN_AUTH_IT=0 bash deploy/chimera_nightly_run.sh dry-run --profile test --green-profile test
bash deploy/chimera_nightly_run.sh status --profile test --green-profile test
bash deploy/chimera_nightly_report.sh latest --profile test

rg -n "watchdog|release_controller|snapshot|Phoenix" docs deploy
bash deploy/chimera_core_test.sh
```

## 5) 验收与收口

```bash
# 先跑 T16 验收项，再跑全量回归
bash deploy/chimera_core_test.sh

# 关键日志
tail -n 150 chimera-bridge/watchdog/audit_watchdog.jsonl
tail -n 150 .runtime/profiles/prod/logs/chimera-gateway.log
```

通过标准：

1. 网关异常可自动恢复。
2. 发布失败可自动回滚。
3. 全流程可审计（状态流转与动作日志可追溯）。

## M2 收口记录（2026-02-25）

1. 已新增 `deploy/chimera_snapshot.sh`，支持 `create/list/show/latest/rollback`。
2. 已新增 `deploy/chimera_release_controller.sh`，支持 `dry-run/run/status`。
3. 已新增回归用例：
   - `tests/test_snapshot_script_smoke.py`
   - `tests/test_release_controller_smoke.py`
4. 全量回归：`bash deploy/chimera_core_test.sh` 通过（100 tests，skipped=3）。

## M3 收口记录（2026-02-26）

1. 已新增 `deploy/chimera_nightly_report.sh`，支持 `generate/latest`。
2. 已新增 `deploy/chimera_nightly_run.sh`，支持 `dry-run/run/status`。
3. 已新增回归用例：
   - `tests/test_nightly_report_smoke.py`
   - `tests/test_nightly_run_smoke.py`
4. 全量回归：`bash deploy/chimera_core_test.sh` 通过（113 tests，skipped=3）。
