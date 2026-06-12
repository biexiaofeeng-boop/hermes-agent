# S13.106 Task Cards: Chimera Legacy Memory Archive

Date: 2026-06-12
Branch: `codex/s13-106-legacy-memory-archive`
Status: IMPLEMENTATION_READY

## T01 - Build Legacy Session Search Helper

Goal: Search old Chimera runtime sessions without touching secrets or config.

Implementation:

- Add `deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py`.
- Read only `.nanobot/sessions/*.jsonl`.
- Add `inspect` and `search` commands.

Acceptance:

- `python3 ... inspect` prints session counts and card anchor hit status.
- `python3 ... search --query "携程 US.TCOM 体验型消费 出境游"` returns old runtime excerpts.

## T02 - Generate Memory Cards

Goal: Create compact recall anchors for high-value old Scout/鹰眼 finance discussions.

Implementation:

- Add `export-cards` command.
- Default output under Hermes profile workspace: `workspace/chimera-history/chimera-memory-cards.md`.
- Include source file and line references for evidence excerpts.

Acceptance:

- Dry-run prints cards to stdout.
- `--write` creates the target file.

## T03 - Install Durable Pointer

Goal: Let Hermes know where the memory cards live without loading all old history into `MEMORY.md`.

Implementation:

- Add `install-pointer` command.
- Dry-run prints pointer.
- `--write` appends pointer to `MEMORY.md` only if absent.
- Create backup before first write.

Acceptance:

- Command is idempotent.
- `MEMORY.md` contains one pointer line.

## T04 - Document Operations

Goal: Make this reproducible on another node.

Implementation:

- Add README with inspect/search/export/install commands.
- Add Issue-Checks task package, task cards, and checks.
- Update June index.

Acceptance:

- Docs state source boundary and secret exclusion.
- Docs state no gateway restart is required.

## T05 - Production Runtime Apply

Goal: Install the card file and memory pointer in production Hermes profile.

Implementation:

- Sync production repo after merge.
- Run `export-cards --write`.
- Run `install-pointer --write`.
- Verify `MEMORY.md` pointer and card file.

Acceptance:

- Production repo remains clean.
- Runtime card file exists.
- No service restart performed.
