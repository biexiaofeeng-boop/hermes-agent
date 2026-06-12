# S13.105 Task Package: Memory Search Backtest

Date: 2026-06-12
Branch: `codex/s13-105-memory-search-backtest`
Status: DESIGN_READY
Fork: `biexiaofeeng-boop/hermes-agent`

## Goal

Validate whether Hermes can recover useful Chimera historical context after memory migration, using only runtime agent materials from the old production profile.

This is not a feature expansion. It is a small acceptance backtest for the current memory/search behavior before deciding whether to add heavier RAG or session indexing.

## Source Policy

Use only old runtime agent state as the backtest source:

```text
/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot
```

Allowed source classes:

- `.nanobot/sessions/*.jsonl`
- `.nanobot/workspace/HEARTBEAT.md`
- `.nanobot/workspace/chimera-bridge/trace/*.jsonl`
- `.nanobot/skills/registry.json`

Do not use `docs/Issue-Checks` content as the answer source. Those files are engineering collaboration records and were not normal conversation memory for the runtime agent.

Do not read or print secrets:

- `.nanobot/.env`
- `.nanobot/secrets.env`
- `.nanobot/config.json`
- backup config or secret files

## Current Memory Baseline

Hermes production eval profile currently has built-in memory active, with no external memory provider configured.

Important migrated Hermes files:

```text
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/MEMORY.md
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/USER.md
/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/workspace/chimera-history/chimera-history-summary.md
```

Known limitation:

- Old raw Chimera sessions were summarized into Hermes workspace memory references.
- Old raw Chimera sessions are not proven to be indexed into Hermes session FTS.
- Therefore this backtest should grade both recall quality and source honesty.

## Primary Backtest Anchor

Use the old `.nanobot` runtime session around the finance/intelligence interaction where the user asked about a travel platform target and provided a screenshot. The assistant later produced an Eagle/Scout style report using:

- travel platform target, later identified as `US.TCOM` / Ctrip;
- experience-consumption / travel demand logic;
- evidence card style;
- Futu market data plus user screenshot;
- latest close around `$47.43`, intraday low around `$47.08`, volume around `3.09M`;
- action/risk plan with support and resistance bands.

This anchor is appropriate because it tests real user-facing memory, not internal development docs.

## Primary Vague Prompt

The operator should send this through Telegram or CLI. It intentionally avoids dates, package names, and exact ticker/price cues:

```text
鹰眼，我想回忆一下之前我们讨论过的那个旅游出行平台标的。你当时不是只把它当普通消费股看，而是从体验型消费、出境游修复、竞争格局和截图里的估值/价格线索去判断。请按你旧的鹰眼口径回答：先给核心结论，再给证据卡，再给行动/风险计划。顺便说明你这次是从记忆/历史摘要里找回来的，还是只是根据常识推断；如果找不到旧记录，就直接说不确定。
```

Why this prompt:

- It is natural language.
- It does not disclose date or timeline.
- It does not mention `TCOM`, `携程`, `$47.43`, `2026-05-30`, or file paths.
- It requires answer-source honesty.
- It tests whether migrated memory can connect vague context to a concrete historical conversation.

## Secondary Vague Prompt

Use this if the primary test is too hard or if the finance anchor needs cross-checking:

```text
鹰眼，帮我回忆一下我们以前为什么总强调盘前简报先盯阿里和百度，再接隔夜中概表现。不要按普通市场评论说，按我们旧系统的任务口径回答：这个简报要拉什么、看什么、最后给我什么，以及它为什么适合我白天没法一直盯盘的使用方式。也请说明你是从旧记忆找回来的，还是不确定。
```

This tests the recurring old runtime cron/session pattern.

## Expected Answer Rubric

### PASS_HIGH

The answer should:

- identify the travel platform as Ctrip / `US.TCOM` or clearly equivalent;
- recover the core thesis: experience consumption, travel resilience, outbound travel margin recovery, clear OTA competitive structure;
- use Eagle/Scout structure: core conclusion -> evidence card -> action/risk plan;
- mention that the old answer used user screenshot plus market data, ideally Futu data;
- recover at least one concrete historical detail such as price around `$47`, intraday low around `$47.08`, volume around `3.09M`, or support/resistance bands;
- explicitly state whether it is using migrated memory/history summary/session archive or making an inference.

### PASS_MEDIUM

The answer should:

- recover the Ctrip/travel-platform theme and Scout style;
- explain experience consumption and outbound travel logic;
- mention evidence-based analysis;
- but miss concrete old details or retrieval source.

### FAIL

The answer fails if it:

- gives a generic travel-stock answer with no old-memory signal;
- invents unrelated holdings or dates;
- claims exact memory without citing a source path or retrieval basis;
- ignores the request to distinguish memory retrieval from inference.

## Operator Flow

1. Run the local read-only fixture check:

```bash
bash deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh inspect
```

2. Send the primary vague prompt to Hermes Telegram or CLI.

3. Save or copy the response into the checks record.

4. Grade with the rubric above.

5. If the result is `PASS_MEDIUM` or `FAIL`, do not immediately add heavy RAG. First decide whether to index old Chimera session JSONL into a Hermes searchable archive.

## Decision Gate

S13.105 should not implement new memory infrastructure unless the backtest demonstrates a real service gap.

The smallest next implementation, if needed, is a read-only archive index for selected old `.nanobot/sessions/*.jsonl`, not a broad RAG system.
