def sum_list(nums):
    """Return the sum of numbers in the list. Raises TypeError if non-numeric."""
    if not isinstance(nums, list):
        raise TypeError("nums must be a list")
    total = 0.0
    for x in nums:
        if not isinstance(x, (int, float)):
            raise TypeError("all elements must be numbers")
        total += x
    return total


def wordcount(text: str) -> int:
    """Count words separated by whitespace."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return len([w for w in text.split() if w])


def word_frequencies(text: str) -> dict:
    """Count whitespace-separated words, case-insensitively."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    counts = {}
    for token in text.split():
        key = token.lower()
        counts[key] = counts.get(key, 0) + 1
    return counts
