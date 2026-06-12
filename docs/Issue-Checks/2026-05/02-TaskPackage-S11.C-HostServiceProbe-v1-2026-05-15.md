# Task Package: S11.C Host Service Probe Readiness

## Repository

`/Users/sourcefire/X-lab/chimera-core`

## Objective

Upgrade host-side skills registry from contract/local-dependency readiness to service-aware readiness. Service-backed skills should not be treated as fully usable unless their required service probes pass or a declared fallback allows degraded operation.

## Scope

`chimera-core` owns:

- Python service probe runner
- host effective-state integration
- CLI inspect/explain output
- capability sync readiness mapping
- release/check visibility for active armory path

`chimera-core` does not own:

- skill contract schema source of truth
- service daemon lifecycle management
- `chimera-iceclaw` Rust ingestion implementation

## Required Work

1. Consume service probe declarations from `chimera-skills` manifests.
2. Implement lightweight probes for `tcp_connect`, `http_get`, and `command`.
3. Integrate service readiness into `HostSkillsRegistry` effective state.
4. Preserve policy precedence: denied/disabled beats service readiness.
5. Extend `skills doctor/explain` with service readiness details.
6. Ensure read-only inspect/list/doctor commands do not dirty tracked capability files.
7. Add tests for service pass/fail/degraded/unchecked cases.

## Acceptance

- `futu-data` can explain backing service unavailable/degraded/effective status.
- `web-intel` can explain backing adapter readiness or fallback state.
- `requires.services` is no longer only opaque unchecked text when probe metadata exists.
- `NANOBOT_SKILLS__ARMORY_DIR` can validate the dev armory path explicitly.
- targeted unit and CLI tests pass.
