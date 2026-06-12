# S13.108 Task Cards: Legacy Cards Session Search

Date: 2026-06-12
Branch: `codex/s13-108-import-legacy-cards-session`
Status: IMPLEMENTATION_READY

## T01 - Add Synthetic Session Import

Goal: Make compact cards visible to `session_search`.

Implementation:

- Extend `chimera_legacy_memory.py` with `import-cards-session`.
- Insert sessions with source `chimera_legacy`.
- Insert two messages per session: recall cue and assistant card content.

Acceptance:

- Synthetic sessions are independent per card.
- Command is idempotent.

## T02 - Validate Against Temp DB

Goal: Avoid corrupting production DB during development.

Implementation:

- Copy production `state.db` to `/tmp`.
- Run `import-cards-session --state-db /tmp/... --write`.
- Query FTS for Ctrip terms.

Acceptance:

- Ctrip query returns `chimera_legacy_card:finance.tcom.travel-platform`.

## T03 - Production Apply

Goal: Apply selected card sessions to production Hermes profile.

Implementation:

- Sync production repo.
- Run import command with `--write`.
- Restart gateway.
- Verify FTS and service status.

Acceptance:

- Four synthetic sessions exist.
- Gateway is running after restart.
