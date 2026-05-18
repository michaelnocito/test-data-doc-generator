"""HTML renderer using Jinja2 templates.

Template: renderers/templates/document.html.j2
CSS diagonal SAMPLE watermark via body::before pseudo-element.
"""

import secrets
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from recordforge.core.models import DocumentData, GeneratedDoc

_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render(data: DocumentData, output_dir: Path) -> GeneratedDoc:
    """Render a DocumentData instance to an HTML file.

    Returns a GeneratedDoc with the output path.
    """
    ...
