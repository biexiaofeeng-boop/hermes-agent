# Checks: S11.G Foundry Ingest Core Bridge v1

## Scope

- Repo: `/Users/sourcefire/X-lab/chimera-core`
- Branch: `codex/s11g-foundry-ingest-core-v1`
- Packet: B1 / S11.G Foundry Ingest Core Bridge

## Verification

Targeted tests:

```bash
python3.11 -m unittest tests.test_foundry_ingest -v
```

Result: PASS.

CLI smoke against the local Foundry adapter:

```bash
python3.11 -m nanobot.cli.commands foundry ingest-note \
  --foundry-repo /Users/sourcefire/X-lab/chimera-foundry \
  --title "Packet B1 core smoke" \
  --content "Core to Foundry smoke digest." \
  --domain project \
  --topic-tag foundry \
  --topic-tag ingest \
  --trace-id trace-core-b1 \
  --task-id task-core-b1 \
  --conversation-id conv-core-b1 \
  --json
```

Result: PASS. The command returns a `foundry.ingest.receipt.v1` receipt from Foundry with `raw_path`, `sidecar_path`, `content_sha256`, and `promoted=false`.

## Acceptance Checklist

- PASS: explicit ingest helper works
- PASS: receipt is parsed and returned
- PASS: failure is clear
- PASS: no automatic chat ingestion is introduced
- PASS: no promotion is triggered by `chimera-core`
- PASS: core calls the Foundry adapter instead of writing Foundry internals directly

## Residual Risks

- uncontrolled scheduled ingestion can create raw spam later
- conversation digests require careful topic/window selection
- The CLI can still be misused to ingest low-signal content; operating discipline should prefer explicit curated notes or topic/window digests.
