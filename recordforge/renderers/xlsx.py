"""XLSX renderer using openpyxl.

Behavior preserved exactly from v1: disclaimer row, bold header row with
green fill, auto-width columns capped at 28 chars.
"""

import secrets
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from recordforge.core.models import GeneratedDoc

DISCLAIMER = "FICTIONAL TEST DATA ONLY - generated for testing, demo, or training use."


def render(dataset: str, rows: list[dict], output_dir: Path) -> GeneratedDoc:
    """Render dataset rows to an XLSX file.

    Returns a GeneratedDoc with the output path.
    """
    ...
