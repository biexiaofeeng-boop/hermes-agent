# 发布记录：Auth + TaskOps 本轮收口

- 日期：2026-02-21
- 发布分支：`codex/feature-taskops-controlplane-v1`
- 目标分支：`master`
- 发布环境：`/Users/sourcefire/X-lab/chimera-core-prod`

## 1) 版本与提交

- `7c03c60`：`feat(taskops,auth): add control plane, guardrail profiles, and mission auth`
- `539743d`：`chore(test): add scripted auth integration checks for main and child nodes`

## 2) 本轮功能收口

- TaskOps ControlPlane v1：
  - `taskops.*` gateway methods（list/add/update/claim/complete）。
  - run-log（jsonl）记录与读取。
  - 关键状态事件广播（claim/complete/notify/fail）。
- Auth 扩展：
  - `exec_policy_mode=guardrail`（默认放行 + 红线拦截）。
  - `scope=mission`（mission_id/node/workspace 约束）。
  - `auth mission-grant`（战役级授权）。
  - `execPolicy.activeProfile/profiles`（主节点宽松/子节点收敛）。
- 发布后联调脚本：
  - `deploy/chimera_auth_it.sh`（`main-smoke`/`child-check`/`remote-acceptance`）。

## 3) 验收与结果

- 自动回归：
  - `bash deploy/chimera_core_test.sh` -> `Ran 54 tests ... OK (skipped=3)`。
  - 说明：skip=3 为远端网络稳定后执行的验收用例。
- 人工联调（sourcefire）：
  - `bash deploy/chimera_auth_it.sh all`。
  - 输出：
    - `ssh_sync_allow ... PASS`
    - `remote_restart_allow ... PASS`
    - `boundary_block ... PASS`
    - `child_strict_check: allowed=False expected=False`

## 4) 发布后 5 项验收清单（prod）

```bash
cd /Users/sourcefire/X-lab/chimera-core-prod
bash deploy/chimera_profile.sh current
bash deploy/chimera_profile.sh status
bash deploy/chimera_profile.sh health
bash deploy/chimera_core_test.sh
bash deploy/chimera_auth_it.sh all
```

通过标准：
- profile 为 `prod`；
- gateway `running`；
- `health` 返回 OK；
- 回归测试通过；
- auth 联调脚本全 PASS。

## 5) 待办（不阻塞发布）

- 远端网络稳定后执行：
  - `bash deploy/chimera_auth_it.sh remote-acceptance`
- 联调结果回写到本文件与 `08-Checks-TaskOps-ControlPlane-v1-2026-02-21.md`。

## 6) 2026-02-22 最终收口补记（T04/T05/T06）

- T04（Bot Dispatcher）：
  - `closure-t04` 任务链 `task-e1259ad0bd`、`task-2f9e7c8c3e`、`task-219ff37066` 全部 `done`。
  - dispatcher 日志显示依赖顺序自动推进。
- T05（Human Notifier）：
  - Telegram 通知链路已实测可达，`lastNotifiedAt` 正常回写。
  - 冷却窗口行为符合预期（短窗口会重发）；已按运行策略调整为 4 小时。
- T06（高风险权限闸门）：
  - strict 模式验证通过：默认拦截 -> 审批 once -> 首次放行 -> 二次回到 pending。
  - reject 流程验证通过，审计日志包含 `requested/approved/consumed/rejected` 完整链路。

结论：本轮 Auth + TaskOps 发布项与收口项全部完成，进入下一阶段迭代。
