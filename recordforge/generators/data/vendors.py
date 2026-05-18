"""Vendors dataset generator."""

import random

from recordforge.core.faker_utils import rand_company, rand_person, rand_phone


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized vendor row dicts.

    Schema: vendor_id, vendor_name, contact_name, phone, status
    """
    statuses = ["Active", "Pending", "Inactive"]
    rows = []
    for i in range(count):
        rows.append({
            "vendor_id": f"VEND-{1000 + i}",
            "vendor_name": rand_company(rng),
            "contact_name": rand_person(rng),
            "phone": rand_phone(rng),
            "status": rng.choice(statuses),
        })
    return rows
