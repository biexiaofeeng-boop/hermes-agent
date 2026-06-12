# S13.104 Worker Smoke Task

You are an external coding worker launched by Hermes. Work inside the provided git repository only.

## Goal

Validate the Hermes external-worker loop with a bounded, low-risk task.

## Task

Inspect these files:

- `docs/Issue-Checks/2026-06/130-TaskPackage-S13.103-Agent-Worker-Integration-v1-2026-06-12.md`
- `docs/Issue-Checks/2026-06/131-TaskCards-S13.103-Agent-Worker-Integration-v1-2026-06-12.md`
- `docs/Issue-Checks/2026-06/132-Checks-S13.103-Agent-Worker-Integration-v1-2026-06-12.md`
- `deploy/hermes-evaluation/agent-worker-integration/README.md`
- `deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh`

Return a short validation report answering:

1. What does the worker wrapper already prove?
2. What does it not prove yet?
3. What is the smallest safe write-mode test for a future run?
4. What exact commands should the operator run for plan mode and write mode?

## Constraints

- Do not print secrets.
- Do not touch production runtime state.
- In plan mode, do not edit files.
- In write mode, if explicitly allowed, only add or edit documentation under `docs/Issue-Checks/2026-06/`.
- Do not run destructive git commands.
