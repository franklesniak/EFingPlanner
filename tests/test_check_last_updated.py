"""Tests for the Last Updated check.

Each test builds a real temporary git repository, commits a base version on
`main`, then commits pull-request changes on a branch with controlled author
dates. Expected results are written from the style guide's rule, not computed
from the script. The script is loaded by file path because its filename is
hyphenated, matching `tests/test_check_session_structure.py`.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-last-updated.py"
SPEC = importlib.util.spec_from_file_location("check_last_updated", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load Last Updated script from {SCRIPT_PATH}")
_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _module
SPEC.loader.exec_module(_module)

last_updated = cast(Any, _module)


def doc(date: str, body: str = "Body text.", version: str | None = None) -> str:
    version_line = f"\n**Version:** 1.0.{version}.0\n" if version else ""
    return (
        f"# Title\n{version_line}\n## Metadata\n\n- **Status:** Active\n- **Owner:** Maintainers\n"
        f"- **Last Updated:** {date}\n- **Scope:** Test.\n\n{body}\n"
    )


class Repo:
    """A throwaway git repository with a `main` base and a `pr` branch."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("config", "core.autocrlf", "false")

    def git(self, *args: str, date: str | None = None) -> str:
        env = dict(os.environ)
        if date:
            env["GIT_AUTHOR_DATE"] = date
            env["GIT_COMMITTER_DATE"] = date
        result = subprocess.run(["git", *args], cwd=self.root, env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        return result.stdout

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode("utf-8"))

    def commit(self, message: str, date: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message, date=date)


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: Any) -> Repo:
    r = Repo(tmp_path)
    r.write("docs/a.md", doc("2026-01-01"))
    r.write("docs/plain.md", "# No metadata\n\nText.\n")
    r.commit("base", "2026-01-01T12:00:00+00:00")
    r.git("switch", "-q", "-c", "pr")
    monkeypatch.chdir(tmp_path)
    return r


def run(repo: Repo) -> list[str]:
    return cast(list[str], last_updated.check("main", "HEAD"))


def test_positive_control_content_change_with_bump_passes(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "New text."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_negative_control_content_change_without_bump_fails(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "New text."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1
    assert "docs/a.md" in problems[0] and "Set it to 2026-03-05" in problems[0]


def test_date_is_the_commit_utc_date_not_the_local_date(repo: Repo) -> None:
    # 23:30 on 2026-03-05 at UTC-05:00 is 04:30 on 2026-03-06 UTC.
    repo.write("docs/a.md", doc("2026-03-05", "New text."))
    repo.commit("change", "2026-03-05T23:30:00-05:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-06" in problems[0]
    repo.write("docs/a.md", doc("2026-03-06", "New text."))
    repo.commit("bump", "2026-03-05T23:40:00-05:00")
    assert run(repo) == []


def test_trailing_whitespace_only_change_needs_no_bump(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01").replace("Body text.", "Body text. "))
    repo.commit("whitespace", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_crlf_and_final_newline_changes_need_no_bump(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01").replace("\n", "\r\n") + "\r\n")
    repo.commit("line endings", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_removing_a_hard_line_break_is_content(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "Line one  \nline two."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Line one\nline two."))
    repo.commit("drop hard break", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_same_day_second_change_with_field_already_today_passes(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "First change."))
    repo.commit("first", "2026-03-05T09:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Second change."))
    repo.commit("second", "2026-03-05T17:00:00+00:00")
    assert run(repo) == []


def test_later_whitespace_commit_does_not_move_the_required_date(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("content", "2026-03-05T09:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed. "))
    repo.commit("whitespace next day", "2026-03-06T09:00:00+00:00")
    assert run(repo) == []


def test_file_without_metadata_is_ignored(repo: Repo) -> None:
    repo.write("docs/plain.md", "# No metadata\n\nChanged text.\n")
    repo.commit("plain", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_new_file_with_stale_date_fails_and_current_date_passes(repo: Repo) -> None:
    repo.write("docs/new.md", doc("2026-02-01"))
    repo.commit("add", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]
    repo.write("docs/new.md", doc("2026-03-05"))
    repo.commit("fix date", "2026-03-05T11:00:00+00:00")
    assert run(repo) == []


def test_version_date_must_match_last_updated(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "New.", version="20260304"))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Version" in problems[0]


def test_pure_rename_needs_no_bump(repo: Repo) -> None:
    repo.git("mv", "docs/a.md", "docs/b.md")
    repo.commit("rename", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_rename_with_content_change_needs_bump(repo: Repo) -> None:
    repo.git("mv", "docs/a.md", "docs/b.md")
    repo.write("docs/b.md", doc("2026-01-01", "Changed while renaming."))
    repo.commit("rename and edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_later_pure_rename_does_not_move_the_required_date(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("content", "2026-03-05T09:00:00+00:00")
    repo.git("mv", "docs/a.md", "docs/b.md")
    repo.commit("rename next day", "2026-03-06T09:00:00+00:00")
    assert run(repo) == []


def test_change_made_only_in_a_merge_commit_is_dated_by_that_merge(repo: Repo) -> None:
    repo.git("switch", "-q", "-c", "side")
    repo.write("docs/plain.md", "# No metadata\n\nSide text.\n")
    repo.commit("side", "2026-03-04T09:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "--no-commit", "side")
    repo.write("docs/a.md", doc("2026-01-01", "Edited during the merge."))
    repo.commit("merge side with an edit", "2026-03-05T09:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]
    repo.write("docs/a.md", doc("2026-03-05", "Edited during the merge."))
    repo.commit("bump", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_example_metadata_inside_a_fence_is_not_the_real_field(repo: Repo) -> None:
    fenced = "```text\n- **Last Updated:** 2000-01-01\n```\n"
    repo.write("docs/plain.md", "# No metadata\n\n" + fenced)
    repo.commit("example only", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_changes_on_main_after_the_fork_are_not_the_prs(repo: Repo) -> None:
    repo.git("switch", "-q", "main")
    repo.write("docs/a.md", doc("2026-01-01", "Main edited it and forgot."))
    repo.commit("main change", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/plain.md", "# No metadata\n\nPR text.\n")
    repo.commit("pr change", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_unattributable_content_change_fails_closed(repo: Repo, monkeypatch: Any) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    monkeypatch.setattr(last_updated, "required_date", lambda base, head, path: None)
    problems = run(repo)
    assert len(problems) == 1 and "required date is unknown" in problems[0]


def test_git_error_is_exit_2_never_a_pass(repo: Repo) -> None:
    assert last_updated.main(["--base", "no-such-ref"]) == 2


def test_main_exit_codes(repo: Repo) -> None:
    assert last_updated.main(["--base", "main"]) == 0
    repo.write("docs/a.md", doc("2026-01-01", "Changed."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    assert last_updated.main(["--base", "main"]) == 1
