"""Fail if a check script exists but nothing runs it.

Copy into the repository's tests (e.g. tests/test_checkers_wired.py) and adjust
CHECKERS and ENTRY_POINTS to the repository's layout. Part of the pr-tidy skill.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Scripts that must be wired in somewhere.
CHECKERS = sorted(ROOT.glob("scripts/check_*.py"))

# Files that can run them: hooks, CI, task runners, and validators.
ENTRY_POINTS = [
    ".pre-commit-config.yaml",
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "Makefile",
    "justfile",
    "noxfile.py",
    "tox.ini",
    "pyproject.toml",
    "package.json",
    "scripts/validate*.py",
]


def entry_point_text() -> str:
    files = {path for pattern in ENTRY_POINTS for path in ROOT.glob(pattern)}
    return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in sorted(files))


def test_every_checker_is_wired_in() -> None:
    text = entry_point_text()
    unwired = [checker.relative_to(ROOT).as_posix() for checker in CHECKERS if checker.stem not in text]
    assert not unwired, f"check scripts nothing runs: {unwired}"
