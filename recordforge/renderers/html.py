"""HTML renderer using Jinja2 templates.

Template: renderers/templates/document.html.j2
CSS diagonal SAMPLE watermark via body::before pseudo-element.
"""

import secrets
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from recordforge.core.faker_utils import sanitize_filename
from recordforge.core.models import DocumentData, GeneratedDoc

_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render(data: DocumentData, output_dir: Path) -> GeneratedDoc:
    """Render a DocumentData instance to an HTML file."""
    stem = sanitize_filename(f"{data.doc_type}_{secrets.token_hex(3)}")
    path = output_dir / f"{stem}.html"

    env = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)), autoescape=True)
    template = env.get_template("document.html.j2")
    path.write_text(template.render(data=data), encoding="utf-8")

    return GeneratedDoc(path=path, doc_type=data.doc_type, format="html")
