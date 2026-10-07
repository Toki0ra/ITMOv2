#!/usr/bin/env python3
"""Minimal MCP-like stdin/stdout loop for demo: supports calc_sum and wordcount.
This is a toy server responding to simple JSON requests: {"tool": ..., "input": ...}.
"""
import json
import sys


def handle(req):
    tool = req.get("tool")
    if tool == "calc_sum":
        data = req.get("input")
        if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
            return {"error": "calc_sum expects a JSON list of numbers"}
        return {"ok": True, "result": sum(data)}
    if tool == "wordcount":
        data = req.get("input")
        if not isinstance(data, str):
            return {"error": "wordcount expects a string"}
        words = [w for w in data.split() if w]
        return {"ok": True, "result": len(words)}
    return {"error": f"unknown tool: {tool}"}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception as e:
            print(json.dumps({"error": f"invalid json: {e}"}), flush=True)
            continue
        resp = handle(req)
        print(json.dumps(resp, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
