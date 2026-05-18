"""Phase A smoke tests.

One test per generator (build returns valid DocumentData).
One test per renderer (output file exists and is non-empty).
One watermark test (PDF contains "SAMPLE").
One seed test (same seed → same doc_number and line item totals).
"""

import random
from decimal import Decimal
from pathlib import Path

import pytest

from recordforge.core.models import DocumentData, GeneratedDoc
from recordforge.core.seed import set_seed


# --- Generator smoke tests ---

def test_invoice_build_returns_document_data():
    """build() returns a DocumentData with the correct doc_type."""
    ...


def test_purchase_order_build_returns_document_data():
    ...


def test_intake_form_build_returns_document_data():
    ...


def test_sop_build_returns_document_data():
    ...


def test_contract_build_returns_document_data():
    ...


def test_offer_letter_build_returns_document_data():
    ...


# --- Renderer smoke tests ---

def test_pdf_renderer_produces_nonempty_file(tmp_path: Path):
    """render() creates a non-empty PDF file."""
    ...


def test_docx_renderer_produces_nonempty_file(tmp_path: Path):
    ...


def test_html_renderer_produces_nonempty_file(tmp_path: Path):
    ...


def test_xlsx_renderer_produces_nonempty_file(tmp_path: Path):
    ...


# --- Watermark test ---

def test_pdf_contains_sample_watermark(tmp_path: Path):
    """Generated PDF contains the string 'SAMPLE' when read as text."""
    ...


# --- Seed reproducibility ---

def test_same_seed_produces_same_doc_number():
    """Two builds with the same seed yield identical doc_number."""
    ...


def test_same_seed_produces_same_line_item_totals():
    """Two builds with the same seed yield identical total_due."""
    ...
