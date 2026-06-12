# S13.104 Task Cards: Worker Delegation Demo

Date: 2026-06-12
Branch: `codex/s13-104-worker-validation`
Status: DESIGN_READY

## T01 - Select Worker Smoke Task

Goal: Pick one bounded task that validates worker orchestration without risking runtime state.

Implementation:

- Use S13.103 docs and `agent_worker.sh` as source material.
- Create `deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md`.
- Keep the task plan-first and doc-only for any later write-mode run.

Acceptance:

- Prompt file exists.
- Prompt states no secrets, no production runtime mutation, and no destructive git commands.

## T02 - Document Direct Worker Commands

Goal: Show exactly how an operator or Hermes can launch Codex/Claude workers.

Implementation:

- Add Codex plan command.
- Add Claude plan command.
- Add write-mode command with explicit `--allow-write`.
- Add isolated worktree setup command.

Acceptance:

- Commands point to `/Users/sourcefire/X-lab/chimera-hermes-agent`.
- Write commands use `.worktrees/s13-104-worker-smoke`.
- Plan commands do not require write authorization.

## T03 - Document Telegram Usage

Goal: Make the mobile/operator UX explicit.

Implementation:

- Add natural-language Telegram prompt for Codex worker.
- Add natural-language Telegram prompt for Claude worker.
- Add `/background` pattern for long worker tasks.
- Add `/agents` inspection pattern.
- Add `/kanban create/list/show/log` pattern for durable task tracking.

Acceptance:

- Telegram section includes copyable messages.
- It clearly distinguishes plan mode and write mode.
- Approval guidance is explicit.

## T04 - Local Non-Mutating Checks

Goal: Verify the wrapper remains usable without running external mutation.

Commands:

```bash
bash -n deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode plan --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent claude --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode plan --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex --workdir /Users/sourcefire/X-lab/chimera-hermes-agent --mode write --dry-run --prompt-file deploy/hermes-evaluation/agent-worker-integration/s13-104-worker-smoke.prompt.md
```

Expected negative result for final command: non-zero exit with `write mode requires --allow-write`.
