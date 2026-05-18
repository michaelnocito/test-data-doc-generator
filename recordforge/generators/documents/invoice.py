"""Invoice document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized invoice DocumentData instance.

    Line items: 2–4 services.
    Dates: doc_date < due_date always.
    """
    ...
