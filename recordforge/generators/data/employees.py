"""Employees dataset generator."""

import random

from recordforge.core.faker_utils import rand_person, rand_phone


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized employee row dicts.

    Schema: employee_id, name, department, title, phone
    """
    departments = ["HR", "Finance", "IT", "Operations", "Legal", "Marketing", "Procurement"]
    titles = ["Analyst", "Manager", "Coordinator", "Specialist", "Director", "Associate", "Lead"]
    rows = []
    for i in range(count):
        rows.append({
            "employee_id": f"EMP-{1000 + i}",
            "name": rand_person(rng),
            "department": rng.choice(departments),
            "title": rng.choice(titles),
            "phone": rand_phone(rng),
        })
    return rows
