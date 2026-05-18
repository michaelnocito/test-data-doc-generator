"""Phase A smoke tests."""

import random
from decimal import Decimal
from pathlib import Path

import pytest

from recordforge.core.models import DocumentData, GeneratedDoc
from recordforge.core.seed import get_rng, set_seed


# --- Generator smoke tests ---

def _fresh_rng() -> random.Random:
    return random.Random(12345)


def test_invoice_build():
    from recordforge.generators.documents.invoice import build
    data = build(_fresh_rng())
    assert isinstance(data, DocumentData)
    assert data.doc_type == "invoice"
    assert data.doc_number.startswith("INV-")
    assert 2 <= len(data.line_items) <= 4


def test_purchase_order_build():
    from recordforge.generators.documents.purchase_order import build
    data = build(_fresh_rng())
    assert data.doc_type == "purchase_order"
    assert data.doc_number.startswith("PO-")
    assert 3 <= len(data.line_items) <= 6


def test_intake_form_build():
    from recordforge.generators.documents.intake_form import build
    data = build(_fresh_rng())
    assert data.doc_type == "intake_form"
    assert len(data.line_items) == 0
    assert data.notes


def test_sop_build():
    from recordforge.generators.documents.sop import build
    data = build(_fresh_rng())
    assert data.doc_type == "sop"
    assert len(data.line_items) == 0


def test_contract_build():
    from recordforge.generators.documents.contract import build
    data = build(_fresh_rng())
    assert data.doc_type == "contract"
    assert len(data.line_items) == 0
    assert "SERVICES AGREEMENT" in data.notes


def test_offer_letter_build():
    from recordforge.generators.documents.offer_letter import build
    data = build(_fresh_rng())
    assert data.doc_type == "offer_letter"
    assert len(data.line_items) == 0
    assert "Base Salary" in data.notes


# --- Line item math ---

def test_line_item_totals_are_computed():
    from recordforge.generators.documents.invoice import build
    data = build(_fresh_rng())
    for item in data.line_items:
        assert item.total == Decimal(item.quantity) * item.unit_price
    assert data.subtotal == sum(i.total for i in data.line_items)
    assert data.total_due == data.subtotal + data.tax


# --- Date ordering ---

def test_invoice_due_date_after_doc_date():
    from datetime import datetime
    from recordforge.generators.documents.invoice import build
    data = build(_fresh_rng())
    fmt = "%B %d, %Y"
    doc = datetime.strptime(data.doc_date, fmt)
    due = datetime.strptime(data.due_date, fmt)
    assert due > doc


# --- Data generator smoke tests ---

def test_customers_build_rows():
    from recordforge.generators.data.customers import build_rows
    rows = build_rows(_fresh_rng(), count=10)
    assert len(rows) == 10
    assert "customer_id" in rows[0]
    assert rows[0]["customer_id"] == "CUST-1000"


def test_vendors_build_rows():
    from recordforge.generators.data.vendors import build_rows
    rows = build_rows(_fresh_rng(), count=5)
    assert len(rows) == 5
    assert "vendor_id" in rows[0]


def test_transactions_build_rows():
    from recordforge.generators.data.transactions import build_rows
    rows = build_rows(_fresh_rng(), count=5)
    assert all(r["currency"] == "USD" for r in rows)


def test_employees_build_rows():
    from recordforge.generators.data.employees import build_rows
    rows = build_rows(_fresh_rng(), count=5)
    assert "employee_id" in rows[0]


def test_inventory_build_rows():
    from recordforge.generators.data.inventory import build_rows
    rows = build_rows(_fresh_rng(), count=5)
    assert "sku" in rows[0]


def test_messy_build_rows():
    from recordforge.generators.data.messy import build_rows
    rows = build_rows(_fresh_rng(), count=20)
    # Must contain at least some None values (dirty by design)
    all_values = [v for row in rows for v in row.values()]
    assert None in all_values


# --- Renderer smoke tests ---

def test_pdf_renderer_produces_nonempty_file(tmp_path: Path):
    from recordforge.generators.documents.invoice import build
    from recordforge.renderers.pdf import render
    data = build(_fresh_rng())
    doc = render(data, tmp_path)
    assert isinstance(doc, GeneratedDoc)
    assert doc.path.exists()
    assert doc.path.stat().st_size > 0


def test_docx_renderer_produces_nonempty_file(tmp_path: Path):
    from recordforge.generators.documents.invoice import build
    from recordforge.renderers.docx import render
    data = build(_fresh_rng())
    doc = render(data, tmp_path)
    assert doc.path.exists()
    assert doc.path.stat().st_size > 0


def test_html_renderer_produces_nonempty_file(tmp_path: Path):
    from recordforge.generators.documents.invoice import build
    from recordforge.renderers.html import render
    data = build(_fresh_rng())
    doc = render(data, tmp_path)
    assert doc.path.exists()
    content = doc.path.read_text(encoding="utf-8")
    assert "SAMPLE" in content
    assert data.doc_number in content


def test_xlsx_renderer_produces_nonempty_file(tmp_path: Path):
    from recordforge.generators.data.customers import build_rows
    from recordforge.renderers.xlsx import render
    rows = build_rows(_fresh_rng(), count=10)
    doc = render("customers", rows, tmp_path)
    assert doc.path.exists()
    assert doc.path.stat().st_size > 0


# --- Watermark test ---

def test_pdf_contains_sample_watermark(tmp_path: Path):
    """Generated PDF contains watermark indicators: Helvetica-Bold font and 0.15 alpha."""
    from recordforge.generators.documents.invoice import build
    from recordforge.renderers.pdf import render
    data = build(_fresh_rng())
    doc = render(data, tmp_path)
    raw = doc.path.read_bytes()
    # Watermark uses Helvetica-Bold at alpha 0.15 — both appear uncompressed in PDF metadata
    assert b"Helvetica-Bold" in raw
    assert b"/ca .15" in raw


# --- Seed reproducibility ---

def test_same_seed_same_doc_number():
    from recordforge.generators.documents.invoice import build
    set_seed(99)
    a = build(get_rng())
    set_seed(99)
    b = build(get_rng())
    assert a.doc_number == b.doc_number


def test_same_seed_same_total_due():
    from recordforge.generators.documents.invoice import build
    set_seed(42)
    a = build(get_rng())
    set_seed(42)
    b = build(get_rng())
    assert a.total_due == b.total_due
