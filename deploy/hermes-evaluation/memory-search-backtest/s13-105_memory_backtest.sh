#!/usr/bin/env bash
set -euo pipefail

CMD="${1:-inspect}"
OLD_NANOBOT_HOME="${OLD_NANOBOT_HOME:-/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot}"
HERMES_HOME="${HERMES_HOME:-/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval}"

case "$CMD" in
  inspect)
    python3 - <<'PY'
import json
import os
from pathlib import Path

old_home = Path(os.environ.get("OLD_NANOBOT_HOME", "/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot"))
hermes_home = Path(os.environ.get("HERMES_HOME", "/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval"))

print("[s13.105] old_nanobot_home=", old_home)
print("[s13.105] hermes_home=", hermes_home)
print("[s13.105] mode=read_only")
print()

sessions = old_home / "sessions"
if not sessions.exists():
    raise SystemExit(f"missing sessions dir: {sessions}")

print("[sessions]")
for path in sorted(sessions.glob("*.jsonl")):
    try:
        line_count = sum(1 for _ in path.open("r", encoding="utf-8"))
    except Exception as exc:
        print(f"- {path.name}: ERROR {exc}")
        continue
    print(f"- {path.name}: {line_count} lines")
print()

primary = sessions / "telegram_8464732775.jsonl"
secondary = sessions / "cron_morning_market_brief.jsonl"

def scan(path: Path, terms, limit=8):
    hits = []
    if not path.exists():
        return hits
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            try:
                item = json.loads(line)
            except Exception:
                continue
            if item.get("_type") == "metadata":
                continue
            content = item.get("content") or ""
            if any(term in content for term in terms):
                text = " ".join(content.split())
                hits.append((lineno, item.get("timestamp", ""), item.get("role", ""), text[:280]))
    return hits[-limit:]

print("[primary_fixture: travel platform / evidence card]")
for lineno, ts, role, text in scan(primary, ["携程", "US.TCOM", "体验型消费", "出境游", "Futu Data API"], 10):
    print(f"- line={lineno} ts={ts} role={role} text={text}")
print()

print("[secondary_fixture: morning brief]")
for lineno, ts, role, text in scan(secondary, ["早盘简报", "阿里", "百度", "隔夜美股中概股"], 8):
    print(f"- line={lineno} ts={ts} role={role} text={text}")
print()

print("[hermes_memory_files]")
for rel in ["memories/MEMORY.md", "memories/USER.md", "workspace/chimera-history/chimera-history-summary.md"]:
    path = hermes_home / rel
    if path.exists():
        print(f"- {rel}: exists size={path.stat().st_size}")
    else:
        print(f"- {rel}: missing")
print()

print("[secret_policy]")
print("- skipped: .env, secrets.env, config.json, backup config/secret files")
print("- skipped: docs/Issue-Checks as answer source")
PY
    ;;
  prompt)
    cat "$(dirname "$0")/s13-105-primary-vague.prompt.txt"
    ;;
  *)
    echo "usage: $0 [inspect|prompt]" >&2
    exit 2
    ;;
esac
