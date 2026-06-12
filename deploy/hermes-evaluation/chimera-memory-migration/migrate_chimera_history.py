#!/usr/bin/env python3
"""Migrate Chimera Core history into a Hermes eval profile safely.

Policy:
- Do not import raw chat history into Hermes MEMORY.md.
- Generate an archive summary under HERMES_HOME/workspace/chimera-history/.
- Append only concise, durable Scout/finance/intel operating facts to MEMORY.md.
- Do not alter USER.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

ENTRY_DELIMITER = "\n§\n"

FOCUS_KEYWORDS = [
    "阿里", "Alibaba", "BABA", "9988", "09988",
    "百度", "Baidu", "BIDU", "9888", "09888",
    "携程", "Ctrip", "TCOM",
    "港股", "美股", "中概", "市场", "情报", "金融", "交易", "仓位", "游击", "核心仓",
    "证据卡", "Evidence", "Futu", "截图", "L2-S", "策略", "风险",
]

TICKER_PATTERNS = [
    r"HK\.\d{5}", r"US\.[A-Z]{1,6}", r"\b[A-Z]{2,6}\b", r"\b\d{4}\.HK\b", r"\b\d{5}\b"
]

NOISE_PREFIXES = (
    "已并入当前议题上下文",
    "[image:",
    "展开日志",
)

DURABLE_MEMORY_ENTRIES = [
    "Migrated Chimera history summary is stored under HERMES_HOME/workspace/chimera-history. Use it as an archive reference for Scout/鹰眼 finance and intelligence continuity instead of loading raw chat history into every prompt.",
    "Scout/鹰眼 historical operating style from Chimera: finance and intelligence answers should prefer conclusion -> evidence card -> action/risk plan, with explicit source/time/confidence labels when market data or screenshots are used.",
    "Chimera finance continuity includes recurring focus on Alibaba/BABA/9988, Baidu/BIDU/9888, Ctrip/TCOM, HK/US China tech, barbell-style core plus swing positioning, cash flexibility, and evidence-gated price/strategy discussion.",
]

DEFAULT_CHIMERA_SESSIONS = Path(
    os.environ.get(
        "CHIMERA_SESSIONS",
        "/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot/sessions",
    )
)
DEFAULT_HERMES_HOME = Path(os.environ.get("HERMES_HOME", ".runtime/hermes-profiles/eval"))

@dataclass
class Message:
    source: str
    role: str
    content: str
    timestamp: str


def parse_jsonl(path: Path) -> list[Message]:
    messages: list[Message] = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("_type") == "metadata":
                continue
            role = str(obj.get("role") or "").strip()
            content = str(obj.get("content") or "").strip()
            timestamp = str(obj.get("timestamp") or "").strip()
            if role not in {"user", "assistant", "system", "tool"} or not content:
                continue
            messages.append(Message(path.name, role, content, timestamp))
    return messages


def is_focus(content: str) -> bool:
    return any(k.lower() in content.lower() for k in FOCUS_KEYWORDS)


def is_noise(content: str) -> bool:
    stripped = content.strip()
    return any(stripped.startswith(p) for p in NOISE_PREFIXES)


def excerpt(text: str, limit: int = 420) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def extract_tickers(messages: Iterable[Message]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for m in messages:
        for pat in TICKER_PATTERNS:
            for found in re.findall(pat, m.content):
                if found in {"INFO", "DEBUG", "ERROR", "PASS", "FAIL", "JSON", "HTTP", "API"}:
                    continue
                counts[found] += 1
        aliases = {
            "阿里": "Alibaba/BABA/9988",
            "Alibaba": "Alibaba/BABA/9988",
            "BABA": "Alibaba/BABA/9988",
            "百度": "Baidu/BIDU/9888",
            "Baidu": "Baidu/BIDU/9888",
            "BIDU": "Baidu/BIDU/9888",
            "携程": "Ctrip/TCOM",
            "Ctrip": "Ctrip/TCOM",
            "TCOM": "Ctrip/TCOM",
        }
        lower = m.content.lower()
        for key, label in aliases.items():
            if key.lower() in lower:
                counts[label] += 1
    return counts


def date_key(ts: str) -> str:
    return ts[:10] if len(ts) >= 10 else "unknown"


def build_archive(messages: list[Message], source_dir: Path) -> str:
    focus = [m for m in messages if is_focus(m.content) and not is_noise(m.content)]
    by_source = Counter(m.source for m in messages)
    by_role = Counter(m.role for m in messages)
    by_day = Counter(date_key(m.timestamp) for m in messages)
    tickers = extract_tickers(focus)

    user_focus = [m for m in focus if m.role == "user"][-30:]
    assistant_focus = [m for m in focus if m.role == "assistant"][-30:]

    themes = [
        ("Finance/market intelligence", ["金融", "市场", "港股", "美股", "中概", "交易", "仓位"]),
        ("Evidence-gated analysis", ["证据卡", "Evidence", "Sources", "Confidence", "L2-S", "截图", "Futu"]),
        ("Portfolio/positioning", ["核心仓", "游击", "现金", "做T", "barbell", "哑铃", "仓位"]),
        ("Ops/tooling continuity", ["执行", "工具", "exec", "cron", "gateway", "skill"]),
    ]
    theme_counts = []
    for label, keys in themes:
        count = sum(1 for m in focus if any(k.lower() in m.content.lower() for k in keys))
        theme_counts.append((label, count))

    lines: list[str] = []
    lines.append("# Chimera History Migration Summary")
    lines.append("")
    lines.append(f"Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Source sessions: `{source_dir}`")
    lines.append("")
    lines.append("## Corpus Stats")
    lines.append("")
    lines.append(f"- Total parsed messages: {len(messages)}")
    lines.append(f"- Focus messages: {len(focus)}")
    lines.append("- Sources: " + ", ".join(f"{k}={v}" for k, v in sorted(by_source.items())))
    lines.append("- Roles: " + ", ".join(f"{k}={v}" for k, v in sorted(by_role.items())))
    if by_day:
        lines.append(f"- Date range: {min(by_day)} -> {max(by_day)}")
    lines.append("")
    lines.append("## Dominant Themes")
    lines.append("")
    for label, count in theme_counts:
        lines.append(f"- {label}: {count} focus messages")
    lines.append("")
    lines.append("## Frequent Symbols / Entities")
    lines.append("")
    for sym, count in tickers.most_common(30):
        lines.append(f"- {sym}: {count}")
    lines.append("")
    lines.append("## Durable Operating Memory Candidates")
    lines.append("")
    for entry in DURABLE_MEMORY_ENTRIES:
        lines.append(f"- {entry}")
    lines.append("")
    lines.append("## Recent User Focus Excerpts")
    lines.append("")
    for m in user_focus:
        lines.append(f"- {m.timestamp} `{m.source}`: {excerpt(m.content)}")
    lines.append("")
    lines.append("## Recent Assistant Finance/Intel Excerpts")
    lines.append("")
    for m in assistant_focus:
        lines.append(f"- {m.timestamp} `{m.source}`: {excerpt(m.content)}")
    lines.append("")
    lines.append("## Migration Policy")
    lines.append("")
    lines.append("- Raw Chimera chat history was not copied into Hermes MEMORY.md.")
    lines.append("- Hermes MEMORY.md receives only short stable facts that improve continuity.")
    lines.append("- Full archive summary remains in workspace for explicit lookup and future RAG/indexing.")
    lines.append("- USER.md is intentionally not modified by this migration.")
    lines.append("")
    return "\n".join(lines)


def load_memory_entries(path: Path) -> list[str]:
    if not path.exists() or not path.read_text(encoding="utf-8").strip():
        return []
    return [p.strip() for p in path.read_text(encoding="utf-8").split(ENTRY_DELIMITER) if p.strip()]


def write_memory_entries(path: Path, entries: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ENTRY_DELIMITER.join(entries).rstrip() + "\n", encoding="utf-8")
    path.chmod(0o600)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chimera-sessions", type=Path, default=DEFAULT_CHIMERA_SESSIONS)
    parser.add_argument("--hermes-home", type=Path, default=DEFAULT_HERMES_HOME)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-empty", action="store_true", help="Write an empty archive if no source messages are found.")
    args = parser.parse_args()

    source_files = [
        args.chimera_sessions / "telegram_8464732775.jsonl",
        args.chimera_sessions / "cron_morning_market_brief.jsonl",
    ]
    messages: list[Message] = []
    for path in source_files:
        if path.exists():
            messages.extend(parse_jsonl(path))

    if not messages and not args.allow_empty:
        print(json.dumps({
            "dry_run": args.dry_run,
            "error": "no Chimera messages found",
            "chimera_sessions": str(args.chimera_sessions),
            "checked_files": [str(p) for p in source_files],
            "hint": "Pass --chimera-sessions, set CHIMERA_SESSIONS, or use --allow-empty intentionally.",
        }, ensure_ascii=False, indent=2))
        return 2

    archive_dir = args.hermes_home / "workspace" / "chimera-history"
    archive_path = archive_dir / "chimera-history-summary.md"
    backup_dir = args.hermes_home / "backups" / ("chimera-history-migration-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    memory_path = args.hermes_home / "memories" / "MEMORY.md"

    summary = build_archive(messages, args.chimera_sessions)

    existing_entries = load_memory_entries(memory_path)
    merged_entries = list(existing_entries)
    for entry in DURABLE_MEMORY_ENTRIES:
        if entry not in merged_entries:
            merged_entries.append(entry)

    print(json.dumps({
        "dry_run": args.dry_run,
        "messages": len(messages),
        "archive_path": str(archive_path),
        "memory_path": str(memory_path),
        "memory_entries_before": len(existing_entries),
        "memory_entries_after": len(merged_entries),
        "backup_dir": str(backup_dir),
        "user_md_modified": False,
    }, ensure_ascii=False, indent=2))

    if args.dry_run:
        return 0

    backup_dir.mkdir(parents=True, exist_ok=True)
    if memory_path.exists():
        shutil.copy2(memory_path, backup_dir / "MEMORY.md.before")
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(summary, encoding="utf-8")
    archive_path.chmod(0o600)
    write_memory_entries(memory_path, merged_entries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
