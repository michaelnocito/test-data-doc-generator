# Troubleshooting

Hit a snag? You can usually unstick the app in a minute or two. Find
your symptom below and follow the fix.

---

## App window opens but is blank white

**Cause:** WebView2 runtime is missing or outdated on the machine.

**Fix:** Download and install the [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) (free, from Microsoft). pywebview on Windows requires WebView2. After installing, relaunch the app.

---

## App opens as raw text / HTML code instead of a window

**Cause:** pywebview was passed a file path via `url=` instead of the HTML content directly. Windows can mishandle local file paths in the WebView2 component and render raw source instead of the page.

**Fix:** Ensure `main.py` loads `ui.html` using `html=` not `url=`:

```python
html = ui_path.read_text(encoding="utf-8")
webview.create_window("...", html=html, js_api=api, ...)
```

---

## Dev tools / inspect window pops up on launch

**Cause:** `webview.start(debug=True)` opens the browser dev tools panel alongside the app.

**Fix:** Set `debug=False` in `main.py`:

```python
webview.start(debug=False)
```

---

## `pyinstaller` is not recognized in PowerShell

**Cause:** pip installed PyInstaller to a user AppData folder that is not in your system PATH.

**Fix:** Call PyInstaller via Python directly:

```powershell
python -m PyInstaller --name "TestDataDocGenerator" --onefile --noconsole --add-data "ui.html;." main.py
```

---

## Generate button stays on "Generating…" and nothing happens

**Cause:** A Python exception occurred in the backend `generate()` function and was not surfaced to the UI.

**Fix:**
1. Temporarily set `debug=True` in `webview.start()` to open dev tools
2. Check the Console tab for JavaScript errors
3. Re-run from PowerShell — Python exceptions will print to the terminal
4. Common causes: missing output folder permissions, unsupported output path with special characters

---

## PDF files are blank or missing content

**Cause:** ReportLab line drawing clipped all text above the page margin.

**Fix:** This is handled automatically in the current build. If you see blank PDFs, ensure you are running the latest `main.py` from this repo — older versions had a y-position bug.

---

## Output folder shows `~/Documents/sample_docs` but files go somewhere unexpected

**Cause:** The `~` path prefix is resolved at runtime by Python's `Path.home()`. On some Windows setups this resolves to a network or roaming profile path.

**Fix:** Use the **Change…** button in the app to pick an explicit local folder (e.g. `C:\Users\YourName\Desktop\test_output`) instead of the default.

---

## Excel files open but show no data rows

**Cause:** A data type was selected in **Both** mode but the mode filter excluded it.

**Fix:** On Step 1, confirm you selected the correct mode (**Data Files** or **Both**) and that the data type checkbox is checked and highlighted in orange.

---

## `ModuleNotFoundError` when running `main.py`

**Cause:** One or more dependencies are not installed.

**Fix:**

```powershell
pip install -r requirements.txt
```

If that still fails, install manually:

```powershell
pip install pywebview reportlab python-docx openpyxl
```
