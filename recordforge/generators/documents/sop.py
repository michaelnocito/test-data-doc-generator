"""Standard operating procedure document generator."""

import random

from recordforge.core.models import DocumentData


def build(rng: random.Random) -> DocumentData:
    """Build a randomized SOP DocumentData instance.

    No line items. Procedure steps go in notes field.
    """
    ...
