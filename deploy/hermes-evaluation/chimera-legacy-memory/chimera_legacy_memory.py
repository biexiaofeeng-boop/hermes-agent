#!/usr/bin/env python3
"""Read-only Chimera legacy memory search and card export helper.

This script intentionally reads only old Nanobot session JSONL files. It does
not read .env, secrets.env, config.json, or backup config files.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List

DEFAULT_OLD_NANOBOT_HOME = Path(
    "/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home/.nanobot"
)
DEFAULT_HERMES_HOME = Path(
    "/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval"
)

POINTER_TEXT = (
    "Chimera high-value memory cards are stored under "
    "HERMES_HOME/workspace/chimera-history/chimera-memory-cards.md. "
    "Use them before generic inference when the user asks to recall old Scout/鹰眼 "
    "finance or intelligence discussions."
)


@dataclass(frozen=True)
class Message:
    file: str
    line: int
    role: str
    timestamp: str
    content: str


@dataclass(frozen=True)
class CardSpec:
    card_id: str
    title: str
    terms: tuple[str, ...]
    recall_cues: tuple[str, ...]
    stable_memory: str
    source_files: tuple[str, ...] = ()


CARDS: tuple[CardSpec, ...] = (
    CardSpec(
        card_id="finance.tcom.travel-platform",
        title="Ctrip / US.TCOM travel-platform thesis",
        terms=("携程", "US.TCOM", "体验型消费", "出境游", "Futu Data API"),
        recall_cues=("旅游出行平台", "体验型消费", "出境游修复", "截图估值线索", "携程", "TCOM"),
        stable_memory=(
            "Old Scout/鹰眼 discussion treated Ctrip/US.TCOM as a travel-platform "
            "candidate, not generic consumption. The thesis linked experience consumption, "
            "outbound travel margin recovery, clear OTA competitive structure, user screenshot "
            "context, and Futu market data. The old answer used core conclusion -> evidence card "
            "-> action/risk plan."
        ),
        source_files=("telegram_8464732775.jsonl",),
    ),
    CardSpec(
        card_id="finance.morning-brief.alibaba-baidu",
        title="Morning market brief for Alibaba/Baidu",
        terms=("早盘简报", "阿里", "百度", "隔夜美股中概股"),
        recall_cues=("早盘简报", "阿里", "百度", "隔夜中概", "白天没法盯盘"),
        stable_memory=(
            "Old recurring Scout task asked to pull Alibaba and Baidu premarket/market data, "
            "check overnight US-listed China ADR performance, and send an execution report. "
            "This served the user's school/work constraint: keep watch while the user cannot "
            "continuously monitor the market."
        ),
        source_files=("cron_morning_market_brief.jsonl",),
    ),
    CardSpec(
        card_id="finance.lenovo-ai-pc",
        title="Lenovo AI PC / edge execution thesis",
        terms=("联想", "AI PC", "ThinkPad", "4000股", "10.49", "12.56"),
        recall_cues=("联想", "AI PC", "端侧AI", "ThinkPad", "开发机", "游戏机"),
        stable_memory=(
            "Old Scout discussion recorded the user's Lenovo thesis: AI model execution is moving "
            "toward local/edge devices, creating PC refresh demand for developers, gamers, and "
            "enterprise users. The discussion contrasted long-term Buffett/Munger style holding "
            "with short-term swing realization."
        ),
        source_files=("telegram_8464732775.jsonl",),
    ),
    CardSpec(
        card_id="finance.msft-mispricing",
        title="Microsoft valuation mispricing / AI enterprise thesis",
        terms=("微软", "MSFT", "市盈率", "Forward PE", "439.8"),
        recall_cues=("微软", "MSFT", "阶段性低位", "AI资本开支", "企业级AI", "建仓"),
        stable_memory=(
            "Old Scout discussion treated Microsoft as an AI enterprise infrastructure and application "
            "mispricing case. The thesis was that market fear around AI capex and SaaS disruption "
            "could be short-sighted because enterprise customers need integrated, compliant AI solutions."
        ),
        source_files=("telegram_8464732775.jsonl",),
    ),
)


def old_home_from_args(args: argparse.Namespace) -> Path:
    return Path(args.old_nanobot_home or os.environ.get("OLD_NANOBOT_HOME") or DEFAULT_OLD_NANOBOT_HOME)


def hermes_home_from_args(args: argparse.Namespace) -> Path:
    return Path(args.hermes_home or os.environ.get("HERMES_HOME") or DEFAULT_HERMES_HOME)


def hermes_state_db_from_args(args: argparse.Namespace) -> Path:
    return Path(args.state_db) if getattr(args, "state_db", "") else hermes_home_from_args(args) / "state.db"


def session_dir(old_home: Path) -> Path:
    return old_home / "sessions"


def iter_session_paths(old_home: Path) -> Iterable[Path]:
    root = session_dir(old_home)
    if not root.exists():
        raise SystemExit(f"missing sessions dir: {root}")
    yield from sorted(root.glob("*.jsonl"))


def iter_messages(old_home: Path) -> Iterable[Message]:
    for path in iter_session_paths(old_home):
        with path.open("r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, 1):
                try:
                    item = json.loads(raw)
                except Exception:
                    continue
                if item.get("_type") == "metadata":
                    continue
                content = item.get("content") or ""
                if not content:
                    continue
                yield Message(
                    file=path.name,
                    line=line_no,
                    role=str(item.get("role") or ""),
                    timestamp=str(item.get("timestamp") or ""),
                    content=" ".join(content.split()),
                )


def score_message(message: Message, terms: list[str]) -> int:
    text = message.content.lower()
    score = 0
    for term in terms:
        t = term.lower()
        if t and t in text:
            score += text.count(t)
    return score


def search_messages(old_home: Path, terms: list[str], limit: int, source_files: tuple[str, ...] = ()) -> list[tuple[int, Message]]:
    scored: list[tuple[int, Message]] = []
    allowed = set(source_files)
    for msg in iter_messages(old_home):
        if allowed and msg.file not in allowed:
            continue
        score = score_message(msg, terms)
        if score:
            scored.append((score, msg))
    scored.sort(key=lambda item: (item[0], item[1].timestamp, item[1].file, item[1].line), reverse=True)
    return scored[:limit]


def format_excerpt(msg: Message, max_chars: int = 420) -> str:
    text = msg.content
    if len(text) > max_chars:
        text = text[: max_chars - 1] + "…"
    return f"- `{msg.file}:{msg.line}` `{msg.timestamp}` `{msg.role}`: {text}"


def inspect(args: argparse.Namespace) -> int:
    old_home = old_home_from_args(args)
    hermes_home = hermes_home_from_args(args)
    print(f"old_nanobot_home={old_home}")
    print(f"hermes_home={hermes_home}")
    print("mode=read_only")
    print("secret_policy=skip .env,secrets.env,config.json,backup configs")
    print()
    print("[sessions]")
    for path in iter_session_paths(old_home):
        count = sum(1 for _ in path.open("r", encoding="utf-8"))
        print(f"- {path.name}: {count} lines")
    print()
    print("[cards]")
    for card in CARDS:
        hits = search_messages(old_home, list(card.terms), limit=3, source_files=card.source_files)
        src = ','.join(card.source_files) if card.source_files else '*'
        print(f"- {card.card_id}: hits={len(hits)} source={src} terms={','.join(card.terms)}")
    print()
    print("[memory_targets]")
    for rel in ("memories/MEMORY.md", "workspace/chimera-history/chimera-memory-cards.md"):
        path = hermes_home / rel
        print(f"- {rel}: {'exists' if path.exists() else 'missing'}")
    return 0


def search(args: argparse.Namespace) -> int:
    old_home = old_home_from_args(args)
    terms = [t for t in args.query.split() if t.strip()]
    if not terms:
        raise SystemExit("query must contain at least one term")
    for score, msg in search_messages(old_home, terms, args.limit):
        print(f"score={score}")
        print(format_excerpt(msg, max_chars=args.max_chars))
    return 0


def build_cards(old_home: Path, max_hits: int) -> str:
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines: list[str] = [
        "# Chimera Legacy Memory Cards",
        "",
        f"Generated at: {generated}",
        f"Source: `{old_home / 'sessions'}`",
        "",
        "These cards are compact recall anchors for old Chimera/Nanobot runtime sessions.",
        "They are not a replacement for source evidence. Use the cited session lines when exact recall matters.",
        "",
    ]
    for card in CARDS:
        hits = search_messages(old_home, list(card.terms), max_hits, source_files=card.source_files)
        lines.extend([
            f"## {card.title}",
            "",
            f"ID: `{card.card_id}`",
            "",
            "Recall cues:",
            "",
        ])
        lines.extend(f"- {cue}" for cue in card.recall_cues)
        lines.extend([
            "",
            "Stable memory:",
            "",
            card.stable_memory,
            "",
            "Evidence excerpts:",
            "",
        ])
        if hits:
            for _score, msg in hits:
                lines.append(format_excerpt(msg))
        else:
            lines.append("- No matching legacy session excerpt found by current terms.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_card_session_content(old_home: Path, card: CardSpec, max_hits: int = 2) -> str:
    hits = search_messages(old_home, list(card.terms), max_hits, source_files=card.source_files)
    lines = [
        f"Chimera legacy memory card: {card.title}",
        f"Card ID: {card.card_id}",
        "",
        "Recall cues:",
        *[f"- {cue}" for cue in card.recall_cues],
        "",
        "Stable memory:",
        card.stable_memory,
        "",
        "Best evidence excerpts:",
    ]
    if hits:
        lines.extend(format_excerpt(msg, max_chars=700) for _score, msg in hits)
    else:
        lines.append("- No matching legacy session excerpt found by current terms.")
    return "\n".join(lines)


def export_cards(args: argparse.Namespace) -> int:
    old_home = old_home_from_args(args)
    hermes_home = hermes_home_from_args(args)
    output = Path(args.output) if args.output else hermes_home / "workspace/chimera-history/chimera-memory-cards.md"
    text = build_cards(old_home, args.max_hits)
    if not args.write:
        sys.stdout.write(text)
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"wrote={output}")
    return 0


def import_cards_session(args: argparse.Namespace) -> int:
    old_home = old_home_from_args(args)
    db_path = hermes_state_db_from_args(args)
    if not db_path.exists():
        raise SystemExit(f"missing Hermes state.db: {db_path}")

    session_prefix = "chimera_legacy_card:"
    backup = db_path.with_suffix(db_path.suffix + ".bak.s13-108")
    if args.write and not backup.exists():
        shutil.copy2(db_path, backup)

    rows = []
    base_ts = datetime.now(timezone.utc).timestamp()
    for index, card in enumerate(CARDS):
        session_id = f"{session_prefix}{card.card_id}"
        content = build_card_session_content(old_home, card, max_hits=args.max_hits)
        rows.append((session_id, card, content, base_ts + index))

    if not args.write:
        print(f"dry_run=1 state_db={db_path}")
        for session_id, card, content, _ts in rows:
            print(f"session_id={session_id} title={card.title} chars={len(content)}")
        return 0

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        old_ids = [
            row[0]
            for row in conn.execute(
                "SELECT id FROM sessions WHERE id LIKE ?",
                (f"{session_prefix}%",),
            ).fetchall()
        ]
        for sid in old_ids:
            conn.execute("DELETE FROM messages WHERE session_id = ?", (sid,))
            conn.execute("DELETE FROM sessions WHERE id = ?", (sid,))

        for session_id, card, content, ts in rows:
            conn.execute(
                """
                INSERT INTO sessions (
                    id, source, user_id, model, started_at, ended_at,
                    end_reason, message_count, tool_call_count, title
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    "chimera_legacy",
                    "sourcefire",
                    "chimera-legacy-memory-card",
                    ts,
                    ts,
                    "imported",
                    2,
                    0,
                    f"Chimera legacy memory: {card.title}",
                ),
            )
            conn.execute(
                """
                INSERT INTO messages (session_id, role, content, timestamp, active)
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    session_id,
                    "user",
                    f"Recall old Chimera/Scout memory card: {card.title}. Cues: {', '.join(card.recall_cues)}",
                    ts,
                ),
            )
            conn.execute(
                """
                INSERT INTO messages (session_id, role, content, timestamp, active)
                VALUES (?, ?, ?, ?, 1)
                """,
                (session_id, "assistant", content, ts + 0.001),
            )
        conn.commit()

    print(f"imported={len(rows)} state_db={db_path} backup={backup}")
    for session_id, card, _content, _ts in rows:
        print(f"- {session_id} :: {card.title}")
    return 0


def install_pointer(args: argparse.Namespace) -> int:
    hermes_home = hermes_home_from_args(args)
    memory_path = Path(args.memory_path) if args.memory_path else hermes_home / "memories/MEMORY.md"
    if not memory_path.exists():
        raise SystemExit(f"missing MEMORY.md: {memory_path}")
    content = memory_path.read_text(encoding="utf-8")
    if POINTER_TEXT in content:
        print(f"pointer=already-present path={memory_path}")
        return 0
    if not args.write:
        print(POINTER_TEXT)
        print(f"dry_run=1 target={memory_path}")
        return 0
    backup = memory_path.with_suffix(memory_path.suffix + ".bak.s13-106")
    if not backup.exists():
        backup.write_text(content, encoding="utf-8")
    sep = "\n§\n" if content.strip() else ""
    memory_path.write_text(content.rstrip() + sep + POINTER_TEXT + "\n", encoding="utf-8")
    print(f"pointer=installed path={memory_path} backup={backup}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chimera legacy memory archive helper")
    parser.add_argument("--old-nanobot-home", default="", help="Old .nanobot home; defaults to chimera-core-prod profile")
    parser.add_argument("--hermes-home", default="", help="Hermes profile home; defaults to chimera-hermes-agent eval profile")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("inspect", help="Read-only fixture inspection")

    p_search = sub.add_parser("search", help="Search old Nanobot sessions")
    p_search.add_argument("--query", required=True, help="Whitespace-separated OR terms")
    p_search.add_argument("--limit", type=int, default=10)
    p_search.add_argument("--max-chars", type=int, default=420)

    p_export = sub.add_parser("export-cards", help="Generate compact Chimera memory cards")
    p_export.add_argument("--output", default="")
    p_export.add_argument("--max-hits", type=int, default=4)
    p_export.add_argument("--write", action="store_true")

    p_import = sub.add_parser("import-cards-session", help="Import memory cards as synthetic Hermes sessions for session_search")
    p_import.add_argument("--state-db", default="")
    p_import.add_argument("--max-hits", type=int, default=2)
    p_import.add_argument("--write", action="store_true")

    p_ptr = sub.add_parser("install-pointer", help="Add card index pointer to MEMORY.md")
    p_ptr.add_argument("--memory-path", default="")
    p_ptr.add_argument("--write", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "inspect":
        return inspect(args)
    if args.command == "search":
        return search(args)
    if args.command == "export-cards":
        return export_cards(args)
    if args.command == "import-cards-session":
        return import_cards_session(args)
    if args.command == "install-pointer":
        return install_pointer(args)
    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
