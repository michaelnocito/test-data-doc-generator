"""Messy dataset generator — intentionally dirty data for ETL testing."""

import random

from recordforge.core.faker_utils import rand_person


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of intentionally messy row dicts.

    Schema: raw_name, email, amount, status, duplicate_key
    Includes nulls, inconsistent casing, and duplicate keys by design.
    """
    rows = []
    for i in range(count):
        name = rand_person(rng)
        amount_int = rng.randint(10, 9999)
        rows.append({
            "raw_name": rng.choice([name, name.lower(), "", None]),
            "email": rng.choice([
                f"user{i}@example.com", f"USER{i}@EXAMPLE.COM", "", None,
            ]),
            "amount": rng.choice([amount_int, f"${amount_int}", "", None]),
            "status": rng.choice(["active", "ACTIVE", " pending ", "", None]),
            "duplicate_key": rng.choice([
                f"DUP-{i // 3}", f"DUP-{i // 5}", "", None,
            ]),
        })
    return rows
