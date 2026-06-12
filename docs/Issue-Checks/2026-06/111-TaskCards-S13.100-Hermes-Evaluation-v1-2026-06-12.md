# S13.100 Task Cards: Hermes Evaluation Baseline

Date: 2026-06-12
Branch: `codex/s13-100-hermes-evaluation`

## T01 - Fork Remote Baseline

Goal: Make the local Hermes checkout use the user fork as the writable base while retaining upstream tracking.

Implementation:

- Set `origin` to `https://github.com/biexiaofeeng-boop/hermes-agent.git`.
- Add or update `upstream` as `https://github.com/NousResearch/hermes-agent.git`.
- Continue work on a topic branch, not directly on `main`.

Acceptance:

- `git remote -v` shows expected fork and upstream remotes.
- Local branch is not `main` for S13.100 edits.

## T02 - Collaboration Standard Migration

Goal: Bring Chimera's Issue-Checks collaboration system into Hermes fork.

Implementation:

- Copy `chimera-core/docs/Issue-Checks/` to `hermes-agent/docs/Issue-Checks/`.
- Keep templates and monthly indexes.
- Add a Hermes fork baseline document explaining what was migrated and what was intentionally not migrated.

Acceptance:

- `docs/Issue-Checks/README.md` exists.
- `docs/Issue-Checks/templates/` exists.
- `docs/Issue-Checks/09-Hermes-Fork-Collaboration-Baseline-2026-06-12.md` exists.

## T03 - Deploy Layout Migration

Goal: Create the Hermes fork operations scaffold without copying incompatible Chimera production scripts.

Implementation:

- Add `deploy/README.md`.
- Add grouped directories: `runtime`, `release`, `ops`, `it`, `automation`, `hermes-evaluation`.
- Add minimal scripts for profile status/init, evaluation precheck, and evaluation status.

Acceptance:

- `deploy/README.md` documents the layout and runtime isolation rule.
- `deploy/runtime/hermes_profile.sh status eval` succeeds.
- `deploy/it/hermes_eval_precheck.sh` succeeds or reports actionable failures.

## T04 - S13.100 Evaluation Design

Goal: Define the evaluation gates before any Hermes customization or production cutover.

Implementation:

- Add S13.100 task package.
- Add S13.100 task cards.
- Add S13.100 checks record.
- Update `2026-06/00-INDEX-2026-06.md`.

Acceptance:

- The S13.100 docs identify scope, non-goals, acceptance criteria, and follow-up packages.
- The package explicitly blocks production replacement during S13.100.

## T05 - Local Precheck

Goal: Verify the new scaffold can be executed from the Hermes checkout.

Commands:

```bash
bash deploy/it/hermes_eval_precheck.sh
bash deploy/runtime/hermes_profile.sh status eval
bash deploy/ops/hermes_eval_status.sh eval
```

Acceptance:

- Scripts pass shell syntax checks.
- Precheck validates remotes, Python version, docs, deploy layout, and sensitive-file tracking.
- Runtime status points at `.runtime/hermes-profiles/eval` unless overridden.
