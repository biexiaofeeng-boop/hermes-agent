# Checks: S11.B Chimera Core Skills Registry v1

## Implementation Backfill

- added host-side registry module: `nanobot/skills/host_registry.py`
- fused the host-registry implementation with the parallel `chimera-skills` contract-normalization work
- expanded `SkillsLoader` with:
  - raw discovery view that can include inactive / policy-blocked / lifecycle-blocked skills
  - `get_skill_manifest(...)` for host-consumable manifest rows
  - normalized manifest/index consumption for `chimera-skills` YAML packs
  - defensive YAML fallback parsing when PyYAML is unavailable
  - normalized metadata fields: display name, owner, category, tags, supported hosts, risk, permission hints, entrypoints, capabilities, context tags, evidence requirement, fallback hint
- kept existing lifecycle registry (`nanobot/skill_registry.py`) as install-state source, without turning it into marketplace logic
- upgraded CLI surface:
  - `nanobot skills list`
  - `nanobot skills doctor`
  - `nanobot skills inspect`
  - `nanobot skills explain`
- integrated normalized skill metadata into capability sync/list surfaces
- preserved the already-merged control-plane `gateway.user_id` behavior and alias-topic continuity regression coverage during closeout review

## Static Checks

- module boundaries are clear
- no hardcoded one-off skill assumptions in core logic
- `chimera-core` owns host-side install/load/policy/effective state
- `chimera-skills` owns manifest/index/schema contract normalization

## Functional Checks

- registry loads current `chimera-skills` baseline
- node gate changes effective status deterministically
- explain output includes disabled/degraded reasons
- missing requirement cases surface as degraded or unavailable
- normalized `chimera-skills/registry/skills.index.json` metadata is consumed without pack-specific special-casing
- services remain advisory/unchecked in core readiness; bins/env/config remain active host gates
- capability registry rows include normalized skill owner/category/risk metadata

## Regression Commands

- `python3.11 -m py_compile nanobot/agent/skills.py nanobot/skills/host_registry.py nanobot/cli/commands.py nanobot/capability/sync.py nanobot/capability/controlplane.py nanobot/agent/loop.py nanobot/config/schema.py`
- `python3.11 -m unittest tests.test_skills_loader tests.test_host_skills_registry tests.test_capability_sync tests.test_cli_smoke tests.test_agent_loop_dialogue_mode -v`
- in `chimera-skills`: `python3 scripts/check_skill_contracts.py`

## Result Summary

- host registry can load current `chimera-skills/registry/skills.index.json` + `packs/*/skill.yaml`
- node policy now has explicit `enabled / disabled / denied` decision surface, while staying backward compatible with existing denylist gate payloads
- effective state now separates:
  - install state
  - policy state
  - load state
  - effective state
- explain output covers:
  - lifecycle-disabled
  - policy-denied / policy-disabled
  - host-unsupported
  - manifest-inactive
  - missing env/bin/config degraded cases
- targeted + combined regression passed: `80` tests, `OK`
- `chimera-skills` contract check passed: `OK: validated 5 skill manifests, registry/skills.index.json, and registry/skills.composition.json`
- closeout review rejected an old-branch regression that would have downgraded `skills list/doctor` from host-registry effective view back to plain loader diagnostics

## Residual Risks

- mismatch between future `chimera-skills` manifest shapes and host normalization
- over-coupling to current index layout
- `requires.services` is currently surfaced as unchecked advisory context, not an active service health probe
