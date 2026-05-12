import json
import os
import random
import secrets
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from tkinter import Tk, filedialog

import webview
from docx import Document
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

RNG = random.Random(secrets.randbits(64))

DOC_TYPES = {"invoice", "purchase_order", "intake_form", "sop", "contract", "offer_letter"}
DATA_TYPES = {"customers", "vendors", "transactions", "employees", "inventory", "messy"}

FIRST_WORDS = ["Apex", "Horizon", "Meridian", "Nexus", "Pinnacle", "Summit", "Catalyst", "Elevate", "Vantage", "Clarity"]
INDUSTRY_WORDS = ["Clinical", "Health", "Analytics", "Solutions", "Systems", "Informatics", "Care", "Data", "Consulting", "Technologies"]
CORP_SUFFIXES = ["LLC", "Inc.", "Group", "Partners", "Associates"]
STREETS = ["Oak", "Maple", "Commerce", "Innovation", "Enterprise", "Corporate", "Tech", "Riverside", "Lakeside"]
STREET_TYPES = ["Blvd", "Dr", "Ave", "Way", "Pkwy", "St", "Ct"]
CITIES = [("Austin", "TX"), ("Nashville", "TN"), ("Atlanta", "GA"), ("Denver", "CO"), ("Charlotte", "NC"),
          ("Phoenix", "AZ"), ("Raleigh", "NC"), ("Tampa", "FL"), ("Columbus", "OH"), ("Indianapolis", "IN")]
FIRST_NAMES = ["Mia", "Liam", "Noah", "Emma", "Olivia", "Ava", "Ethan", "Lucas", "James", "Sophia"]
LAST_NAMES = ["Carter", "Hayes", "Brooks", "Foster", "Morgan", "Bennett", "Turner", "Parker", "Bailey", "Reed"]

DISCLAIMER = "FICTIONAL TEST DATA ONLY - generated for testing, demo, or training use."


@dataclass
class Party:
    name: str
    address1: str
    address2: str
    phone: str


def rand_phone():
    return f"({RNG.randint(200, 989)}) {RNG.randint(200, 989)}-{RNG.randint(1000, 9999)}"


def rand_address():
    city, state = RNG.choice(CITIES)
    street = f"{RNG.randint(100, 9999)} {RNG.choice(STREETS)} {RNG.choice(STREET_TYPES)}"
    return street, f"{city}, {state} {RNG.randint(10000, 99999)}"


def rand_company():
    return f"{RNG.choice(FIRST_WORDS)} {RNG.choice(INDUSTRY_WORDS)} {RNG.choice(CORP_SUFFIXES)}"


def rand_person():
    return f"{RNG.choice(FIRST_NAMES)} {RNG.choice(LAST_NAMES)}"


def rand_contract_number():
    return f"AGR-{RNG.randint(2024, 2026)}-{RNG.randint(10000, 99999)}"


def rand_invoice_number():
    return f"INV-{RNG.randint(100000, 999999)}"


def rand_po_number():
    return f"PO-{RNG.randint(100000, 999999)}"


def rand_date_near():
    d = date.today() + timedelta(days=RNG.randint(-60, 60))
    return d.strftime("%B %d, %Y")


def sanitize_filename(s):
    s = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(s).strip())
    return s[:100] or "output"


def random_party():
    a1, a2 = rand_address()
    return Party(name=rand_company(), address1=a1, address2=a2, phone=rand_phone())


def build_document_text(doc_type, buyer, vendor):
    if doc_type == "invoice":
        return f"""{DISCLAIMER}

SAMPLE INVOICE
Invoice Number: {rand_invoice_number()}
Invoice Date: {rand_date_near()}

Bill To:
{buyer.name}
{buyer.address1}
{buyer.address2}
{buyer.phone}

Vendor:
{vendor.name}
{vendor.address1}
{vendor.address2}
{vendor.phone}

Line Items:
- Implementation Services .......... $12,500
- Configuration Support ............ $4,800
- Training Session ................. $2,200

Total Due: $19,500
"""
    if doc_type == "purchase_order":
        return f"""{DISCLAIMER}

SAMPLE PURCHASE ORDER
PO Number: {rand_po_number()}
PO Date: {rand_date_near()}

Buyer:
{buyer.name}
{buyer.address1}
{buyer.address2}

Vendor:
{vendor.name}
{vendor.address1}
{vendor.address2}

Items:
- Laptop Docking Stations x 15
- Monitors x 10
- Wireless Keyboards x 20
"""
    if doc_type == "intake_form":
        return f"""{DISCLAIMER}

SAMPLE INTAKE FORM
Record ID: {secrets.token_hex(4).upper()}
Submitted: {rand_date_near()}

Organization:
{buyer.name}

Primary Contact:
{rand_person()}
{buyer.phone}

Requested Service:
Platform onboarding and implementation review
"""
    if doc_type == "sop":
        return f"""{DISCLAIMER}

SAMPLE SOP
Document ID: SOP-{RNG.randint(1000,9999)}
Effective Date: {rand_date_near()}

Department: Operations
Owner: {rand_person()}

Procedure:
1. Receive request.
2. Validate required fields.
3. Route to assigned specialist.
4. Log completion status.
"""
    if doc_type == "contract":
        return f"""{DISCLAIMER}

SAMPLE CONTRACT
Contract Number: {rand_contract_number()}
Effective Date: {rand_date_near()}

Buyer:
{buyer.name}
{buyer.address1}
{buyer.address2}
{buyer.phone}

Vendor:
{vendor.name}
{vendor.address1}
{vendor.address2}
{vendor.phone}

This is a fictional agreement for testing and demo purposes only.
"""
    if doc_type == "offer_letter":
        return f"""{DISCLAIMER}

SAMPLE OFFER LETTER
Candidate: {rand_person()}
Date: {rand_date_near()}

Employer:
{buyer.name}

Position:
Business Systems Analyst

Compensation:
Base Salary: $85,000
Start Date: {rand_date_near()}
"""
    return f"{DISCLAIMER}\n\nSample output"


def export_pdf(path, title, body):
    c = canvas.Canvas(str(path), pagesize=LETTER)
    width, height = LETTER
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, title)
    c.setFont("Helvetica", 10)
    y = height - 100
    for line in body.splitlines():
        if y < 72:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 72
        c.drawString(72, y, line[:110])
        y -= 14
    c.save()


def export_docx(path, title, body):
    doc = Document()
    p = doc.add_paragraph()
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(16)
    doc.add_paragraph("")
    for line in body.splitlines():
        doc.add_paragraph(line)
    doc.save(str(path))


def export_html(path, title, body):
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title>
<style>
body{{font-family:Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 20px;line-height:1.5}}
.notice{{background:#fff3cd;border:1px solid #f0d98a;padding:12px 14px;border-radius:8px;margin-bottom:20px}}
pre{{white-space:pre-wrap;font-family:inherit}}
</style></head>
<body>
<div class="notice">{DISCLAIMER}</div>
<h1>{title}</h1>
<pre>{body}</pre>
</body></html>"""
    path.write_text(html, encoding="utf-8")


def generate_dataset_rows(dataset, count=50):
    rows = []
    for i in range(count):
        if dataset == "customers":
            rows.append({
                "customer_id": f"CUST-{1000+i}",
                "name": rand_person(),
                "company": rand_company(),
                "email": f"user{i+1}@example.com",
                "phone": rand_phone()
            })
        elif dataset == "vendors":
            rows.append({
                "vendor_id": f"VEND-{1000+i}",
                "vendor_name": rand_company(),
                "contact_name": rand_person(),
                "phone": rand_phone(),
                "status": RNG.choice(["Active", "Pending", "Inactive"])
            })
        elif dataset == "transactions":
            rows.append({
                "txn_id": f"TXN-{100000+i}",
                "account": f"ACCT-{RNG.randint(1000,9999)}",
                "amount": RNG.randint(50, 5000),
                "currency": "USD",
                "posted_date": rand_date_near()
            })
        elif dataset == "employees":
            rows.append({
                "employee_id": f"EMP-{1000+i}",
                "name": rand_person(),
                "department": RNG.choice(["HR", "Finance", "IT", "Operations"]),
                "title": RNG.choice(["Analyst", "Manager", "Coordinator", "Specialist"]),
                "phone": rand_phone()
            })
        elif dataset == "inventory":
            rows.append({
                "sku": f"SKU-{10000+i}",
                "item_name": RNG.choice(["Monitor", "Laptop", "Dock", "Keyboard", "Headset"]),
                "quantity": RNG.randint(0, 250),
                "warehouse": RNG.choice(["East", "West", "Central"]),
                "status": RNG.choice(["In Stock", "Low Stock", "Backorder"])
            })
        elif dataset == "messy":
            rows.append({
                "raw_name": RNG.choice([rand_person(), rand_person().lower(), "", None]),
                "email": RNG.choice([f"user{i}@example.com", f"USER{i}@EXAMPLE.COM", "", None]),
                "amount": RNG.choice([RNG.randint(10,9999), f"${RNG.randint(10,9999)}", "", None]),
                "status": RNG.choice(["active", "ACTIVE", " pending ", "", None]),
                "duplicate_key": RNG.choice([f"DUP-{i//3}", f"DUP-{i//5}", "", None])
            })
    return rows


def export_xlsx(path, dataset, rows):
    wb = Workbook()
    ws = wb.active
    ws.title = dataset[:31]
    ws.append([DISCLAIMER])
    headers = list(rows[0].keys()) if rows else ["note"]
    ws.append(headers)
    fill = PatternFill(fill_type="solid", fgColor="D9EAD3")
    bold = Font(bold=True)
    for col, _ in enumerate(headers, start=1):
        cell = ws.cell(row=2, column=col)
        cell.font = bold
        cell.fill = fill
    for row in rows:
        ws.append([row.get(h) for h in headers])
    for col_cells in ws.columns:
        max_len = 0
        col_letter = col_cells[0].column_letter
        for cell in col_cells:
            val = "" if cell.value is None else str(cell.value)
            max_len = max(max_len, len(val))
        ws.column_dimensions[col_letter].width = min(max_len + 2, 28)
    wb.save(str(path))


def generate_doc_file(doc_type, fmt, out_dir):
    buyer = random_party()
    vendor = random_party()
    title = doc_type.replace("_", " ").title()
    body = build_document_text(doc_type, buyer, vendor)
    stem = sanitize_filename(f"{doc_type}_{secrets.token_hex(3)}")
    if fmt == "pdf":
        path = out_dir / f"{stem}.pdf"
        export_pdf(path, title, body)
    elif fmt == "docx":
        path = out_dir / f"{stem}.docx"
        export_docx(path, title, body)
    else:
        path = out_dir / f"{stem}.html"
        export_html(path, title, body)
    return path


def generate_data_file(dataset, out_dir, row_count=50):
    rows = generate_dataset_rows(dataset, row_count)
    path = out_dir / f"{sanitize_filename(dataset)}_{secrets.token_hex(3)}.xlsx"
    export_xlsx(path, dataset, rows)
    return path


class API:
    def choose_folder(self):
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory()
        root.destroy()
        return folder or None

    def open_path(self, path):
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return True
        except Exception:
            return False

    def open_folder(self, path):
        return self.open_path(path)

    def generate(self, payload):
        try:
            mode = payload.get("mode", "documents")
            selected = payload.get("docTypes", [])
            qty = max(1, int(payload.get("quantity", 1)))
            fmt = (payload.get("format") or "").lower().strip()
            out_folder = payload.get("outputFolder") or str(Path.home() / "Documents" / "sample_docs")

            if out_folder.startswith("~/"):
                out_folder = str(Path.home() / out_folder[2:])

            out_dir = Path(out_folder)
            out_dir.mkdir(parents=True, exist_ok=True)

            generated_files = []
            wants_docs = mode in ("documents", "both")
            wants_data = mode in ("data", "both")

            doc_keys = [t for t in selected if t in DOC_TYPES]
            data_keys = [t for t in selected if t in DATA_TYPES]

            if wants_docs:
                if fmt not in {"pdf", "docx", "html"}:
                    raise ValueError("Choose a document format before generating documents.")
                for doc_type in doc_keys:
                    for _ in range(qty):
                        generated_files.append(str(generate_doc_file(doc_type, fmt, out_dir)))

            if wants_data:
                for dataset in data_keys:
                    for _ in range(qty):
                        generated_files.append(str(generate_data_file(dataset, out_dir)))

            return {"success": True, "files": generated_files, "folder": str(out_dir)}
        except Exception as e:
            return {"success": False, "error": str(e), "files": []}


if __name__ == "__main__":
    api = API()
    ui_path = Path(__file__).parent / "ui.html"
    html = ui_path.read_text(encoding="utf-8")

    webview.create_window(
        "Test Data & Document Generator",
        html=html,
        js_api=api,
        width=860,
        height=780,
        min_size=(700, 600),
        resizable=True,
    )
    webview.start(debug=False)
