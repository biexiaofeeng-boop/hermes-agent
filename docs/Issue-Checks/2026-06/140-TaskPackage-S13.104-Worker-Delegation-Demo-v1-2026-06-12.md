# S13.104 Task Package: Worker Delegation Demo

Date: 2026-06-12
Branch: `codex/s13-104-worker-validation`
Status: DESIGN_READY
Fork: `biexiaofeeng-boop/hermes-agent`

## Goal

Prove the practical operating pattern for asking Hermes to use Codex or Claude Code as external coding workers, especially from Telegram.

This package is intentionally small. It demonstrates how to arrange worker work before we rely on worker delegation for real production changes.

## Test Task

Use a bounded documentation-analysis task as the first worker validation:

> Inspect S13.103 worker integration docs and wrapper scripts, then return a short validation report: what is already proven, what is not proven, and the smallest safe write-mode test.

Prompt template:

```text
deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

Why this task:

- It is repository-grounded.
- It exercises file reading and command planning.
- It does not need secrets.
- It does not touch production runtime.
- It can run in `plan` mode first and later in `write` mode with a doc-only target.

## Worker Choices

### Codex worker

Use when the task is coding, git diff, patching, test repair, or repository refactor work.

Wrapper path:

```bash
deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
```

Plan command:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent codex \
  --workdir /Users/sourcefire/X-lab/chimera-hermes-agent \
  --mode plan \
  --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

Write command after operator approval:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent codex \
  --workdir /Users/sourcefire/X-lab/chimera-hermes-agent/.worktrees/s13-104-worker-smoke \
  --mode write \
  --allow-write \
  --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

### Claude Code worker

Use when the task benefits from an independent second implementation/review pass, broad codebase inspection, or alternate reasoning.

Plan command:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent claude \
  --workdir /Users/sourcefire/X-lab/chimera-hermes-agent \
  --mode plan \
  --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

Write command after operator approval:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent claude \
  --workdir /Users/sourcefire/X-lab/chimera-hermes-agent/.worktrees/s13-104-worker-smoke \
  --mode write \
  --allow-write \
  --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

## Recommended Worktree Setup

For write-mode tests, create an isolated worktree first:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
git fetch origin
git worktree add .worktrees/s13-104-worker-smoke -b codex/s13-104-worker-smoke origin/main
```

Reason:

- production gateway checkout remains stable;
- worker changes are isolated;
- `git diff`, tests, commit, and rollback are easier;
- multiple workers can run without stepping on the active service checkout.

## Telegram Usage

### Minimal natural-language pattern

Send this to the Hermes Telegram chat:

```text
请按 S13.104 方式安排一个 Codex worker：
目标：读取 S13.103 worker integration 文档和 agent_worker.sh，输出验证报告。
限制：plan mode，不允许改文件，不允许打印 secrets。
请使用 /Users/sourcefire/X-lab/chimera-hermes-agent 作为 workdir，prompt 使用 deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md。
完成后返回 worker log 路径、关键结论和下一步是否需要 write mode。
```

Claude Code variant:

```text
请按 S13.104 方式安排一个 Claude Code worker：
目标：读取 S13.103 worker integration 文档和 agent_worker.sh，输出独立验证报告。
限制：plan mode，不允许改文件，不允许打印 secrets。
workdir=/Users/sourcefire/X-lab/chimera-hermes-agent
prompt-file=deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
完成后返回 worker log 路径、关键结论和风险。
```

### Long task pattern

For a long-running worker task, start from Telegram with:

```text
/background 请按 S13.104 安排 Codex worker 做 plan-mode 验证，使用 s13-104-worker-smoke.prompt.md。完成后总结 worker log、diff 状态和测试建议。
```

Then inspect state:

```text
/agents
```

If Hermes asks for approval for a terminal command, approve only after checking the command is `agent_worker.sh run --mode plan` or an explicitly approved `--mode write --allow-write` command.

### Kanban pattern

For durable task tracking, create a Kanban card from Telegram:

```text
/kanban create "S13.104 Codex worker smoke" --assignee default --workspace dir:/Users/sourcefire/X-lab/chimera-hermes-agent --skill codex --body "Run the S13.104 plan-mode worker smoke using deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md. Do not edit files. Return worker log path and validation summary."
```

Then watch or inspect:

```text
/kanban list
/kanban show <task_id>
/kanban log <task_id>
```

## Acceptance

- Worker wrapper `check` reports `codex`, `claude`, and `git` availability.
- Codex plan dry-run prints a safe non-mutating command.
- Claude plan dry-run prints a safe non-mutating command.
- Write mode without `--allow-write` fails closed.
- Telegram runbook explains natural-language, background, and Kanban usage.
- No production gateway restart is required for this package.
- No secrets or runtime logs are tracked.

## Decision

The first true execution should be `plan` mode only. If the result is coherent, the next operator-approved step is a doc-only write-mode run in an isolated worktree.
