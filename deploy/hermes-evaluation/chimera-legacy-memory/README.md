# S13.106 Chimera Legacy Memory Archive

This package adds a minimal bridge from Hermes to old Chimera/Nanobot runtime memory.

It does not import raw history into Hermes session DB. It reads old `.nanobot/sessions/*.jsonl`, generates compact memory cards, and optionally installs a pointer in Hermes `MEMORY.md`.

## Inspect

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py inspect
```

## Search

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py search --query "携程 US.TCOM 体验型消费 出境游" --limit 8
```

## Export Cards

Preview:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py export-cards
```

Write to production Hermes eval profile:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py export-cards --write
```

## Install Pointer

Dry-run:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py install-pointer
```

Write:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py install-pointer --write
```

## Secret Boundary

The helper reads only old Nanobot session JSONL files. It skips `.env`, `secrets.env`, `config.json`, and backup config/secret files.

## Import Cards Into Session Search

Dry-run:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session
```

Write selected cards as isolated synthetic Hermes sessions:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session --write
```

This imports only compact memory cards, not full raw Chimera history. Each card is a separate session with id prefix `chimera_legacy_card:` so `session_search` can retrieve the right topic without mixing Ctrip and Lenovo context.
