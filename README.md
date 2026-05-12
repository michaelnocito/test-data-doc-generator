# Test Data & Document Generator

A Windows desktop app that generates **fictional** PDFs, Word docs, HTML files, and Excel data sets for testing, QA, demos, and training workflows.

> ⚠️ All output is synthetic and fictional. Never use for legal, financial, medical, regulatory, or identity purposes.

---

## ⬇️ Download & Install (Windows)

1. Go to [**Releases**](https://github.com/michaelnocito/test-data-doc-generator/releases)
2. Download `TestDataDocGeneratorSetup.exe`
3. Double-click the installer and follow the wizard (Next → Next → Finish)
4. Launch from the **Desktop shortcut** or **Start Menu**

No Python required. Works on Windows 10 and Windows 11.

> **Blank white screen after launch?** Your machine may be missing the Microsoft Edge WebView2 Runtime — this is required by the app. [Download it free from Microsoft](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) and reinstall. See [Troubleshooting](docs/TROUBLESHOOTING.md) for more help.

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

## Run from Source (Developers)

If you prefer to run the Python source directly:

```powershell
git clone https://github.com/michaelnocito/test-data-doc-generator.git
cd test-data-doc-generator
pip install -r requirements.txt
python main.py
```

Requires Python 3.11+ and pip.

---

## Project Structure

```
test-data-doc-generator/
├── main.py                    # App logic, data generation, pywebview API
├── ui.html                    # Wizard UI (loaded by pywebview at runtime)
├── installer.iss              # Inno Setup installer script
├── requirements.txt           # Python dependencies
├── CHANGELOG.md
├── INSTALL.md                 # EXE + installer build instructions
├── PRIVACY.md
├── .gitignore
├── README.md
└── docs/
    ├── TROUBLESHOOTING.md
    └── CONTRIBUTING.md
```

---

## Need Help?

- [Installation & Build Guide](INSTALL.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## Safety & Privacy

- No real personal data is ever used in generated output
- No network calls — fully offline
- User-entered output folder paths are not stored or transmitted
- Generated files stay on your machine in the folder you choose
- See [PRIVACY.md](PRIVACY.md) for full details

---

## More Tools

**[🧼 Spreadsheet Cleaner](https://github.com/michaelnocito/spreadsheet-cleaner)** — A Python learning project that teaches you to build a real data-cleaning tool, the kind used in professional data migration work. Three layers: Basic, Intermediate, and Advanced.

---

If this project saved you time, the best thing you can do is [⭐ star the repo](https://github.com/michaelnocito/test-data-doc-generator) — it helps others find it.

If you'd like to support the work, a coffee is always appreciated but never expected.

<a href="https://buymeacoffee.com/michaelnocito" target="_blank">
  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" height="50">
</a>

---

Built with 🐍 Python | Maintained by [Michael Nocito](https://github.com/michaelnocito)
