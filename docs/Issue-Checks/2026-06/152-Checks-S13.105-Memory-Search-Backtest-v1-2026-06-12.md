# S13.105 Checks: Memory Search Backtest

Date: 2026-06-12
Branch: `codex/s13-105-memory-search-backtest`
Status: PASS_FIXTURE_PENDING_MANUAL_PROMPT

## Scope

This check validates a backtest design and fixture inspection for Hermes memory/search behavior after Chimera memory migration.

It does not mutate Hermes runtime state and does not restart the gateway.

## Source Boundary

Backtest source:

```text
/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot
```

Excluded:

```text
.env
secrets.env
config.json
config backups
```

`docs/Issue-Checks` is excluded as an answer source because those are engineering collaboration documents, not normal runtime conversation memory.

## Commands

```bash
git branch --show-current
git status --short
bash -n deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh
bash deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh inspect
```

## Expected Fixture Evidence

The inspect command should show:

- old `.nanobot/sessions` files are present;
- primary fixture evidence exists in `telegram_8464732775.jsonl`;
- secondary fixture evidence exists in `cron_morning_market_brief.jsonl`;
- Hermes eval memory files exist in production profile;
- no secret/config files are printed.

## Manual Prompt

Primary prompt:

```text
鹰眼，我想回忆一下之前我们讨论过的那个旅游出行平台标的。你当时不是只把它当普通消费股看，而是从体验型消费、出境游修复、竞争格局和截图里的估值/价格线索去判断。请按你旧的鹰眼口径回答：先给核心结论，再给证据卡，再给行动/风险计划。顺便说明你这次是从记忆/历史摘要里找回来的，还是只是根据常识推断；如果找不到旧记录，就直接说不确定。
```

## Acceptance Matrix

| Check | Expected | Status |
|---|---|---|
| Branch | `codex/s13-105-memory-search-backtest` | PASS |
| Source policy | `.nanobot` runtime only | PASS |
| Prompt leakage | no date/ticker/price/file path in primary prompt | PASS |
| Helper syntax | `bash -n` passes | PASS |
| Fixture inspect | read-only and finds source anchors | PASS |
| Manual Hermes answer | graded by rubric | PENDING |
| Source honesty | answer states retrieval vs inference | PENDING |

## Grading

### PASS_HIGH

The answer identifies Ctrip / `US.TCOM` or equivalent, restores the Eagle/Scout evidence-card format, mentions screenshot plus market data, and recovers at least one concrete old detail such as price around `$47`, intraday low, volume, or support/resistance bands.

### PASS_MEDIUM

The answer recovers the travel-platform thesis and Eagle/Scout style but misses concrete historical details or source honesty.

### FAIL

The answer is generic, hallucinates unrelated facts, or claims exact old memory without a retrieval/source basis.

## Result Log

### Non-Mutating Fixture Checks

Branch:

```text
codex/s13-105-memory-search-backtest
```

Commands passed:

```bash
bash -n deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh
bash deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh inspect
```

Fixture evidence:

```text
.sessions present: cli_budget-guard, cli_heartbeat, cli_lobby, cli_loop-guard, cli_plan, cron_morning_market_brief, telegram_8464732775
primary anchor: telegram_8464732775 lines 1102, 1109, 1111 identify travel-platform/Ctrip/US.TCOM, Futu data, screenshot, and Eagle evidence-card report
secondary anchor: cron_morning_market_brief recurring Alibaba/Baidu + overnight China ADR task
Hermes eval memory files: MEMORY.md, USER.md, chimera-history-summary.md present
secret policy: .env, secrets.env, config.json, and config backups skipped
```

Prompt leakage check:

```text
PASS: primary prompt contains no exact ticker/date/price/path leakage
```

### Manual Hermes Run

Pending. Send the primary prompt through Telegram or CLI and grade the answer with the rubric above.
