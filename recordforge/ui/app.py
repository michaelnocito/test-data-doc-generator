"""pywebview API bridge for the RecordForge desktop UI.

Preserves the exact JSON contract from v1:
  generate() → {"success": bool, "files": list[str], "folder": str}
             or {"success": false, "error": str, "files": []}
"""

import os
import subprocess
import sys
from pathlib import Path
from tkinter import Tk, filedialog

from recordforge import generate
from recordforge.core.models import GeneratedDoc


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
        """Open a folder picker dialog and return the selected path."""
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        folder = filedialog.askdirectory()
        root.destroy()
        return folder or None

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
        ...
