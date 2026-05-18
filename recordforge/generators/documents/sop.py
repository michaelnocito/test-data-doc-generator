"""Standard operating procedure document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_DEPARTMENTS = [
    "Operations", "Finance", "IT", "Human Resources",
    "Compliance", "Procurement", "Customer Success",
]

_PROCEDURES = [
    [
        "Receive and log the incoming request.",
        "Validate all required fields are populated.",
        "Route to the assigned specialist queue.",
        "Confirm receipt with the requesting party.",
        "Log completion status in the tracking system.",
    ],
    [
        "Review submitted documentation for completeness.",
        "Cross-reference against current policy guidelines.",
        "Escalate any discrepancies to the department lead.",
        "Issue acknowledgment within one business day.",
        "Archive finalized records per retention schedule.",
    ],
    [
        "Initiate the intake checklist upon request receipt.",
        "Assign a case owner from the available specialist pool.",
        "Schedule kickoff call within 48 hours.",
        "Capture meeting notes and distribute to stakeholders.",
        "Close the record upon written sign-off.",
    ],
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized SOP DocumentData instance.

    No line items. Procedure steps go in notes field.
    """
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, _ = rand_date_pair(rng)
    owner = rand_person(rng)
    dept = rng.choice(_DEPARTMENTS)
    steps = rng.choice(_PROCEDURES)
    numbered = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
    notes = f"Department: {dept}\nOwner: {owner}\n\nProcedure:\n{numbered}"
    return DocumentData(
        doc_type="sop",
        doc_number=f"SOP-{rng.randint(1000, 9999)}",
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
