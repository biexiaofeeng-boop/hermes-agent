# S13.108 Task Package: Legacy Cards Session Search

Date: 2026-06-12
Branch: `codex/s13-108-import-legacy-cards-session`
Status: IMPLEMENTATION_READY

## Goal

Make selected Chimera legacy memory cards discoverable by Hermes `session_search`.

S13.106 created `chimera-memory-cards.md` and a `MEMORY.md` pointer, but Telegram behavior showed Hermes still preferred `session_search` and did not read the cards file. S13.108 imports each selected card as an isolated synthetic Hermes session so the existing FTS-backed `session_search` can find it directly.

## Design

- Do not import full raw Chimera history.
- Import only compact selected cards.
- Create one synthetic session per card, not one combined session.
- Use source `chimera_legacy` and id prefix `chimera_legacy_card:`.
- Delete/recreate prior synthetic card sessions idempotently.
- Let existing SQLite triggers update `messages_fts` and `messages_fts_trigram`.
- Create a `state.db.bak.s13-108` backup before first write.

## Why One Session Per Card

If all cards live in one session, `session_search` bookends and context windows can mix unrelated topics, such as Ctrip and Lenovo. Separate sessions keep topic recall isolated.

## Command

Dry-run:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session
```

Write:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session --write
```

## Acceptance

- Dry-run lists the synthetic sessions to be imported.
- Write imports four synthetic sessions.
- FTS search for `携程 OR TCOM OR 体验型消费` returns the Ctrip/US.TCOM session.
- Search does not require reading `docs/Issue-Checks` or raw config/secrets.
- Gateway restart after write reloads the updated DB for live Telegram usage.
