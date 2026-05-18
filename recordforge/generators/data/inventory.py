"""Inventory dataset generator."""

import random

from recordforge.core.faker_utils import PRODUCTS


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized inventory row dicts.

    Schema: sku, item_name, quantity, warehouse, status
    """
    warehouses = ["East", "West", "Central", "North", "South"]
    statuses = ["In Stock", "Low Stock", "Backorder"]
    rows = []
    for i in range(count):
        rows.append({
            "sku": f"SKU-{10000 + i}",
            "item_name": rng.choice(PRODUCTS),
            "quantity": rng.randint(0, 250),
            "warehouse": rng.choice(warehouses),
            "status": rng.choice(statuses),
        })
    return rows
