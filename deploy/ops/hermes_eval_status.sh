#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PROFILE="${1:-eval}"

echo "[hermes-eval-status] root=$ROOT_DIR"
git -C "$ROOT_DIR" rev-parse --short HEAD | sed 's/^/[hermes-eval-status] head=/'
git -C "$ROOT_DIR" branch --show-current | sed 's/^/[hermes-eval-status] branch=/'
git -C "$ROOT_DIR" remote -v | sed 's/^/[hermes-eval-status] remote /'
git -C "$ROOT_DIR" status --short | sed 's/^/[hermes-eval-status] change /' || true
bash "$ROOT_DIR/deploy/runtime/hermes_profile.sh" status "$PROFILE"
