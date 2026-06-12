# S13.100 Task Package: Hermes Evaluation Baseline

Date: 2026-06-12
Branch: `codex/s13-100-hermes-evaluation`
Fork: `biexiaofeeng-boop/hermes-agent`
Upstream: `NousResearch/hermes-agent`

## Background

Chimera Core has evolved toward a simple personal-agent control plane where Codex and Claude Code are primary execution agents, while Core provides long-running state, memory, task checkpoints, skills governance, artifacts, and gateway APIs.

Hermes Agent appears to already implement many of those platform-level capabilities:

- multi-platform gateway;
- profiles;
- built-in and optional skills;
- Skills Hub compatibility;
- memory files and memory provider abstraction;
- session search and context compression;
- Codex app-server runtime integration;
- MCP and plugin extension points;
- kanban and cron capabilities;
- desktop/dashboard/TUI surfaces.

S13.100 creates a safe evaluation baseline before deciding whether Hermes should become the primary personal-agent runtime and whether Chimera should become a domain skill/project layer.

## Goal

Prepare the Hermes fork for structured evaluation and future customization by migrating Chimera collaboration standards and adding a minimal operations/precheck scaffold.

## Non-Goals

- Do not replace `chimera-core-prod`.
- Do not start or restart Hermes gateway as part of this baseline.
- Do not copy Chimera-specific production deploy scripts as if they were Hermes-compatible.
- Do not migrate secrets.
- Do not modify Hermes core runtime behavior in S13.100.
- Do not enable broad skill sets before evaluation confirms scope and context cost.

## Scope

In scope:

- Point local Hermes checkout at the user fork as `origin`.
- Preserve NousResearch remote as `upstream`.
- Import `docs/Issue-Checks/` collaboration material.
- Add Hermes fork collaboration baseline doc.
- Add deploy directory layout for runtime, release, ops, IT, automation, and evaluation scripts.
- Add an evaluation precheck script that validates local readiness without mutating real `~/.hermes`.
- Define evaluation task cards and acceptance checks.

Out of scope for this package:

- Full Hermes installation.
- Gateway pairing.
- Memory migration.
- Skill migration.
- Production cutover.
- Upstream pull request strategy.

## Design

### Repository Model

```text
upstream/NousResearch/main -> local topic branch -> origin/biexiaofeeng-boop topic/main
```

The fork is the customization baseline. Upstream remains the vendor source for updates.

### Runtime Model

S13.100 evaluation must use isolated runtime state:

```text
hermes-agent/.runtime/hermes-profiles/eval
```

The profile helper may initialize this directory, but must not touch `~/.hermes` by default.

### Deploy Model

The initial deploy layout is intentionally minimal:

```text
deploy/runtime/hermes_profile.sh
deploy/it/hermes_eval_precheck.sh
deploy/ops/hermes_eval_status.sh
deploy/hermes-evaluation/hermes_eval_precheck.sh
```

The scripts provide precheck and status. They do not perform release, gateway restart, credential migration, or production mutation.

### Evaluation Dimensions

S13.100 sets up later evaluation against these dimensions:

| Dimension | Question |
|---|---|
| Gateway | Can Hermes reliably support the required messaging entry point without replacing production too early? |
| Codex/Claude | Can Hermes share skills and runtime context with Codex/Claude without reducing their standalone value? |
| Memory | Does Hermes recall, session search, and compression outperform Chimera's current markdown + SQLite memory behavior? |
| Skills | Can Chimera domain capabilities become Hermes skills without context explosion? |
| Config/secrets | Can keys move into profile-scoped config and `.env` without plain-text sprawl? |
| Ops | Can we operate Hermes with precheck, status, logs, backup, rollback, and clear acceptance records? |

## Acceptance Criteria

- `origin` points to `biexiaofeeng-boop/hermes-agent`.
- `upstream` points to `NousResearch/hermes-agent`.
- `docs/Issue-Checks/` exists in the Hermes fork and includes templates/history.
- S13.100 task package, task cards, and checks exist under `docs/Issue-Checks/2026-06/`.
- `deploy/README.md` describes the Hermes fork deploy layout.
- `bash deploy/it/hermes_eval_precheck.sh` runs without mutating real `~/.hermes`.
- `bash deploy/runtime/hermes_profile.sh status eval` reports the isolated evaluation home.
- No secrets or runtime homes are tracked.

## Follow-Up Packages

S13.101: Hermes isolated install and profile setup.

S13.102: Gateway evaluation with one controlled messaging channel.

S13.103: Memory and session-search backtest against Chimera historical cases.

S13.104: Chimera skill migration spike for Tavily/web-search and one finance/intel workflow.

S13.105: Production cutover design, rollback, and operator runbook if S13.101-S13.104 pass.
