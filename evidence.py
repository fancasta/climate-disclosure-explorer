"""Trace a reference match back to its sentence and PDF page."""
import argparse
import json
import math
import re
from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def closest_pair(references, candidates):
    """Return (reference row, candidate row, cosine), or None for no overlap.

    Visit reference rows in order. Equal scores prefer the first reference,
    then the first candidate. Only one row of similarities is held at a time.
    """
    best = None
    for index in range(references.shape[0]):
        if candidates.shape[0] == 0:
            break
        scores = cosine_similarity(references[index], candidates, dense_output=False).tocsr()
        if scores.nnz:
            column = int(scores.argmax())
            score = min(float(scores[0, column]), 1.0)
            if best is None or score > best[2]:
                best = (index, column, score)
    return best


def report_evidence(pdf, references):
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(references)
    for page_number, page in enumerate(PdfReader(pdf).pages, start=1):
        text = " ".join((page.extract_text() or "").split())
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", text) if s]
        match = closest_pair(matrix, vectorizer.transform(sentences)) if sentences else None
        row = {"page": page_number, "status": "no_overlap" if sentences else "no_text",
               "sentence": None, "reference": None, "cosine": None}
        if match is not None:
            reference, candidate, score = match
            row.update(status="candidate" if score >= math.cos(math.radians(30)) else "below_threshold",
                       sentence=sentences[candidate], reference=references[reference], cosine=round(score, 4))
        yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("references", type=Path, help="One reference sentence per line")
    args = parser.parse_args()
    references = [s.strip() for s in args.references.read_text(encoding="utf-8").splitlines() if s.strip()]
    if not any(re.search(r"\b\w\w+\b", s) for s in references):
        parser.error("Supply at least one reference with a word of two or more characters.")
    for row in report_evidence(args.pdf, references):
        print(json.dumps(row, ensure_ascii=True))


if __name__ == "__main__":
    main()
