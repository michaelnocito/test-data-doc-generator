"""Purchase order document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_line_items, rand_party
from recordforge.core.models import DocumentData

_SHIPPING_TERMS = [
    "FOB Destination — title and risk of loss transfer upon delivery to the ship-to address.",
    "FOB Origin — title and risk of loss transfer upon pickup from vendor's location. Buyer assumes freight costs.",
    "DDP (Delivered Duty Paid) — vendor is responsible for all shipping costs, duties, and customs clearance.",
]

_PO_CONDITIONS = """PURCHASE ORDER TERMS AND CONDITIONS

1. Acceptance. Vendor's acknowledgment of this Purchase Order, delivery of goods, or commencement of services shall constitute acceptance of all terms and conditions stated herein. Additional or conflicting terms in Vendor's acknowledgment are rejected unless expressly agreed to in writing by Buyer.

2. Delivery. Time is of the essence. Vendor must notify Buyer within 48 hours of any anticipated delay. Buyer reserves the right to cancel the order or purchase substitute goods elsewhere if delivery is not made by the required date, with any cost difference charged to Vendor.

3. Inspection and Acceptance. Buyer reserves the right to inspect all goods upon delivery. Goods not conforming to specifications may be returned at Vendor's expense. Acceptance of delivery does not waive Buyer's right to revoke acceptance for latent defects discovered after inspection.

4. Invoicing. Vendor shall submit invoices referencing this Purchase Order number to the accounts payable contact listed herein. Invoices without a valid PO number will not be processed.

5. Payment. Payment terms are Net 45 from receipt of conforming goods and correct invoice, unless otherwise stated on this PO. Buyer may withhold payment on disputed quantities without interest pending resolution.

6. Warranty. Vendor warrants that all goods: (a) are free from defects in materials and workmanship; (b) conform to applicable specifications; (c) are new and not refurbished unless expressly specified; and (d) do not infringe any third-party intellectual property rights.

7. Compliance. Vendor shall comply with all applicable federal, state, and local laws, including occupational safety, environmental, and labor laws. Vendor certifies that goods were produced in compliance with all applicable labor standards.

8. Confidentiality. Vendor shall keep the contents of this Purchase Order confidential and shall not use Buyer's name in any publicity or marketing without prior written consent.

9. Governing Law. This Purchase Order shall be governed by the laws of the state of Buyer's principal place of business."""


def build(rng: random.Random) -> DocumentData:
    """Build a randomized purchase order DocumentData instance.

    Line items: 3–6 products.
    Dates: doc_date < due_date always.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, due_date = rand_date_pair(rng)
    line_items = rand_line_items(rng, "products", rng.randint(3, 6))
    shipping_terms = rng.choice(_SHIPPING_TERMS)
    po_num = f"PO-{rng.randint(100000, 999999)}"

    notes = f"""DELIVERY INFORMATION

Ship To:
{buyer.name}
Attn: Receiving Department
{buyer.address1}
{buyer.address2}

Required Delivery Date: {due_date}
Shipping Terms: {shipping_terms}

All shipments must include a packing slip referencing PO number {po_num}. Partial shipments are permitted but must be noted on the packing slip. Contact {buyer.email} to schedule receiving appointments for large orders.

VENDOR CONFIRMATION

Vendor must confirm receipt and acceptance of this Purchase Order within two (2) business days by contacting {buyer.email} or {buyer.phone}. Failure to confirm within this timeframe may result in order cancellation.

ACCOUNTS PAYABLE CONTACT

Questions regarding payment should be directed to {buyer.email}. Please reference PO number {po_num} on all invoices and correspondence.

{_PO_CONDITIONS}"""

    return DocumentData(
        doc_type="purchase_order",
        doc_number=po_num,
        doc_date=doc_date,
        due_date=due_date,
        buyer=buyer,
        vendor=vendor,
        line_items=line_items,
        notes=notes,
    )
