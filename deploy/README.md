# Hermes Fork Deploy Layout

This directory carries the Chimera collaboration and operations layout into the Hermes fork.

The first goal is evaluation safety, not production takeover. Scripts in this tree must default to read-only checks or isolated runtime paths unless a command name explicitly says it mutates state.

## Groups

- `deploy/runtime/`
  - Local runtime/profile helpers for isolated Hermes evaluation.
- `deploy/release/`
  - Fork/upstream release preflight helpers. Production release scripts come later after S13.100 acceptance.
- `deploy/ops/`
  - Operational status and readiness checks.
- `deploy/it/`
  - Integration-test and acceptance wrappers.
- `deploy/automation/`
  - Reserved for scheduled evaluation or report generation.
- `deploy/hermes-evaluation/`
  - S13.100 evaluation-specific scripts.

## Baseline Commands

```bash
bash deploy/it/hermes_eval_precheck.sh
bash deploy/runtime/hermes_profile.sh status eval
bash deploy/ops/hermes_eval_status.sh eval
```

Optional deep check:

```bash
bash deploy/it/hermes_eval_precheck.sh --deep
```

## Runtime Isolation

Evaluation profiles default to:

```text
.runtime/hermes-profiles/<profile>
```

Override with:

```bash
HERMES_EVAL_HOME=/path/to/hermes-home bash deploy/runtime/hermes_profile.sh status eval
```

Do not point S13.100 evaluation scripts at the user's real `~/.hermes` until gateway, memory, skills, config, and rollback behavior have passed acceptance.
