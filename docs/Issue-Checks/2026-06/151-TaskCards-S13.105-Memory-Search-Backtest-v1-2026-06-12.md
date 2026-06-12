# S13.105 Task Cards: Memory Search Backtest

Date: 2026-06-12
Branch: `codex/s13-105-memory-search-backtest`
Status: DESIGN_READY

## T01 - Confirm Valid Source Boundary

Goal: Use only old runtime agent state for memory/search backtesting.

Implementation:

- Read from `/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot`.
- Prefer `.nanobot/sessions/*.jsonl` and workspace runtime traces.
- Do not use `docs/Issue-Checks` as answer facts.
- Do not read `.env`, `secrets.env`, `config.json`, or backups.

Acceptance:

- Task package states the source boundary.
- Helper script excludes secret/config paths.

## T02 - Select Runtime Backtest Anchors

Goal: Pick real user-facing historical memory anchors.

Implementation:

- Primary: travel platform / Ctrip / `US.TCOM` analysis from old Telegram session.
- Secondary: recurring morning brief workflow for Alibaba/Baidu and overnight China ADRs.

Acceptance:

- Anchors are found in old `.nanobot/sessions/*.jsonl`.
- Prompts avoid dates and exact source hints.

## T03 - Create Vague Natural-Language Prompts

Goal: Test memory retrieval, not prompt leakage.

Implementation:

- Add primary prompt under `deploy/hermes-evaluation/memory-search-backtest/s13-105-primary-vague.prompt.txt`.
- Avoid exact date, ticker, price, file path, and package ID.
- Ask Hermes to distinguish retrieved memory from inference.

Acceptance:

- Prompt is copyable into Telegram.
- Prompt does not mention `TCOM`, `携程`, `$47.43`, or any date.

## T04 - Add Read-Only Inspection Helper

Goal: Make the fixture reproducible on another node without mutating production state.

Implementation:

- Add `deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh`.
- `inspect` prints source file counts, selected fixture excerpts, and current Hermes memory file availability.
- No secrets/config are read.

Acceptance:

- `bash -n` passes.
- `inspect` runs read-only.

## T05 - Manual Backtest And Grade

Goal: Run the prompt against Hermes and record the result.

Implementation:

- Send primary prompt through Telegram or CLI.
- Grade response as `PASS_HIGH`, `PASS_MEDIUM`, or `FAIL`.
- Record source honesty and whether session archive lookup was used.

Acceptance:

- Checks file contains command evidence and manual result area.
- If result is not high, next step is archive indexing design, not broad RAG by default.
