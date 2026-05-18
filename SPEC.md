# RecordForge v2 — Phase A Spec

## Overview

RecordForge generates realistic synthetic documents and data files for
data engineers, QA engineers, and ETL pipeline developers. Output is
always clearly marked as fictional (watermark + disclaimer). Fully
offline. No external API calls.

Phase A scope: refactor v1 monolith into a proper package, upgrade the
PDF renderer to a real document layout with a diagonal watermark, add
relational integrity to all document types, add a CLI, and expose a
Python API. No new document types in Phase A.

---

## Repo / Package

- Repo name: `recordforge`
- Python package: `recordforge`
- Entry points: CLI (`recordforge`) and desktop app (`python -m recordforge`)
- Python: 3.11+

---

## Package Structure

```
recordforge/
├── __init__.py              # public Python API
├── __main__.py              # python -m recordforge → launches desktop UI
├── cli.py                   # Typer CLI
├── core/
│   ├── __init__.py
│   ├── models.py            # dataclasses: Party, LineItem, GeneratedDoc
│   ├── faker_utils.py       # all rand_* helpers + expanded word lists
│   ├── watermark.py         # diagonal overlay engine (reportlab)
│   └── seed.py              # RNG singleton + seed control
├── generators/
│   ├── __init__.py
│   ├── documents/
│   │   ├── __init__.py      # exports: DOCUMENT_REGISTRY dict
│   │   ├── invoice.py
│   │   ├── purchase_order.py
│   │   ├── intake_form.py
│   │   ├── sop.py
│   │   ├── contract.py
│   │   └── offer_letter.py
│   └── data/
│       ├── __init__.py      # exports: DATA_REGISTRY dict
│       ├── customers.py
│       ├── vendors.py
│       ├── transactions.py
│       ├── employees.py
│       ├── inventory.py
│       └── messy.py
├── renderers/
│   ├── __init__.py
│   ├── pdf.py               # reportlab layout engine
│   ├── docx.py              # python-docx renderer
│   ├── html.py              # Jinja2 renderer
│   └── xlsx.py              # openpyxl renderer
└── ui/
    ├── app.py               # pywebview API bridge (was main.py API class)
    └── ui.html              # wizard UI (update branding to RecordForge)
```

---

## Core Models  (`core/models.py`)

```python
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

@dataclass
class Party:
    name: str
    address1: str
    address2: str
    phone: str
    email: str        # new in v2

@dataclass
class LineItem:
    description: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return Decimal(self.quantity) * self.unit_price

@dataclass
class DocumentData:
    doc_type: str
    doc_number: str
    doc_date: str
    due_date: str | None
    buyer: Party
    vendor: Party
    line_items: list[LineItem] = field(default_factory=list)
    notes: str = ""

    @property
    def subtotal(self) -> Decimal:
        return sum(item.total for item in self.line_items)

    @property
    def tax(self) -> Decimal:
        return (self.subtotal * Decimal("0.08")).quantize(Decimal("0.01"))

    @property
    def total_due(self) -> Decimal:
        return self.subtotal + self.tax

@dataclass
class GeneratedDoc:
    path: Path
    doc_type: str
    format: str
```

---

## Seed Control  (`core/seed.py`)

- Single `random.Random` instance created at import, seeded with
  `secrets.randbits(64)` by default.
- `set_seed(n: int)` replaces the instance with `random.Random(n)`.
- All `rand_*` functions in `faker_utils.py` use this shared instance.
- Never use the `random` module globals anywhere in the codebase.

```python
# usage
from recordforge.core.seed import set_seed
set_seed(42)  # reproducible output
```

---

## Faker Utils  (`core/faker_utils.py`)

Expand all word lists to minimum 40 entries each. Current v1 lists have
10 entries — obvious repetition at batch sizes > 10.

Required lists (minimum sizes):
- `FIRST_WORDS` — 40 entries
- `INDUSTRY_WORDS` — 40 entries
- `CORP_SUFFIXES` — 10 entries
- `STREETS` — 40 entries
- `STREET_TYPES` — 10 entries
- `CITIES` — 40 (city, state) tuples, all US
- `FIRST_NAMES` — 60 entries (diverse)
- `LAST_NAMES` — 60 entries (diverse)
- `EMAIL_DOMAINS` — 20 entries (generic business domains, no real brands)
- `PRODUCTS` — 30 entries (generic B2B items for line items)
- `SERVICES` — 30 entries (generic professional services for line items)

New helpers required:
- `rand_email(company_name: str) -> str` — derives from company name
- `rand_line_items(rng, kind: Literal["products","services"], count: int = 3) -> list[LineItem]`
  - Amounts must be realistic: unit prices $15–$500 for products,
    $500–$8000 for services; quantities 1–50 for products, 1–5 for services
  - Returns proper `LineItem` dataclass instances

---

## Document Generators  (`generators/documents/`)

Each module exposes one function:

```python
def build(rng: random.Random) -> DocumentData:
    ...
```

All randomness goes through the passed `rng`. No module-level state.

### Relational integrity rules (ALL document types)

- Dates must be logically sequenced: `doc_date` < `due_date` always.
- Line item totals must compute correctly from `LineItem.quantity *
  LineItem.unit_price`. No hardcoded dollar strings.
- `DocumentData.total_due` = subtotal + 8% tax, computed by the model.
- Doc numbers use the same format as v1 (INV-XXXXXX etc).
- Both `buyer` and `vendor` must have all `Party` fields populated
  including `email`.

### Per-type line item requirements

| Type | Line items | Count |
|---|---|---|
| invoice | services | 2–4 |
| purchase_order | products | 3–6 |
| contract | services | 0 (no line items; use flat fee field) |
| offer_letter | 0 (salary fields instead) | — |
| intake_form | 0 | — |
| sop | 0 | — |

`contract` and `offer_letter` must use the `notes` field on
`DocumentData` to carry their extra text (flat fee description for
contract; salary/start-date block for offer letter). Do NOT add new
fields to `DocumentData` in Phase A — the `notes: str` field is the
extension point. Renderers display `notes` as a body paragraph below
the party block.

### DOCUMENT_REGISTRY

```python
# generators/documents/__init__.py
from .invoice import build as build_invoice
# ... etc

DOCUMENT_REGISTRY: dict[str, callable] = {
    "invoice": build_invoice,
    "purchase_order": build_purchase_order,
    "intake_form": build_intake_form,
    "sop": build_sop,
    "contract": build_contract,
    "offer_letter": build_offer_letter,
}
```

---

## Data Generators  (`generators/data/`)

Each module exposes:

```python
def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    ...
```

Preserve all 6 v1 data types exactly. No schema changes in Phase A.

DATA_REGISTRY mirrors DOCUMENT_REGISTRY pattern.

---

## PDF Renderer  (`renderers/pdf.py`)

This is the biggest v2 change. Replace the raw line-by-line text output
with a proper document layout.

### Layout requirements

Every PDF document must have:

**Header block** (top of page 1 only):
- Document type as large title (18pt bold)
- Doc number + date right-aligned on the same row
- Thin horizontal rule below the header

**Party block**:
- Two-column layout: "Bill To" (buyer) left, "From" (vendor) right
- Each column: company name (bold), address line 1, address line 2,
  phone, email

**Line items table** (invoice and purchase_order only):
- Columns: Description | Qty | Unit Price | Total
- Alternating row shading (very light gray on even rows)
- Header row: bold, slightly darker background
- Right-align all numeric columns
- Bottom of table: Subtotal / Tax (8%) / Total Due rows, right-aligned

**Footer** (every page):
- Centered disclaimer text: "FICTIONAL — For testing, demo, and training
  use only. Not a valid legal or financial document."
- Small font (7pt), light gray

**Watermark** (every page, applied last):
- See watermark spec below.

### Implementation approach

Use `reportlab.platypus` (Flowable/Frame system) NOT `canvas` line-by-line.
Specifically use `SimpleDocTemplate` + `Table` + `Paragraph` + `Spacer`.
This gives proper text wrapping, page breaks, and table layout without
manual coordinate math.

Apply the watermark as a post-processing canvas overlay on every page
using `canvas.Canvas` + `onFirstPage` / `onLaterPages` callbacks, or
by subclassing `SimpleDocTemplate` to inject the watermark via
`afterPage`.

Required reportlab imports:
```python
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
```

---

## Watermark Engine  (`core/watermark.py`)

### Spec

- Text: `"SAMPLE"` (all caps)
- Font: Helvetica-Bold
- Size: 72pt
- Color: red, 15% opacity (alpha = 0.15)
- Rotation: 45 degrees, centered on the page
- Applied to EVERY page of every PDF
- Applied AFTER all content (renders on top)

### Implementation

```python
def apply_watermark(canvas, doc):
    """
    Called via SimpleDocTemplate(onFirstPage=apply_watermark,
                                  onLaterPages=apply_watermark)
    """
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 72)
    canvas.setFillColorRGB(1, 0, 0, alpha=0.15)
    canvas.translate(LETTER[0] / 2, LETTER[1] / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "SAMPLE")
    canvas.restoreState()
```

This function signature is the contract. The renderer calls it; the
watermark module owns the implementation.

---

## DOCX Renderer  (`renderers/docx.py`)

Upgrade from v1 (plain paragraphs) to structured layout:
- Title paragraph (heading style)
- Party table (2-column, borderless)
- Line items table (with borders, styled header row)
- Totals section (right-aligned, bold Total Due)
- Footer paragraph (small, gray, italic)
- No watermark on DOCX (not supported cleanly — add a "SAMPLE" text
  box in the header area instead, gray, centered)

---

## HTML Renderer  (`renderers/html.py`)

Replace f-string HTML with Jinja2 templates.

- Template file: `renderers/templates/document.html.j2`
- Accepts `DocumentData` dict (serialized)
- Must render a professional-looking document: proper table, totals,
  party block, header
- "SAMPLE" diagonal watermark via CSS:
  ```css
  body::before {
    content: "SAMPLE";
    position: fixed;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 8rem; font-weight: 900;
    color: rgba(255,0,0,0.08);
    pointer-events: none; z-index: 9999;
  }
  ```

---

## XLSX Renderer  (`renderers/xlsx.py`)

Preserve v1 behavior exactly. No changes in Phase A.

---

## CLI  (`cli.py`)

Built with Typer.

```
recordforge generate \
  --type invoice \           # or: purchase_order, contract, etc. / customers, vendors, etc.
  --format pdf \             # pdf | docx | html | xlsx (xlsx only for data types)
  --count 5 \                # number of files (default: 1)
  --output ./out \           # output directory (default: ~/Documents/recordforge)
  --seed 42                  # optional: integer seed for reproducibility

recordforge list-types       # prints all available doc and data types
recordforge version          # prints version
```

Validation rules:
- `--format xlsx` only valid for data types; error with message if used
  with doc types
- `--format pdf/docx/html` only valid for doc types; error if used with
  data types
- `--count` clamps to 1–100

---

## Python API  (`__init__.py`)

```python
from recordforge import generate, list_types, set_seed

# generate returns list[GeneratedDoc]
docs = generate(
    type="invoice",
    format="pdf",
    count=3,
    output="./out",
    seed=42,          # optional
)

for doc in docs:
    print(doc.path)
```

`generate()` signature:
```python
def generate(
    type: str,
    format: str,
    count: int = 1,
    output: str | Path | None = None,
    seed: int | None = None,
) -> list[GeneratedDoc]:
```

---

## Desktop UI  (`ui/`)

- Rebrand all UI text from "Test Data & Document Generator" to "RecordForge"
- `ui/app.py` is a cleaned-up version of v1's `API` class
  - Imports from `recordforge` package instead of local functions
  - Preserves `choose_folder`, `open_path`, `open_folder`, `generate`
- `ui/ui.html` — no functional changes in Phase A, branding update only

---

## Requirements  (`requirements.txt`)

Add to v1 deps:
```
typer>=0.12
jinja2>=3.1
```

Keep all v1 deps (reportlab, python-docx, openpyxl, pywebview).

---

## What to Preserve from v1 (Exactly)

- All 6 document type identifiers (keys stay the same)
- All 6 data type identifiers (keys stay the same)
- `sanitize_filename()` logic
- XLSX column auto-width logic
- `secrets.token_hex()` for file stem uniqueness (keep alongside seed)
- `open_path()` platform detection logic

---

## What to Delete from v1

- `build_document_text()` — replaced by per-type `build()` functions
- `export_pdf()` — replaced by `renderers/pdf.py`
- `export_docx()` — replaced by `renderers/docx.py`
- `export_html()` — replaced by `renderers/html.py`
- `export_xlsx()` — replaced by `renderers/xlsx.py`
- `generate_dataset_rows()` — replaced by per-type `build_rows()`
- `generate_doc_file()` / `generate_data_file()` — replaced by
  `recordforge.generate()`
- The `API` class in `main.py` — moved to `ui/app.py`
- Module-level constants that move to `faker_utils.py`

---

## Rename Checklist (Final Step of Phase A)

- [ ] Rename GitHub repo: `test-data-doc-generator` → `recordforge`
- [ ] Update `README.md` — new name, new install instructions, new CLI docs
- [ ] Update `CHANGELOG.md` — add v2.0.0 entry
- [ ] Update `installer.iss` — new app name, new exe name
- [ ] Update pywebview window title
- [ ] Tag release: `v2.0.0`

---

## Out of Scope for Phase A

- New document types (bank statement, W-2, 1099, EOB, remittance)
- Scan simulation / OCR noise mode
- Locale / internationalization
- Schema import (custom templates via JSON/YAML)
- Web UI
- CI/CD integration
