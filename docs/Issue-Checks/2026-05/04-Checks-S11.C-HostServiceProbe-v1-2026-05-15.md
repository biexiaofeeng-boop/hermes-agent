# Checks: S11.C Host Service Probe Readiness

## Scope

Repository: `/Users/sourcefire/X-lab/chimera-core`
Branch: `codex/s11-c-host-service-probe-v1`
Active armory path used for smoke checks: `/Users/sourcefire/X-lab/chimera-skills`

Host boundary: `chimera-core` executes bounded probes and computes host-effective readiness. Command probe allowlist/policy lives in this host repo/runtime only; `chimera-skills` remains contract-only.

## Implementation Summary

- `SkillsLoader` now defensively consumes normalized `service_endpoints` from `chimera-skills` index/manifests.
- `HostSkillsRegistry` now computes service readiness with bounded `tcp_connect`, `http_get`, and policy-gated `command` probes.
- Required services influence effective state:
  - passing probes preserve `effective`
  - failed probes with usable fallback become `degraded`
  - failed probes with `blocked` or missing fallback become `unavailable`
  - unsupported or policy-blocked probes become `unchecked`
- `skills list/doctor/inspect/explain` now expose `active_armory_path`, service state, probe kind, reason, and fallback details.
- `capability sync --from skills` now writes service readiness into capability metadata/state without dirtying tracked files when pointed at a runtime capability dir.

## Validation Commands

```bash
NANOBOT_SKILLS__ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
NANOBOT_ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
python3.11 -m unittest tests.test_host_skills_registry tests.test_skills_loader tests.test_capability_sync tests.test_cli_smoke -v

NANOBOT_SKILLS__ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
NANOBOT_ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
python3.11 -m nanobot.cli.commands skills doctor futu-data

tmpdir=$(mktemp -d) && \
NANOBOT_SKILLS__ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
NANOBOT_ARMORY_DIR=/Users/sourcefire/X-lab/chimera-skills \
CHIMERA_BRIDGE_CAPABILITIES_DIR="$tmpdir/capabilities" \
python3.11 -m nanobot.cli.commands capability sync --from skills
```

## Results

- Unit/CLI regression: `Ran 45 tests in 9.417s` / `OK`.
- `skills doctor futu-data`: pass; output showed `active_armory_path=/Users/sourcefire/X-lab/chimera-skills`, `service_state=degraded`, required `futu-opend` TCP probe failure, and command probes blocked by host policy rather than executed.
- `capability sync --from skills` with temp capability dir: pass; `incoming=15`, `added=15`, state reflected `futu-data=degraded`, `macro-reg-intel=unknown` for policy-blocked command probes, and no tracked repo files were dirtied by the smoke.

## Residual Risks

- Runtime/default armory may still differ from development armory until explicitly synchronized.
- Command probes remain unchecked unless `NANOBOT_SKILLS_PROBE_COMMAND_ALLOWLIST` or future host config explicitly allows their command prefix.
- Probe execution is intentionally bounded and read-only; service startup/lifecycle remains outside `chimera-core`.
