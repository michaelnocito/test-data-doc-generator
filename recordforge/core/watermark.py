"""Diagonal SAMPLE watermark overlay for reportlab PDFs."""

from reportlab.lib.pagesizes import LETTER


def apply_watermark(canvas, doc) -> None:
    """Apply diagonal SAMPLE watermark centered on the page.

    Pass as onFirstPage and onLaterPages to SimpleDocTemplate so every
    page receives the watermark.
    """
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 72)
    canvas.setFillColorRGB(1, 0, 0, alpha=0.15)
    canvas.translate(LETTER[0] / 2, LETTER[1] / 2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "SAMPLE")
    canvas.restoreState()
