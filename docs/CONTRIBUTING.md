# Contributing

RecordForge is open source and contributions are welcome.

Whether you're filing a bug report, suggesting a new document type,
or submitting a pull request — this guide walks you through the rhythm:
report cleanly, suggest sharply, ship changes with care.

---

## Reporting Issues

Found a bug? You can help fix it fastest by filing a tight report.

1. Go to **Issues** → **New Issue**
2. Include:
   - What you were trying to do
   - What happened instead
   - Your Windows version and Python version (`python --version`)
   - Any error messages from the terminal
3. Do **not** paste real personal data, real file paths containing sensitive info, or screenshots with private data into issues

---

## Suggesting Features

You can shape the roadmap by opening an issue with the label
`enhancement`. Strong suggestions include:

- New document types (NDA, SOW, Work Order, etc.)
- New data set types
- UI improvements
- Export format additions

---

## Making Changes

With write access, you can ship a change end to end:

1. Create a branch from `main`:
   ```powershell
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Test locally: `python main.py`
4. Commit with a clear message:
   ```powershell
   git commit -m "Add: NDA document type"
   ```
5. Open a Pull Request against `main`
6. Do not merge your own PRs — request a review first

---

## Code Standards

Keep changes consistent with the rest of the project:

- Python 3.11+
- No external data sources — all generated content must be synthetic
- No real personal data in defaults, seeds, examples, or comments
- Keep `main.py` and `ui.html` as the two primary files — avoid splitting into multiple modules unless scope grows significantly
- All new document/data types must include the `DISCLAIMER` string in output
- Test both PDF and docx export for any new document type before submitting

---

## Privacy Rule (Non-Negotiable)

Before pushing any commit, scan your diff line by line:
- No real names, addresses, emails, or phone numbers
- No real company names
- No sample output files committed to the repo
- No internal file paths or system info in code comments

When in doubt, ask before pushing.
