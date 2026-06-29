#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXPECTED_ORIGIN="${EXPECTED_ORIGIN:-https://github.com/biexiaofeeng-boop/hermes-agent.git}"
EXPECTED_UPSTREAM="${EXPECTED_UPSTREAM:-https://github.com/NousResearch/hermes-agent.git}"
DEEP=0

for arg in "$@"; do
  case "$arg" in
    --deep) DEEP=1 ;;
    -h|--help)
      cat <<USAGE
Usage: bash deploy/hermes-evaluation/hermes_eval_precheck.sh [--deep]

Checks fork baseline, local tooling, runtime isolation, docs, and deploy layout.
Default mode avoids dependency installation and avoids touching real ~/.hermes.
USAGE
      exit 0
      ;;
    *)
      echo "[hermes-eval-precheck] unknown argument: $arg" >&2
      exit 2
      ;;
  esac
done

failures=0
warnings=0

ok() { echo "[OK] $*"; }
warn() { echo "[WARN] $*"; warnings=$((warnings + 1)); }
fail() { echo "[FAIL] $*"; failures=$((failures + 1)); }

normalize_github_remote() {
  local url="${1:-}"
  printf '%s' "$url" | sed -E 's#^https?://##; s#^git@([^:]+):#\1/#; s#\.git$##'
}

cd "$ROOT_DIR"

branch="$(git branch --show-current 2>/dev/null || true)"
head="$(git rev-parse --short HEAD 2>/dev/null || true)"
ok "git branch=${branch:-detached} head=${head:-unknown}"

origin="$(git remote get-url origin 2>/dev/null || true)"
upstream="$(git remote get-url upstream 2>/dev/null || true)"
origin_norm="$(normalize_github_remote "$origin")"
expected_origin_norm="$(normalize_github_remote "$EXPECTED_ORIGIN")"
upstream_norm="$(normalize_github_remote "$upstream")"
expected_upstream_norm="$(normalize_github_remote "$EXPECTED_UPSTREAM")"
if [ "$origin_norm" = "$expected_origin_norm" ]; then
  ok "origin=$origin"
else
  fail "origin mismatch: got '${origin:-missing}', expected '$EXPECTED_ORIGIN'"
fi
if [ "$upstream_norm" = "$expected_upstream_norm" ]; then
  ok "upstream=$upstream"
else
  warn "upstream mismatch: got '${upstream:-missing}', expected '$EXPECTED_UPSTREAM'"
fi

status_count="$(git status --porcelain | wc -l | tr -d ' ')"
if [ "$status_count" = "0" ]; then
  ok "worktree clean"
else
  warn "worktree has $status_count changed paths"
  git status --short
fi

check_python_range() {
  local label="$1"
  local exe="$2"
  local strict="$3"
  if "$exe" - <<'PY'
import sys
raise SystemExit(0 if (3, 11) <= sys.version_info < (3, 14) else 1)
PY
  then
    ok "$label supported ($("$exe" -V 2>&1))"
  else
    if [ "$strict" = "1" ]; then
      fail "$label must satisfy Hermes requires-python >=3.11,<3.14; found $("$exe" -V 2>&1)"
    else
      warn "$label outside Hermes requires-python >=3.11,<3.14; found $("$exe" -V 2>&1)"
    fi
  fi
}

if [ -x .venv/bin/python ]; then
  check_python_range ".venv python" ".venv/bin/python" 1
elif command -v python3 >/dev/null 2>&1; then
  check_python_range "system python3" "python3" 0
else
  fail "no python available"
fi

if command -v uv >/dev/null 2>&1; then
  ok "uv found: $(uv --version 2>/dev/null | head -n 1)"
else
  warn "uv not found; Hermes source install and locked checks may be unavailable"
fi

if command -v node >/dev/null 2>&1; then
  node_major="$(node -p 'process.versions.node.split(`.`)[0]' 2>/dev/null || echo 0)"
  if [ "${node_major:-0}" -ge 20 ]; then
    ok "node >= 20 ($(node -v))"
  else
    warn "node < 20 ($(node -v 2>/dev/null || echo unknown)); desktop/web workspace may fail"
  fi
else
  warn "node not found; desktop/web workspace checks skipped"
fi

if command -v rg >/dev/null 2>&1; then
  ok "rg found"
else
  warn "rg not found; developer search workflow degraded"
fi

if [ -L .venv ]; then
  target="$(readlink .venv || true)"
  case "$target" in
    .venv|./.venv|*/.venv)
      fail ".venv appears self-referential: $target"
      ;;
    *)
      ok ".venv symlink target=$target"
      ;;
  esac
elif [ -d .venv ]; then
  ok ".venv directory present"
else
  warn ".venv missing; run setup before deep runtime tests"
fi

for path in docs/Issue-Checks deploy/README.md deploy/runtime/hermes_profile.sh deploy/hermes-evaluation/hermes_eval_precheck.sh; do
  if [ -e "$path" ]; then
    ok "required path present: $path"
  else
    fail "required path missing: $path"
  fi
done

if git ls-files .env .env.local config.yaml 2>/dev/null | grep -q .; then
  fail "sensitive local config appears tracked"
else
  ok "no root .env/config.yaml tracked"
fi

bash -n deploy/runtime/hermes_profile.sh || fail "syntax: deploy/runtime/hermes_profile.sh"
bash -n deploy/hermes-evaluation/hermes_eval_precheck.sh || fail "syntax: deploy/hermes-evaluation/hermes_eval_precheck.sh"

if [ "$DEEP" = "1" ]; then
  if [ -x .venv/bin/python ]; then
    if .venv/bin/python -m hermes_cli.main --help >/dev/null 2>&1; then
      ok "deep: .venv hermes_cli help works"
    else
      warn "deep: .venv hermes_cli help failed"
    fi
  else
    warn "deep: .venv/bin/python missing; skipping Hermes CLI import check"
  fi
fi

if [ "$failures" -gt 0 ]; then
  echo "[hermes-eval-precheck] FAIL failures=$failures warnings=$warnings"
  exit 1
fi

echo "[hermes-eval-precheck] PASS failures=0 warnings=$warnings"
