# Task Cards: S11.G Foundry Ingest Core Bridge v1

## T01: Config Surface

- define Foundry repo path config or use a safe default
- define Python/module command invocation path
- keep node-local path configurable

## T02: Envelope Builder

- build envelope from explicit note/topic/digest content
- include source system, node id, local/UTC time, title, domains, topic tags, evidence grade, promotion target, source refs
- default target should be `open_question` unless user asks otherwise

## T03: Invocation Helper

- invoke Foundry ingest adapter
- capture stdout/stderr
- parse receipt JSON
- return concise receipt to caller

## T04: Tests

- envelope builder test
- successful command invocation with fake adapter or temp script
- failure path test

## T05: Docs and Checks

- update Issue-Checks with result
- mention explicit usage and no-auto-promotion boundary
