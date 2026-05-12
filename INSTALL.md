# Installation & Build Guide

---

## Option 1 — Windows Installer (Recommended)

Download the latest `TestDataDocGeneratorSetup.exe` from the [Releases page](https://github.com/michaelnocito/test-data-doc-generator/releases).

1. Double-click `TestDataDocGeneratorSetup.exe`
2. Click **Next** through the install wizard
3. Click **Finish** — optionally launch the app immediately
4. Find the app in your **Start Menu** or on your **Desktop**
5. To uninstall: Windows Settings → Apps → Test Data & Document Generator → Uninstall

No Python required.

---

## Option 2 — Run from Python Source

Requires Python 3.11+ and pip.

```powershell
git clone https://github.com/michaelnocito/test-data-doc-generator.git
cd test-data-doc-generator
pip install -r requirements.txt
python main.py
```

---

## Option 3 — Build the EXE Yourself (PyInstaller)

From the project folder in PowerShell:

```powershell
pip install pyinstaller
python -m PyInstaller --name "TestDataDocGenerator" --onefile --noconsole --add-data "ui.html;." main.py
```

> Use `python -m PyInstaller` not `pyinstaller` directly.
> On Windows, pip installs PyInstaller to a user AppData folder that may not be in PATH.

Output: `dist\TestDataDocGenerator.exe`

### ui.html path fix for bundled EXE

If the UI does not load after building, update `main.py`:

```python
import sys
base_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
ui_path = base_path / "ui.html"
```

---

## Option 4 — Build the Installer Yourself (Inno Setup)

1. Install [Inno Setup](https://jrsoftware.org/isdl.php) (free)
2. Build the EXE first using Option 3 above
3. Open Inno Setup → File → Open → select `installer.iss` from the project folder
4. Press **F9** to compile
5. Installer output: `Output\TestDataDocGeneratorSetup.exe`
