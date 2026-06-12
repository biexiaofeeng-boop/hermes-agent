# S13.106 Task Package: Chimera Legacy Memory Archive

Date: 2026-06-12
Branch: `codex/s13-106-legacy-memory-archive`
Status: IMPLEMENTATION_READY
Fork: `biexiaofeeng-boop/hermes-agent`

## Goal

Fix the S13.105 backtest gap without adding a heavy RAG system.

Hermes currently has only coarse Chimera memory facts. Old detailed Chimera/Nanobot conversations still exist in `.nanobot/sessions/*.jsonl`, but they are not indexed in Hermes `state.db`, so `session_search` cannot reliably recover them.

S13.106 adds a minimal legacy archive bridge:

1. read-only search over old `.nanobot/sessions/*.jsonl`;
2. compact high-value memory cards under Hermes workspace;
3. a single durable pointer in `MEMORY.md` so the agent knows where to look;
4. no raw-history DB import and no gateway restart required.

## Problem Statement

The user tested a vague recall prompt about a previously discussed travel-platform stock. Hermes did not recover the old detailed record. It only found coarse migrated memory around `Ctrip/TCOM`, then returned generic or reconstructed analysis.

Root causes:

- `MEMORY.md` contains only a short finance-continuity summary.
- `chimera-history-summary.md` contains only theme-level excerpts.
- Hermes `session_search` searches Hermes `state.db/messages_fts`, not old Chimera `.nanobot/sessions/*.jsonl`.
- Old detailed records exist in Chimera runtime sessions but are outside the current search surface.

## Scope

In scope:

- Add `deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py`.
- Support `inspect`, `search`, `export-cards`, and `install-pointer` commands.
- Generate high-value memory cards for selected old Scout/鹰眼 finance anchors.
- Install an idempotent pointer in Hermes `MEMORY.md`.
- Keep all operations explicit and operator-visible.

Out of scope:

- No broad RAG/vector DB.
- No import of old raw sessions into Hermes `state.db`.
- No automatic gateway restart.
- No reading secrets or config files.
- No change to Telegram gateway behavior in this task.

## Source Boundary

Allowed source:

```text
/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot/sessions/*.jsonl
```

Excluded:

```text
.env
secrets.env
config.json
config backups
runtime logs unrelated to sessions
```

## Memory Card Output

Default output:

```text
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/workspace/chimera-history/chimera-memory-cards.md
```

Default pointer target:

```text
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/MEMORY.md
```

Pointer text is intentionally short. It tells Hermes where to find memory cards but avoids injecting large raw history into every prompt.

## Initial Cards

- `finance.tcom.travel-platform`: Ctrip / `US.TCOM` travel-platform thesis.
- `finance.morning-brief.alibaba-baidu`: recurring Alibaba/Baidu morning market brief.
- `finance.lenovo-ai-pc`: Lenovo AI PC / edge execution thesis.
- `finance.msft-mispricing`: Microsoft valuation mispricing / enterprise AI thesis.

## Acceptance

- Script runs with Python stdlib only.
- `inspect` finds old session files and anchor hits.
- `search` can find the travel-platform/Ctrip/TCOM old record.
- `export-cards --write` creates `chimera-memory-cards.md`.
- `install-pointer --write` adds one idempotent pointer to `MEMORY.md` and creates a backup.
- No secrets/config files are read.
- No service restart required.

## Follow-Up

If this minimal bridge proves useful, later work can make Hermes call this search helper as a skill/tool. Do not add vector RAG until the card+archive path fails a real usage test.
