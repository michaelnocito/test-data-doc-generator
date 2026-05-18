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

from recordforge.core.faker_utils import sanitize_filename
from recordforge.core.models import DocumentData, GeneratedDoc
from recordforge.core.watermark import apply_watermark

_FOOTER = (
    "FICTIONAL — For testing, demo, and training use only. "
    "Not a valid legal or financial document."
)
_LIGHT_GRAY = colors.HexColor("#F4F4F4")
_HEADER_GRAY = colors.HexColor("#E0E0E0")
_LABEL_COLOR = colors.HexColor("#888888")


def _page_decorations(canvas, doc) -> None:
    """Watermark + footer on every page."""
    apply_watermark(canvas, doc)
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.lightgrey)
    canvas.drawCentredString(LETTER[0] / 2, 0.45 * inch, _FOOTER)
    canvas.restoreState()


def render(data: DocumentData, output_dir: Path) -> GeneratedDoc:
    """Render a DocumentData instance to a PDF file."""
    stem = sanitize_filename(f"{data.doc_type}_{secrets.token_hex(3)}")
    path = output_dir / f"{stem}.pdf"

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "RFTitle", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=18, spaceAfter=4,
    )
    label_style = ParagraphStyle(
        "RFLabel", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=7,
        textColor=_LABEL_COLOR, spaceAfter=2,
    )
    party_name_style = ParagraphStyle(
        "RFPartyName", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=9,
    )
    body_style = ParagraphStyle(
        "RFBody", parent=styles["Normal"], fontSize=9, leading=13,
    )
    footer_style = ParagraphStyle(
        "RFFooter", parent=styles["Normal"],
        fontSize=7, textColor=colors.lightgrey, alignment=1,
    )

    story = []

    # --- Header block ---
    title_text = data.doc_type.replace("_", " ").title()
    meta_right = data.doc_number
    if data.due_date:
        meta_right += f"   ·   Due: {data.due_date}"

    header_data = [[
        Paragraph(title_text, title_style),
        Paragraph(
            f'<para align="right"><font size="9" color="#888888">'
            f'{data.doc_number}<br/>{data.doc_date}</font></para>',
            styles["Normal"],
        ),
    ]]
    header_table = Table(header_data, colWidths=[4 * inch, 3 * inch])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10))

    # --- Party block ---
    def _party_cell(label: str, party) -> list:
        return [
            Paragraph(label, label_style),
            Paragraph(party.name, party_name_style),
            Paragraph(party.address1, body_style),
            Paragraph(party.address2, body_style),
            Paragraph(party.phone, body_style),
            Paragraph(party.email, body_style),
        ]

    party_table = Table(
        [[_party_cell("BILL TO", data.buyer), _party_cell("FROM", data.vendor)]],
        colWidths=[3.5 * inch, 3.5 * inch],
    )
    party_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 20),
    ]))
    story.append(party_table)
    story.append(Spacer(1, 0.25 * inch))

    # --- Line items table ---
    if data.line_items:
        col_widths = [3.75 * inch, 0.6 * inch, 1.25 * inch, 1.1 * inch]
        rows = [["Description", "Qty", "Unit Price", "Total"]]
        for item in data.line_items:
            rows.append([
                item.description,
                str(item.quantity),
                f"${item.unit_price:,.2f}",
                f"${item.total:,.2f}",
            ])
        rows.append(["", "", "Subtotal", f"${data.subtotal:,.2f}"])
        rows.append(["", "", "Tax (8%)", f"${data.tax:,.2f}"])
        rows.append(["", "", "Total Due", f"${data.total_due:,.2f}"])

        n = len(data.line_items)
        ts = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), _HEADER_GRAY),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, n), 0.25, colors.HexColor("#CCCCCC")),
            ("LINEABOVE", (2, n + 1), (-1, n + 1), 0.5, colors.grey),
            ("FONTNAME", (2, n + 3), (-1, n + 3), "Helvetica-Bold"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
        # Alternating row shading on data rows
        for i in range(2, n + 1, 2):
            ts.add("BACKGROUND", (0, i), (-1, i), _LIGHT_GRAY)

        item_table = Table(rows, colWidths=col_widths)
        item_table.setStyle(ts)
        story.append(item_table)
        story.append(Spacer(1, 0.2 * inch))

    # --- Notes ---
    if data.notes:
        for line in data.notes.split("\n"):
            story.append(Paragraph(line or "&nbsp;", body_style))
        story.append(Spacer(1, 0.2 * inch))

    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=inch,
    )
    doc.build(story, onFirstPage=_page_decorations, onLaterPages=_page_decorations)

    return GeneratedDoc(path=path, doc_type=data.doc_type, format="pdf")
