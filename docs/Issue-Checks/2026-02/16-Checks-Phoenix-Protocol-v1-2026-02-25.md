# 验收清单：T16 Phoenix Protocol v1

- 日期: 2026-02-25
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`
- 目标: 验证“可自愈 + 可发布 + 可回滚 + 可追溯”闭环

## A. 自愈能力

| 用例ID | 场景 | 操作 | 预期 | 结论 |
|---|---|---|---|---|
| P16-A1 | 网关进程异常退出 | 人为 kill 主进程 | watchdog 在阈值内拉起新进程 | PASS（2026-02-26，手工 kill test gateway 后 `restart_ok`，新 pid 拉起） |
| P16-A2 | `/health` 连续失败 | 模拟健康探针失败 3 次 | 触发一次受控重启 | TODO |
| P16-A3 | 网络抖动恢复 | 注入 Telegram 网络错误 | 达到阈值后重建通道并恢复收发 | TODO |
| P16-A4 | 防重启风暴 | 连续制造故障 | 触发熔断并进入人工接管模式 | TODO |

## B. 发布状态机

| 用例ID | 场景 | 操作 | 预期 | 结论 |
|---|---|---|---|---|
| P16-B1 | preflight 通过 | 执行 release dry-run | 状态机规划与输入校验通过 | PASS（2026-02-25，`RUN_TESTS=0 RUN_AUTH_IT=0 bash deploy/chimera_release_controller.sh dry-run --profile test --green-profile test`） |
| P16-B2 | preflight 失败 | 故意制造配置缺失 | 发布中止且不影响当前运行版本 | TODO |
| P16-B3 | cutover 成功 | real-run 发布 | 状态机走到 `DONE` | PASS（2026-02-26，`release-test-20260226-214153-b3e5797`） |
| P16-B4 | post-verify 失败 | 模拟新版本异常 | 自动进入 `ROLLBACK` | PASS（2026-02-26，`SIMULATE_POST_VERIFY_FAIL=1` 联调通过） |

## C. 回滚与审计

| 用例ID | 场景 | 操作 | 预期 | 结论 |
|---|---|---|---|---|
| P16-C1 | snapshot 可用 | 发布前创建 snapshot | snapshot 记录完整可回放 | PASS（2026-02-25，`bash deploy/chimera_snapshot.sh create --profile test --id-only` + `latest/list`） |
| P16-C2 | 自动回滚成功 | 触发失败发布 | 恢复到上一稳定版本 | PASS（2026-02-26，`rollback_ok` + 最终 `result=rolled_back`） |
| P16-C3 | 审计日志完整 | 检查 `audit_watchdog.jsonl` / `audit_release.jsonl` | 含 request/state/result/ts | PASS（2026-02-25，dry-run 产生 `audit_release.jsonl` 状态流转） |
| P16-C4 | 次晨战报 | 生成 nightly report | 包含成功/失败/回滚统计 | PASS（2026-02-26，`deploy/chimera_nightly_run.sh dry-run` 产出 `nightly-2026-02-26.md`） |

## D. 建议验证命令（草案）

```bash
cd /Users/sourcefire/X-lab/chimera-core

# 1) 先看当前运行状态
bash deploy/chimera_core_deploy.sh status
bash deploy/chimera_watchdog.sh status --profile test
bash deploy/chimera_watchdog.sh status --profile prod

# 2) dry-run 发布状态机
bash deploy/chimera_release_controller.sh dry-run
bash deploy/chimera_release_controller.sh status

# 3) 人工故障注入（示例）
pkill -f "nanobot.cli.commands gateway"

# 4) 查看自愈审计
tail -n 80 chimera-bridge/watchdog/audit_watchdog.jsonl
tail -n 80 chimera-bridge/watchdog/audit_release.jsonl
```

## E. 回填模板

- 分支:
- 提交Hash:
- 测试时间:
- 执行命令:
- 关键日志:
- 结论: PASS / FAIL
- 未决风险:
