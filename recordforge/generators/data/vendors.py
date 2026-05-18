"""Vendors dataset generator."""

import random


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized vendor row dicts.

    Schema: vendor_id, vendor_name, contact_name, phone, status
    """
    ...
