# S13.108 Checks: Legacy Cards Session Search

Date: 2026-06-12
Branch: `codex/s13-108-import-legacy-cards-session`
Status: PASS

## Commands

```bash
python3 -m py_compile deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py
TMP_DB=/tmp/hermes-state-s13-108-test.db
cp /Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/state.db "$TMP_DB"
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session --state-db "$TMP_DB"
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session --state-db "$TMP_DB" --write
sqlite3 "$TMP_DB" "select id, source, title, message_count from sessions where id like 'chimera_legacy_card:%' order by id;"
sqlite3 "$TMP_DB" "select s.id, s.title, snippet(messages_fts,0,'[',']','...',20) from messages_fts join messages m on m.id=messages_fts.rowid join sessions s on s.id=m.session_id where messages_fts match '携程 OR TCOM OR 体验型消费' order by bm25(messages_fts) limit 5;"
```

## Acceptance Matrix

| Check | Expected | Status |
|---|---|---|
| Py compile | passes | PASS |
| Dry-run | lists four synthetic sessions | PASS |
| Temp DB import | imports four sessions | PASS |
| FTS query | Ctrip/US.TCOM session returned | PASS |
| Topic isolation | no Lenovo hit for Ctrip query | PASS |
| Production apply | import into live state.db | PASS |
| Gateway restart | running after restart | PASS |

## Result Log

### Local Temp DB

Result:

```text
imported=4 state_db=/tmp/hermes-state-s13-108-test.db backup=/tmp/hermes-state-s13-108-test.db.bak.s13-108
chimera_legacy_card:finance.tcom.travel-platform returned for query: 携程 OR TCOM OR 体验型消费
```

### Production Apply

Production repo:

```text
/Users/sourcefire/X-lab/chimera-hermes-agent
```

HEAD after sync:

```text
9309e643f
```

Commands passed:

```bash
python3 -m py_compile deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py
python3 deploy/hermes-evaluation/chimera-legacy-memory/chimera_legacy_memory.py import-cards-session --write
sqlite3 .runtime/hermes-profiles/eval/state.db "select id, source, title, message_count from sessions where id like 'chimera_legacy_card:%' order by id;"
sqlite3 .runtime/hermes-profiles/eval/state.db "select s.id, s.title, snippet(messages_fts,0,'[',']','...',20) from messages_fts join messages m on m.id=messages_fts.rowid join sessions s on s.id=m.session_id where messages_fts match '携程 OR TCOM OR 体验型消费' order by bm25(messages_fts) limit 5;"
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh restart
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
```

Runtime outputs:

```text
imported=4 state_db=/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/state.db backup=/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/state.db.bak.s13-108
chimera_legacy_card:finance.tcom.travel-platform returned for query: 携程 OR TCOM OR 体验型消费
new gateway PID: 59073
```

Topic isolation: Ctrip query returned the Ctrip synthetic session and did not return Lenovo.
