"""Compare collected answers with simple etalons heuristically.
Writes a markdown report to records/comparison.md.
Standard library only.
"""
from __future__ import annotations
import json
from pathlib import Path


def load_answers_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data


def pass_criteria(idx: int, content: str) -> bool:
    c = content.lower()
    if idx == 1:
        return ("make test" in c) and ("unittest" in c or "python3 -m unittest" in c)
    if idx == 2:
        return ("valueerror" in c) and ("empty name" in c)
    if idx == 3:
        return ("не реализ" in c) or ("нет" in c and "unsubscribe" in c)
    if idx == 4:
        return ("нет" in c and "ci" in c) or ("сведений" in c and "нет" in c)
    if idx == 5:
        return ("не сохраня" in c) and ("памяти" in c or "subscribers" in c)
    return False


def main():
    root = Path(__file__).resolve().parent
    records = root / "records"
    out = records / "comparison.md"
    qa_path = records / "questions_answers.json"
    if not qa_path.exists():
        out.write_text("No questions_answers.json found. Run run_questions.py first.\n", encoding="utf-8")
        print("Missing questions_answers.json")
        return
    data = load_answers_json(qa_path)
    lines = ["# Сравнение ответов", ""]
    passed = 0
    for i, item in enumerate(data, start=1):
        q = item.get("question", "")
        resp = item.get("response") or {}
        content = (resp.get("message") or {}).get("content", "")
        ok = pass_criteria(i, content)
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        lines.append(f"{i}. {status}: {q}")
        lines.append("")
        lines.append("Ответ модели:")
        lines.append("")
        lines.append(content.strip())
        lines.append("")
    lines.append("")
    lines.append(f"Итог: {passed}/{len(data)} совпадений по критериям.")
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Saved:", out)


if __name__ == "__main__":
    main()
