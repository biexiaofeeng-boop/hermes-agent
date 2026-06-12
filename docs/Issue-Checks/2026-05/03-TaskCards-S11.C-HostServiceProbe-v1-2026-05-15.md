# Task Cards: S11.C Host Service Probe Readiness

## T01: Manifest Consumption

- extend normalized skill metadata to include service endpoints and probe fields
- keep defensive parsing for partial manifests
- preserve existing manifest/index compatibility

## T02: Probe Runner

- implement bounded TCP connect probe
- implement bounded HTTP GET probe
- implement bounded command probe with safe timeout and stderr capture
- do not auto-start services

## T03: Effective State Mapping

- required service probe pass -> continue normal readiness
- required service probe fail with fallback -> `degraded`
- required service probe fail without fallback -> `unavailable`
- no host implementation for probe kind -> `unchecked`

## T04: CLI Explainability

- show active armory path
- show service id, probe kind, readiness, reason, and fallback
- keep Telegram/user-facing summaries concise

## T05: Capability Sync

- reflect service readiness in capability state
- avoid write churn from read-only commands
- add tests around `capability sync --from skills`

## T06: Regression

- run skills loader tests
- run host registry tests
- run capability sync tests
- run CLI smoke tests
