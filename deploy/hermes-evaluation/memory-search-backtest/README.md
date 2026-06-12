# S13.105 Memory Search Backtest

This package validates Hermes memory/search behavior after Chimera memory migration.

It uses old runtime agent state from:

```text
/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot
```

It intentionally does not use `docs/Issue-Checks` as the answer source.

## Run Fixture Inspection

```bash
bash deploy/hermes-evaluation/memory-search-backtest/s13-105_memory_backtest.sh inspect
```

## Primary Telegram Prompt

```text
鹰眼，我想回忆一下之前我们讨论过的那个旅游出行平台标的。你当时不是只把它当普通消费股看，而是从体验型消费、出境游修复、竞争格局和截图里的估值/价格线索去判断。请按你旧的鹰眼口径回答：先给核心结论，再给证据卡，再给行动/风险计划。顺便说明你这次是从记忆/历史摘要里找回来的，还是只是根据常识推断；如果找不到旧记录，就直接说不确定。
```

Pass criteria are documented in:

```text
docs/Issue-Checks/2026-06/152-Checks-S13.105-Memory-Search-Backtest-v1-2026-06-12.md
```
