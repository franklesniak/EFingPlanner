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


def test_a_later_merge_edit_beats_an_earlier_normal_edit(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "First edit."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "-c", "side", "main")
    repo.write("docs/plain.md", "# No metadata\n\nSide text.\n")
    repo.commit("side", "2026-03-05T11:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "--no-commit", "side")
    repo.write("docs/a.md", doc("2026-03-05", "Edited again in the merge."))
    repo.commit("merge with an edit", "2026-03-06T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-06" in problems[0]


def test_merging_main_in_adds_no_requirement(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "PR edit."))
    repo.commit("pr edit", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.write("docs/plain.md", "# No metadata\n\nMain moved on.\n")
    repo.commit("main change", "2026-03-06T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "-m", "merge main", "main", date="2026-03-07T10:00:00+00:00")
    assert run(repo) == []


def test_a_merge_that_takes_one_side_unchanged_adds_no_date(repo: Repo) -> None:
    # The side branch edits a.md; the PR line edits another file; the merge takes a.md
    # unchanged from the side. The date is the side commit's, never the merge's.
    repo.git("switch", "-q", "-c", "side", "main")
    repo.write("docs/a.md", doc("2026-03-04", "Changed on the side."))
    repo.commit("side edit", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/plain.md", "# No metadata\n\nPR text.\n")
    repo.commit("pr edit", "2026-03-05T10:00:00+00:00")
    repo.git("merge", "-q", "--no-ff", "-m", "merge side", "side", date="2026-03-07T10:00:00+00:00")
    required = last_updated.required_date("main", "HEAD", "docs/a.md")
    assert required is not None and required.isoformat() == "2026-03-04"
    assert run(repo) == []


def test_clean_merge_across_a_rename_is_dated_by_the_side_edit(repo: Repo) -> None:
    repo.git("mv", "docs/a.md", "docs/b.md")
    repo.commit("rename", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "-c", "side", "main")
    repo.write("docs/a.md", doc("2026-03-05", "Edited on the side."))
    repo.commit("side edit", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "-m", "merge side", "side", date="2026-03-07T10:00:00+00:00")
    assert "Edited on the side." in repo.git("show", "HEAD:docs/b.md")
    assert run(repo) == []


def test_activating_a_backslash_hard_break_is_content(repo: Repo) -> None:
    bs = chr(92)
    repo.write("docs/a.md", doc("2026-01-01", "Line one" + bs + " \nline two."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Line one" + bs + "\nline two."))
    repo.commit("activate the break", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_an_escaped_final_backslash_is_not_a_break(repo: Repo) -> None:
    bs = chr(92)
    repo.write("docs/a.md", doc("2026-01-01", "Path " + bs + bs + " \nline two."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Path " + bs + bs + "\nline two."))
    repo.commit("strip trailing space", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_clean_merge_combining_both_sides_edits_adds_no_requirement(repo: Repo) -> None:
    body = "\n".join(["Para one."] + ["filler %d" % i for i in range(12)] + ["Para two."])
    repo.write("docs/a.md", doc("2026-01-01", body))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-03-05", body.replace("Para one.", "Para one, edited.")))
    repo.commit("pr edit", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.write("docs/a.md", doc("2026-01-01", body.replace("Para two.", "Para two, edited on main.")))
    repo.commit("main edit", "2026-03-05T11:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "-m", "merge main", "main", date="2026-03-06T10:00:00+00:00")
    text = repo.git("show", "HEAD:docs/a.md")
    assert "Para one, edited." in text and "Para two, edited on main." in text
    assert run(repo) == []


def test_octopus_merge_taking_one_side_unchanged_adds_no_date(repo: Repo) -> None:
    repo.git("switch", "-q", "-c", "side1", "main")
    repo.write("docs/a.md", doc("2026-03-04", "Changed on side one."))
    repo.commit("side one", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "-c", "side2", "main")
    repo.write("docs/other.md", "# Other\n\nSide two.\n")
    repo.commit("side two", "2026-03-04T11:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "-m", "octopus", "side1", "side2", date="2026-03-07T10:00:00+00:00")
    assert len(repo.git("rev-parse", "HEAD^@").split()) == 3
    assert run(repo) == []


def test_four_space_fence_line_does_not_close_a_fence(repo: Repo) -> None:
    inner = "```text\n    ```\n- **Last Updated:** 2000-01-01\n```\n"
    repo.write("docs/plain.md", "# No metadata\n\n" + inner)
    repo.commit("indented fence line", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_field_may_not_move_back_behind_the_base(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-09-23"))
    repo.commit("newer base", "2026-09-23T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-03-05", "Old change, rebased."))
    repo.commit("rebased old commit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "moved back from 2026-09-23 to 2026-03-05" in problems[0]


def test_filename_with_a_leading_colon_is_read_literally(repo: Repo) -> None:
    # Built with plumbing, because a leading colon is not a legal Windows filename.
    def commit_with(text: str, message: str, date: str, parent: str) -> str:
        blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=repo.root, input=text,
                              capture_output=True, text=True, check=True).stdout.strip()
        base_tree = repo.git("rev-parse", parent + "^{tree}").strip()
        listing = repo.git("ls-tree", "-z", base_tree)
        entries = [e for e in listing.split("\0") if e and not e.endswith("\t:foo.md")]
        entries.append("100644 blob %s\t:foo.md" % blob)
        tree = subprocess.run(["git", "mktree", "-z"], cwd=repo.root, input="\0".join(entries) + "\0",
                              capture_output=True, text=True, check=True).stdout.strip()
        return repo.git("commit-tree", tree, "-p", parent, "-m", message, date=date).strip()

    base = commit_with(doc("2026-01-01"), "add colon file", "2026-01-01T12:00:00+00:00", "main")
    repo.git("update-ref", "refs/heads/main", base)
    head = commit_with(doc("2026-01-01", "Changed."), "edit colon file", "2026-03-05T10:00:00+00:00", base)
    problems = last_updated.check("main", head)
    assert len(problems) == 1 and ":foo.md" in problems[0] and "Set it to 2026-03-05" in problems[0]


def test_removing_the_field_fails(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "Changed.").replace("- **Last Updated:** 2026-01-01\n", ""))
    repo.commit("drop the field", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "removed it" in problems[0]


def test_non_ascii_and_spaced_paths_are_checked(repo: Repo) -> None:
    repo.write("docs/café guide.md", doc("2026-01-01"))
    repo.commit("add", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/café guide.md", doc("2026-01-01", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "café guide.md" in problems[0] and "Set it to 2026-03-05" in problems[0]


def test_example_in_a_longer_outer_fence_is_not_the_real_field(repo: Repo) -> None:
    nested = "````markdown\n```text\n- **Last Updated:** 2000-01-01\n```\n````\n"
    repo.write("docs/plain.md", "# No metadata\n\n" + nested)
    repo.commit("nested example", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_real_field_after_a_nested_fence_is_still_found(repo: Repo) -> None:
    nested = "````markdown\n```text\nexample\n```\n````\n"
    repo.write("docs/a.md", doc("2026-01-01", nested + "\nChanged."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_tab_then_two_spaces_is_a_hard_break(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "Line one\t  \nline two."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Line one\nline two."))
    repo.commit("drop hard break", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_spaces_then_a_final_tab_are_not_a_hard_break(repo: Repo) -> None:
    # CommonMark needs the spaces immediately before the line end; a tab after them breaks that.
    repo.write("docs/a.md", doc("2026-01-01", "Line one  \t\nline two."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Line one\nline two."))
    repo.commit("strip trailing whitespace", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_outer_fence_stays_open_after_an_inner_fence_closes(repo: Repo) -> None:
    nested = "````markdown\n```text\nexample\n```\n- **Last Updated:** 2000-01-01\n````\n"
    repo.write("docs/plain.md", "# No metadata\n\n" + nested)
    repo.commit("nested example", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_exact_copy_of_an_existing_file_is_dated_by_its_commit(repo: Repo) -> None:
    repo.write("docs/copy.md", doc("2026-01-01"))
    repo.commit("copy a.md", "2026-01-01T13:00:00+00:00")
    assert run(repo) == []
    repo.write("docs/copy.md", doc("2026-01-01", "Now changed."))
    repo.commit("edit the copy", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_lone_trailing_tab_is_mechanical(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01").replace("Body text.", "Body text.\t"))
    repo.commit("tab", "2026-03-05T10:00:00+00:00")
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


def test_show_returns_none_only_for_a_missing_path(repo: Repo) -> None:
    assert last_updated.show("HEAD", "docs/no-such-file.md") is None
    assert "Last Updated" in last_updated.show("HEAD", "docs/a.md")


def test_show_raises_on_a_git_failure_instead_of_reporting_absent(repo: Repo) -> None:
    with pytest.raises(last_updated.GitError):
        last_updated.show("0" * 40, "docs/a.md")


def test_show_propagates_a_failing_git_show(repo: Repo, monkeypatch: Any) -> None:
    # Failure injection: the path exists, so ls-tree succeeds, and only `git show` fails.
    real_git = last_updated.git

    def failing_show(*args: str) -> str:
        if args and args[0] == "show":
            raise last_updated.GitError("injected git show failure")
        return cast(str, real_git(*args))

    monkeypatch.setattr(last_updated, "git", failing_show)
    with pytest.raises(last_updated.GitError):
        last_updated.show("HEAD", "docs/a.md")


def test_git_error_is_exit_2_never_a_pass(repo: Repo) -> None:
    assert last_updated.main(["--base", "no-such-ref"]) == 2


def test_main_exit_codes(repo: Repo) -> None:
    assert last_updated.main(["--base", "main"]) == 0
    repo.write("docs/a.md", doc("2026-01-01", "Changed."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    assert last_updated.main(["--base", "main"]) == 1
