"""Diagonal SAMPLE watermark overlay for reportlab PDFs."""

from reportlab.lib.pagesizes import LETTER


def apply_watermark(canvas, doc) -> None:
    """Apply diagonal SAMPLE watermark centered on the page.

    Pass as onFirstPage and onLaterPages to SimpleDocTemplate so every
    page receives the watermark.
    """
    ...
