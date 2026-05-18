"""Contract document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party
from recordforge.core.models import DocumentData

_SCOPE_LINES = [
    "Vendor shall provide professional services as mutually agreed upon.",
    "Scope of work to be defined in the attached Statement of Work exhibit.",
    "Services include advisory, implementation, and post-launch support.",
    "Deliverables and acceptance criteria are detailed in Exhibit A.",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized contract DocumentData instance.

    No line items. Flat fee description and contract terms go in notes field.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, due_date = rand_date_pair(rng)
    flat_fee = rng.randint(5, 50) * 1000
    scope = rng.choice(_SCOPE_LINES)
    notes = (
        f"Flat Fee: ${flat_fee:,}\n\n"
        f"Scope:\n{scope}\n\n"
        "This is a fictional agreement for testing and demo purposes only. "
        "Terms and conditions are not legally binding."
    )
    return DocumentData(
        doc_type="contract",
        doc_number=f"AGR-{rng.randint(2024, 2026)}-{rng.randint(10000, 99999)}",
        doc_date=doc_date,
        due_date=due_date,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
