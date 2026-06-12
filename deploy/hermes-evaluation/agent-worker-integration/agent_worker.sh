#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$ROOT_DIR/.runtime/hermes-profiles/eval}"
RUN_ROOT="${AGENT_WORKER_RUN_DIR:-$HERMES_HOME/agent-worker-runs}"

usage() {
  cat <<USAGE
Usage:
  bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh check
  bash deploy/hermes-evaluation/agent-worker-integration/agent_worker.sh run --agent codex|claude --workdir <git-repo> --prompt <text> [options]

Options for run:
  --prompt-file <file>   Read prompt from file instead of --prompt.
  --mode plan|write      Default: plan. write requires --allow-write.
  --allow-write          Required for --mode write.
  --dry-run              Print the command without executing it.
  --allow-non-git        Allow running outside a git repository.

Safety defaults:
  - plan mode appends a no-edit instruction.
  - write mode is blocked unless --allow-write is present.
  - command output is saved under HERMES_HOME/agent-worker-runs/.
USAGE
}

shell_join() {
  local out=""
  local arg
  for arg in "$@"; do
    printf -v q '%q' "$arg"
    out+=" $q"
  done
  printf '%s\n' "${out# }"
}

check_one() {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    echo "[OK] $name=$(command -v "$name")"
    "$name" --version 2>/dev/null | head -n 1 || true
  else
    echo "[WARN] $name not found"
  fi
}

cmd="${1:-}"
shift || true

case "$cmd" in
  -h|--help|help|'')
    usage
    exit 0
    ;;
  check)
    echo "[agent-worker] root=$ROOT_DIR"
    echo "[agent-worker] HERMES_HOME=$HERMES_HOME"
    check_one codex
    check_one claude
    check_one git
    exit 0
    ;;
  run)
    ;;
  *)
    echo "[agent-worker] unknown command: $cmd" >&2
    usage >&2
    exit 2
    ;;
esac

AGENT=""
WORKDIR=""
PROMPT=""
PROMPT_FILE=""
MODE="plan"
ALLOW_WRITE=0
DRY_RUN=0
ALLOW_NON_GIT=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --agent) AGENT="${2:-}"; shift 2 ;;
    --workdir) WORKDIR="${2:-}"; shift 2 ;;
    --prompt) PROMPT="${2:-}"; shift 2 ;;
    --prompt-file) PROMPT_FILE="${2:-}"; shift 2 ;;
    --mode) MODE="${2:-}"; shift 2 ;;
    --allow-write) ALLOW_WRITE=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --allow-non-git) ALLOW_NON_GIT=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "[agent-worker] unknown option: $1" >&2; exit 2 ;;
  esac
done

case "$AGENT" in
  codex|claude) ;;
  *) echo "[agent-worker] --agent must be codex or claude" >&2; exit 2 ;;
esac

if [ -z "$WORKDIR" ]; then
  echo "[agent-worker] --workdir is required" >&2
  exit 2
fi
if [ ! -d "$WORKDIR" ]; then
  echo "[agent-worker] workdir does not exist: $WORKDIR" >&2
  exit 2
fi

if [ -n "$PROMPT_FILE" ]; then
  if [ ! -f "$PROMPT_FILE" ]; then
    echo "[agent-worker] prompt file does not exist: $PROMPT_FILE" >&2
    exit 2
  fi
  PROMPT="$(cat "$PROMPT_FILE")"
fi
if [ -z "$PROMPT" ]; then
  echo "[agent-worker] --prompt or --prompt-file is required" >&2
  exit 2
fi

case "$MODE" in
  plan|write) ;;
  *) echo "[agent-worker] --mode must be plan or write" >&2; exit 2 ;;
esac
if [ "$MODE" = "write" ] && [ "$ALLOW_WRITE" != "1" ]; then
  echo "[agent-worker] write mode requires --allow-write" >&2
  exit 2
fi

if [ "$ALLOW_NON_GIT" != "1" ] && ! git -C "$WORKDIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[agent-worker] workdir must be a git repository unless --allow-non-git is set" >&2
  exit 2
fi

if [ "$MODE" = "plan" ]; then
  PROMPT="$PROMPT

Constraint: do not edit files, do not run destructive commands, and return only an implementation plan, risks, and validation commands."
fi

case "$AGENT" in
  codex)
    command -v codex >/dev/null 2>&1 || { echo "[agent-worker] codex not found" >&2; exit 1; }
    CMD=(codex exec "$PROMPT")
    ;;
  claude)
    command -v claude >/dev/null 2>&1 || { echo "[agent-worker] claude not found" >&2; exit 1; }
    if [ "$MODE" = "plan" ]; then
      CMD=(claude -p "$PROMPT" --permission-mode plan --allowedTools Read,Grep,Glob,LS)
    else
      CMD=(claude -p "$PROMPT" --permission-mode default)
    fi
    ;;
esac

mkdir -p "$RUN_ROOT"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$RUN_ROOT/$TS-$AGENT-$MODE.log"

printf '[agent-worker] workdir=%s\n' "$WORKDIR"
printf '[agent-worker] log=%s\n' "$LOG"
printf '[agent-worker] command=%s\n' "$(shell_join "${CMD[@]}")"

if [ "$DRY_RUN" = "1" ]; then
  exit 0
fi

(
  cd "$WORKDIR"
  "${CMD[@]}"
) 2>&1 | tee "$LOG"
