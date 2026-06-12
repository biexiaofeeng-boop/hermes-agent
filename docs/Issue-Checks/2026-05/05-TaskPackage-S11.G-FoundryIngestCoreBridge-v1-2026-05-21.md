# Task Package: S11.G Foundry Ingest Core Bridge v1

## Repository

`/Users/sourcefire/X-lab/chimera-core`

## Goal

Add a minimal explicit bridge from `chimera-core` to `chimera-foundry` raw ingestion so conversation agents can send reviewed/selected notes or topic digests into Foundry.

## Required Work

- add a small helper or CLI command to build a Foundry ingestion envelope
- call Foundry adapter command with configured repo path
- return receipt to caller
- keep operation explicit, not automatic for every message
- add tests for envelope generation or invocation
- document intended use

## Boundaries

- no automatic import of every chat message
- no durable/wiki/decision promotion
- no direct writes into Foundry internals
- no Cherry Studio ingestion
- no web capture implementation in this repo

## Acceptance

- explicit note/digest ingestion path can produce Foundry receipt
- failure is reported clearly
- tests pass
