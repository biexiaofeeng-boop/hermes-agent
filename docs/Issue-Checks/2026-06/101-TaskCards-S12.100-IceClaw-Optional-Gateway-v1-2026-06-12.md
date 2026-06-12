# S12.100 Task Cards: IceClaw Optional Gateway

Date: 2026-06-12

## T01 - Release Defaults

Change `deploy/chimera_dual_service_release.sh` so IceClaw is skipped by default:

- `ICECLAW_MODE=skip`
- `RUN_ICECLAW=0`
- default preflight does not require `ICECLAW_DIR`

## T02 - Explicit Opt-in

Keep IceClaw release/restart available for manual operations:

- `--with-iceclaw`
- `--iceclaw-mode release`
- `--iceclaw-mode restart-current`
- `--iceclaw-mode restart-binary --iceclaw-binary <path>`

## T03 - Summary Behavior

Do not call IceClaw service status in the default path. Report:

```text
iceclaw_binary=skipped-optional
```

## T04 - Docs

Update release runbook and Issue-Checks docs to state:

- IceClaw is a legacy optional gateway.
- Core release does not depend on IceClaw.
- Personal-agent execution should prefer Codex/Claude Code plus shared skills/context/checkpoint contracts.

## T05 - Regression Tests

Add tests proving:

- Default check-only does not require IceClaw.
- Explicit IceClaw opt-in still validates IceClaw checkout.
- Default dry-run reports optional skip.
