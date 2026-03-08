#!/usr/bin/env python3
"""
CTF Flag Hunter
---------------
Recursively searches files and directories for CTF flag patterns.

Supports:
  - Plain text and binary files
  - ZIP and TAR archives (searches inside without extracting)
  - Image EXIF metadata (requires the `Pillow` package)
  - Customisable flag prefix (default: "CTF")
  - Colourised output showing file path + line/byte offset

Usage:
    python3 scripts/flag_hunter.py [--prefix CTF] <path> [path ...]
    python3 scripts/flag_hunter.py --prefix FLAG /tmp/challenge/
    python3 scripts/flag_hunter.py archive.zip image.png ./challenge_dir/

Why this script?
  CTF flags are often hidden in unexpected places: inside archived files, buried
  in binary blobs, or tucked away in image metadata.  This script automates the
  tedious first pass so you can focus on the interesting parts of the challenge.
"""

import argparse
import io
import os
import re
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Iterator

# ─────────────────────────── ANSI colour helpers ────────────────────────────

CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def _colour(text: str, code: str) -> str:
    """Wrap *text* in the given ANSI *code* and reset afterwards."""
    return f"{code}{text}{RESET}"


# ──────────────────────────── Flag-pattern helpers ───────────────────────────


def build_pattern(prefix: str) -> re.Pattern[bytes]:
    """
    Build a compiled regex pattern that matches ``<prefix>{…}``.

    The pattern is case-insensitive and compiled against *bytes* so it works
    on both text and binary content without any extra decoding step.

    Args:
        prefix: The flag prefix to look for, e.g. ``"CTF"`` or ``"FLAG"``.

    Returns:
        A compiled ``re.Pattern[bytes]`` ready to use with ``re.finditer``.
    """
    # Escape the prefix in case it contains regex-special characters, then
    # match the opening brace, any content, and the closing brace.
    escaped = re.escape(prefix.encode())
    return re.compile(escaped + rb"\{[^}]*\}", re.IGNORECASE)


# ─────────────────────────── Search implementations ──────────────────────────


def _report(label: str, offset_info: str, match: bytes) -> None:
    """
    Print a single match result to stdout.

    Args:
        label:       Human-readable location (file path, archive member, …).
        offset_info: String describing where in the file the match was found
                     (e.g. ``"line 42"`` or ``"offset 0x1f3a"``).
        match:       The raw bytes of the matched flag string.
    """
    flag_str = match.decode("utf-8", errors="replace")
    print(
        f"  {_colour('🚩 FOUND', GREEN + BOLD)}  "
        f"{_colour(label, CYAN)}  "
        f"{_colour(f'[{offset_info}]', YELLOW)}  "
        f"{_colour(flag_str, GREEN)}"
    )


def search_bytes(
    data: bytes,
    pattern: re.Pattern[bytes],
    label: str,
) -> int:
    """
    Search raw *data* for flag *pattern* and print every match.

    Line numbers are reported for printable text; raw byte offsets are used
    for binary content (detected by the presence of null bytes).

    Args:
        data:    The bytes to search.
        pattern: Compiled regex returned by :func:`build_pattern`.
        label:   Human-readable name printed with each match.

    Returns:
        The number of matches found.
    """
    matches = list(pattern.finditer(data))
    if not matches:
        return 0

    # Decide whether to show line numbers or hex offsets.
    # If the data contains null bytes it is likely binary.
    is_binary = b"\x00" in data

    for m in matches:
        if is_binary:
            offset_info = f"offset 0x{m.start():x}"
        else:
            # Count newlines up to the match start to get the line number.
            line_num = data[: m.start()].count(b"\n") + 1
            offset_info = f"line {line_num}"
        _report(label, offset_info, m.group())

    return len(matches)


def search_file(
    path: Path,
    pattern: re.Pattern[bytes],
) -> int:
    """
    Search a single file (text or binary) for flag matches.

    Args:
        path:    Absolute or relative path to the file.
        pattern: Compiled regex returned by :func:`build_pattern`.

    Returns:
        The number of matches found, or 0 on read error.
    """
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(f"  {_colour(f'[!] Cannot read {path}: {exc}', RED)}")
        return 0
    return search_bytes(data, pattern, str(path))


def search_zip(
    path: Path,
    pattern: re.Pattern[bytes],
) -> int:
    """
    Search all members inside a ZIP archive for flag matches.

    Archives are processed in-memory; nothing is extracted to disk.

    Args:
        path:    Path to the ``.zip`` file.
        pattern: Compiled regex returned by :func:`build_pattern`.

    Returns:
        Total matches found across all archive members.
    """
    total = 0
    try:
        with zipfile.ZipFile(path, "r") as zf:
            for info in zf.infolist():
                # Skip directories stored inside the zip.
                if info.filename.endswith("/"):
                    continue
                label = f"{path}::{info.filename}"
                try:
                    data = zf.read(info.filename)
                except Exception as exc:
                    print(f"  {_colour(f'[!] Cannot read {label}: {exc}', RED)}")
                    continue
                total += search_bytes(data, pattern, label)
    except zipfile.BadZipFile as exc:
        print(f"  {_colour(f'[!] Bad ZIP {path}: {exc}', RED)}")
    return total


def search_tar(
    path: Path,
    pattern: re.Pattern[bytes],
) -> int:
    """
    Search all members inside a TAR (optionally compressed) archive.

    Supports ``.tar``, ``.tar.gz``, ``.tgz``, ``.tar.bz2``, ``.tar.xz``.
    Archives are processed in-memory; nothing is extracted to disk.

    Args:
        path:    Path to the tar archive.
        pattern: Compiled regex returned by :func:`build_pattern`.

    Returns:
        Total matches found across all archive members.
    """
    total = 0
    try:
        with tarfile.open(path, "r:*") as tf:
            for member in tf.getmembers():
                if not member.isfile():
                    continue
                label = f"{path}::{member.name}"
                try:
                    fobj = tf.extractfile(member)
                    if fobj is None:
                        continue
                    data = fobj.read()
                except Exception as exc:
                    print(f"  {_colour(f'[!] Cannot read {label}: {exc}', RED)}")
                    continue
                total += search_bytes(data, pattern, label)
    except tarfile.TarError as exc:
        print(f"  {_colour(f'[!] Bad TAR {path}: {exc}', RED)}")
    return total


def search_exif(
    path: Path,
    pattern: re.Pattern[bytes],
) -> int:
    """
    Search image EXIF metadata for flag matches.

    Requires the ``Pillow`` package (``pip install Pillow``).  If Pillow is not
    installed the function silently returns 0 — the file is still searched as a
    plain binary by :func:`search_file`.

    Args:
        path:    Path to the image file.
        pattern: Compiled regex returned by :func:`build_pattern`.

    Returns:
        Number of matches found in EXIF data.
    """
    try:
        from PIL import Image
    except ImportError:
        # Pillow is optional; no EXIF search without it.
        return 0

    total = 0
    try:
        with Image.open(path) as img:
            exif_data = img._getexif()  # type: ignore[attr-defined]
            if exif_data is None:
                return 0
            # Concatenate all EXIF string values and search them.
            combined = " ".join(str(v) for v in exif_data.values()).encode("utf-8", errors="replace")
            matches = list(pattern.finditer(combined))
            for m in matches:
                _report(f"{path} [EXIF]", "EXIF metadata", m.group())
            total = len(matches)
    except Exception:
        # Not a valid image or EXIF unavailable — skip gracefully.
        pass
    return total


# ──────────────────────────── Directory walker ───────────────────────────────

# Extensions that we recognise as archives.
_ZIP_EXTS = {".zip"}
_TAR_EXTS = {".tar", ".gz", ".tgz", ".bz2", ".xz"}
# Extensions that are likely images worth checking for EXIF.
_IMG_EXTS = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".webp"}


def _iter_paths(targets: list[str]) -> Iterator[Path]:
    """
    Yield every file reachable from *targets*.

    If a target is a file it is yielded directly.  If it is a directory it is
    walked recursively.

    Args:
        targets: List of file or directory path strings from the command line.

    Yields:
        :class:`pathlib.Path` objects for each reachable file.
    """
    for t in targets:
        p = Path(t)
        if p.is_file():
            yield p
        elif p.is_dir():
            for root, _dirs, files in os.walk(p):
                for fname in sorted(files):
                    yield Path(root) / fname
        else:
            print(f"  {_colour(f'[!] Not found: {t}', RED)}")


def hunt(
    targets: list[str],
    pattern: re.Pattern[bytes],
) -> int:
    """
    Main search loop: iterate over all targets and dispatch to the right
    search function based on file type.

    Args:
        targets: List of file or directory path strings to search.
        pattern: Compiled regex returned by :func:`build_pattern`.

    Returns:
        Grand total of flag matches found across all targets.
    """
    grand_total = 0

    for path in _iter_paths(targets):
        suffix = path.suffix.lower()

        print(f"{CYAN}[~] Scanning:{RESET} {path}")

        if suffix in _ZIP_EXTS:
            # Search inside the archive AND as a raw binary (in case the flag
            # is hidden in the zip file's comment or header bytes).
            grand_total += search_zip(path, pattern)
            grand_total += search_file(path, pattern)

        elif suffix in _TAR_EXTS or (suffix == ".gz" and ".tar" in path.name):
            grand_total += search_tar(path, pattern)
            grand_total += search_file(path, pattern)

        else:
            # Always scan the raw bytes.
            grand_total += search_file(path, pattern)
            # For images, also check EXIF metadata.
            if suffix in _IMG_EXTS:
                grand_total += search_exif(path, pattern)

    return grand_total


# ────────────────────────────── Entry point ──────────────────────────────────


def main() -> None:
    """Parse CLI arguments and run the flag hunter."""
    parser = argparse.ArgumentParser(
        description=(
            "Recursively hunt for CTF flags in files, directories, archives, "
            "and image EXIF metadata."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 flag_hunter.py ./challenge/
  python3 flag_hunter.py --prefix FLAG secret.zip image.png
  python3 flag_hunter.py --prefix picoCTF /tmp/ctf/
        """,
    )
    parser.add_argument(
        "targets",
        nargs="+",
        metavar="PATH",
        help="Files or directories to search (supports ZIP/TAR archives).",
    )
    parser.add_argument(
        "--prefix",
        default="CTF",
        metavar="PREFIX",
        help='Flag prefix to search for (default: "CTF").  '
             'Use the prefix printed in the challenge description, '
             'e.g. --prefix picoCTF',
    )
    args = parser.parse_args()

    prefix: str = args.prefix
    pattern = build_pattern(prefix)

    print(f"\n{BOLD}{CYAN}🏴 CTF Flag Hunter{RESET}")
    print(f"{CYAN}   Searching for pattern: {RESET}"
          f"{BOLD}{GREEN}{re.escape(prefix)}{{...}}{RESET}\n")

    total = hunt(args.targets, pattern)

    print()
    if total:
        print(_colour(f"[✓] Done — {total} match(es) found.", GREEN + BOLD))
    else:
        print(_colour("[✗] No flags found. Try a different prefix or check manually.", YELLOW))
    print()


if __name__ == "__main__":
    main()
