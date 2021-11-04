import unittest
from shingle import Shingle
import compare_sets


class TestSuite(unittest.TestCase):
    def test_jaccard_similarity(self):
        shingle1 = Shingle(4, 'tests/text_1.txt')
        shingle2 = Shingle(4, 'tests/text_2.txt')
        shingle3 = Shingle(4, 'tests/text_3.txt')
        jaccard_similarity = compare_sets.jaccard_similarity(shingle1.set, shingle2.set)
        self.assertEqual(jaccard_similarity, 4/56)
        jaccard_similarity = compare_sets.jaccard_similarity(shingle1.set, shingle3.set)
        self.assertEqual(jaccard_similarity, 0)
        jaccard_similarity = compare_sets.jaccard_similarity(shingle3.set, shingle3.set)
        self.assertEqual(jaccard_similarity, 0)