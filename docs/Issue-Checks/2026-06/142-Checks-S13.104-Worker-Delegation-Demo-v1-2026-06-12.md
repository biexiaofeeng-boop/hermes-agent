# S13.104 Checks: Worker Delegation Demo

Date: 2026-06-12
Branch: `codex/s13-104-worker-validation`
Status: PASS_NON_MUTATING

## Scope

This check verifies task design and non-mutating worker arrangement. It does not run a live LLM worker in write mode.

## Commands

```bash
git branch --show-current
git status --short
bash -n deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode plan --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent claude --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode plan --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode write --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

Expected final command: fail closed with `write mode requires --allow-write`.

## Acceptance Matrix

| Check | Expected | Status |
|---|---|---|
| Branch | `codex/s13-104-worker-validation` | PASS |
| Prompt template | present and bounded | PASS |
| Worker syntax | `bash -n` passes | PASS |
| Worker check | codex/claude/git availability reported | PASS |
| Codex dry-run | prints plan-mode command | PASS |
| Claude dry-run | prints plan-mode command | PASS |
| Write guard | fails without `--allow-write` | PASS |
| Telegram guide | natural-language, background, and kanban patterns documented | PASS |
| Secrets | no secret values or runtime state tracked | PASS |

## Manual Telegram Acceptance

Send this first:

```text
请按 S13.104 方式安排一个 Codex worker：目标是读取 S13.103 worker integration 文档和 agent_worker.sh，输出验证报告。限制：plan mode，不允许改文件，不允许打印 secrets。workdir=/Users/sourcefire/X-lab/chimera-hermes-agent，prompt-file=deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md。完成后返回 worker log 路径、关键结论和下一步是否需要 write mode。
```

Pass criteria:

- Hermes either runs `agent_worker.sh run --agent codex --mode plan ...` or asks for confirmation before terminal execution.
- Hermes returns the worker log path.
- `git status --short` remains clean unless the operator explicitly approved write mode.

## Follow-Up

If Telegram plan mode passes, run a doc-only write-mode task in an isolated worktree and record the result in this checks file.

## Result Log

Branch:

```text
codex/s13-104-worker-validation
```

Worker availability:

```text
[OK] codex=/opt/homebrew/bin/codex
[OK] claude=/Users/sourcefire/.local/bin/claude
2.1.172 (Claude Code)
[OK] git=/opt/homebrew/bin/git
git version 2.53.0
```

Codex plan dry-run produced a `codex exec` command with the appended no-edit constraint.

Claude plan dry-run produced a `claude -p` command with `--permission-mode plan --allowedTools Read,Grep,Glob,LS`.

Write guard negative test:

```text
[agent-worker] write mode requires --allow-write
```

Secret scan note: grep matched documentation words such as `secrets`, but no secret values, token literals, `.env` content, or runtime logs are tracked.

## Conclusion

Status: PASS_NON_MUTATING

S13.104 is ready for operator Telegram plan-mode validation. Do not run write mode until the operator confirms an isolated worktree and doc-only target.
