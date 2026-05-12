# Test Data & Document Generator

A Windows desktop app that generates **fictional** PDFs, Word docs, HTML files, and Excel data sets for testing, QA, demos, and training workflows.

> ⚠️ All output is synthetic and fictional. Never use for legal, financial, medical, regulatory, or identity purposes.

---

## Features

- 3-step wizard: **Mode & Type → Settings → Generate**
- **Document types** (PDF / Word `.docx` / HTML)
  - Invoice
  - Purchase Order
  - Intake Form
  - SOP
  - Contract
  - Offer Letter
- **Data types** (Excel `.xlsx` — automatic, no format selection needed)
  - Customer Records
  - Vendor Master
  - Transactions
  - Employee Records
  - Inventory
  - Messy Data (nulls, dupes, bad formatting — for cleanup testing)
- All org names, addresses, contacts, and party info are **randomly generated**
- Choose your own output folder via folder picker
- Open generated files directly from the app

---

## Requirements

- Windows 10 or Windows 11
- Python 3.11 or higher
- `pip` available in your PATH

---

## Installation

```powershell
git clone https://github.com/michaelnocito/test-data-doc-generator.git
cd test-data-doc-generator
pip install -r requirements.txt
```

---

## Running the App

```powershell
python main.py
```

The wizard window will open. No browser needed.

---

## How to Use

**Step 1 — Mode & Type**
- Choose **Documents**, **Data Files**, or **Both**
- Select the types you want (you can pick multiple)

**Step 2 — Settings**
- Set how many files per type (1–20)
- Choose a document format: **PDF**, **Word .docx**, or **HTML**
  - Skip this if you are only generating data files
- Set your output folder (defaults to `~/Documents/sample_docs`)

**Step 3 — Review & Generate**
- Confirm your selections in the summary
- Click **Generate Test Files**
- Click any file or **Open Output Folder** when done

---

## Project Structure

```
test-data-doc-generator/
├── main.py           # App logic, data generation, pywebview API
├── ui.html           # Wizard UI (loaded by pywebview at runtime)
├── requirements.txt  # Python dependencies
├── INSTALL.md        # Windows installer / EXE build instructions
├── .gitignore
└── README.md
```

---

## Safety & Privacy

- No real personal data is ever used in generated output
- No network calls are made — fully offline
- User-entered output folder paths are not stored or transmitted
- Generated files stay on your machine in the folder you choose
