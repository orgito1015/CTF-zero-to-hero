#!/usr/bin/env python3
"""
CTF Crypto Quick-Solver
Tries common encodings/ciphers on input and prints results.
Usage: python3 scripts/crypto_solver.py "your_ciphertext_here"
       echo "ciphertext" | python3 scripts/crypto_solver.py
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

def looks_like_flag(s):
    """Check if result looks like a CTF flag."""
    s = s.strip()
    return bool(re.search(r'[Cc][Tt][Ff]\s*\{', s) or
                re.search(r'flag\s*\{', s, re.IGNORECASE) or
                re.search(r'[a-zA-Z0-9_\-\{\}]{10,}', s))

def try_decode(label, func, data, results):
    try:
        result = func(data)
        if result and result.strip():
            flag = "🚩 POSSIBLE FLAG!" if looks_like_flag(result) else ""
            results.append((label, result.strip(), flag))
    except Exception:
        pass

def rot_n(text, n):
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result.append(chr((ord(ch) - base + n) % 26 + base))
        else:
            result.append(ch)
    return ''.join(result)

def main():
    if len(sys.argv) > 1:
        data = ' '.join(sys.argv[1:])
    elif not sys.stdin.isatty():
        data = sys.stdin.read().strip()
    else:
        print(f"{YELLOW}Usage: python3 crypto_solver.py <ciphertext>{RESET}")
        sys.exit(1)

    print(f"{CYAN}[*] Input: {data[:80]}{'...' if len(data) > 80 else ''}{RESET}\n")

    results = []

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

    # All ROT variants
    for n in range(1, 26):
        if n == 13:
            continue
        rotated = rot_n(data, n)
        if looks_like_flag(rotated):
            results.append((f"ROT{n}", rotated, "🚩 POSSIBLE FLAG!"))

    # Binary
    try_decode("Binary",
        lambda d: ''.join(chr(int(b, 2)) for b in d.split()),
        data, results)

    # Morse (basic)
    MORSE = {'.-':'A','−...':'B','−.−.':'C','−..':'D','.':'E','..−.':'F',
             '−−.':'G','....':'H','..':'I','.−−−':'J','−.−':'K','.-..':'L',
             '−−':'M','−.':'N','−−−':'O','.--.':'P','--.-':'Q','.-.':'R',
             '...':'S','−':'T','..-':'U','...-':'V','.--':'W','-..-':'X',
             '-.--':'Y','--..':'Z','-----':'0','.----':'1','..---':'2',
             '...--':'3','....-':'4','.....':'5','-....':'6','--...':'7',
             '---..':'8','----.':'9'}
    if all(c in '.-− /' for c in data):
        try:
            words = data.split(' / ')
            decoded = ' '.join(''.join(MORSE.get(c, '?') for c in w.split()) for w in words)
            results.append(("Morse Code", decoded, "🚩 POSSIBLE FLAG!" if looks_like_flag(decoded) else ""))
        except Exception:
            pass

    # Print results
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
