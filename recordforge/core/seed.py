"""RNG singleton with seed control.

All randomness in the codebase flows through get_rng(). Never call
random module globals directly.
"""

import random
import secrets

_rng: random.Random = random.Random(secrets.randbits(64))


def get_rng() -> random.Random:
    """Return the shared Random instance."""
    return _rng


def set_seed(n: int) -> None:
    """Replace the shared RNG with a seeded instance for reproducible output."""
    global _rng
    _rng = random.Random(n)
