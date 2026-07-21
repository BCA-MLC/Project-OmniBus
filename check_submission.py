"""
Static submission checker — run before accepting any agent.py submission.

Usage
-----
    python check_submission.py participant_starter/agent.py

Exit codes
----------
0  No suspicious patterns found.
1  One or more suspicious patterns detected — reject the submission.

What it looks for
-----------------
The in-place mutation exploit works by:
  1. Grabbing a reference to an obs/info array (info["time_matrix"], obs["bus_states"], etc.)
  2. Zeroing / overwriting it via  arr[...] = x  or  arr.fill(x)  or  arr[:] = x

This script flags any of those patterns.  It is a *stopgap* — the real
fixes are in env.py (read-only copies) and eval_runner.py (score from
env-internal state).  But a static check lets you catch the attempt at
review time and reject the submission before it runs.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Patterns to flag
# ---------------------------------------------------------------------------
# Each entry is (regex_pattern, human_readable_description).
# All patterns are searched case-sensitively on each source line.
SUSPICIOUS_PATTERNS: list[tuple[str, str]] = [
    # Ellipsis slice assignment:  arr[...] = x
    (r"\.\.\.\s*\]", "Ellipsis in-place assignment  arr[...] = x"),
    # Any slice / index assignment on a subscript:  arr[:] = x  arr[0] = x
    (r"\[[\s\d:,\.]*\]\s*=", "Slice / index assignment  arr[:] = x"),
    # .fill()  method call
    (r"\.fill\s*\(", "NumPy .fill() in-place mutation"),
    # .flags.writeable assignment — attempting to lift our read-only flag
    (r"\.flags\.writeable\s*=\s*True", "Attempt to make a read-only array writeable"),
    # np.copyto / np.ndarray.flat assignment
    (r"np\.copyto\s*\(", "np.copyto() in-place write"),
    (r"\.flat\s*=", ".flat assignment"),
    # ctypes / memoryview tricks
    (r"ctypes", "ctypes usage (potential memory bypass)"),
    (r"memoryview", "memoryview usage (potential memory bypass)"),
]

# ---------------------------------------------------------------------------


def check_file(path: Path) -> list[tuple[int, str, str]]:
    """Return a list of (line_number, matched_pattern_desc, line_text) for hits."""
    hits: list[tuple[int, str, str]] = []
    source = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(source.splitlines(), start=1):
        for pattern, description in SUSPICIOUS_PATTERNS:
            if re.search(pattern, line):
                hits.append((lineno, description, line.rstrip()))
                break  # one hit per line is enough
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Static check for reward-hacking mutation patterns in agent.py submissions.",
    )
    parser.add_argument(
        "submission",
        nargs="?",
        default="participant_starter/agent.py",
        help="Path to the submitted agent.py file.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any hit regardless of context (default: exit 1).",
    )
    args = parser.parse_args(argv)

    path = Path(args.submission)
    if not path.exists():
        print(f"ERROR: submission file not found: {path}", file=sys.stderr)
        return 1

    hits = check_file(path)

    if not hits:
        print(f"[PASS] No suspicious in-place mutation patterns found in {path}.")
        return 0

    print(f"[FAIL] Suspicious patterns detected in {path}:")
    print()
    for lineno, desc, text in hits:
        print(f"  Line {lineno:>4}: {desc}")
        print(f"            {text}")
        print()
    print(
        "Submission flagged for manual review.\n"
        "Legitimate agents should never need to write to obs/info arrays.\n"
        "See sbrp_env/env.py for the security contract."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
