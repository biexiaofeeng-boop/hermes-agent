# S13.107 Recall Continuation Policy

This package installs a compact behavior rule for old-memory recall conversations.

When the user sends a short clarification after a failed/uncertain recall, Hermes should treat it as continuation, search the memory cards/archive, and answer only the delta instead of repeating the previous disclaimer.

## Dry Run

```bash
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py
```

## Install

```bash
python3 deploy/hermes-evaluation/recall-continuation/recall_continuation_policy.py --write
```
