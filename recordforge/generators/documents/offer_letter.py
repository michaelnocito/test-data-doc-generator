"""Offer letter document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized offer letter DocumentData instance.

    No line items. Salary, position, and start date go in notes field.
    """
    ...
