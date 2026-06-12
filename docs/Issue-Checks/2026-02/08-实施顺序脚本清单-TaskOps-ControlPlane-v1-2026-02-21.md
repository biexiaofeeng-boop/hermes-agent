# 实施顺序脚本清单：TaskOps ControlPlane v1

- 任务ID: T10
- 分支: `codex/feature-taskops-controlplane-v1`（已合并至 `master`）
- 适用目录: `/Users/sourcefire/X-lab/chimera-core-prod`
- 目标: 按 M1/M2/M3 顺序推进，确保每阶段可独立验收与回滚。

## 0) 预检与基线

```bash
cd /Users/sourcefire/X-lab/chimera-core-prod
git status --short
bash deploy/chimera_core_test.sh
```

通过标准：基线测试通过，且当前分支工作区状态清晰（便于定位新增变更）。

## 1) M1 - TaskOps Gateway API（控制面打通）

### 1.1 开发与联调顺序

```bash
# 1) 新增/接入 gateway methods 与 handler
rg -n "taskops|gateway|methods" nanobot

# 2) 增加 method 参数校验与错误码映射
rg -n "schema|validate|ValueError" nanobot/taskops nanobot/cli

# 3) 本地命令回归
python -m nanobot.cli.commands taskops list
python -m nanobot.cli.commands taskops add --title "smoke" --owner-type bot
python -m nanobot.cli.commands taskops update task-xxxxxxxxxx --status in_progress
```

### 1.2 阶段验证

```bash
bash deploy/chimera_profile.sh use prod
bash deploy/chimera_profile.sh restart
bash deploy/chimera_core_test.sh
```

通过标准：C01-C05 通过（`taskops.list/add/update/claim/complete` 可用），CLI 兼容不回归。

## 2) M2 - Run Log（可观测）

### 2.1 开发与联调顺序

```bash
# 1) 落地 run log 模块（append/read/prune）
rg -n "dispatcher|notifier|complete_task|jsonl|run" nanobot/taskops

# 2) 触发 bot/human 路径，检查日志产出
python -m nanobot.cli.commands taskops board
ls -la chimera-bridge/taskops/runs
```

### 2.2 阶段验证

```bash
bash deploy/chimera_core_test.sh
python -m unittest -k taskops
```

通过标准：C06-C09 通过（run log 可读、可限流、可裁剪）。

## 3) M3 - 事件广播（实时协同）

### 3.1 开发与联调顺序

```bash
# 1) 在 claim/complete/notify/fail 节点发事件
rg -n "claim|complete|notify|fail|publish|event" nanobot

# 2) 验证状态接口与事件链路
curl -s http://127.0.0.1:18790/health
curl -s -H "X-Status-Token: $NANOBOT_STATUS_TOKEN" http://127.0.0.1:18790/status
```

### 3.2 阶段验证

```bash
bash deploy/chimera_core_test.sh
```

通过标准：C10-C12 通过（`taskops.changed` 事件可观测，事件内容完整）。

## 4) 收口与文档回写

```bash
# 更新验收记录与 backlog 状态
rg -n "T10|C0[1-9]|C1[0-2]" docs/Issue-Checks
```

通过标准：
- `08-Checks-TaskOps-ControlPlane-v1-2026-02-21.md` 中 C01-C12 全部收口。
- `01-Phase1-Issue-Backlog.md` 中 T10 状态更新为 `DONE`。

## 4.1 发布后联调脚本（本轮新增）

```bash
cd /Users/sourcefire/X-lab/chimera-core-prod
bash deploy/chimera_auth_it.sh all
```

通过标准：
- `ssh_sync_allow` / `remote_restart_allow` / `boundary_block` 全部 PASS。
- `child_strict_check` 为 `allowed=False expected=False`。

## 5) 回滚脚本（若阶段失败）

```bash
cd /Users/sourcefire/X-lab/chimera-core-prod
git restore --source=HEAD -- nanobot/taskops nanobot/cli/commands.py
bash deploy/chimera_profile.sh restart
bash deploy/chimera_core_test.sh
```

通过标准：gateway 恢复可用，基线测试回到改造前稳定态。
