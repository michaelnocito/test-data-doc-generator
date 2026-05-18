"""Purchase order document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_line_items, rand_party
from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized purchase order DocumentData instance.

    Line items: 3–6 products.
    Dates: doc_date < due_date always.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, due_date = rand_date_pair(rng)
    return DocumentData(
        doc_type="purchase_order",
        doc_number=f"PO-{rng.randint(100000, 999999)}",
        doc_date=doc_date,
        due_date=due_date,
        buyer=buyer,
        vendor=vendor,
        line_items=rand_line_items(rng, "products", rng.randint(3, 6)),
    )
