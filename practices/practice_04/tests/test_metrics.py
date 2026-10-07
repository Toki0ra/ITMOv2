import unittest

from app.metrics import sum_list, wordcount


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


if __name__ == "__main__":
    unittest.main()
