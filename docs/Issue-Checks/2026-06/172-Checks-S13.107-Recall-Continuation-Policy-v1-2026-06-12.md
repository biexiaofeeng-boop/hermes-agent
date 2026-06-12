# S13.107 Checks: Recall Continuation Policy

Date: 2026-06-12
Branch: `codex/s13-107-recall-continuation-policy`
Status: PASS

## Commands

```bash
python3 -m py_compile deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py --write
```

## Acceptance Matrix

| Check | Expected | Status |
|---|---|---|
| Py compile | passes | PASS |
| Dry-run | prints policy and does not write | PASS |
| Production write | policy installed once | PASS |
| Gateway restart | not required / not performed | PASS |

## Result Log

### Local Checks

Commands passed:

```bash
python3 -m py_compile deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
```

Dry-run printed the recall-continuation rule and did not write.

### Production Apply

Production repo:

```text
/Users/sourcefire/X-lab/chimera-hermes-agent
```

HEAD after sync:

```text
f625620bb
```

Commands passed:

```bash
python3 -m py_compile deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py --write
rg -n "Recall-continuation rule" .runtime/hermes-profiles/eval/memories/MEMORY.md
```

Runtime outputs:

```text
policy=installed path=/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/MEMORY.md backup=/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/MEMORY.md.bak.s13-107
MEMORY.md policy: present once
```

Gateway restart: not required by package and not performed. For an already-open Telegram session, start a new session or restart gateway if immediate prompt reload is needed.

Production git status after runtime apply:

```text
## main...origin/main
```
