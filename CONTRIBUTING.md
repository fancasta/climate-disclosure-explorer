# Reproduce or contribute a case study

[Explore all ESG reports](https://fancasta.github.io/climate-disclosure-explorer/)　·　[Browse companies](https://fancasta.github.io/climate-disclosure-explorer/?view=explore)　·　[Cross-sector cases](CASE_STUDIES.md#search-across-sectors)

[Overview](README.md)　·　[Case studies and results](CASE_STUDIES.md)　·　**Reproduction guide**

## Reference results for reproduction

Use these six cases to check page ordering against the recorded PDF editions. The source links open at the page used for interpretation.

| Source and case | First retrieved page | Review page |
| --- | ---: | ---: |
| Oracle · Renewable electricity in the cloud | [p. 37](https://www.oracle.com/a/ocom/docs/environmental-and-social-impact-report-2024.pdf#page=37) | [p. 37](https://www.oracle.com/a/ocom/docs/environmental-and-social-impact-report-2024.pdf#page=37) |
| Oracle · Water and waste targets | [p. 36](https://www.oracle.com/a/ocom/docs/environmental-and-social-impact-report-2024.pdf#page=36) | [p. 36](https://www.oracle.com/a/ocom/docs/environmental-and-social-impact-report-2024.pdf#page=36) |
| Anthropic · Projected power demand | [p. 3](https://assets.claude.com/0dc382a2086f6a054eeb17e8a531bd9625b8e6e5.pdf#page=3) | [p. 5](https://assets.claude.com/0dc382a2086f6a054eeb17e8a531bd9625b8e6e5.pdf#page=5) |
| Anthropic · Transmission upgrades | [p. 19](https://assets.claude.com/0dc382a2086f6a054eeb17e8a531bd9625b8e6e5.pdf#page=19) | [p. 19](https://assets.claude.com/0dc382a2086f6a054eeb17e8a531bd9625b8e6e5.pdf#page=19) |
| OpenAI · Power-use reporting | [p. 8](https://cdn.openai.com/pdf/compute-campus-policy-blueprint.pdf#page=8) | [p. 8](https://cdn.openai.com/pdf/compute-campus-policy-blueprint.pdf#page=8) |
| OpenAI · On-site cooling | [p. 8](https://cdn.openai.com/pdf/compute-campus-policy-blueprint.pdf#page=8) | [p. 8](https://cdn.openai.com/pdf/compute-campus-policy-blueprint.pdf#page=8) |

The top result lands on the selected review page in five cases. For the US power forecast, page 3 summarizes the number and page 5 explains its scope. [Read the interpretations and full rankings](CASE_STUDIES.md).

## Run the study

Download the three publisher PDFs and save them in one directory as `Oracle.pdf`, `Anthropic.pdf` and `OpenAI.pdf`. The [source manifest](examples/public-reports.json) contains the direct download links, edition fingerprints, queries and review pages.

```sh
python -m pip install -r requirements-demo.txt
python review_reports.py path/to/pdfs
```

The command verifies each PDF's SHA-256 fingerprint, preserves physical page numbering (including covers), and returns the top three pages with positive cosine similarity for each query. Compare its output with the [recorded results](examples/case-results.json). A fingerprint mismatch means the publisher served a different edition.

To add a case, identify a source passage and record whether it describes a measurement, target, forecast or proposal. Write the search terms, run the query, then document the page you read alongside the actual ranking, including any miss. Include a short interpretation and a publisher link with a page number. Use short paraphrases for the published study and retain the full PDF at its publisher.
