"""RecordForge — synthetic document and data file generator."""

from pathlib import Path

from recordforge.core.models import GeneratedDoc
from recordforge.core.seed import set_seed

__version__ = "2.0.0"


def generate(
    type: str,
    format: str,
    count: int = 1,
    output: str | Path | None = None,
    seed: int | None = None,
) -> list[GeneratedDoc]:
    """Generate synthetic documents or data files.

    Returns a list of GeneratedDoc instances, one per file created.
    Raises ValueError for invalid type/format combinations.
    """
    from recordforge.core.seed import get_rng, set_seed as _set_seed
    from recordforge.generators.data import DATA_REGISTRY
    from recordforge.generators.documents import DOCUMENT_REGISTRY
    from recordforge.renderers import docx, html, pdf, xlsx

    if seed is not None:
        _set_seed(seed)

    rng = get_rng()
    out_dir = Path(output) if output else Path.home() / "Documents" / "recordforge"
    out_dir.mkdir(parents=True, exist_ok=True)
    count = max(1, min(count, 100))

    results: list[GeneratedDoc] = []

    if type in DOCUMENT_REGISTRY:
        if format not in {"pdf", "docx", "html"}:
            raise ValueError(
                f"Format '{format}' is not valid for document types. Use pdf, docx, or html."
            )
        _doc_renderers = {"pdf": pdf.render, "docx": docx.render, "html": html.render}
        builder = DOCUMENT_REGISTRY[type]
        renderer = _doc_renderers[format]
        for _ in range(count):
            results.append(renderer(builder(rng), out_dir))

    elif type in DATA_REGISTRY:
        if format != "xlsx":
            raise ValueError(
                f"Format '{format}' is not valid for data types. Use xlsx."
            )
        builder = DATA_REGISTRY[type]
        for _ in range(count):
            results.append(xlsx.render(type, builder(rng), out_dir))

    else:
        valid = sorted(DOCUMENT_REGISTRY) + sorted(DATA_REGISTRY)
        raise ValueError(f"Unknown type '{type}'. Valid types: {', '.join(valid)}")

    return results


def list_types() -> dict[str, list[str]]:
    """Return all available type keys grouped by category."""
    from recordforge.generators.data import DATA_REGISTRY
    from recordforge.generators.documents import DOCUMENT_REGISTRY

    return {
        "documents": sorted(DOCUMENT_REGISTRY.keys()),
        "data": sorted(DATA_REGISTRY.keys()),
    }


__all__ = ["generate", "list_types", "set_seed", "GeneratedDoc", "__version__"]
