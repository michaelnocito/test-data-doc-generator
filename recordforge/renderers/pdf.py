"""PDF renderer using reportlab platypus.

Uses SimpleDocTemplate + Flowables — not canvas line-by-line.
Watermark applied via onFirstPage/onLaterPages callbacks on every page.
"""

import secrets
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from recordforge.core.models import DocumentData, GeneratedDoc
from recordforge.core.watermark import apply_watermark


def render(data: DocumentData, output_dir: Path) -> GeneratedDoc:
    """Render a DocumentData instance to a PDF file.

    Returns a GeneratedDoc with the output path.
    """
    ...
