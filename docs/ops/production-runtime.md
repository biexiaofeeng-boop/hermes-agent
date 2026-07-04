# Hermes Production Runtime

## Path Contract

| Role | Path | Purpose |
|---|---|---|
| Development checkout | `/Users/sourcefire/data/workspace_agents/hermes-agent` | Source changes, branch work, tests, docs, local CLI-only experiments. Do not run the long-lived gateway here by default. |
| Production checkout | `/Users/sourcefire/X-lab/chimera-hermes-agent` | Stable runtime checkout, gateway service, node synchronization target, release notes. |
| Production profile | `/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval` | Production `HERMES_HOME`: `.env`, `config.yaml`, sessions, memory, kanban state, auth, logs. |

`~/data/workspace_agents/` is the development lane. `~/X-lab` is the production lane.

## Current Endpoint

The production eval profile is configured for the DMX endpoint:

```yaml
model:
  provider: custom:dmx
  default: gpt-5.4

providers:
  dmx:
    api: https://www.dmxapi.cn/v1
    key_env: DMX_API_KEY
```

Secrets are stored only in:

```bash
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/.env
```

Do not copy production `.env`, `auth.json`, `state.db`, memories, sessions, or kanban DB back into the development checkout unless doing an explicit, documented migration.

## Runtime Environment

Use this shell shape for production commands:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"
```

Useful checks:

```bash
.venv/bin/hermes doctor
.venv/bin/hermes config
.venv/bin/hermes gateway status
```

## Node Synchronization

### Source Sync: Development to GitHub

Run from the development checkout:

```bash
cd /Users/sourcefire/data/workspace_agents/hermes-agent
git status --short
scripts/run_tests.sh
git push origin main
```

Only source, docs, templates, and migration scripts should move through Git. Runtime state stays out of Git.

### Production Sync: GitHub to Production

Run from the production checkout:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"
git fetch origin main
git pull --ff-only origin main
```

Then run a preflight:

```bash
.venv/bin/hermes doctor
.venv/bin/hermes config check
```

Restart the gateway only when code, gateway config, dependencies, tools, or skills changed:

```bash
.venv/bin/hermes gateway restart
.venv/bin/hermes gateway status
```

Documentation-only changes do not require a restart.

### Runtime State Sync

Initial migration may copy selected runtime files from development to production:

```bash
rsync -a \
  --exclude 'logs/' \
  --exclude '*.lock' \
  --exclude '*.pid' \
  --exclude 'gateway_state.json' \
  --exclude 'state.db-wal' \
  --exclude 'state.db-shm' \
  /path/to/dev/profile/ \
  /Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/
```

After cutover, production is authoritative for runtime state.

## Gateway Policy

Telegram polling is single-owner. Do not run the same Telegram bot token from both development and production at the same time.

Default production posture:

- Development checkout: gateway stopped.
- Production checkout: gateway installed/running.
- Telegram and Feishu enabled only after real secrets and allowlists are set.
- Use allowlists or pairing before exposing terminal-capable bots.

## Release Note Template

Create one file per production sync under `docs/ops/releases/`:

```markdown
# Release YYYY-MM-DD

## Summary

- 

## Source

- Development path: `/Users/sourcefire/data/workspace_agents/hermes-agent`
- Production path: `/Users/sourcefire/X-lab/chimera-hermes-agent`
- Commit before:
- Commit after:

## Changes

- 

## Config / Runtime

- Endpoint:
- Gateway platforms:
- Skills:
- Kanban:

## Verification

- [ ] `git pull --ff-only origin main`
- [ ] `.venv/bin/hermes doctor`
- [ ] `.venv/bin/hermes config check`
- [ ] gateway restart/status, if required
- [ ] Telegram smoke test, if enabled
- [ ] Feishu smoke test, if enabled

## Rollback

- Known good commit:
- Rollback command:
```

## Rollback

Prefer fast rollback in production:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"
.venv/bin/hermes gateway stop
git checkout <known-good-commit>
.venv/bin/hermes gateway start
```

Avoid emergency fallback to the development checkout unless the production checkout itself is unrecoverable.
