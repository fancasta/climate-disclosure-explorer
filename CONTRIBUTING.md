# Reproduce or contribute a case study

[Overview](README.md)　·　[Case studies and results](CASE_STUDIES.md)　·　**Reproduction guide**

Download the three publisher PDFs and save them in one directory as `Oracle.pdf`, `Anthropic.pdf` and `OpenAI.pdf`. The [source manifest](examples/public-reports.json) contains the direct download links, edition fingerprints, queries and review pages.

```sh
python -m pip install -r requirements-demo.txt
python review_reports.py path/to/pdfs
```

The command verifies each PDF's SHA-256 fingerprint, preserves physical page numbering (including covers), and returns the top three pages with positive cosine similarity for each query. Compare its output with the [recorded results](examples/case-results.json). A fingerprint mismatch means the publisher served a different edition.

To add a case, identify a source passage and record whether it describes a measurement, target, forecast or proposal. Write the search terms, run the query, then document the page you read alongside the actual ranking, including any miss. Include a short interpretation and a publisher link with a page number. Use short paraphrases for the published study and retain the full PDF at its publisher.
