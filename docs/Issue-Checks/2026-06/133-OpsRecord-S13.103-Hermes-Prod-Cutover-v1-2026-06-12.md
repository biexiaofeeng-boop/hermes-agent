# S13.103 Ops Record: Hermes Production Cutover

Date: 2026-06-12
Status: PASS
Production path: `/Users/sourcefire/X-lab/chimera-hermes-agent`
Previous dev path: `/Users/sourcefire/1data/X-Chimera/hermes-agent`

## Purpose

Move the long-running Hermes gateway service out of the development checkout and into a dedicated production checkout.

The development checkout remains for source changes, CLI tests, and branch work. It should not normally run the Telegram gateway because Telegram bot polling is a single-owner runtime and duplicate gateways cause conflicts.

## Final Layout

| Role | Path | Usage |
|---|---|---|
| Development | `/Users/sourcefire/1data/X-Chimera/hermes-agent` | Branch development, docs, scripts, CLI tests. Do not run gateway by default. |
| Production | `/Users/sourcefire/X-lab/chimera-hermes-agent` | Running Hermes gateway service and production profile state. |
| Runtime profile | `/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval` | Current production profile, migrated from the eval profile. |
| Service manager | `launchd` | User-level service `ai.hermes.gateway`. |

## Git Model

Production checkout was created from the local synchronized fork snapshot because both HTTPS and SSH remote clone attempts disconnected during transfer.

After local clone, production `origin` was set to SSH:

```bash
git remote set-url origin git@github.com:biexiaofeeng-boop/hermes-agent.git
```

Production HEAD at cutover:

```text
f6f3c82f2 Add S13.103 agent worker integration package
```

## Runtime Migration

The following runtime data was migrated from the development eval profile to the production eval profile:

- `config.yaml`
- `.env`
- `auth.json`
- `SOUL.md`
- `memories/`
- `sessions/`
- `state.db`
- `kanban.db`
- `skills/.usage.json`, `.curator_state`, `.bundled_manifest`

The following process/cache state was intentionally not migrated:

- `gateway.pid`
- `gateway.lock`
- `gateway_state.json`
- `logs/`
- `image_cache/`
- `*.lock`
- `state.db-wal`, `state.db-shm`

## Cutover Commands Used

Stop and uninstall the development-bound service:

```bash
cd /Users/sourcefire/1data/X-Chimera/hermes-agent
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway stop
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway uninstall
```

Install and start the production-bound service:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway install
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway start
```

## Verification

Production gateway status:

```text
Launchd plist: /Users/sourcefire/Library/LaunchAgents/ai.hermes.gateway.plist
Service definition matches the current Hermes install
Gateway service is loaded
PID = 14164
Program = /Users/sourcefire/X-lab/chimera-hermes-agent/.venv/bin/python
```

Production log confirmed:

```text
[Telegram] Connected to Telegram (polling mode)
✓ telegram connected
Gateway running with 1 platform(s)
Cron ticker started
kanban dispatcher: embedded in gateway
```

Hermes status confirmed:

```text
Project: /Users/sourcefire/X-lab/chimera-hermes-agent
Python: 3.11.14
Model: gpt-5.4
Provider: custom:dmx
Telegram: configured
Gateway Service: running
Manager: launchd
PID(s): 14164
```

Vision/profile config confirmed before cutover:

```text
provider custom:dmx
model gpt-5.4
model_context_length 1048576
supports_vision True
image_input_mode native
skills_external_dirs ['~/1data/Chimera-Projs/chimera-skills']
```

## Daily Operations

Use production path for gateway operations:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh restart
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh logs
```

Development path can still run CLI-only checks:

```bash
cd /Users/sourcefire/1data/X-Chimera/hermes-agent
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes --help
```

Do not install/start gateway from the development path unless intentionally rolling back.

## Production Update SOP

For doc/script/code updates already merged to `origin/main`:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
git pull --ff-only origin main
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh precheck
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh restart
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
```

If the change is documentation-only, restart is not required.

## Rollback

If production gateway fails after a future update:

1. Stop production service:

```bash
cd /Users/sourcefire/X-lab/chimera-hermes-agent
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway stop
```

2. Reset production checkout to the last known good commit if needed:

```bash
git log --oneline -5
git checkout <known-good-commit>
```

3. Restart production service:

```bash
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway start
```

Emergency fallback to development checkout is possible but not preferred:

```bash
cd /Users/sourcefire/1data/X-Chimera/hermes-agent
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway install
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/hermes gateway start
```

## Conclusion

Status: PASS

The active Telegram gateway is now production-bound under `/Users/sourcefire/X-lab/chimera-hermes-agent`. The development checkout should remain gateway-stopped for normal branch development and CLI testing.
