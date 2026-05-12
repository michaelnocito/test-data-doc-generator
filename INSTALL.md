# Building a Windows EXE (Optional)

If you want to share this app without requiring Python to be installed, you can build a standalone `.exe` using PyInstaller.

---

## Prerequisites

- Python 3.11+
- All dependencies installed: `pip install -r requirements.txt`
- PyInstaller: `pip install pyinstaller`

---

## Build the EXE

From the project folder in PowerShell:

```powershell
pyinstaller `
  --name "TestDataDocGenerator" `
  --onefile `
  --noconsole `
  --add-data "ui.html;." `
  main.py
```

### What each flag does

| Flag | Purpose |
|---|---|
| `--name` | Sets the output `.exe` filename |
| `--onefile` | Bundles everything into a single `.exe` |
| `--noconsole` | Hides the terminal window when running |
| `--add-data "ui.html;."` | Includes `ui.html` inside the bundle |

---

## Output

After the build completes, your EXE will be at:

```
dist\TestDataDocGenerator.exe
```

You can copy this file anywhere and run it on any Windows 10/11 machine — no Python installation required.

---

## Important: `ui.html` Path Fix for EXE

When running as a bundled `.exe`, PyInstaller extracts files to a temp folder. You need to handle this in `main.py`. The current code already handles this correctly via:

```python
ui_path = Path(__file__).parent / "ui.html"
```

If you ever run the built EXE and the UI does not load, update that line to:

```python
import sys
base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
ui_path = base_path / "ui.html"
```

This tells PyInstaller where to find `ui.html` inside the temp bundle.

---

## Optional: Create a Desktop Shortcut Installer (Inno Setup)

For a proper Windows installer with a Start Menu shortcut and uninstaller:

1. Download [Inno Setup](https://jrsoftware.org/isinfo.php) (free)
2. Point it at `dist\TestDataDocGenerator.exe`
3. Follow the wizard to create a `.exe` installer

This is optional and only needed if you plan to distribute the app to others.
