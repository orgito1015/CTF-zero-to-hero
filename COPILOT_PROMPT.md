# 🤖 GitHub Copilot Agent Prompt
## Use this prompt to have Copilot help build out the CTF Zero to Hero toolkit

---

## PROMPT (copy-paste into Copilot Chat or Agent mode)

```
You are helping build a CTF (Capture The Flag) learning repository called "ctf-zero-to-hero".
This is a beginner-focused toolkit for competitive cybersecurity competitions.

The repository already contains:
- README.md with project overview
- scripts/setup.sh — environment setup
- scripts/recon.py — auto-recon helper
- scripts/crypto_solver.py — encoding/cipher identifier
- challenges/web/NOTES_TEMPLATE.md
- challenges/crypto/NOTES_TEMPLATE.md
- challenges/pwn/NOTES_TEMPLATE.md
- challenges/forensics/NOTES_TEMPLATE.md
- challenges/re/NOTES_TEMPLATE.md
- presentation/CTF_Beginners.pptx — the full slide deck

Please help me with the following tasks:

TASK 1 — Create scripts/flag_hunter.py
A script that recursively searches a directory or file for CTF flag patterns.
Should support: custom flag prefix (default "CTF"), search inside zip/tar archives,
search inside image EXIF data, binary files, and text files.
Output should be colorized and show file path + line/offset of each match.

TASK 2 — Create scripts/pwn_template.py  
An interactive pwntools exploit template generator.
Ask the user:
  - Binary path
  - Remote host:port (optional)
  - Is there a known win function? (y/n)
  - Is there a libc? (y/n)
Then generate a ready-to-run exploit.py tailored to their answers.

TASK 3 — Create resources/payloads/web_payloads.txt
A categorized collection of web exploitation payloads including:
  - SQL Injection (MySQL, PostgreSQL, SQLite, MSSQL variants)
  - XSS (reflected, stored, DOM-based)
  - SSTI for Jinja2, Twig, Freemarker, ERB
  - Path traversal / LFI
  - Command injection
  - XXE payloads
  - SSRF bypass techniques

TASK 4 — Create a GitHub Actions workflow (.github/workflows/test.yml)
That runs on push to main and:
  - Sets up Python 3.11
  - Installs dependencies (pwntools, pycryptodome, requests)
  - Runs any Python scripts in scripts/ with --help to verify they don't crash
  - Validates all markdown files have a "Flag" section (grep check)

TASK 5 — Add docstrings and type hints to all existing Python scripts
Go through scripts/recon.py and scripts/crypto_solver.py and add:
  - Module-level docstring
  - Function-level docstrings with Args/Returns
  - Type hints on all function signatures
  - Input validation where missing

For all tasks: write clean, well-commented code. Use Python 3.10+ features where appropriate.
Keep the beginner-friendly philosophy — add comments explaining WHY, not just what.
```

---

## Tips for using with Copilot Agent

- In VS Code: open the repo folder, then press `Ctrl+Shift+I` to open Copilot Chat
- Switch to **Agent mode** using the dropdown in the chat
- Paste the prompt above and hit Enter
- Copilot will create files directly in your workspace
- Review each file before committing — always verify AI-generated code!

## Tips for using with GitHub Copilot in the browser

- Go to your repo on GitHub.com
- Press `.` to open the web editor (github.dev)
- Open Copilot Chat from the left sidebar
- Paste the prompt task by task for best results
