"""Typer CLI for RecordForge."""

from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(name="recordforge", help="Generate synthetic documents and data files.")


@app.command()
def generate(
    type: str = typer.Option(..., help="Document or data type key"),
    format: str = typer.Option(..., help="Output format: pdf | docx | html | xlsx"),
    count: int = typer.Option(1, help="Number of files to generate (1–100)"),
    output: Optional[Path] = typer.Option(None, help="Output directory"),
    seed: Optional[int] = typer.Option(None, help="Integer seed for reproducible output"),
) -> None:
    """Generate synthetic documents or data files."""
    ...


@app.command(name="list-types")
def list_types() -> None:
    """Print all available document and data type keys."""
    ...


@app.command()
def version() -> None:
    """Print the RecordForge version."""
    ...
