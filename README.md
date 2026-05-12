# test-data-doc-generator

Generate puretly fictional test documents and sample data for QA, OCR testing, implementation workflows, and data migration demos.

Built for data professionals, implementation analysts, QA teams, and solution engineers who need realistic test artifacts without using real data.

---

## What It Does

- Generates fictional test documents: contracts, COIs, amendments
- Supports PDF and Word (.docx) export
- All data is randomly generated — no real personal or business information
- Vertical-aware: Healthcare, Higher Education, Government, Commercial

---

## Test Document Disclaimer

This tool generates **test documents and fictional test data** for testing, demo, training, OCR validation, migration workflows, and sandbox setup.

Generated outputs are **not valid for legal, financial, medical, regulatory, or identity purposes** and must not be represented as authentic business records.

All generated documents are marked with a visible **TEST DOCUMENT** watermark and footer notice.

Default generated content is fictional. Review any user-entered content before sharing or using outputs outside a controlled testing context.

---

## Stack

| Dependency | Purpose |
|---|---|
| `customtkinter` | GUI |
| `reportlab` | PDF export |
| `python-docx` | Word export |

```bash
pip install customtkinter reportlab python-docx
```

---

## Running

```bash
python doc_generator_gui.py
```

---

## Status

Active development. Private build. Not yet released publicly.
