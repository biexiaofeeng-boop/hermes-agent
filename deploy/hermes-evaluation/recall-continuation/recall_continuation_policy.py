#!/usr/bin/env python3
"""Install a compact recall-continuation behavior rule into Hermes MEMORY.md."""
from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_MEMORY = Path("/Users/sourcefire/X-lab/chimera-hermes-agent/.runtime/hermes-profiles/eval/memories/MEMORY.md")
POLICY = (
    "Recall-continuation rule: when the user asks to recall old Scout/鹰眼 history and then sends "
    "a short clarification such as '是携程', '是那个', '继续', or another brief entity cue, treat it "
    "as a continuation of the previous recall task. Search the Chimera memory cards/archive first, "
    "reply with only the delta or corrected answer, and do not repeat the previous disclaimer or a "
    "generic reconstructed analysis unless no archive evidence is found."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-path", default=str(DEFAULT_MEMORY))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    path = Path(args.memory_path)
    if not path.exists():
        raise SystemExit(f"missing memory file: {path}")
    content = path.read_text(encoding="utf-8")
    if POLICY in content:
        print(f"policy=already-present path={path}")
        return 0
    if not args.write:
        print(POLICY)
        print(f"dry_run=1 target={path}")
        return 0
    backup = path.with_suffix(path.suffix + ".bak.s13-107")
    if not backup.exists():
        backup.write_text(content, encoding="utf-8")
    sep = "\n§\n" if content.strip() else ""
    path.write_text(content.rstrip() + sep + POLICY + "\n", encoding="utf-8")
    print(f"policy=installed path={path} backup={backup}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
