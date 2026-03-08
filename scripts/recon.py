#!/usr/bin/env python3
"""
CTF Auto-Recon Script
---------------------
Automates common first-pass reconnaissance tasks for CTF challenges across
three modes:

  web   — HTTP header inspection, robots.txt, .git exposure, common paths
  file  — file-type detection, strings, hex dump, binwalk, exiftool
  pwn   — checksec, interesting strings, symbol table, suggested GDB commands

Usage:
    python3 scripts/recon.py <target_url_or_ip> [--mode web|file|pwn]

Examples:
    python3 scripts/recon.py http://challenge.ctf.site --mode web
    python3 scripts/recon.py ./suspicious_file.png     --mode file
    python3 scripts/recon.py ./vuln                    --mode pwn
"""

import argparse
import subprocess
import os
import sys
from pathlib import Path

CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
RED   = "\033[91m"
RESET = "\033[0m"


def banner() -> None:
    """Print the ASCII-art banner for the recon tool."""
    print(f"""{CYAN}
  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
  CTF Auto-Recon  |  Zero to Hero
{RESET}""")


def run(cmd: str, label: str) -> None:
    """
    Execute a shell command and print its output.

    Uses a 30-second timeout so a hanging tool (e.g. nmap without -T4) does
    not block the entire recon run.

    Args:
        cmd:   The shell command to run (passed to ``subprocess.run`` with
               ``shell=True``).
        label: A short human-readable description printed before the output.
    """
    print(f"{YELLOW}[*] {label}...{RESET}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout.strip():
            print(result.stdout.strip())
        if result.returncode != 0 and result.stderr:
            print(f"{RED}    [!] {result.stderr.strip()[:200]}{RESET}")
    except subprocess.TimeoutExpired:
        print(f"{RED}    [!] Timed out{RESET}")
    except Exception as e:
        print(f"{RED}    [!] Error: {e}{RESET}")
    print()


def web_recon(target: str) -> None:
    """
    Run web-focused reconnaissance against *target*.

    Checks HTTP headers, robots.txt, sitemap.xml, and whether a ``.git``
    directory is publicly accessible (a common misconfiguration that leaks
    source code).  Also prints a list of common admin/debug paths to probe
    manually or with a fuzzer.

    Args:
        target: The base URL of the web application (e.g.
                ``http://challenge.ctf.site``).
    """
    print(f"{CYAN}{'='*50}")
    print(f"  WEB RECON: {target}")
    print(f"{'='*50}{RESET}\n")

    run(f"curl -sI '{target}' | head -30",            "Fetching HTTP headers")
    run(f"curl -s '{target}/robots.txt'",              "Checking robots.txt")
    run(f"curl -s '{target}/sitemap.xml' | head -30",  "Checking sitemap.xml")
    run(f"curl -s '{target}/.git/HEAD'",               "Checking for .git exposure")

    print(f"{YELLOW}[*] Common paths to manually check:{RESET}")
    paths = ["/admin", "/login", "/flag", "/secret", "/api", "/backup",
             "/config", "/.env", "/upload", "/dashboard", "/console"]
    for p in paths:
        print(f"    {target}{p}")
    print()

    print(f"{GREEN}[✓] Web recon complete. Try Burp Suite for deeper inspection.{RESET}")


def file_recon(filepath: str) -> None:
    """
    Run file-focused reconnaissance on *filepath*.

    Identifies the file type, searches for flag/password strings, dumps the
    first 20 lines as hex, checks for embedded files with binwalk, and
    extracts metadata with exiftool.

    Args:
        filepath: Path to the file to analyse.  The script exits with an
                  error message if the file does not exist.
    """
    print(f"{CYAN}{'='*50}")
    print(f"  FILE RECON: {filepath}")
    print(f"{'='*50}{RESET}\n")

    if not os.path.exists(filepath):
        print(f"{RED}[!] File not found: {filepath}{RESET}")
        sys.exit(1)

    run(f"file '{filepath}'",                          "Detecting file type")
    run(f"strings '{filepath}' | grep -iE 'ctf|flag|password|key|secret'", "Searching for flag strings")
    run(f"xxd '{filepath}' | head -20",                "Hex dump (first 20 lines)")
    run(f"binwalk '{filepath}'",                       "Checking for embedded files (binwalk)")
    run(f"exiftool '{filepath}' 2>/dev/null | head -30","Extracting metadata (exiftool)")

    print(f"{GREEN}[✓] File recon complete.{RESET}")


def pwn_recon(binary: str) -> None:
    """
    Run binary-focused reconnaissance on *binary*.

    Checks security mitigations (checksec), interesting strings, exported
    symbols that might indicate a win function, and linked shared libraries.
    Also prints useful GDB commands to copy-paste during manual analysis.

    Args:
        binary: Path to the ELF binary to analyse.  The script exits with an
                error message if the file does not exist.
    """
    print(f"{CYAN}{'='*50}")
    print(f"  BINARY RECON: {binary}")
    print(f"{'='*50}{RESET}\n")

    if not os.path.exists(binary):
        print(f"{RED}[!] Binary not found: {binary}{RESET}")
        sys.exit(1)

    run(f"file '{binary}'",                            "File type")
    run(f"checksec --file='{binary}' 2>/dev/null || python3 -c \"from pwn import *; e=ELF('{binary}'); print(e.checksec())\"", "Security checks (checksec)")
    run(f"strings '{binary}' | grep -iE 'flag|ctf|win|shell|password'", "Interesting strings")
    run(f"nm '{binary}' 2>/dev/null | grep -iE 'win|flag|shell|system'", "Symbol table — interesting functions")
    run(f"ldd '{binary}' 2>/dev/null",                 "Linked libraries")

    print(f"{CYAN}[*] Suggested GDB commands:{RESET}")
    print(f"    gdb '{binary}'")
    print(f"    (gdb) info functions")
    print(f"    (gdb) disassemble main")
    print(f"    (gdb) run <<< $(python3 -c \"print('A'*100)\")")
    print()
    print(f"{GREEN}[✓] Binary recon complete.{RESET}")


def main() -> None:
    """
    Parse command-line arguments and dispatch to the appropriate recon function.

    Exits with a non-zero status if the target does not exist (for file/pwn
    modes) or if an invalid mode is specified.
    """
    banner()
    parser = argparse.ArgumentParser(description="CTF Auto-Recon Helper")
    parser.add_argument("target", help="URL, IP, file path, or binary path")
    parser.add_argument("--mode", choices=["web", "file", "pwn"], default="web",
                        help="Recon mode (default: web)")
    args = parser.parse_args()

    if args.mode == "web":
        web_recon(args.target)
    elif args.mode == "file":
        file_recon(args.target)
    elif args.mode == "pwn":
        pwn_recon(args.target)


if __name__ == "__main__":
    main()
