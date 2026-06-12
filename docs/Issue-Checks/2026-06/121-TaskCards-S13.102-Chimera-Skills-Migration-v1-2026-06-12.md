# S13.102 Task Cards: Chimera Skills Migration

Date: 2026-06-12
Branch: `codex/s13-102-chimera-skills-migration`
Status: IMPLEMENTED_WITH_OPERATOR_ACTION

## T01 - Chimera Skill Inventory And Decisions

Goal: Freeze the initial migration list before any copying or profile changes.

Implementation:

- Enumerate `chimera-core/nanobot/skills/*/SKILL.md`.
- Classify each skill as migrate, reuse Hermes native, skip, optional, or defer.
- Record the reason for each decision.

Acceptance:

- Inventory table exists in the S13.102 task package.
- First migration set is limited to `chimera-web-search-tavily`, `chimera-prod-release-ops`, and one project skill skeleton.
- No broad auto-migration is authorized.

## T02 - Chimera Skill Armory Baseline

Goal: Create a clean external skill armory that Hermes can mount without modifying Hermes core.

Implementation:

- Use `~/1data/Chimera-Projs/chimera-skills` as the default armory path unless the operator overrides it.
- Create category directories such as `research/`, `ops/`, and `finance/`.
- Add an armory `README.md` documenting ownership, no-secrets policy, and rollback path.

Acceptance:

- Armory exists outside `hermes-agent` unless the operator explicitly chooses vendoring.
- Armory contains no `.env`, runtime home, token, cache, or private data files.
- Category layout is compatible with Hermes skill category detection.

## T03 - Hermes Profile External-Dir Wiring

Goal: Let a Hermes evaluation profile discover the Chimera armory through config only.

Implementation:

- Update the selected evaluation profile `config.yaml` with `skills.external_dirs`.
- Add high-risk ops skill names to `skills.disabled`.
- If a chat/gateway profile is used, also add `skills.platform_disabled.telegram` for ops skills.

Acceptance:

- `hermes skills list` shows migrated Chimera skills.
- `hermes skills list --enabled-only` hides disabled ops skills.
- Removing `skills.external_dirs` restores the baseline list.

## T04 - Migrate Tavily Web Search Skill

Goal: Convert Chimera `web-search` into a Hermes-compatible, Tavily-first skill.

Implementation:

- Create `research/chimera-web-search-tavily/SKILL.md`.
- Require `TAVILY_API_KEY` from environment.
- If adding a script, place it under `scripts/` and ensure it never prints the key.
- Document missing-key behavior and result format.

Acceptance:

- `hermes skills audit chimera-web-search-tavily` passes or returns only actionable non-secret warnings.
- A safe query smoke test returns title, URL, and summary fields.
- Missing `TAVILY_API_KEY` fails closed with a clear message.
- No output contains the API key value.

## T05 - Migrate Production Release Ops As Disabled Runbook

Goal: Preserve Chimera release knowledge without exposing production mutation by default.

Implementation:

- Create `ops/chimera-prod-release-ops/SKILL.md`.
- Convert direct commands into staged operator runbook steps.
- Require explicit operator confirmation before any mutating command.
- Keep the skill disabled in normal and chat profiles.

Acceptance:

- Skill appears in `hermes skills list` but not in `hermes skills list --enabled-only` for non-ops profile.
- The skill does not auto-run release commands.
- It states required precheck, snapshot, canary, cutover, verify, and rollback gates.

## T06 - Create First Project Skill Skeleton

Goal: Define the pattern for Chimera project capabilities without dumping project context into Hermes.

Implementation:

- Create a finance/intel project skill under `finance/` or a specific project category.
- Keep `SKILL.md` as summary-first procedural guidance.
- Put project resource contracts in `references/`.
- Put report output examples in `templates/`.

Acceptance:

- Skill identifies allowed data refs, allowed output paths, and artifact naming.
- Loading the skill does not reveal raw private data.
- The project skill can be disabled or removed independently of generic skills.

## T07 - Secret And Resource Guardrail Check

Goal: Prevent migration from reintroducing the config/key sprawl that S8 removed from Chimera.

Implementation:

- Run secret grep against the armory and Hermes repo before commit.
- Verify `.env`, runtime homes, caches, and backups are ignored or outside git.
- Document required environment variables per skill.

Acceptance:

- No tracked file contains literal API keys or tokens.
- Each migrated skill documents secret refs by name only.
- Filesystem write paths are explicit for project and ops skills.

## T08 - Backtest And Rollback Runbook

Goal: Make the first migration reversible and measurable.

Implementation:

- Capture baseline `hermes skills list` output.
- Add external dir and capture migrated list output.
- Run `--enabled-only` check.
- Run Tavily missing-key and real-key smoke tests when authorized.
- Remove external dir or disable migrated skills to confirm rollback.

Acceptance:

- Checks document records baseline, migrated, disabled, smoke, and rollback results.
- Rollback does not require Hermes core code changes.
- Any failing check has a clear next action.

## T09 - Documentation Backfill

Goal: Keep the collaboration standard current for the next implementation agent.

Implementation:

- Update `docs/Issue-Checks/2026-06/00-INDEX-2026-06.md`.
- If S13.100 follow-up numbering conflicts with S13.102, add a numbering note.
- Record remaining risks and follow-up packages.

Acceptance:

- Index lists S13.102 task package, task cards, and checks.
- Future agents can execute the migration from the docs without rediscovering the strategy.
