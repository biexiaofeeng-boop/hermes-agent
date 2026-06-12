# S12.100 Task Package: IceClaw Optional Gateway

Date: 2026-06-12

## Background

Chimera Core is moving back toward a simpler personal-agent service shape:

- Codex and Claude Code are the primary interactive execution agents.
- Chimera Core should provide long-running state, memory, task checkpoints, skills governance, artifacts, and lightweight gateway APIs.
- IceClaw is useful as an optional UI/gateway, but it should not be required for the default personal-agent release path.

The current dual-service release script still treats `chimera-iceclaw` as a default release/restart target. This increases operational complexity and makes failures caused by network, proxy, or UI-service issues look like Core release failures.

## Goal

Pause IceClaw from the default Core release orchestration while preserving explicit manual opt-in.

## Non-goals

- Do not remove IceClaw code or historical docs.
- Do not change Core runtime task, memory, or skills logic.
- Do not introduce a new service boundary.
- Do not replace Codex or Claude Code execution behavior.

## Design

Default path:

```text
chimera-skills sync -> chimera-core-prod deploy -> taskops template sync
```

IceClaw path:

```text
explicit opt-in -> chimera-iceclaw release/restart
```

`deploy/chimera_dual_service_release.sh` should:

- Default `ICECLAW_MODE=skip`.
- Default `RUN_ICECLAW=0`.
- Avoid requiring `ICECLAW_DIR` during default preflight.
- Avoid querying IceClaw service status in the default summary.
- Keep `--with-iceclaw` and `--iceclaw-mode` as explicit opt-in paths.

## Operating Principle

IceClaw is a legacy optional gateway. Chimera Core remains the gateway/control-plane source for personal-agent operations. Codex and Claude Code should integrate through context packets, checkpoints, artifacts, and skills registry contracts rather than through a mandatory IceClaw service.

## Acceptance Criteria

- Default dual-service `--check-only` passes without a local `chimera-iceclaw` checkout.
- Explicit `--with-iceclaw` still fails fast when the IceClaw checkout is missing.
- Default dry-run reports IceClaw as skipped/optional.
- Integrated release docs explain that IceClaw is no longer part of the default personal-agent path.
