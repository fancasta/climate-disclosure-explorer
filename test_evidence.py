import unittest
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

from evidence import closest_pair, report_evidence


class EvidenceTests(unittest.TestCase):
    def test_retrieves_the_original_pair_with_stable_ties(self):
        vectorizer = TfidfVectorizer()
        refs = vectorizer.fit_transform(["solar array", "electric fleet", "electric fleet"])
        inputs = vectorizer.transform(["unrelated", "electric fleet", "electric fleet"])
        ref, sentence, score = closest_pair(refs, inputs)
        self.assertEqual((ref, sentence), (1, 1))
        self.assertAlmostEqual(score, 1)

    def test_pdf_to_evidence_in_page_order(self):
        folder = Path(__file__).parent / "examples"
        refs = (folder / "reference.txt").read_text(encoding="utf-8").splitlines()
        rows = list(report_evidence(folder / "mock-report.pdf", refs))
        self.assertEqual([row["page"] for row in rows], [1, 2, 3, 4])
        self.assertEqual([row["status"] for row in rows],
                         ["candidate", "below_threshold", "no_overlap", "no_text"])
        self.assertEqual(rows[0]["reference"], refs[0])
        self.assertIn("electric vehicles", rows[0]["sentence"])
        self.assertIsNone(rows[-1]["cosine"])


if __name__ == "__main__":
    unittest.main()
