import unittest

from app.metrics import sum_list, word_frequencies, wordcount


class MetricsTest(unittest.TestCase):
    def test_sum_list(self):
        self.assertAlmostEqual(sum_list([1, 2, 3.5]), 6.5)

    def test_sum_list_type(self):
        with self.assertRaises(TypeError):
            sum_list("oops")
        with self.assertRaises(TypeError):
            sum_list([1, "a"])  # non-numeric

    def test_wordcount(self):
        self.assertEqual(wordcount("hello world"), 2)
        self.assertEqual(wordcount("  a   b c  "), 3)

    def test_wordcount_type(self):
        with self.assertRaises(TypeError):
            wordcount(123)

    def test_word_frequencies_repeated(self):
        self.assertEqual(
            word_frequencies("the cat and the cat"),
            {"the": 2, "cat": 2, "and": 1},
        )

    def test_word_frequencies_case_insensitive(self):
        self.assertEqual(word_frequencies("Word word WORD"), {"word": 3})

    def test_word_frequencies_whitespace(self):
        self.assertEqual(word_frequencies("  a\tb\n a "), {"a": 2, "b": 1})

    def test_word_frequencies_keeps_punctuation(self):
        self.assertEqual(word_frequencies("cat, cat"), {"cat,": 1, "cat": 1})

    def test_word_frequencies_empty(self):
        self.assertEqual(word_frequencies(""), {})
        self.assertEqual(word_frequencies("   \t\n"), {})

    def test_word_frequencies_type(self):
        for bad in (None, False, 0, 123, ["word"], []):
            with self.subTest(bad=bad):
                with self.assertRaises(TypeError):
                    word_frequencies(bad)


if __name__ == "__main__":
    unittest.main()
