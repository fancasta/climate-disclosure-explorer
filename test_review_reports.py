import unittest
from review_reports import rank_pages


class PageRankingTests(unittest.TestCase):
    def test_page_numbers_ties_and_no_overlap(self):
        first, absent = rank_pages(["", "wind power", "wind power"], ["wind", "ocean"])
        self.assertEqual([hit["page"] for hit in first], [2, 3])
        self.assertEqual(absent, [])

    def test_empty_text(self):
        self.assertEqual(rank_pages(["", "the"], ["solar"]), [[]])
