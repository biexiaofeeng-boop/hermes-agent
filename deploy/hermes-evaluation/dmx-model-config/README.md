# DMX Eval Config Template

This template configures the isolated Hermes eval profile for DMX `gpt-5.4`, native image input, Chimera skills, and Tavily search.

## Target Profile

```bash
export HERMES_HOME="$PWD/.runtime/hermes-profiles/eval"
```

## Files

- `config.yaml.template`: tracked, non-secret runtime config baseline.
- `.env.template`: tracked secret-name template only; replace values locally.

## Apply

```bash
cp deploy/hermes-evaluation/dmx-model-config/config.yaml.template "$HERMES_HOME/config.yaml"
cp deploy/hermes-evaluation/dmx-model-config/.env.template "$HERMES_HOME/.env"
chmod 600 "$HERMES_HOME/.env"
```

Then edit `$HERMES_HOME/.env` and replace placeholders.

## Vision Routing

The template declares:

```yaml
model:
  supports_vision: true
  context_length: 1048576
agent:
  image_input_mode: auto
providers:
  dmx:
    models:
      gpt-5.4:
        supports_vision: true
        context_length: 1048576
```

This makes user-attached screenshots route as native image input instead of falling back to the auxiliary vision text pipeline.

## Chimera Skills

The template mounts:

```yaml
skills:
  external_dirs:
    - ~/1data/Chimera-Projs/chimera-skills
```

`chimera-prod-release-ops` stays disabled by default and on Telegram.

## Validate

```bash
HERMES_HOME="$PWD/.runtime/hermes-profiles/eval" .venv/bin/python - <<'PY'
from hermes_cli.config import load_config
from agent.image_routing import decide_image_input_mode, _lookup_supports_vision
cfg = load_config()
provider = cfg['model']['provider']
model = cfg['model']['default']
print('supports_vision', _lookup_supports_vision(provider, model, cfg))
print('image_input_mode', decide_image_input_mode(provider, model, cfg))
PY
```

Expected:

```text
supports_vision True
image_input_mode native
```
