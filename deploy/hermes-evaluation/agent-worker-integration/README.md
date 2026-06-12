# S13.103 Agent Worker Integration

This package gives Hermes a small operations layer for two needs:

1. Keep the Hermes gateway running as a managed local service.
2. Let Hermes delegate complex coding work to Codex or Claude Code as external workers.

It intentionally does not modify Hermes core runtime behavior.

## Service Operations

Use the gateway service helper from the Hermes checkout:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh install
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh start
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh restart
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh logs
```

Default profile:

```bash
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"
```

Override `HERMES_HOME` when operating a production profile.

## Worker Delegation

Check local worker availability:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
```

Plan-only Codex run:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent codex \
  --workdir /path/to/project \
  --mode plan \
  --prompt "Review this repository and propose the smallest safe fix."
```

Plan-only Claude Code run:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent claude \
  --workdir /path/to/project \
  --mode plan \
  --prompt "Review this repository and propose the smallest safe fix."
```

Write mode requires explicit operator intent:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent codex \
  --workdir /path/to/project \
  --mode write \
  --allow-write \
  --prompt-file /path/to/task.md
```

Outputs are saved under:

```text
$HERMES_HOME/agent-worker-runs/
```

This path is runtime state and must remain untracked.

## Hermes Gateway Usage Pattern

From Telegram, the intended pattern is:

1. Hermes receives and summarizes the task.
2. Hermes asks for operator confirmation if code mutation is required.
3. Hermes calls `agent_worker.sh` through the terminal tool.
4. Codex or Claude Code works inside a git repository or worktree.
5. Hermes reads the worker log, `git diff`, and test output, then summarizes the result.

## Safety Rules

- Default to `--mode plan`.
- Use `--mode write --allow-write` only after operator confirmation.
- Prefer isolated git worktrees for long tasks.
- Do not store API keys, tokens, or private runtime data in prompts or templates.
- Keep `.runtime/` out of git.
- Treat Codex/Claude as external execution workers, not Hermes core dependencies.

## Backtest Case

A minimal non-mutating acceptance test:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run \
  --agent claude \
  --workdir "$PWD" \
  --mode plan \
  --dry-run \
  --prompt "Inspect S13.103 and return validation commands."
```
