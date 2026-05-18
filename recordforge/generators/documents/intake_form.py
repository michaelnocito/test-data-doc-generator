"""Intake form document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized intake form DocumentData instance.

    No line items. Body content goes in notes field.
    """
    ...
