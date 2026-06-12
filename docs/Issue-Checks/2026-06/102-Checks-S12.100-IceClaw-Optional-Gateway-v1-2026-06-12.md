# S12.100 Checks: IceClaw Optional Gateway

Date: 2026-06-12

## Scope

This check record verifies that Chimera Core release orchestration no longer depends on IceClaw by default.

## Expected Behavior

- Default release orchestration skips IceClaw.
- Missing `chimera-iceclaw` checkout does not block Core preflight.
- Explicit IceClaw operations still require a valid checkout.
- Dry-run summary clearly marks IceClaw as optional/skipped.

## Regression Commands

```bash
python3.11 -m unittest tests.test_dual_service_release_iceclaw_optional -v
```

```bash
bash deploy/chimera_dual_service_release.sh --help
```

```bash
CORE_REF=HEAD CORE_PROD_DIR=/Users/sourcefire/X-lab/chimera-core-prod \
  bash deploy/chimera_dual_service_release.sh --dry-run --skip-skills --skip-core
```

## Result

Passed in branch `codex/s12-100-iceclaw-optional-gateway`.

```text
Ran 3 tests in 0.262s

OK
```

`bash deploy/chimera_dual_service_release.sh --help` also confirms the default flow now skips `chimera-iceclaw` as a legacy optional gateway.

The explicit dry-run produced:

```text
[chimera-dual-release] skip chimera-iceclaw
[chimera-dual-release] iceclaw_binary=skipped-optional
```
