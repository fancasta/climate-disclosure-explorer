"""Rank PDF pages for the case-study queries. Supply a directory with the publisher PDFs."""
import argparse
import hashlib
import json
import unicodedata
from pathlib import Path

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

MANIFEST = Path(__file__).parent / "examples/public-reports.json"


def rank_pages(pages, queries):
    """Fit once per document. Rank positive overlaps with stable page-order ties."""
    vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True)
    try:
        matrix = vectorizer.fit_transform(pages)
    except ValueError as exc:
        if "empty vocabulary" in str(exc):
            return [[] for _ in queries]
        raise
    scores = linear_kernel(vectorizer.transform(queries), matrix)
    results = []
    for row in scores:
        order = sorted(range(len(row)), key=lambda i: (-row[i], i))
        results.append([{"page": i + 1, "cosine": round(float(row[i]), 4)}
                        for i in order[:3] if row[i] > 0])
    return results


def review(folder):
    for publisher, source in json.loads(MANIFEST.read_text(encoding="utf-8")).items():
        path = folder / (publisher + ".pdf")
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            raise ValueError(f"{path.name} differs from the recorded publisher edition")
        pages = [unicodedata.normalize("NFKC", page.extract_text() or "")
                 for page in PdfReader(path).pages]
        queries = source["queries"]
        ranked = rank_pages(pages, [case["query"] for case in queries])
        for case, hits in zip(queries, ranked):
            yield {"publisher": publisher, "pages": len(pages), **case, "hits": hits}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf_directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(list(review(args.pdf_directory)), indent=2))
