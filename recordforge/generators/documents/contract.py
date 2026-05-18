"""Contract document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized contract DocumentData instance.

    No line items. Flat fee description and contract terms go in notes field.
    """
    ...
