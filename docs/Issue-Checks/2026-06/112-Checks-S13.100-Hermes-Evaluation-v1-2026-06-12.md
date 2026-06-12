# S13.100 Checks: Hermes Evaluation Baseline

Date: 2026-06-12
Branch: `codex/s13-100-hermes-evaluation`

## Verification Scope

This check record verifies only the S13.100 baseline:

- fork remote setup;
- collaboration docs migration;
- deploy/evaluation scaffold;
- isolated runtime profile helper;
- non-mutating precheck behavior.

It does not verify Hermes installation, gateway operation, memory quality, skill migration, or production readiness.

## Required Commands

```bash
git remote -v
git branch --show-current
git status --short
bash deploy/it/hermes_eval_precheck.sh
bash deploy/runtime/hermes_profile.sh status eval
bash deploy/ops/hermes_eval_status.sh eval
```

Optional deep check after local dependencies are installed:

```bash
bash deploy/it/hermes_eval_precheck.sh --deep
```

## Acceptance Matrix

| Check | Expected Result | Status |
|---|---|---|
| Fork origin | `origin` is `https://github.com/biexiaofeeng-boop/hermes-agent.git` | PASS |
| Upstream remote | `upstream` is `https://github.com/NousResearch/hermes-agent.git` | PASS |
| Topic branch | Work happens on `codex/s13-100-hermes-evaluation` | PASS |
| Issue-Checks | `docs/Issue-Checks/` exists with templates and history | PASS |
| S13.100 docs | `110`, `111`, `112` documents exist under `2026-06` | PASS |
| Deploy layout | `deploy/README.md` and grouped script dirs exist | PASS |
| Precheck script | `bash deploy/it/hermes_eval_precheck.sh` runs | PASS_WITH_WARNINGS |
| Runtime isolation | profile helper points to `.runtime/hermes-profiles/eval` by default | PASS |
| Secrets | no root `.env`, `.env.local`, or `config.yaml` tracked | PASS |

## Remote Sync Note

Remote connectivity was rechecked successfully after an initial transient GitHub SSL failure.

```text
origin/main   = 6db65e687
upstream/main = 24f74eb88
origin/main...upstream/main = 0 ahead / 2 behind
```

S13.100 intentionally stays on the fork snapshot at `origin/main` to avoid mixing vendor updates into the collaboration/deploy baseline migration. Before S13.101 runtime setup, decide whether to fast-forward the fork to `upstream/main`.

## Command Result Summary

Executed on branch `codex/s13-100-hermes-evaluation` at base HEAD `6db65e687`.

```text
bash deploy/it/hermes_eval_precheck.sh
PASS failures=0 warnings=4
```

Warnings:

- worktree has expected S13.100 uncommitted changes before commit;
- system `python3` is `3.14.3`, outside Hermes `requires-python >=3.11,<3.14`;
- `uv` is not available on the current shell path;
- `.venv` has not been created yet.

```text
bash deploy/runtime/hermes_profile.sh status eval
```

Result:

- default evaluation home is `.runtime/hermes-profiles/eval`;
- profile home does not exist yet;
- no `config.yaml`, `.env`, `MEMORY.md`, `USER.md`, or `SOUL.md` exists in the isolated home.

```text
bash deploy/ops/hermes_eval_status.sh eval
```

Result:

- reports fork/upstream remotes;
- reports branch `codex/s13-100-hermes-evaluation`;
- reports isolated evaluation profile status.

## Final Conclusion

Status: PASS_WITH_WARNINGS

S13.100 baseline is ready for commit. S13.101 should first install a supported Python runtime, preferably via `uv` or a `.venv` using Python 3.11-3.13, before any deep Hermes runtime or gateway checks.
