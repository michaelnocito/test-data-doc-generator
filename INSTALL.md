# Building a Windows EXE (Optional)

If you want to share this app without requiring Python to be installed, you can build a standalone `.exe` using PyInstaller.

---

## Prerequisites

- Windows 10 or Windows 11
- Python 3.11+
- All dependencies installed:

```powershell
pip install -r requirements.txt
```

- PyInstaller installed:

```powershell
pip install pyinstaller
```

---

## Build the EXE

From the project folder in PowerShell:

```powershell
python -m PyInstaller --name "TestDataDocGenerator" --onefile --noconsole --add-data "ui.html;." main.py
```

> **Note:** Use `python -m PyInstaller` instead of `pyinstaller` directly.
> On Windows, pip sometimes installs PyInstaller to a user AppData folder that is not in your PATH.
> Calling it via `python -m PyInstaller` bypasses this issue every time.

### What each flag does

| Flag | Purpose |
|---|---|
| `--name` | Sets the output `.exe` filename |
| `--onefile` | Bundles everything into a single `.exe` |
| `--noconsole` | Hides the terminal window when running |
| `--add-data "ui.html;."` | Includes `ui.html` inside the bundle |

---

## Output

After the build completes (1–2 minutes), your EXE will be at:

```
dist\TestDataDocGenerator.exe
```

You can copy this file anywhere and run it on any Windows 10/11 machine — no Python installation required.

---

## Important: `ui.html` Path Fix for EXE

When running as a bundled `.exe`, PyInstaller extracts files to a temp folder. If the UI does not load after building, update the `ui_path` line in `main.py` from:

```python
ui_path = Path(__file__).parent / "ui.html"
```

To:

```python
import sys
base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
ui_path = base_path / "ui.html"
```

This tells PyInstaller where to find `ui.html` inside the temp bundle at runtime.

---

## Optional: Create a Desktop Installer (Inno Setup)

For a proper Windows installer with a Start Menu shortcut and uninstaller:

1. Download [Inno Setup](https://jrsoftware.org/isinfo.php) (free)
2. Point it at `dist\TestDataDocGenerator.exe`
3. Follow the wizard to generate a `.exe` installer package

This is optional and only needed if you plan to distribute the app widely.
