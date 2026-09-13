"""Regression tests for local-only Markdown lint exclusions.

`package.json`, `.remarkignore`, and `.github/scripts/lint-nested-markdown.js`
each skip a small set of local-only working paths by name. Those exclusions are
unconditional: if such a path is ever committed, link validation and
nested-fence validation stop covering it, silently and permanently.

These tests make the safety condition explicit. Each local-only path must be
ignored by the committed `.gitignore`, must be untracked, and must appear in
every one of the three lint exclusion lists.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

# Single source of truth. Each entry is (gitignore pattern, git pathspec).
LOCAL_ONLY_PATHS = (
    (".orchestration/", ".orchestration"),
    ("ORCHESTRATOR_PROMPT.md", "ORCHESTRATOR_PROMPT.md"),
)

# How each scanner spells the exclusion.
LINT_MD_TOKENS = ("#.orchestration", "#ORCHESTRATOR_PROMPT.md")
REMARKIGNORE_LINES = (".orchestration/", "ORCHESTRATOR_PROMPT.md")
NESTED_IGNORE_TOKENS = ("'.orchestration/**'", "'ORCHESTRATOR_PROMPT.md'")


def _gitignore_patterns() -> list[str]:
    """Return the non-comment, non-blank patterns in the committed .gitignore."""
    text = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    patterns = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)
    return patterns


@pytest.mark.parametrize(("pattern", "pathspec"), LOCAL_ONLY_PATHS)
def test_local_only_path_is_in_gitignore(pattern: str, pathspec: str) -> None:
    """The committed .gitignore must carry each local-only path."""
    assert pattern in _gitignore_patterns(), (
        f"{pattern!r} is excluded from Markdown linting but is absent from "
        ".gitignore. Add it to .gitignore, or remove the lint exclusion."
    )


@pytest.mark.parametrize(("pattern", "pathspec"), LOCAL_ONLY_PATHS)
def test_local_only_path_is_untracked(pattern: str, pathspec: str) -> None:
    """No local-only path may be tracked by git."""
    result = subprocess.run(
        ["git", "ls-files", "--", pathspec],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    tracked = [line for line in result.stdout.splitlines() if line.strip()]
    assert not tracked, (
        f"{pathspec!r} is tracked by git but is excluded from link validation "
        "and nested-Markdown validation. Remove the file from git, or remove "
        f"the lint exclusions for it. Tracked files: {tracked}"
    )


def test_lint_md_script_excludes_local_only_paths() -> None:
    """The lint:md script must exclude every local-only path."""
    package_json = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
    script = package_json["scripts"]["lint:md"]
    for token in LINT_MD_TOKENS:
        assert token in script, f"package.json lint:md does not exclude {token!r}."


def test_remarkignore_excludes_local_only_paths() -> None:
    """.remarkignore must exclude every local-only path."""
    lines = [
        line.strip()
        for line in (REPO_ROOT / ".remarkignore").read_text(encoding="utf-8").splitlines()
    ]
    for entry in REMARKIGNORE_LINES:
        assert entry in lines, f".remarkignore does not exclude {entry!r}."


def test_nested_markdown_linter_excludes_local_only_paths() -> None:
    """The nested-Markdown linter must exclude every local-only path."""
    source = (REPO_ROOT / ".github" / "scripts" / "lint-nested-markdown.js").read_text(
        encoding="utf-8"
    )
    for token in NESTED_IGNORE_TOKENS:
        assert token in source, f"lint-nested-markdown.js does not exclude {token}."
