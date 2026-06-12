# Task Package: S11.B Chimera Core Skills Registry v1

## Goal

Implement the first host-side skills registry and node policy layer in `chimera-core`.

## Background

`chimera-skills` is now the independent shared armory repository.
`chimera-core` should stop relying on implicit capability assumptions and instead compute an explicit effective skill view for the current host and node.

## Scope

1. define host-side registry models
2. load and normalize metadata from `chimera-skills`
3. define node policy / gate source for local enable-disable control
4. compute effective skill status
5. expose inspect / explain surfaces for operators and developers

## Required Outcomes

- `chimera-core` can answer:
  - what skills exist
  - which are effective on this node
  - which are disabled or degraded
  - why a skill is unavailable
- the design remains reusable by `chimera-iceclaw`

## Out of Scope

- no marketplace
- no remote skill service
- no heavy hot-reload system
- no direct modification of skill pack implementation content inside this task

## Deliverables

1. registry model/module
2. discovery adapter for `chimera-skills`
3. node policy gate
4. effective status computation
5. explain/list/inspect surface
6. tests

## Acceptance

- host-side registry works against the current `chimera-skills` baseline
- node policy behavior is explicit and test-covered
- disabled/degraded reason can be explained without guesswork
