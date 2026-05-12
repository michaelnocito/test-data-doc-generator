# Changelog

All notable changes to this project are documented here.

---

## [1.0.0] — 2026-05-12

### First stable release

**App**
- 3-step wizard UI (Mode & Type → Settings → Generate)
- pywebview desktop window loads `ui.html` as rendered HTML via `html=` parameter
- `debug=False` for clean production window — no dev tools popup

**Document generation**
- Invoice, Purchase Order, Intake Form, SOP, Contract, Offer Letter
- Export formats: PDF (ReportLab), Word .docx (python-docx), HTML
- All party / org data randomly generated — no manual input required

**Data generation**
- Customer Records, Vendor Master, Transactions, Employee Records, Inventory, Messy Data
- All data types export as Excel `.xlsx` (openpyxl) automatically — no format selection needed
- Messy Data includes nulls, duplicates, inconsistent casing, and bad formatting for cleanup testing

**Output**
- Choose any output folder via native folder picker dialog
- Open individual files or the output folder directly from the app after generation
- All filenames include a random hex token to prevent overwriting

**Safety**
- Disclaimer row injected into every Excel file
- Disclaimer block included in every document body
- No real personal data used anywhere
- Fully offline — no network calls

---

## Upcoming

- Windows EXE release via PyInstaller
- Additional document types (NDA, SOW, Work Order)
- Configurable row count for data sets
- Dark mode UI toggle
