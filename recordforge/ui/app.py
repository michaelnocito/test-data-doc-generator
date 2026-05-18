"""pywebview API bridge for the RecordForge desktop UI.

Preserves the exact JSON contract from v1:
  generate() → {"success": True, "files": list[str], "folder": str}
             or {"success": False, "error": str, "files": []}
"""

import os
import subprocess
import sys
from pathlib import Path

import webview

import recordforge as rf
from recordforge.generators.data import DATA_REGISTRY
from recordforge.generators.documents import DOCUMENT_REGISTRY


def sanitize_filename(s: str) -> str:
    """Preserve v1 sanitize_filename behavior exactly."""
    s = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(s).strip())
    return s[:100] or "output"


def open_path(path: str) -> bool:
    """Open a file or folder using the OS default handler. Preserve v1 logic exactly."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
        return True
    except Exception:
        return False


class API:
    def choose_folder(self) -> str | None:
        """Open a folder picker using pywebview's native dialog (avoids tkinter/WebView2 conflict)."""
        windows = webview.windows
        if not windows:
            return None
        result = windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if result:
            return result[0]
        return None

    def open_path(self, path: str) -> bool:
        """Open a file with its default OS handler."""
        return open_path(path)

    def open_folder(self, path: str) -> bool:
        """Open a folder in the OS file explorer."""
        return open_path(path)

    def generate(self, payload: dict) -> dict:
        """Generate files from the UI wizard payload.

        Returns {"success": True, "files": [...], "folder": str}
             or {"success": False, "error": str, "files": []}
        """
        try:
            mode = payload.get("mode", "documents")
            selected = payload.get("docTypes", [])
            qty = max(1, int(payload.get("quantity", 1)))
            fmt = (payload.get("format") or "").lower().strip()
            out_folder = (
                payload.get("outputFolder")
                or str(Path.home() / "Documents" / "recordforge")
            )

            if out_folder.startswith("~/"):
                out_folder = str(Path.home() / out_folder[2:])

            out_dir = Path(out_folder)
            out_dir.mkdir(parents=True, exist_ok=True)

            doc_keys = [t for t in selected if t in DOCUMENT_REGISTRY]
            data_keys = [t for t in selected if t in DATA_REGISTRY]
            wants_docs = mode in ("documents", "both")
            wants_data = mode in ("data", "both")
            generated_files: list[str] = []

            if wants_docs:
                if fmt not in {"pdf", "docx", "html"}:
                    raise ValueError("Choose a document format before generating documents.")
                for doc_type in doc_keys:
                    docs = rf.generate(type=doc_type, format=fmt, count=qty, output=out_folder)
                    generated_files.extend(str(d.path) for d in docs)

            if wants_data:
                for dataset in data_keys:
                    docs = rf.generate(type=dataset, format="xlsx", count=qty, output=out_folder)
                    generated_files.extend(str(d.path) for d in docs)

            return {"success": True, "files": generated_files, "folder": str(out_dir)}

        except Exception as exc:
            return {"success": False, "error": str(exc), "files": []}
