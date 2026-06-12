# S13.107 Task Package: Recall Continuation Policy

Date: 2026-06-12
Branch: `codex/s13-107-recall-continuation-policy`
Status: IMPLEMENTATION_READY

## Goal

Reduce repeated multi-turn disclaimers in old-memory recall tasks.

When the user sends a short clarification after Hermes says it cannot find an old record, Hermes should not restart the same explanation. It should treat the short message as a continuation cue, search the Chimera memory cards/archive, and return only the corrected delta.

## Minimal Approach

This task intentionally avoids deeper Telegram/session code changes. It installs a compact policy into Hermes `MEMORY.md` so the behavior can improve immediately after memory reload/new session.

## Acceptance

- Policy helper supports dry-run and idempotent write.
- `MEMORY.md` receives one short recall-continuation rule.
- No gateway restart is required by the package, though a new session/restart may be needed for an already-running agent to reload memory.
