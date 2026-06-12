# S13.102 Task Package: Chimera Skills Migration

Date: 2026-06-12
Branch: `codex/s13-102-chimera-skills-migration`
Status: PASS
Fork: `biexiaofeeng-boop/hermes-agent`
Upstream: `NousResearch/hermes-agent`

## Numbering Note

S13.100 originally listed S13.102 as gateway evaluation and S13.104 as Chimera skill migration. The current operator decision moves Chimera skill migration forward to S13.102 because Hermes runtime setup and memory migration are already available for evaluation, while gateway cutover can remain separate.

Updated sequence:

- S13.101: Hermes isolated install, profile setup, memory migration baseline.
- S13.102: Chimera skills migration package and first controlled capability migration.
- S13.103: Memory and session-search quality backtest.
- S13.104: Gateway evaluation with one controlled messaging channel.
- S13.105: Production cutover design if the prior packages pass.

## Background

Chimera Core already accumulated reusable capabilities as skills: web search, production release operations, RPA/vision, tmux orchestration, memos writing, weather, GitHub operations, summarization, and skill authoring. Hermes Agent also has its own skill system with profile-scoped skill directories, built-in skills, optional skills, external skill directories, hub installation, audit, enable/disable config, platform-specific disabling, and curator support.

The migration question is not whether all Chimera skills can be copied into Hermes. The practical question is how to migrate only the stable, high-value Chimera capabilities into Hermes without creating context explosion, secret sprawl, or a fork that diverges unnecessarily from upstream Hermes.

## Goal

Create a controlled Chimera skill migration path for Hermes:

- keep Hermes core clean;
- expose Chimera capabilities through a shared external skill armory;
- migrate only the first small capability set;
- keep high-risk operational skills disabled by default;
- define config, secret, resource, and rollback rules;
- provide acceptance checks for future implementation agents.

## Non-Goals

- Do not replace `chimera-core-prod`.
- Do not perform production cutover.
- Do not enable all Chimera skills globally.
- Do not store API keys, tokens, account IDs, or private runtime paths inside `SKILL.md`.
- Do not copy Chimera production runtime state into Hermes.
- Do not modify Hermes core skill loader unless external-dir migration proves insufficient.
- Do not treat this package as a gateway or messaging-channel evaluation.

## Current Facts

### Hermes Skill Mechanism

Relevant Hermes behavior observed in code:

- local skill root is `<HERMES_HOME>/skills`;
- external skill directories are configured via `skills.external_dirs` in profile `config.yaml`;
- local skill root is scanned before external directories, so local skills win name conflicts;
- disabled skills are configured via `skills.disabled`;
- platform-specific disabled lists are configured via `skills.platform_disabled.<platform>`;
- `hermes skills list --enabled-only` hides disabled skills;
- `hermes skills audit [name]` can re-scan installed skills;
- skill directories use `SKILL.md` plus optional `scripts/`, `references/`, `templates/`, and `assets/`.

### Chimera Skill Inventory

Initial Chimera source skills under `chimera-core/nanobot/skills`:

| Chimera Skill | Migration Decision | Hermes Target | Rationale |
|---|---|---|---|
| `web-search` | migrate first | `chimera-web-search-tavily` | High-value generic capability; user confirms Tavily is the current primary web search provider. |
| `prod-release-ops` | migrate first, disabled by default | `chimera-prod-release-ops` | Operationally useful but high-risk; must be profile-gated and never globally enabled. |
| project finance/intel skill | create first skeleton | `chimera-finance-intel` or project-specific name | Represents project skill pattern: stable project workflow, references, data contracts, and report output conventions. |
| `github` | do not migrate initially | use Hermes GitHub skills | Hermes already has GitHub-focused built-ins; avoid duplicate capability surface. |
| `skill-creator` | do not migrate initially | use Hermes skill authoring | Hermes already has skill authoring conventions and tools. |
| `weather` | skip | use Hermes/builtin or ad hoc tool | Low strategic value; not worth migration overhead. |
| `summarize` | optional later | `chimera-summarize-cli` if needed | Only migrate if summarize.sh remains a real daily dependency. |
| `tmux` | optional later | `chimera-tmux-orchestration` | Useful for multi-agent TTY orchestration, but should wait until Codex/Claude/Hermes flow is clarified. |
| `rpa-vision` | defer | `chimera-rpa-vision` | Needs browser/computer-use comparison with Hermes capabilities first. |
| `memos-writer` | defer | `chimera-memos-writer` | Depends on final memory/report storage path after Hermes memory evaluation. |

## Target Architecture

### Three-Layer Skills Model

1. Hermes native skills
   - Built-in, optional, and hub-installed skills owned by Hermes.
   - Used whenever they already solve the capability.

2. Chimera skill armory
   - User-controlled external skill directory.
   - Contains Chimera-specific generic, ops, and project skills.
   - Mounted into Hermes through `skills.external_dirs`.

3. Project skills
   - Thin procedural wrappers around stable project capabilities.
   - Use references and scripts instead of injecting large project context into every session.
   - May be enabled only in project or ops profiles.

### Proposed Armory Path

Default external armory:

```text
~/1data/Chimera-Projs/chimera-skills
```

Suggested layout:

```text
chimera-skills/
├── research/
│   └── chimera-web-search-tavily/
│       ├── SKILL.md
│       └── scripts/
├── ops/
│   └── chimera-prod-release-ops/
│       ├── SKILL.md
│       └── references/
├── finance/
│   └── chimera-finance-intel/
│       ├── SKILL.md
│       ├── references/
│       └── templates/
└── README.md
```

Hermes uses the first folder under an external skills root as category, so this structure keeps categories visible in `hermes skills list`.

### Profile Wiring

Example profile config:

```yaml
skills:
  external_dirs:
    - ~/1data/Chimera-Projs/chimera-skills
  disabled:
    - chimera-prod-release-ops
```

Ops profile may explicitly enable ops skills by removing them from `disabled`, or use platform-specific controls:

```yaml
skills:
  external_dirs:
    - ~/1data/Chimera-Projs/chimera-skills
  disabled:
    - chimera-prod-release-ops
  platform_disabled:
    telegram:
      - chimera-prod-release-ops
```

## Skill Authoring Standard

Each migrated Chimera skill must follow this minimum contract:

```text
skill-name/
├── SKILL.md
├── scripts/       # deterministic helpers only when needed
├── references/    # optional docs loaded on demand
├── templates/     # report/output templates
└── assets/        # static assets only if needed
```

`SKILL.md` rules:

- frontmatter must include `name` and concise `description`;
- `name` must use stable lowercase hyphen style and start with `chimera-`;
- instructions must describe when to use the skill and when not to use it;
- large project knowledge must move to `references/`, not the main body;
- API keys must be referenced as environment variables only;
- scripts must fail closed with clear missing-env or missing-dependency messages;
- outputs must identify artifacts, evidence, and fallback state.

## Resource And Secret Contract

### Secrets

Allowed:

- `TAVILY_API_KEY` for `chimera-web-search-tavily`;
- profile `.env` files outside git;
- documented secret reference names.

Forbidden:

- literal tokens in `SKILL.md`;
- literal tokens in examples;
- command snippets that print secrets;
- migration scripts that copy secrets into the armory.

### Filesystem Resources

Every project or ops skill must document:

- allowed read paths;
- allowed write paths;
- artifact output path convention;
- whether state is ephemeral or persistent;
- rollback or cleanup command if it writes files.

### Context Size

A migrated skill should keep `SKILL.md` small enough to load as procedural guidance. Project details should be summarized in references and loaded only when needed. The default stance is that Codex, Claude Code, and Hermes are already capable agents; skills should add local procedure, not generic AI explanations.

## Implementation Strategy

### Phase A: Inventory And Armory Baseline

- Create or verify `~/1data/Chimera-Projs/chimera-skills`.
- Add `README.md` describing ownership and no-secrets rule.
- Record source skill inventory and migration decisions.

### Phase B: External Directory Wiring

- Add the armory path to the selected Hermes evaluation profile.
- Keep `chimera-prod-release-ops` disabled by default.
- Verify `hermes skills list` sees only intended skills.

### Phase C: First Generic Skill

- Convert Chimera `web-search` into `chimera-web-search-tavily`.
- Add deterministic script only if it improves repeatability.
- Require `TAVILY_API_KEY`; do not fall back to hardcoded or legacy key names.
- Smoke test with a safe query and confirm no key appears in output.

### Phase D: First Ops Skill

- Convert `prod-release-ops` into `chimera-prod-release-ops`.
- Keep it disabled in normal profiles and disabled on chat platforms by default.
- Make it a runbook skill, not an automatic release executor.
- Require explicit operator confirmation before any mutating release command.

### Phase E: First Project Skill Skeleton

- Create one finance/intel project skill skeleton.
- Keep domain facts in `references/` and report templates in `templates/`.
- Document data references instead of embedding private raw data.

## Acceptance Criteria

S13.102 is accepted when:

- a Chimera skill armory path is defined and documented;
- profile config can mount the armory through `skills.external_dirs`;
- `hermes skills list` can show migrated Chimera skills as local/external skills;
- `hermes skills list --enabled-only` excludes disabled ops skills;
- `chimera-web-search-tavily` can be loaded or audited without leaking secrets;
- `chimera-prod-release-ops` is present but disabled in non-ops profile;
- at least one project skill skeleton defines resource refs, outputs, and summary-first usage;
- no Hermes core runtime file needs to change for the first migration;
- no secret or runtime state file is tracked by git;
- rollback can restore the baseline by removing the external dir config or disabling the migrated skill names.

## Risks And Controls

| Risk | Control |
|---|---|
| Context explosion | Keep `SKILL.md` procedural and move details to `references/`. |
| Secret leakage | Environment variables only; no copied config values; run secret grep before commit. |
| Duplicate skills | Prefer Hermes native skills; migrate only Chimera-specific capabilities. |
| High-risk ops execution | Disable ops skill by default and by platform; require explicit operator confirmation. |
| External dir drift | Keep armory source-controlled separately or documented as operator-owned. |
| Curator or self-editing surprises | Do not let autonomous cleanup rewrite the armory until policy is validated. |
| Runtime coupling | Skills reference project APIs/scripts, not Chimera process internals, unless explicitly scoped. |

## Backtest Design

The first implementation agent must run a small backtest before enabling any migrated skill broadly:

| Case | Input | Expected Result |
|---|---|---|
| Discovery | armory path with three skills | `hermes skills list` shows migrated skills with categories. |
| Disable guard | non-ops profile | `chimera-prod-release-ops` is hidden from `--enabled-only`. |
| Tavily smoke | safe web query | returns result summary and source URLs; no API key in stdout/stderr. |
| Missing key | no `TAVILY_API_KEY` | fails with actionable missing-env message. |
| Project context | project skill load | loads summary and references contract, not raw private data. |
| Rollback | remove external dir or disable skill names | Hermes returns to baseline skill list. |

## Follow-Up Packages

S13.103 should evaluate memory/session-search quality and how project skill references should link to long-term memory.

S13.104 should evaluate gateway/channel behavior after skills and memory are stable enough to support real work.

## Execution Summary 2026-06-12

First execution pass completed:

- added Hermes bridge skills under `/Users/sourcefire/1data/Chimera-Projs/chimera-skills`;
- mounted the armory into the Hermes eval profile through `skills.external_dirs`;
- kept `chimera-prod-release-ops` disabled globally and on Telegram platform;
- verified discovery: 3 Chimera local skills discovered, 2 enabled, 1 disabled;
- verified Tavily missing-key behavior and script compilation;
- verified real-key Tavily smoke after `TAVILY_API_KEY` was added to the eval profile `.env`;
- simulated rollback by removing `skills.external_dirs` in a temporary Hermes home.

Detailed evidence is recorded in `122-Checks-S13.102-Chimera-Skills-Migration-v1-2026-06-12.md`.
