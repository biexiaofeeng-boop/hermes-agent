# S13.103 Task Package: Agent Worker Integration

Date: 2026-06-12
Branch: `codex/s13-103-agent-worker-integration`
Status: IMPLEMENTING
Fork: `biexiaofeeng-boop/hermes-agent`

## Numbering Note

S13.102 previously listed S13.103 as memory/session-search quality backtest. The operator decision moved agent-worker integration forward because Hermes gateway is now running and the next operational risk is how to reliably call Codex or Claude Code for complex tasks.

Updated near-term sequence:

- S13.103: Hermes gateway service operations and Codex/Claude worker integration.
- S13.104: memory/session-search quality backtest.
- S13.105: production profile and cutover design if prior packages pass.

## Background

Hermes now works as the messaging gateway and long-running task entry point. The user observed that Codex and Claude Code are already strong PC-side execution agents. The desired architecture is therefore not to rebuild a coding agent inside Hermes, but to let Hermes orchestrate external coding workers through stable skills, scripts, and operator-confirmed execution gates.

## Goal

Create the smallest useful integration layer that lets Hermes:

- run as a stable managed gateway service;
- expose consistent service operations for status/start/stop/restart/logs/precheck;
- delegate coding tasks to Codex or Claude Code from a controlled wrapper;
- default to non-mutating plan mode;
- require explicit write-mode authorization;
- save worker logs under runtime state for review;
- keep all changes reversible and outside Hermes core.

## Non-Goals

- Do not modify Hermes core agent loop.
- Do not replace Hermes native delegation or kanban features.
- Do not auto-run Codex/Claude on every task.
- Do not store secrets in prompts, templates, or tracked config.
- Do not force a production directory split in this package.
- Do not create a generic multi-agent scheduler before the wrapper proves useful.

## Design

### Runtime Roles

```text
Telegram / gateway
  -> Hermes session, memory, skills, routing, operator confirmation
  -> terminal wrapper
  -> Codex or Claude Code external worker
  -> git diff / tests / worker log
  -> Hermes summary back to user
```

### Service Layer

Add a tracked helper:

```text
deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh
```

It standardizes:

- `status`
- `install`
- `start`
- `stop`
- `restart`
- `logs`
- `follow`
- `doctor`
- `precheck`
- `uninstall`

The script defaults to:

```text
HERMES_HOME=$PWD/.runtime/hermes-profiles/eval
HERMES_BIN=$PWD/.venv/bin/hermes
```

Both can be overridden for a production profile.

### Worker Layer

Add a tracked helper:

```text
deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
```

Supported modes:

| Mode | Behavior |
|---|---|
| `check` | Reports local `codex`, `claude`, and `git` availability. |
| `run --mode plan` | Calls Codex or Claude Code with an appended no-edit instruction. |
| `run --mode write --allow-write` | Allows a mutating worker run after explicit operator confirmation. |
| `--dry-run` | Prints the exact worker command without executing it. |

Worker output is saved under:

```text
$HERMES_HOME/agent-worker-runs/
```

This is runtime state and remains ignored by git.

## Acceptance Criteria

- S13.103 docs exist under `docs/Issue-Checks/2026-06/` and are indexed.
- `hermes_gateway_service.sh` passes shell syntax check.
- `agent_worker.sh` passes shell syntax check.
- Gateway service `status` works without mutating repository files.
- `agent_worker.sh check` reports available worker binaries without exposing secrets.
- `agent_worker.sh run --dry-run --mode plan` prints a safe non-mutating worker command.
- `agent_worker.sh run --mode write` fails unless `--allow-write` is supplied.
- No `.runtime`, `.env`, tokens, or worker logs are tracked.

## Rollback

This package is additive. Rollback options:

1. Stop using the wrappers and call Hermes/Codex/Claude manually.
2. Remove `deploy/hermes-evaluation/agent-worker-integration/` from the fork.
3. If a launchd service was installed for the wrong profile, run:

```bash
HERMES_HOME=<profile-home> .venv/bin/hermes gateway uninstall
```

## Follow-Up

S13.104 should define a real backtest where Telegram asks Hermes to delegate a bounded coding task to Codex or Claude Code in an isolated git worktree, then Hermes returns worker log, diff, and test result summary.
