"""DOCX renderer using python-docx.

Layout: title paragraph, party table (2-col borderless), line items table,
totals block, footer paragraph. SAMPLE text box in header area (no true
watermark support in docx).
"""

import secrets
from pathlib import Path

from docx import Document
from docx.shared import Pt

from recordforge.core.models import DocumentData, GeneratedDoc


def render(data: DocumentData, output_dir: Path) -> GeneratedDoc:
    """Render a DocumentData instance to a DOCX file.

    Returns a GeneratedDoc with the output path.
    """
    ...
