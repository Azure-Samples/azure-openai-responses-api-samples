#!/usr/bin/env python3
"""Fail CI if the repo contains paths that are invalid/problematic on Windows.

This guards against issues like trailing spaces or dots in path segments, which can
cause `git clone` / checkout failures on NTFS.

Inspired by: https://github.com/Azure-Samples/azure-openai-responses-api-samples/issues/23
"""

from __future__ import annotations

import re
import subprocess
import sys


INVALID_CHARS = re.compile(r'[:*?"<>|]')


def git_ls_files() -> list[str]:
    # Use git's index listing so we validate tracked paths (not the working tree).
    out = subprocess.check_output(["git", "ls-files", "-z"], stderr=subprocess.STDOUT)
    return [p.decode("utf-8", errors="strict") for p in out.split(b"\x00") if p]


def main() -> int:
    problems: list[str] = []

    for path in git_ls_files():
        parts = path.split("/")

        for part in parts:
            # Windows forbids trailing spaces or dots in path components.
            if part.endswith(" "):
                problems.append(f"{path}  (segment '{part}' ends with a space)")
            if part.endswith("."):
                problems.append(f"{path}  (segment '{part}' ends with a dot)")

            # Windows forbids these characters in file/directory names.
            if INVALID_CHARS.search(part):
                problems.append(f"{path}  (segment '{part}' contains an invalid Windows character)")

            # Extra guardrail: backslashes in git paths are almost always a mistake.
            if "\\" in part:
                problems.append(f"{path}  (segment '{part}' contains a backslash)")

    if problems:
        print("Found paths that are invalid/problematic on Windows:\n", file=sys.stderr)
        for p in problems:
            print(f"- {p}", file=sys.stderr)
        return 1

    print("OK: no invalid Windows paths detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
