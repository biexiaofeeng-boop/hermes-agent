# Execution Plan: S11.B Chimera Core Skills Registry v1

## This Thread Owns

- host-side skills registry
- node policy
- effective status resolution
- explain / inspect surface

## This Thread Does Not Own

- changing skill pack implementation behavior
- large schema redesign inside `chimera-skills`
- marketplace or distribution concerns

## Inputs Expected From `chimera-skills`

- stable manifest/index/schema baseline
- explicit support metadata when possible
- requirements/risk/category/tag clarity when available

## Defensive Rule

The core host must not assume perfect source data.
It should normalize defensively and surface degraded or partial states clearly.

## Delivery Sequence

1. registry models
2. discovery adapter
3. node gate
4. effective state resolution
5. explain/list/inspect surface
6. tests

## Integration Check

After implementation, validate against the current `chimera-skills` main branch rather than a one-off local snapshot.
