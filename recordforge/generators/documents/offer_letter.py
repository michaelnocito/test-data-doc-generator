"""Offer letter document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_POSITIONS = [
    "Business Systems Analyst",
    "Data Engineer",
    "Project Manager",
    "Operations Coordinator",
    "Financial Analyst",
    "IT Specialist",
    "Solutions Architect",
    "Compliance Officer",
    "Product Manager",
    "Senior Consultant",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized offer letter DocumentData instance.

    No line items. Salary, position, and start date go in notes field.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, start_date = rand_date_pair(rng)
    candidate = rand_person(rng)
    position = rng.choice(_POSITIONS)
    salary = rng.randint(55, 145) * 1000
    notes = (
        f"Candidate: {candidate}\n\n"
        f"Position: {position}\n\n"
        f"Compensation:\n"
        f"Base Salary: ${salary:,}\n"
        f"Start Date: {start_date}"
    )
    return DocumentData(
        doc_type="offer_letter",
        doc_number=f"OFR-{rng.randint(100000, 999999)}",
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
