"""Ask five questions from QUESTIONS.md against local Ollama, save answers.
Standard library only; read-only context from demo/.
"""
import json
import re
import time
import urllib.request
from pathlib import Path


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_questions(md: str) -> list[str]:
    lines = md.splitlines()
    qs = []
    for line in lines:
        m = re.match(r"\s*\d+\.\s+(.*)$", line)
        if m:
            qs.append(m.group(1).strip())
    return qs


def chat_ollama(model: str, messages: list[dict], options: dict) -> dict:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": options,
    }
    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.load(resp)


def main():
    root = Path(__file__).resolve().parent
    demo = root / "demo"
    records = root / "records"
    records.mkdir(exist_ok=True)

    system_prompt = read_utf8(demo / "repo-system.txt")
    questions = load_questions(read_utf8(root / "QUESTIONS.md"))

    # Read-only context: combine key demo files
    context_parts = []
    for rel in [
        "README.md",
        "Makefile",
        "service.py",
        "test_service.py",
    ]:
        p = demo / rel
        if p.exists():
            context_parts.append(f"===== {rel} =====\n" + read_utf8(p))
    context = "\n\n".join(context_parts)

    model = "qwen3.5:4b"  # test model; agent model is configured in OpenCode
    options = {"temperature": 0.2, "seed": 42, "num_ctx": 4096, "num_predict": 512}

    results = []
    for idx, q in enumerate(questions, start=1):
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": context + f"\n\nВопрос {idx}: {q}",
            },
        ]
        started = time.perf_counter()
        try:
            answer = chat_ollama(model, messages, options)
        except Exception as exc:
            results.append({
                "question": q,
                "error": str(exc),
            })
            continue
        results.append({
            "question": q,
            "response": answer,
            "wall_seconds": time.perf_counter() - started,
            "load_seconds": answer.get("load_duration", 0) / 1e9,
            "total_seconds": answer.get("total_duration", 0) / 1e9,
        })

    out = records / "questions_answers.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Saved:", out)


if __name__ == "__main__":
    main()
