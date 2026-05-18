"""Transactions dataset generator."""

import random


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized transaction row dicts.

    Schema: txn_id, account, amount, currency, posted_date
    """
    ...
