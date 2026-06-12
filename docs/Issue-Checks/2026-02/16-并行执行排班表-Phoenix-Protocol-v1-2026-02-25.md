# 并行执行排班表：T16 Phoenix Protocol v1

- 日期: 2026-02-25
- 目标: 在不影响现网的前提下，尽快形成可运行 MVP

## 任务泳道

| 泳道 | 子任务 | 负责人建议 | 依赖 | 产出 |
|---|---|---|---|---|
| A（Runtime） | M1 watchdog 自愈脚本 | codex | 无 | `deploy/chimera_watchdog.sh` + 审计日志 |
| B（Release） | M2 发布状态机 + snapshot | codex | A（部分） | `deploy/chimera_release_controller.sh` / `deploy/chimera_snapshot.sh` |
| C（Docs/Ops） | Runbook 与验收回填 | 人机协同 | A/B | 更新运维文档与验收结论 |

## 时间窗口建议（夜间）

1. 20:00-20:40：泳道 A（watchdog）编码与本地验证。
2. 20:40-21:20：泳道 B（release/snapshot）编码与 dry-run。
3. 21:20-21:40：泳道 C（文档回填 + 验收清单更新）。
4. 21:40-22:00：全量回归与次晨战报草稿。

## 每阶段可检验点（Gate）

1. Gate-A：手动 kill 网关后，watchdog 在阈值内自动拉起。
2. Gate-B：发布脚本 dry-run 通过，状态机日志完整。
3. Gate-C：模拟 post-verify 失败触发 rollback 成功。
4. Gate-D：`bash deploy/chimera_core_test.sh` 全绿。

## 风险控制

1. 为避免误伤现网，优先在 test profile 演练，再切 prod。
2. 所有自动动作必须落审计日志（jsonl），不接受黑盒执行。
3. 切流步骤必须有单实例锁，防止并发发布。
