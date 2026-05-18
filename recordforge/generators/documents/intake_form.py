"""Intake form document generator."""

import random
import secrets

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_SERVICES = [
    "Platform onboarding and implementation review",
    "Data migration assessment and scoping",
    "System integration discovery",
    "Compliance gap analysis",
    "Infrastructure readiness review",
    "Vendor evaluation support",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized intake form DocumentData instance.

    No line items. Body content goes in notes field.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, _ = rand_date_pair(rng)
    contact = rand_person(rng)
    service = rng.choice(_SERVICES)
    notes = (
        f"Primary Contact: {contact}\n"
        f"{buyer.phone}\n\n"
        f"Requested Service:\n{service}"
    )
    return DocumentData(
        doc_type="intake_form",
        doc_number=f"INT-{secrets.token_hex(4).upper()}",
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
