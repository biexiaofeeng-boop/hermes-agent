# Chimera History Migration

Safely migrates Chimera Core Scout/finance history into the isolated Hermes eval profile.

Policy:

- Do not import raw Telegram/session logs into `MEMORY.md`.
- Generate an archive summary under `HERMES_HOME/workspace/chimera-history/`.
- Append only concise, durable operating facts to `memories/MEMORY.md`.
- Do not modify `memories/USER.md`.

Design:

- `SOUL.md` is identity/persona continuity.
- `MEMORY.md` is durable operating memory and must stay small.
- `workspace/chimera-history/` is the historical archive reference.
- Raw Chimera sessions should remain outside the always-loaded Hermes prompt unless a later RAG/index step explicitly retrieves them.

Usage:

```bash
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"

.venv/bin/python deploy/hermes-evaluation/chimera-memory-migration/migrate_chimera_history.py --dry-run
.venv/bin/python deploy/hermes-evaluation/chimera-memory-migration/migrate_chimera_history.py
```

Optional source override:

```bash
export CHIMERA_SESSIONS="/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot/sessions"
```

Outputs:

- `$HERMES_HOME/workspace/chimera-history/chimera-history-summary.md`
- `$HERMES_HOME/memories/MEMORY.md`
- `$HERMES_HOME/backups/chimera-history-migration-*/MEMORY.md.before`

Acceptance:

```bash
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"

.venv/bin/python deploy/hermes-evaluation/chimera-memory-migration/migrate_chimera_history.py --dry-run
sed -n '1,120p' "$HERMES_HOME/workspace/chimera-history/chimera-history-summary.md"
sed -n '1,120p' "$HERMES_HOME/memories/MEMORY.md"
```

Expected:

- dry-run reports non-zero `messages`
- rerunning dry-run keeps `memory_entries_before` equal to `memory_entries_after`
- `USER.md` is not modified

`/sethome` note:

- `/sethome` is a messaging delivery setting, not a project workspace setting.
- Running `/sethome` in Telegram stores the current chat/thread as the platform home channel.
- Cron delivery, handoff, startup notifications, and platform-targeted messages can use that home channel.
- Separate finance/scout/project spaces should be modeled with Hermes profiles, `SOUL.md`, workspace archives, sessions, skills, or future RAG indexes.
