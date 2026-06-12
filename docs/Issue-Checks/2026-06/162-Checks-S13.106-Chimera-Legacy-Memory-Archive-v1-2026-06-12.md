# S13.106 Checks: Chimera Legacy Memory Archive

Date: 2026-06-12
Branch: `codex/s13-106-legacy-memory-archive`
Status: PASS_LOCAL_PENDING_PROD_APPLY

## Commands

```bash
git branch --show-current
git status --short
python3 -m py_compile deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py inspect
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py search --query "携程 US.TCOM 体验型消费 出境游" --limit 5
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py export-cards > /tmp/s13-106-chimera-memory-cards.preview.md
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py install-pointer
```

Production apply after merge:

```bash
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py export-cards --write
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py install-pointer --write
```

## Acceptance Matrix

| Check | Expected | Status |
|---|---|---|
| Branch | `codex/s13-106-legacy-memory-archive` | PASS |
| Py compile | passes | PASS |
| Inspect | session files and card hits found | PASS |
| Search | Ctrip/US.TCOM excerpts found | PASS |
| Export preview | card markdown generated | PASS |
| Pointer dry-run | pointer text printed, no write | PASS |
| Production cards | `chimera-memory-cards.md` exists | PENDING |
| Production pointer | `MEMORY.md` contains one pointer | PENDING |
| Gateway restart | not required / not performed | PENDING |

## Result Log

### Local Checks

Branch:

```text
codex/s13-106-legacy-memory-archive
```

Commands passed:

```bash
python3 -m py_compile deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py inspect
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py search --query "携程 US.TCOM 体验型消费 出境游" --limit 5
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py export-cards > /tmp/s13-106-chimera-memory-cards.preview.md
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py install-pointer
```

Local evidence:

```text
inspect: session files found; all four card anchors produced hits
search: top Ctrip/US.TCOM hit is telegram_8464732775.jsonl:1111 with Futu Data API, screenshot, $47.43, $47.08, 3.09M volume, and evidence-card analysis
export preview: 102-line markdown generated
pointer dry-run: prints one MEMORY.md pointer and does not write
```

### Production Apply

Pending merge and production sync.
