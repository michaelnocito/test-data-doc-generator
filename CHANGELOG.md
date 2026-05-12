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
- All data types export as Excel `.xlsx` (openpyxl) automatically
- Messy Data includes nulls, duplicates, inconsistent casing, bad formatting for cleanup testing

**Output**
- Native folder picker dialog for output folder selection
- Open individual files or output folder directly from the app
- Random hex token in filenames prevents overwriting

**Distribution**
- Windows installer built with Inno Setup
- Start Menu and Desktop shortcuts created on install
- Uninstaller registered in Windows Settings → Apps
- Standalone `.exe` also available via PyInstaller

**Safety**
- Disclaimer row injected into every Excel file
- Disclaimer block in every document body
- No real personal data used anywhere
- Fully offline — no network calls

---

## Upcoming

- Additional document types (NDA, SOW, Work Order)
- Configurable row count for data sets
- Dark mode UI toggle
