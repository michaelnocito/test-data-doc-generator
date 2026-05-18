"""Purchase order document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized purchase order DocumentData instance.

    Line items: 3–6 products.
    Dates: doc_date < due_date always.
    """
    ...
