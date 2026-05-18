"""Inventory dataset generator."""

import random


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized inventory row dicts.

    Schema: sku, item_name, quantity, warehouse, status
    """
    ...
