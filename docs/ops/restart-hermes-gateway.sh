#!/usr/bin/env bash
set -euo pipefail

LABEL="ai.hermes.gateway"
UID_VALUE="$(id -u)"
PLIST="/Users/sourcefire/Library/LaunchAgents/${LABEL}.plist"
ROOT="/Users/sourcefire/X-lab/chimera-hermes-agent"
HERMES_HOME="${ROOT}/.runtime/hermes-profiles/eval"

if [[ ! -f "${PLIST}" ]]; then
  echo "Missing launchd plist: ${PLIST}" >&2
  exit 1
fi

echo "Checking plist..."
plutil -lint "${PLIST}"

echo "Stopping ${LABEL} if loaded..."
launchctl bootout "gui/${UID_VALUE}/${LABEL}" 2>/dev/null || true

echo "Starting ${LABEL}..."
launchctl bootstrap "gui/${UID_VALUE}" "${PLIST}"

echo "Waiting for gateway startup..."
sleep 3

echo "Launchd status:"
launchctl print "gui/${UID_VALUE}/${LABEL}" | sed -n '1,95p'

echo
echo "Hermes gateway status:"
HERMES_HOME="${HERMES_HOME}" "${ROOT}/.venv/bin/hermes" gateway status || true

echo
echo "Recent gateway log:"
tail -n 80 "${HERMES_HOME}/logs/gateway.log"
