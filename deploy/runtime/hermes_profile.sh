#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CMD="${1:-status}"
PROFILE="${2:-eval}"
BASE_HOME="${HERMES_EVAL_HOME:-$ROOT_DIR/.runtime/hermes-profiles/$PROFILE}"

usage() {
  cat <<USAGE
Usage: bash deploy/runtime/hermes_profile.sh <status|init|env> [profile]

Environment:
  HERMES_EVAL_HOME  Override the profile home path.
USAGE
}

case "$CMD" in
  status)
    echo "[hermes-profile] root=$ROOT_DIR"
    echo "[hermes-profile] profile=$PROFILE"
    echo "[hermes-profile] hermes_home=$BASE_HOME"
    if [ -d "$BASE_HOME" ]; then
      echo "[hermes-profile] home_exists=1"
    else
      echo "[hermes-profile] home_exists=0"
    fi
    for rel in config.yaml .env MEMORY.md USER.md SOUL.md; do
      if [ -e "$BASE_HOME/$rel" ]; then
        echo "[hermes-profile] file:$rel=present"
      else
        echo "[hermes-profile] file:$rel=missing"
      fi
    done
    ;;
  init)
    mkdir -p "$BASE_HOME" "$BASE_HOME/skills" "$BASE_HOME/logs" "$BASE_HOME/sessions" "$BASE_HOME/memory" "$BASE_HOME/workspace"
    echo "[hermes-profile] initialized=$BASE_HOME"
    ;;
  env)
    echo "export HERMES_HOME='$BASE_HOME'"
    echo "export HERMES_PROFILE='$PROFILE'"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
