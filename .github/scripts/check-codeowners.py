#!/usr/bin/env python3
"""
Check that every file changed under plugins/ in a PR is covered by a specific
(non-wildcard) entry in .github/CODEOWNERS.

Environment variables (set by the GitHub Actions workflow):
  BASE_SHA  - base commit SHA of the pull request
  HEAD_SHA  - head commit SHA of the pull request
"""

import os
import subprocess
import sys


def parse_codeowners(path: str) -> list[tuple[str, list[str]]]:
    """Return a list of (pattern, owners) for every non-comment, non-wildcard line."""
    entries: list[tuple[str, list[str]]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            pattern, owners = parts[0], parts[1:]
            entries.append((pattern, owners))
    return entries


def matches(filepath: str, pattern: str) -> bool:
    """
    Return True when *filepath* (relative to repo root, no leading slash) is
    covered by *pattern* using the CODEOWNERS subset of gitignore rules that
    is relevant to this repository:

    - Patterns that start with '/' are anchored to the repository root.
    - Patterns that end with '/' match the directory and all content beneath it.
    - A bare '*' matches everything (wildcard / catch-all).
    - Otherwise the pattern is treated as a path prefix.
    """
    # Bare wildcard — skip (we want to find *specific* entries only)
    if pattern == "*":
        return False

    # Strip leading slash to normalize for prefix comparison
    p = pattern.lstrip("/")

    # Directory pattern (trailing slash): match anything inside
    if p.endswith("/"):
        return filepath.startswith(p)

    # Exact file or prefix match (the pattern itself is a directory without trailing slash)
    return filepath == p or filepath.startswith(p + "/")


def get_changed_plugin_files(base_sha: str, head_sha: str) -> list[str]:
    """Return changed/added/modified files under plugins/ between two commits."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", base_sha, head_sha],
        capture_output=True,
        text=True,
        check=True,
    )
    return [
        f
        for f in result.stdout.splitlines()
        if f.startswith("plugins/")
    ]


def main() -> int:
    base_sha = os.environ.get("BASE_SHA", "")
    head_sha = os.environ.get("HEAD_SHA", "")

    if not base_sha or not head_sha:
        print("::error::BASE_SHA and HEAD_SHA environment variables must be set.")
        return 1

    changed_files = get_changed_plugin_files(base_sha, head_sha)
    if not changed_files:
        print("No files changed under plugins/ — nothing to check.")
        return 0

    codeowners_path = ".github/CODEOWNERS"
    entries = parse_codeowners(codeowners_path)

    uncovered: list[str] = []
    for filepath in changed_files:
        covered = any(matches(filepath, pattern) for pattern, _ in entries)
        if not covered:
            uncovered.append(filepath)

    if uncovered:
        print(
            "The following changed files under plugins/ are not covered by a specific "
            "entry in .github/CODEOWNERS (the catch-all '*' does not count):\n"
        )
        for f in uncovered:
            print(f"  - {f}")
        print(
            "\nPlease add an entry to .github/CODEOWNERS that covers these paths, "
            "assigning the appropriate owner(s)."
        )
        return 1

    print(
        f"All {len(changed_files)} changed file(s) under plugins/ have a specific "
        "CODEOWNERS entry. ✓"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
