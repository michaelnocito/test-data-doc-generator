"""Invoice document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_line_items, rand_party
from recordforge.core.models import DocumentData

_PAYMENT_METHODS = [
    "ACH / Electronic Funds Transfer",
    "Check (payable to {vendor})",
    "Wire Transfer",
]

_PAYMENT_TERMS_NOTES = [
    "Payment is due within 30 days of the invoice date (Net 30). Invoices outstanding beyond 30 days are subject to a late fee of 1.5% per month on the unpaid balance.",
    "Payment is due within 45 days of the invoice date (Net 45). A 2% early payment discount is available if payment is received within 10 days (2/10 Net 45).",
    "Payment is due upon receipt of this invoice. For questions regarding payment, contact our billing department at the address or email listed above.",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized invoice DocumentData instance.

    Line items: 2–4 services.
    Dates: doc_date < due_date always.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, due_date = rand_date_pair(rng)
    line_items = rand_line_items(rng, "services", rng.randint(2, 4))
    payment_method = rng.choice(_PAYMENT_METHODS).format(vendor=vendor.name)
    payment_note = rng.choice(_PAYMENT_TERMS_NOTES)
    inv_num = f"INV-{rng.randint(100000, 999999)}"

    notes = f"""PAYMENT TERMS

{payment_note}

Preferred Payment Method: {payment_method}

Please reference invoice number {inv_num} on all payments and correspondence.

REMITTANCE INFORMATION

Payable To: {vendor.name}
Mailing Address: {vendor.address1}, {vendor.address2}
Email: {vendor.email}
Phone: {vendor.phone}

QUESTIONS

If you have any questions regarding this invoice, please contact our billing team at {vendor.email} or {vendor.phone}. We are available Monday through Friday, 9:00 AM – 5:00 PM local time.

Thank you for your business."""

    return DocumentData(
        doc_type="invoice",
        doc_number=inv_num,
        doc_date=doc_date,
        due_date=due_date,
        buyer=buyer,
        vendor=vendor,
        line_items=line_items,
        notes=notes,
    )
