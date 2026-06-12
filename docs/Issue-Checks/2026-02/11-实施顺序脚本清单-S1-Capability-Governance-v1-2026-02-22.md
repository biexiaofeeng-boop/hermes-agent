# 实施顺序脚本清单：S1 核心能力治理 v1

- 任务ID: T11
- 分支: `codex/feature-capability-governance-v1`
- 适用目录: `/Users/sourcefire/X-lab/chimera-core`
- 目标: 按 M1/M2/M3/M4 顺序推进，每阶段独立可验收与回滚。

## 0) 基线预检

```bash
cd /Users/sourcefire/X-lab/chimera-core
git status --short
bash deploy/chimera_core_test.sh
```

通过标准：基线测试通过，工作区状态清晰。

## 1) M1 - 能力注册统一

### 1.1 开发检查点

```bash
rg -n "toolchain|skills|registry|capability" nanobot
rg -n "taskops|schema" chimera-bridge/taskops
```

### 1.2 冒烟验证

```bash
python -m nanobot.cli.commands capability sync
python -m nanobot.cli.commands capability list
```

通过标准：C01-C04 通过。

## 2) M2 - readiness 检查引擎

### 2.1 开发检查点

```bash
rg -n "readiness|check|blocked|degraded|state" nanobot
```

### 2.2 冒烟验证

```bash
python -m nanobot.cli.commands capability check
ls -la chimera-bridge/capabilities
```

通过标准：C05-C08 通过。

## 3) M3 - Task Feasibility + Executor Router

### 3.1 开发检查点

```bash
rg -n "requiredCapabilities|preferredExecutor|fallbackExecutors|feasibility" nanobot chimera-bridge/taskops
rg -n "codex|claude|executor|router|adapter" nanobot
```

### 3.2 冒烟验证

```bash
python -m nanobot.cli.commands taskops list
python -m nanobot.cli.commands taskops feasibility
python -m nanobot.cli.commands taskops board
```

通过标准：C09-C14 通过。

## 4) M4 - 控制面 API + 回归收口

### 4.1 开发检查点

```bash
rg -n "capability\.list|capability\.check|capability\.sync|taskops\.feasibility" nanobot
```

### 4.2 冒烟验证

```bash
bash deploy/chimera_core_deploy.sh restart
curl -s http://127.0.0.1:28790/health
curl -s -H "X-Status-Token: $NANOBOT_STATUS_TOKEN" http://127.0.0.1:28790/status
bash deploy/chimera_core_test.sh
```

通过标准：C15-C20 通过。

## 5) 文档回写与状态收口

```bash
rg -n "T11|C0[1-9]|C1[0-9]|C20" docs/Issue-Checks
```

通过标准：
- `11-Checks-S1-Capability-Governance-v1-2026-02-22.md` 中 C01-C20 完整回填。
- `01-Phase1-Issue-Backlog.md` 中 T11 状态从 TODO -> CHECK -> DONE。
- 月索引已登记对应文档。

## 6) 回滚脚本（阶段失败时）

```bash
cd /Users/sourcefire/X-lab/chimera-core
git restore --source=HEAD -- nanobot/capability nanobot/taskops nanobot/cli/commands.py chimera-bridge/capabilities
bash deploy/chimera_core_deploy.sh restart
bash deploy/chimera_core_test.sh
```

通过标准：恢复到改造前稳定态，gateway 与测试可用。
