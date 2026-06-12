# S13.102 Checks: Chimera Skills Migration

Date: 2026-06-12
Branch: `codex/s13-102-chimera-skills-migration`
Status: PASS_WITH_OPERATOR_ACTION

## Verification Scope

This check record defines the verification gate for migrating Chimera skills into Hermes through an external armory. It verifies the migration package and provides commands for the first implementation pass.

It does not verify production cutover, gateway channel behavior, or long-term memory quality.

## Baseline Observations

Chimera source skills observed:

```text
github
memos-writer
prod-release-ops
rpa-vision
skill-creator
summarize
tmux
weather
web-search
```

Hermes skill capabilities observed:

```text
skills.external_dirs
skills.disabled
skills.platform_disabled.<platform>
hermes skills list
hermes skills list --enabled-only
hermes skills audit [name]
hermes skills install/update/uninstall
```

## Required Pre-Migration Commands

Run from the Hermes checkout:

```bash
git branch --show-current
git status --short
find /Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/skills -maxdepth 2 -name SKILL.md -print | sort
hermes skills list
hermes skills list --enabled-only
```

If `hermes` is not on PATH, use the project runtime command established in S13.101.

## Implementation Verification Commands

After the armory and profile wiring are created:

```bash
hermes skills list
hermes skills list --enabled-only
hermes skills audit chimera-web-search-tavily
hermes skills audit chimera-prod-release-ops
```

For Tavily missing-key behavior:

```bash
env -u TAVILY_API_KEY hermes --skills chimera-web-search-tavily -z "Search for OpenAI official docs home page. Return only the missing-key behavior if the key is absent."
```

For Tavily real-key smoke, run only after the operator confirms the key is available in the active profile environment:

```bash
hermes --skills chimera-web-search-tavily -z "Search Tavily for OpenAI official docs home page. Return title, URL, and one-sentence summary. Do not print environment variables."
```

For disabled ops behavior:

```bash
hermes skills list --enabled-only | grep -q 'chimera-prod-release-ops' && echo FAIL || echo PASS
```

For rollback:

```bash
cp "$HERMES_HOME/config.yaml" "$HERMES_HOME/config.yaml.bak.$(date +%Y%m%d-%H%M%S)"
# Remove the Chimera armory path from skills.external_dirs, or add migrated names to skills.disabled.
hermes skills list --enabled-only
```

## Acceptance Matrix

| Check | Expected Result | Status |
|---|---|---|
| S13.102 docs | `120`, `121`, `122` documents exist under `2026-06` | PASS_DOCUMENTED |
| Index | `00-INDEX-2026-06.md` lists S13.102 docs | PASS_DOCUMENTED |
| Armory path | `~/1data/Chimera-Projs/chimera-skills` exists or is operator-overridden | PASS |
| External dir wiring | profile `config.yaml` contains `skills.external_dirs` entry | PASS |
| Web search skill | `chimera-web-search-tavily` is discovered | PASS |
| Tavily missing key | fails closed with clear missing-env message | PASS |
| Tavily real key | returns result without leaking key | TODO_OPERATOR_AUTH |
| Ops skill disabled | `chimera-prod-release-ops` is not shown by `--enabled-only` in non-ops profile | PASS |
| Project skill skeleton | one project skill exists with resource refs and templates | PASS |
| Secrets | no tracked literals for API keys/tokens | PASS_REFERENCES_ONLY |
| Rollback | removing external dir or disabling migrated names restores baseline | PASS_SIMULATED |

## Backtest Cases

### C01 - Discovery Baseline

Input:

- active Hermes evaluation profile;
- no Chimera external dir configured.

Expected:

- `hermes skills list` shows Hermes baseline only;
- output saved as baseline evidence.

### C02 - Discovery After External Dir

Input:

- `skills.external_dirs` includes the Chimera armory path.

Expected:

- `hermes skills list` shows `chimera-web-search-tavily`, `chimera-prod-release-ops`, and the first project skill;
- category names reflect armory first-level folders.

### C03 - Disabled Ops Guard

Input:

- `skills.disabled` contains `chimera-prod-release-ops`.

Expected:

- `hermes skills list` may show the skill as disabled;
- `hermes skills list --enabled-only` does not show it;
- direct use requires explicit operator action.

### C04 - Tavily Missing Key

Input:

- `TAVILY_API_KEY` unset.

Expected:

- skill reports missing environment variable;
- no stack trace with secret paths;
- no fallback to legacy config key.

### C05 - Tavily Smoke With Key

Input:

- `TAVILY_API_KEY` set by active profile environment;
- safe query.

Expected:

- output contains title, URL, and concise content;
- output does not contain the API key or env dump;
- failure is classified as missing_key, network_error, api_error, or no_results.

### C06 - Project Skill Context Hygiene

Input:

- load the project skill explicitly.

Expected:

- skill provides procedure, data refs, and report paths;
- raw private holdings, account data, or large historical logs are not embedded in the main `SKILL.md`.

### C07 - Rollback

Input:

- remove armory from `skills.external_dirs` or add all migrated skill names to `skills.disabled`.

Expected:

- enabled skill list returns to baseline;
- no Hermes core code changes are required;
- armory files can remain on disk safely.

## Secret Scan Commands

Use targeted grep before any commit:

```bash
rg -n "(api[_-]?key|token|secret|password|TAVILY_API_KEY|TELEGRAM_BOT_TOKEN|OPENAI_API_KEY)" \
  docs/Issue-Checks/2026-06 \
  ~/1data/Chimera-Projs/chimera-skills \
  --glob '!**/.env' \
  --glob '!**/.env.*' \
  --glob '!**/node_modules/**' \
  --glob '!**/.venv/**'
```

This command may report allowed reference names. It must not report literal secret values.

## Rollback Policy

Rollback order:

1. Disable migrated skill names in profile config.
2. Remove the armory path from `skills.external_dirs`.
3. Restore `config.yaml` from the timestamped backup if needed.
4. Leave armory files on disk unless the operator explicitly wants deletion.

Rollback must not require deleting Hermes built-in skills or modifying Hermes core code.

## Execution Record 2026-06-12

Branch:

```text
codex/s13-102-chimera-skills-migration
```

Implemented armory bridge skills:

```text
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/research/chimera-web-search-tavily/SKILL.md
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/research/chimera-web-search-tavily/scripts/tavily_search.py
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/ops/chimera-prod-release-ops/SKILL.md
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/ops/chimera-prod-release-ops/references/chimera-prod-release-runbook.md
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/finance/chimera-finance-intel/SKILL.md
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/finance/chimera-finance-intel/references/resource-contract.md
/Users/sourcefire/1data/Chimera-Projs/chimera-skills/finance/chimera-finance-intel/templates/intel-report-template.md
```

Profile config updated:

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

Profile config backup:

```text
.runtime/hermes-profiles/eval/config.yaml.bak.s13-102-20260612-150346
```

Discovery results:

```text
Before migration: 0 hub-installed, 71 builtin, 0 local - 71 enabled, 0 disabled
After migration:  0 hub-installed, 71 builtin, 3 local - 73 enabled, 1 disabled
Enabled only:     0 hub-installed, 71 builtin, 2 local - 73 enabled shown
```

Discovered Chimera skills:

```text
chimera-finance-intel     local enabled
chimera-web-search-tavily local enabled
chimera-prod-release-ops  local disabled
```

Validation results:

```text
python -m py_compile tavily_search.py
PASS

env -u TAVILY_API_KEY tavily_search.py "OpenAI official docs home page" --count 2 --json
PASS: state=missing_key, exit=1

Tavily real-key smoke
SKIP: TAVILY_API_KEY is not present in eval profile .env

Hermes local skill audit
N/A: `hermes skills audit` audits hub-installed skills only and reports "No hub-installed skills to audit."

Rollback simulation
PASS: temporary Hermes home without skills.external_dirs no longer shows chimera-* skills.
```

Secret scan result:

```text
PASS_REFERENCES_ONLY
```

The scan found only documented reference names such as `TAVILY_API_KEY` and policy words such as token/secret. It did not expose literal secret values in the migrated bridge skill files.

## Current Conclusion

Status: PASS_WITH_OPERATOR_ACTION

The S13.102 first execution pass is complete for local discovery, disabled ops guard, missing-key behavior, project skill skeleton, secret-reference hygiene, and rollback simulation.

Remaining operator action: add `TAVILY_API_KEY` to the eval profile environment when ready, then run the real-key Tavily smoke test before treating `chimera-web-search-tavily` as fully online.
