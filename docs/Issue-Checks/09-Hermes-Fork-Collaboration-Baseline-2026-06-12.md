# Hermes Fork Collaboration Baseline

Date: 2026-06-12
Repository: `biexiaofeeng-boop/hermes-agent`
Base upstream: `NousResearch/hermes-agent`

## Purpose

This fork imports the Chimera collaboration and operations standards into the Hermes Agent codebase so future Hermes evaluation, customization, and production-hardening work can follow the same engineering protocol used in Chimera Core.

The imported standards are not a claim that Hermes should copy Chimera runtime internals. The intent is to reuse the collaboration discipline:

- branch-first development;
- explicit task packages and task cards;
- acceptance records before release;
- safe deploy/precheck scripts;
- operations-first rollback thinking;
- clear handoff between planning, implementation, and verification agents.

## Git Baseline

- `origin`: `https://github.com/biexiaofeeng-boop/hermes-agent.git`
- `upstream`: `https://github.com/NousResearch/hermes-agent.git`
- Local iteration branch pattern: `codex/<topic>`.
- Mainline sync pattern:
  - fetch `upstream/main` for vendor updates;
  - rebase or merge into a local topic branch only after reading upstream changes;
  - push fork branches to `origin`;
  - merge to fork `main` only after acceptance.

## Directory Mapping

| Chimera Standard | Hermes Fork Path | Purpose |
|---|---|---|
| `docs/Issue-Checks/` | `docs/Issue-Checks/` | Collaboration, task design, verification, handoff records. |
| `deploy/runtime/` | `deploy/runtime/` | Isolated runtime/profile helpers. |
| `deploy/it/` | `deploy/it/` | Integration and acceptance checks. |
| `deploy/ops/` | `deploy/ops/` | Operational status and readiness checks. |
| `deploy/release/` | `deploy/release/` | Release preflight and future fork release scripts. |
| `deploy/automation/` | `deploy/automation/` | Future scheduled reports and recurring evaluations. |

## Migration Boundary

Do migrate:

- Issue-Checks templates, naming conventions, and monthly indexes.
- Branch-first collaboration rule.
- Precheck-before-mutation operational discipline.
- Acceptance records with concrete commands and results.
- Runtime isolation principle.

Do not blindly migrate:

- Chimera Core production release scripts that assume `nanobot`, `chimera-core-prod`, or `.nanobot/config.json`.
- Chimera-specific TaskOps JSON schemas unless a Hermes-compatible target is designed.
- Legacy IceClaw release assumptions.
- Secrets or local runtime state.

## Operating Rule

S13 work must keep Chimera production untouched until Hermes passes an isolated evaluation gate. Hermes customization should first land as profile config, skills, docs, or small wrappers before touching core runtime behavior.

## First Evaluation Package

- `docs/Issue-Checks/2026-06/110-TaskPackage-S13.100-Hermes-Evaluation-v1-2026-06-12.md`
- `docs/Issue-Checks/2026-06/111-TaskCards-S13.100-Hermes-Evaluation-v1-2026-06-12.md`
- `docs/Issue-Checks/2026-06/112-Checks-S13.100-Hermes-Evaluation-v1-2026-06-12.md`
