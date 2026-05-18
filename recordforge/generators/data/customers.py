"""Customers dataset generator."""

import random

from recordforge.core.faker_utils import rand_company, rand_email, rand_person, rand_phone


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized customer row dicts.

    Schema: customer_id, name, company, email, phone
    """
    rows = []
    for i in range(count):
        company = rand_company(rng)
        rows.append({
            "customer_id": f"CUST-{1000 + i}",
            "name": rand_person(rng),
            "company": company,
            "email": rand_email(rng, company),
            "phone": rand_phone(rng),
        })
    return rows
