#!/usr/bin/env python3
"""Simple runner that validates a trivial rule and prints a result.
Acts as an "automatic check" example: ensures presentation exists and lists MCP tools.
"""
from pathlib import Path
import json


def main():
    root = Path(__file__).resolve().parent
    ok = True
    notes = []
    # Check presentation files exist
    for rel in ("presentation.pdf", "presentation.pptx"):
        p = root / rel
        if not p.exists():
            ok = False
            notes.append(f"missing {rel}")
    # Check MCP server script
    mcp = root / ".opencode" / "mcp" / "calc_server.py"
    if not mcp.exists():
        ok = False
        notes.append("missing MCP calc_server")
    # List skill directory
    skill = root / ".opencode" / "skills" / "repo-assist" / "SKILL.md"
    if not skill.exists():
        ok = False
        notes.append("missing repo-assist skill")
    result = {
        "ok": ok,
        "notes": notes,
        "mcp_tools": ["calc_sum", "wordcount"],
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
