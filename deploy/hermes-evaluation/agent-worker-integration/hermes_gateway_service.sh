#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$ROOT_DIR/.runtime/hermes-profiles/eval}"
HERMES_ACCEPT_HOOKS="${HERMES_ACCEPT_HOOKS:-1}"
LINES="${LINES:-120}"

if [ -x "$ROOT_DIR/.venv/bin/hermes" ]; then
  HERMES_BIN="${HERMES_BIN:-$ROOT_DIR/.venv/bin/hermes}"
elif command -v hermes >/dev/null 2>&1; then
  HERMES_BIN="${HERMES_BIN:-$(command -v hermes)}"
else
  HERMES_BIN="${HERMES_BIN:-$ROOT_DIR/.venv/bin/hermes}"
fi

usage() {
  cat <<USAGE
Usage: bash deploy/hermes-evaluation/agent-worker-integration/hermes_gateway_service.sh <command>

Commands:
  status      Show Hermes gateway service status and process summary.
  install     Install the user-level gateway service for the active HERMES_HOME.
  start       Start the gateway service.
  stop        Stop the gateway service.
  restart     Restart the gateway service.
  logs        Tail gateway logs. Set LINES=200 to change line count.
  follow      Follow gateway logs.
  doctor      Run Hermes doctor under the active HERMES_HOME.
  precheck    Run repository and gateway readiness checks.
  uninstall   Uninstall the gateway service.

Environment:
  HERMES_HOME  Default: $ROOT_DIR/.runtime/hermes-profiles/eval
  HERMES_BIN   Default: $ROOT_DIR/.venv/bin/hermes when present
USAGE
}

run_hermes() {
  HERMES_HOME="$HERMES_HOME" HERMES_ACCEPT_HOOKS="$HERMES_ACCEPT_HOOKS" "$HERMES_BIN" "$@"
}

launchd_summary() {
  if command -v launchctl >/dev/null 2>&1; then
    launchctl list | grep -i 'ai.hermes.gateway' || true
  fi
}

process_summary() {
  ps aux | grep -E '[h]ermes.*gateway|[p]ython.*hermes_cli.*gateway|[p]ython.*hermes.*gateway' || true
}

cmd="${1:-}"
case "$cmd" in
  -h|--help|help|'')
    usage
    ;;
  status)
    echo "[hermes-gateway-service] root=$ROOT_DIR"
    echo "[hermes-gateway-service] HERMES_HOME=$HERMES_HOME"
    echo "[hermes-gateway-service] HERMES_BIN=$HERMES_BIN"
    run_hermes gateway status || true
    launchd_summary
    process_summary
    ;;
  install)
    run_hermes gateway install
    ;;
  start)
    run_hermes gateway start
    ;;
  stop)
    run_hermes gateway stop
    ;;
  restart)
    run_hermes gateway restart
    ;;
  uninstall)
    run_hermes gateway uninstall
    ;;
  logs)
    if [ -f "$HERMES_HOME/logs/gateway.log" ]; then
      tail -n "$LINES" "$HERMES_HOME/logs/gateway.log"
    else
      echo "[hermes-gateway-service] missing log: $HERMES_HOME/logs/gateway.log" >&2
      exit 1
    fi
    ;;
  follow)
    if [ -f "$HERMES_HOME/logs/gateway.log" ]; then
      tail -n "$LINES" -f "$HERMES_HOME/logs/gateway.log"
    else
      echo "[hermes-gateway-service] missing log: $HERMES_HOME/logs/gateway.log" >&2
      exit 1
    fi
    ;;
  doctor)
    run_hermes doctor
    ;;
  precheck)
    if [ -x "$ROOT_DIR/deploy/hermes-evaluation/hermes_eval_precheck.sh" ]; then
      bash "$ROOT_DIR/deploy/hermes-evaluation/hermes_eval_precheck.sh" --deep || exit $?
    else
      echo "[WARN] missing deploy/hermes-evaluation/hermes_eval_precheck.sh"
    fi
    [ -x "$HERMES_BIN" ] && echo "[OK] hermes bin: $HERMES_BIN" || { echo "[FAIL] hermes bin missing: $HERMES_BIN"; exit 1; }
    [ -d "$HERMES_HOME" ] && echo "[OK] HERMES_HOME exists: $HERMES_HOME" || { echo "[FAIL] HERMES_HOME missing: $HERMES_HOME"; exit 1; }
    [ -f "$HERMES_HOME/config.yaml" ] && echo "[OK] config.yaml exists" || echo "[WARN] config.yaml missing"
    [ -f "$HERMES_HOME/.env" ] && echo "[OK] .env exists" || echo "[WARN] .env missing"
    run_hermes gateway status || true
    ;;
  *)
    echo "[hermes-gateway-service] unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac
