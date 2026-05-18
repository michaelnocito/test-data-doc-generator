"""Messy dataset generator — intentionally dirty data for ETL testing."""

import random


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of intentionally messy row dicts.

    Schema: raw_name, email, amount, status, duplicate_key
    Includes nulls, inconsistent casing, and duplicate keys by design.
    """
    ...
