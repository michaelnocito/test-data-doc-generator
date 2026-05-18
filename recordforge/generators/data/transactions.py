"""Transactions dataset generator."""

import random
from datetime import date, timedelta


def build_rows(rng: random.Random, count: int = 50) -> list[dict]:
    """Build a list of randomized transaction row dicts.

    Schema: txn_id, account, amount, currency, posted_date
    """
    rows = []
    for i in range(count):
        posted = date.today() + timedelta(days=rng.randint(-180, 0))
        rows.append({
            "txn_id": f"TXN-{100000 + i}",
            "account": f"ACCT-{rng.randint(1000, 9999)}",
            "amount": rng.randint(50, 5000),
            "currency": "USD",
            "posted_date": posted.strftime("%Y-%m-%d"),
        })
    return rows
