#!/usr/bin/env python3
"""
CTF Crypto Quick-Solver
-----------------------
Tries common encodings and ciphers on an input string and prints all results
that decode to printable text.  Likely flag candidates are highlighted with a
🚩 marker.

Supported formats (attempted automatically):
  Base64, Base32, Hex, URL encoding, ROT-13, ROT-1 … ROT-25, Binary, Morse

Usage:
    python3 scripts/crypto_solver.py "your_ciphertext_here"
    echo "ciphertext" | python3 scripts/crypto_solver.py

Why this script?
  In CTF competitions ciphertexts are often trivially encoded (Base64, Hex,
  ROT-13, …).  Rather than opening CyberChef for every challenge, this script
  brute-forces the most common encodings in under a second and flags anything
  that looks like a CTF flag pattern.
"""

import sys
import base64
import binascii
import codecs
import string
import re

CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW= "\033[93m"
RESET = "\033[0m"


def looks_like_flag(s: str) -> bool:
    """
    Heuristically decide whether *s* looks like a CTF flag.

    Checks for the most common flag patterns:
      - ``CTF{...}`` (case-insensitive)
      - ``flag{...}`` (case-insensitive)
      - Any alphanumeric token of 10 or more characters (could be a flag in
        an unusual format)

    Args:
        s: The decoded string to evaluate.

    Returns:
        ``True`` if the string resembles a CTF flag, ``False`` otherwise.
    """
    s = s.strip()
    return bool(re.search(r'[Cc][Tt][Ff]\s*\{', s) or
                re.search(r'flag\s*\{', s, re.IGNORECASE) or
                re.search(r'[a-zA-Z0-9_\-\{\}]{10,}', s))


def try_decode(
    label: str,
    func: object,
    data: str,
    results: list[tuple[str, str, str]],
) -> None:
    """
    Apply *func* to *data*, catch any exception, and record the result.

    If the function succeeds and returns non-empty text the result is appended
    to *results* together with a flag emoji when it looks like a CTF flag.

    Args:
        label:   Human-readable name for this decoding attempt (e.g. "Base64").
        func:    A callable that accepts the ciphertext string and returns a
                 decoded string.  Any exception it raises is silently ignored.
        data:    The raw ciphertext string passed to *func*.
        results: Accumulator list; each entry is a 3-tuple of
                 ``(label, decoded_text, flag_marker)``.
    """
    try:
        result = func(data)
        if result and result.strip():
            flag = "🚩 POSSIBLE FLAG!" if looks_like_flag(result) else ""
            results.append((label, result.strip(), flag))
    except Exception:
        pass


def rot_n(text: str, n: int) -> str:
    """
    Apply a Caesar-cipher rotation of *n* positions to *text*.

    Only ASCII letters are shifted; digits, punctuation, and whitespace are
    preserved unchanged.

    Args:
        text: The input string to rotate.
        n:    The shift amount (1–25 for non-ROT-13 variants).

    Returns:
        The rotated string.
    """
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + n) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)


def main() -> None:
    """
    Entry point — read input, attempt all decodings, and print results.

    Input is read from the command-line arguments (joined with spaces) or from
    stdin if no arguments are given and stdin is not a terminal (pipe mode).
    The script exits with a usage hint when called interactively with no input.
    """
    if len(sys.argv) > 1:
        data = ' '.join(sys.argv[1:])
    elif not sys.stdin.isatty():
        data = sys.stdin.read().strip()
    else:
        print(f"{YELLOW}Usage: python3 crypto_solver.py <ciphertext>{RESET}")
        sys.exit(1)

    # Validate that we received non-empty input.
    if not data:
        print(f"{YELLOW}[!] Empty input — nothing to decode.{RESET}")
        sys.exit(1)

    print(f"{CYAN}[*] Input: {data[:80]}{'...' if len(data) > 80 else ''}{RESET}\n")

    results: list[tuple[str, str, str]] = []

    # Base64
    try_decode("Base64",
        lambda d: base64.b64decode(d + '==').decode('utf-8', errors='replace'),
        data, results)

    # Base32
    try_decode("Base32",
        lambda d: base64.b32decode(d.upper() + '=' * ((8 - len(d) % 8) % 8)).decode('utf-8', errors='replace'),
        data, results)

    # Hex
    try_decode("Hex",
        lambda d: bytes.fromhex(d.replace(' ', '')).decode('utf-8', errors='replace'),
        data, results)

    # URL decode
    try_decode("URL decode",
        lambda d: __import__('urllib.parse', fromlist=['unquote']).unquote(d),
        data, results)

    # ROT13
    try_decode("ROT13",
        lambda d: codecs.decode(d, 'rot_13'),
        data, results)

    # All ROT variants (ROT1–ROT25, skipping ROT13 which is handled above)
    for n in range(1, 26):
        if n == 13:
            continue
        rotated = rot_n(data, n)
        if looks_like_flag(rotated):
            results.append((f"ROT{n}", rotated, "🚩 POSSIBLE FLAG!"))

    # Binary (space-separated 8-bit groups)
    try_decode("Binary",
        lambda d: ''.join(chr(int(b, 2)) for b in d.split()),
        data, results)

    # Morse (basic — dots, dashes, and '/' as word separator)
    MORSE: dict[str, str] = {
        '.-':'A','-...':'B','-.-.':'C','-..':'D','.':'E','..-.':'F',
        '--.':'G','....':'H','..':'I','.---':'J','-.-':'K','.-..':'L',
        '--':'M','-.':'N','---':'O','.--.':'P','--.-':'Q','.-.':'R',
        '...':'S','-':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
        '-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2',
        '...--':'3','....-':'4','.....':'5','-....':'6','--...':'7',
        '---..':'8','----.':'9',
    }
    if all(c in '.- /' for c in data):
        try:
            words = data.split(' / ')
            decoded = ' '.join(''.join(MORSE.get(c, '?') for c in w.split()) for w in words)
            results.append(("Morse Code", decoded, "🚩 POSSIBLE FLAG!" if looks_like_flag(decoded) else ""))
        except Exception:
            pass

    # ── Print results ──────────────────────────────────────────────────────
    if results:
        print(f"{YELLOW}{'─'*60}{RESET}")
        for label, result, flag in results:
            marker = f"  {GREEN}{flag}{RESET}" if flag else ""
            print(f"{CYAN}[{label}]{RESET}{marker}")
            print(f"  {result[:200]}")
            print()
    else:
        print(f"{YELLOW}[!] No common encodings recognized. Try CyberChef Magic mode.{RESET}")

    print(f"{YELLOW}{'─'*60}{RESET}")
    print(f"[*] Also try: https://gchq.github.io/CyberChef/#recipe=Magic(3,false,false,'')")


if __name__ == "__main__":
    main()
