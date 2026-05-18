"""RecordForge — synthetic document and data file generator."""

from pathlib import Path

from recordforge.core.models import GeneratedDoc
from recordforge.core.seed import set_seed


def generate(
    type: str,
    format: str,
    count: int = 1,
    output: str | Path | None = None,
    seed: int | None = None,
) -> list[GeneratedDoc]:
    """Generate synthetic documents or data files.

    Returns a list of GeneratedDoc instances, one per file created.
    """
    ...


def list_types() -> dict[str, list[str]]:
    """Return all available type keys grouped by category.

    Returns {"documents": [...], "data": [...]}
    """
    ...


__all__ = ["generate", "list_types", "set_seed", "GeneratedDoc"]
