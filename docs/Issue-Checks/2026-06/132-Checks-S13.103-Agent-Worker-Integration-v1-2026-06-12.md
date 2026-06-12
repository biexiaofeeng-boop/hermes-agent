# S13.103 Checks: Agent Worker Integration

Date: 2026-06-12
Branch: `codex/s13-103-agent-worker-integration`
Status: PASS_WITH_WARNINGS

## Verification Scope

This check verifies the additive operational wrapper package for Hermes gateway service management and Codex/Claude worker delegation.

It does not verify a real mutating coding task. Mutating worker execution is deferred until the operator selects a bounded test repository and confirms write authorization.

## Required Commands

```bash
git branch --show-current
git status --short
bash -n deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh
bash -n deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh status
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent claude --workdir "$PWD" --mode plan --dry-run --prompt "Inspect S13.103 and return validation commands."
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir "$PWD" --mode plan --dry-run --prompt "Inspect S13.103 and return validation commands."
```

Negative gate:

```bash
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir "$PWD" --mode write --dry-run --prompt "test"
```

Expected: non-zero exit with `write mode requires --allow-write`.

## Acceptance Matrix

| Check | Expected Result | Status |
|---|---|---|
| Branch | `codex/s13-103-agent-worker-integration` | PASS |
| Service helper syntax | `bash -n` passes | PASS |
| Worker helper syntax | `bash -n` passes | PASS |
| Gateway status | reports active profile/service without mutation | PASS |
| Worker check | reports `codex`, `claude`, and `git` availability | PASS |
| Claude plan dry-run | prints non-mutating command | PASS |
| Codex plan dry-run | prints non-mutating command | PASS |
| Write guard | fails without `--allow-write` | PASS |
| Docs | task package/cards/checks/index present | PASS |
| Secrets | no tracked runtime/secrets/logs | PASS |
| Eval precheck | `hermes_eval_precheck.sh --deep` passes | PASS_WITH_WARNINGS |

## Result Log

Branch:

```text
codex/s13-103-agent-worker-integration
```

Gateway service status:

```text
Launchd plist: /Users/sourcefire/Library/LaunchAgents/ai.hermes.gateway.plist
Gateway service is loaded
PID = 99332
Program = /Users/sourcefire/1data/X-Chimera/hermes-agent/.venv/bin/python
ProgramArguments = python -m hermes_cli.main gateway run --replace
```

Worker check:

```text
[OK] codex=/opt/homebrew/bin/codex
[OK] claude=/Users/sourcefire/.local/bin/claude
2.1.172 (Claude Code)
[OK] git=/opt/homebrew/bin/git
git version 2.53.0
```

Claude dry-run command includes the no-edit constraint:

```text
claude -p 'Inspect S13.103 and return validation commands.

Constraint: do not edit files, do not run destructive commands, and return only an implementation plan, risks, and validation commands.' --permission-mode plan --allowedTools Read,Grep,Glob,LS
```

Codex dry-run command includes the no-edit constraint:

```text
codex exec 'Inspect S13.103 and return validation commands.

Constraint: do not edit files, do not run destructive commands, and return only an implementation plan, risks, and validation commands.'
```

Negative write guard:

```text
[agent-worker] write mode requires --allow-write
negative_exit=2
```

Deep eval precheck:

```text
[hermes-eval-precheck] PASS failures=0 warnings=1
```

Warning is expected before commit because the worktree contains the S13.103 changes.

Secret scan against the new package returned no matches for API-key/token patterns.

## Conclusion

Status: PASS_WITH_WARNINGS

S13.103 is ready for commit. The package is additive and defaults to non-mutating operation. The next package should run one controlled end-to-end worker task from Telegram only after the operator confirms a test repository and write authorization.
