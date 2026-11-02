import unittest

from app.wordstats import (
    InvalidLimit,
    InvalidText,
    TextTooLong,
    analyze,
)


class AnalyzeTest(unittest.TestCase):
    def test_orders_by_count_desc_then_word(self):
        result = analyze("b a b c a b", 3)
        self.assertEqual(
            result["items"],
            [
                {"word": "b", "count": 3},
                {"word": "a", "count": 2},
                {"word": "c", "count": 1},
            ],
        )
        self.assertEqual(result["total_words"], 6)
        self.assertEqual(result["unique_words"], 3)

    def test_limit_does_not_change_counters(self):
        result = analyze("a b c d", 2)
        self.assertEqual(result["items"], [{"word": "a", "count": 1}, {"word": "b", "count": 1}])
        self.assertEqual(result["total_words"], 4)
        self.assertEqual(result["unique_words"], 4)

    def test_equal_counts_are_alphabetical(self):
        result = analyze("c b a")
        self.assertEqual([item["word"] for item in result["items"]], ["a", "b", "c"])

    def test_case_insensitive_tokens(self):
        result = analyze("Word word WORD")
        self.assertEqual(result["items"], [{"word": "word", "count": 3}])

    def test_empty_text(self):
        result = analyze("   \t\n", 3)
        self.assertEqual(result, {"items": [], "total_words": 0, "unique_words": 0})

    def test_invalid_text(self):
        for bad in (None, 123, False, ["word"]):
            with self.subTest(bad=bad):
                with self.assertRaises(InvalidText):
                    analyze(bad)

    def test_text_too_long(self):
        with self.assertRaises(TextTooLong):
            analyze("a" * 10001)

    def test_invalid_limit(self):
        for bad in (0, 101, 1.5, True, "3", None):
            with self.subTest(bad=bad):
                with self.assertRaises(InvalidLimit):
                    analyze("a", bad)


if __name__ == "__main__":
    unittest.main()
