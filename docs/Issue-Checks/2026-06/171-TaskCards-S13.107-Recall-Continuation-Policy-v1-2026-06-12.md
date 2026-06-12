# S13.107 Task Cards: Recall Continuation Policy

Date: 2026-06-12
Branch: `codex/s13-107-recall-continuation-policy`
Status: IMPLEMENTATION_READY

## T01 - Add Policy Installer

Goal: Make the recall continuation behavior reproducible.

Implementation:

- Add `deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py`.
- Support dry-run and `--write`.
- Write only to Hermes `MEMORY.md`.

Acceptance:

- Python compile passes.
- Dry-run prints policy.
- Write is idempotent.

## T02 - Production Apply

Goal: Install the policy into the production Hermes eval profile.

Acceptance:

- `MEMORY.md` contains the policy once.
- Backup is created before first write.
- Git worktree remains clean.
