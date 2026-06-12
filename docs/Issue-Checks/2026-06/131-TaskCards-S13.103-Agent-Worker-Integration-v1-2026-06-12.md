# S13.103 Task Cards: Agent Worker Integration

Date: 2026-06-12
Branch: `codex/s13-103-agent-worker-integration`
Status: IMPLEMENTING

## T01 - Gateway Service Helper

Goal: Make Hermes gateway operations repeatable and visible.

Implementation:

- Add `deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh`.
- Support `status`, `install`, `start`, `stop`, `restart`, `logs`, `follow`, `doctor`, `precheck`, and `uninstall`.
- Use profile-scoped `HERMES_HOME` with eval default.

Acceptance:

- `bash -n` passes.
- `status` prints root, `HERMES_HOME`, `HERMES_BIN`, gateway status, launchd summary, and process summary.
- `precheck` composes the existing Hermes evaluation precheck with profile checks.

## T02 - Agent Worker Wrapper

Goal: Provide a controlled bridge from Hermes to Codex and Claude Code.

Implementation:

- Add `deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh`.
- Support `check` and `run`.
- Support `--agent codex|claude`, `--workdir`, `--prompt`, `--prompt-file`, `--mode plan|write`, `--dry-run`.
- Require `--allow-write` for `--mode write`.
- Require git workdir unless `--allow-non-git` is explicitly set.

Acceptance:

- `bash -n` passes.
- `check` reports binary availability.
- `run --mode plan --dry-run` appends a no-edit instruction.
- `run --mode write` without `--allow-write` fails closed.

## T03 - Operator Runbook

Goal: Document how Hermes should use worker delegation from Telegram.

Implementation:

- Add `deploy/hermes-evaluation/agent-worker-integration/README.md`.
- Explain service operations, worker delegation, safety rules, runtime log path, and a minimal backtest.

Acceptance:

- README contains exact commands for service status and worker dry-run.
- README states that Codex/Claude are external workers, not Hermes core dependencies.

## T04 - Issue-Checks Package

Goal: Preserve task design and acceptance context for future developer agents.

Implementation:

- Add S13.103 task package.
- Add S13.103 task cards.
- Add S13.103 checks record.
- Update `docs/Issue-Checks/2026-06/00-INDEX-2026-06.md`.

Acceptance:

- Files are present and indexed.
- Numbering note records the S13.103 scope change.

## T05 - Local Verification

Goal: Prove the package is usable without mutating production state.

Commands:

```bash
bash -n deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh
bash -n deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent claude --workdir "$PWD" --mode plan --dry-run --prompt "Inspect S13.103 and return validation commands."
```

Negative check:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir "$PWD" --mode write --dry-run --prompt "test"
```

Expected: exits non-zero because `--allow-write` is missing.
