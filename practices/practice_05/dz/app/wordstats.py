"""Pure word-statistics logic for the Word Frequency Explorer."""

MAX_TEXT_LENGTH = 10000
MIN_LIMIT = 1
MAX_LIMIT = 100
DEFAULT_LIMIT = 3


class AnalysisError(ValueError):
    """Base error carrying a contract error code and HTTP status."""

    code = "invalid_request"
    status = 400


class InvalidText(AnalysisError):
    code = "invalid_text"


class InvalidLimit(AnalysisError):
    code = "invalid_limit"


class TextTooLong(AnalysisError):
    code = "text_too_long"
    status = 413


def analyze(text, limit=DEFAULT_LIMIT):
    """Return word frequencies ordered by count desc, then word asc."""
    if not isinstance(text, str):
        raise InvalidText("Текст должен быть строкой")
    if len(text) > MAX_TEXT_LENGTH:
        raise TextTooLong(f"Текст длиннее {MAX_TEXT_LENGTH} символов")
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise InvalidLimit("Количество слов должно быть целым числом")
    if not MIN_LIMIT <= limit <= MAX_LIMIT:
        raise InvalidLimit(f"Количество слов должно быть от {MIN_LIMIT} до {MAX_LIMIT}")

    tokens = text.split()
    counts = {}
    for token in tokens:
        key = token.lower()
        counts[key] = counts.get(key, 0) + 1

    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    items = [{"word": word, "count": count} for word, count in ordered[:limit]]
    return {
        "items": items,
        "total_words": len(tokens),
        "unique_words": len(counts),
    }
