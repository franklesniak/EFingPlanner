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


def doc(date: str, body: str = "Body text.", version: str | None = None, revision: int = 0, minor: int = 0) -> str:
    version_line = f"\n**Version:** 1.{minor}.{version}.{revision}\n" if version else ""
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


@pytest.mark.parametrize("path", ["docs/a.md", "docs/new.md"], ids=["modified", "added"])
def test_file_already_on_the_base_branch_tip_passes(repo: Repo, path: str) -> None:
    # The pull request re-makes a change main already has, later; the file adds nothing to the
    # merge, so neither its later date nor its repeated Version is a problem.
    edited = doc("2026-03-05", "Edited.", version="20260305")
    repo.git("switch", "-q", "main")
    repo.write(path, edited)
    repo.commit("change on main", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write(path, edited)
    repo.commit("same change, later", "2026-03-07T10:00:00+00:00")
    assert run(repo) == []


def test_mechanical_change_passes_after_the_base_branch_moved(repo: Repo) -> None:
    # main changed the file after the fork, so the head no longer equals the tip; the pull
    # request's own change is trailing whitespace only, which needs no bump.
    repo.git("switch", "-q", "main")
    repo.write("docs/a.md", doc("2026-03-04", "Changed on main."))
    repo.commit("change on main", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01").replace("Body text.", "Body text. "))
    repo.commit("whitespace", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_metadata_the_base_branch_added_after_the_fork_is_reported(repo: Repo) -> None:
    # main gives docs/plain.md a metadata block; the PR edits its body. They merge cleanly, and
    # the merged file would keep main's older date over the PR's newer content.
    repo.git("switch", "-q", "main")
    repo.write("docs/plain.md", doc("2026-03-04", "Text."))
    repo.commit("add metadata on main", "2026-03-04T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/plain.md", "# No metadata\n\nText changed.\n")
    repo.commit("edit the body", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/plain.md" in problems[0] and "has added a Last Updated field" in problems[0]


def test_wrong_shape_date_in_a_new_file_is_reported(repo: Repo) -> None:
    repo.write("docs/new.md", doc("2026-03-05").replace("2026-03-05", "2026/03/05"))
    repo.commit("add", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/new.md" in problems[0] and "YYYY-MM-DD form" in problems[0]


def test_version_too_long_to_read_is_reported(repo: Repo) -> None:
    huge = doc("2026-03-05", "Changed.", version="20260305").replace(".20260305.0", ".20260305." + "9" * 5000)
    repo.write("docs/a.md", huge)
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/a.md" in problems[0] and "cannot be read as numbers" in problems[0]


def test_unreadable_base_version_does_not_stop_the_check(repo: Repo) -> None:
    # main's copy carries a Version too long to read; the PR's own Version is judged as if main had none.
    huge = doc("2026-01-01", "Body.", version="20260101").replace(".20260101.0", ".20260101." + "9" * 5000)
    publish(repo, huge, "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305"))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_impossible_calendar_date_is_reported_by_file(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-02-30", "Changed."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/a.md" in problems[0] and "not a real calendar date" in problems[0]


def test_impossible_base_date_does_not_stop_the_check(repo: Repo) -> None:
    publish(repo, doc("2026-02-30", "Body."), "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
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


def test_rewrite_below_the_rename_threshold_is_a_new_file_dated_by_its_move(repo: Repo) -> None:
    # git reports a rename that keeps too little content as a deletion and an addition. With
    # honest dates the addition is the newest change, so its date is required.
    old_body = "\n\n".join("Old paragraph %d says something." % i for i in range(40))
    new_body = "\n\n".join("New paragraph %d says something else entirely." % i for i in range(40))
    publish(repo, doc("2026-01-01", old_body), "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-06", old_body + "\n\nAn edit."))
    repo.commit("edit", "2026-03-06T10:00:00+00:00")
    repo.git("mv", "docs/a.md", "docs/b.md")
    repo.write("docs/b.md", doc("2026-03-06", new_body))
    repo.commit("rename and rewrite", "2026-03-07T10:00:00+00:00")
    changed = repo.git("diff", "--name-status", "-M", "main", "HEAD", "--", "docs")
    assert "D\tdocs/a.md" in changed and "A\tdocs/b.md" in changed   # below git's threshold
    problems = run(repo)
    assert len(problems) == 1 and "docs/b.md" in problems[0] and "Set it to 2026-03-07" in problems[0]


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


def octopus_sides(repo: Repo, field: str) -> str:
    """Two side branches edit separate paragraphs of docs/a.md; returns their body."""
    body = "\n".join(["Para one."] + ["filler %d" % i for i in range(12)] + ["Para two."]
                     + ["more %d" % i for i in range(12)] + ["Para three."])
    repo.write("docs/a.md", doc("2026-01-01", body))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "-c", "side1", "main")
    repo.write("docs/a.md", doc(field, body.replace("Para one.", "Para one, side one.")))
    repo.commit("side one", "2026-03-05T09:00:00+00:00")
    repo.git("switch", "-q", "-c", "side2", "main")
    repo.write("docs/a.md", doc(field, body.replace("Para three.", "Para three, side two.")))
    repo.commit("side two", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "pr")
    return body


def test_automatic_octopus_merge_is_dated_by_the_side_edits(repo: Repo) -> None:
    octopus_sides(repo, "2026-01-01")
    repo.git("merge", "-q", "--no-ff", "-m", "octopus", "side1", "side2", date="2026-03-06T10:00:00+00:00")
    text = repo.git("show", "HEAD:docs/a.md")
    assert "Para one, side one." in text and "Para three, side two." in text
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_octopus_check_needs_no_git_identity(repo: Repo, monkeypatch: Any, tmp_path_factory: Any) -> None:
    # CI runners configure no user name or email; the temporary merge steps must not need one.
    octopus_sides(repo, "2026-03-05")
    repo.git("merge", "-q", "--no-ff", "-m", "octopus", "side1", "side2", date="2026-03-06T10:00:00+00:00")
    empty = tmp_path_factory.mktemp("config") / "gitconfig"
    empty.write_bytes(b"")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for name in ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL", "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL", "EMAIL"):
        monkeypatch.delenv(name, raising=False)
    repo.git("config", "--unset", "user.name")
    repo.git("config", "--unset", "user.email")
    repo.git("config", "user.useConfigOnly", "true")
    assert run(repo) == []


def test_octopus_merge_with_its_own_edit_is_dated_by_the_merge(repo: Repo) -> None:
    body = octopus_sides(repo, "2026-03-05")
    repo.git("merge", "-q", "--no-ff", "--no-commit", "side1", "side2")
    edited = body.replace("Para one.", "Para one, side one.").replace("Para three.", "Para three, side two.")
    repo.write("docs/a.md", doc("2026-03-05", edited.replace("Para two.", "Para two, edited in the merge.")))
    repo.git("add", "-A")
    repo.git("commit", "-q", "-m", "octopus with an edit", date="2026-03-06T10:00:00+00:00")
    assert len(repo.git("rev-parse", "HEAD^@").split()) == 3
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-06" in problems[0]


def test_replacing_a_file_with_a_symlink_reports_the_removed_field(repo: Repo) -> None:
    # Built with plumbing, because creating a symlink on Windows needs extra privileges.
    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=repo.root, input="elsewhere.md",
                          capture_output=True, text=True, check=True).stdout.strip()
    repo.git("update-index", "--cacheinfo", "120000,%s,docs/a.md" % blob)
    repo.git("commit", "-q", "-m", "replace with a symlink", date="2026-03-05T10:00:00+00:00")
    assert repo.git("diff", "--name-status", "main..HEAD").startswith("T")
    problems = run(repo)
    assert len(problems) == 1 and "docs/a.md" in problems[0] and "removed it" in problems[0]


def test_commented_out_field_is_not_the_real_field(repo: Repo) -> None:
    commented = "<!--\n- **Last Updated:** 2000-01-01\n-->\n"
    repo.write("docs/plain.md", "# No metadata\n\n" + commented + "\nText.\n")
    repo.commit("comment", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/plain.md", "# No metadata\n\n" + commented + "\nText changed.\n")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_real_field_after_a_one_line_comment_is_still_found(repo: Repo) -> None:
    repo.write("docs/a.md", "<!-- markdownlint-disable MD013 -->\n" + doc("2026-01-01", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_fence_line_inside_a_comment_does_not_open_a_fence(repo: Repo) -> None:
    repo.write("docs/a.md", "<!--\n```\n-->\n" + doc("2026-01-01", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_comment_marker_inside_a_fence_does_not_open_a_comment(repo: Repo) -> None:
    repo.write("docs/a.md", "```html\n<!--\n```\n\n" + doc("2026-01-01", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_whitespace_only_line_losing_its_spaces_is_mechanical(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "Para.\n  \nNext."))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Para.\n\nNext."))
    repo.commit("strip", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_spaces_at_the_end_of_the_file_are_not_a_hard_break(repo: Repo) -> None:
    # No final newline: the spaces are not before a line ending, so nothing breaks.
    repo.write("docs/a.md", doc("2026-01-01", "Last line")[:-1] + "  ")
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", "Last line")[:-1])
    repo.commit("strip", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


@pytest.mark.parametrize("before, after", [
    ("Para.  \n\nNext.", "Para.\n\nNext."),                      # end of a paragraph
    ("## Heading  \n\nText.", "## Heading\n\nText."),            # after an ATX heading
    ("```text\ncode  \nmore\n```", "```text\ncode\nmore\n```"),  # inside a code block
    ("Intro  \n- item", "Intro\n- item"),                        # before a list item
], ids=["paragraph-end", "heading", "code-block", "before-list-item"])
def test_spaces_that_do_not_render_a_break_are_mechanical(repo: Repo, before: str, after: str) -> None:
    repo.write("docs/a.md", doc("2026-01-01", before))
    repo.commit("base-ish", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-01-01", after))
    repo.commit("strip", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


# The other required fields, so that only the structure under test keeps the line from being the field.
REQUIRED = "- **Status:** Active\n- **Owner:** Maintainers\n- **Scope:** Test.\n"


@pytest.mark.parametrize("block", [
    "<div>\n" + REQUIRED + "- **Last Updated:** 2000-01-01\n</div>",
    "<pre>\n" + REQUIRED + "- **Last Updated:** 2000-01-01\n</pre>",
    "".join("> " + line + "\n" for line in (REQUIRED + "- **Last Updated:** 2000-01-01").split("\n")),
    REQUIRED + "- Outer\n  - **Last Updated:** 2000-01-01",
    REQUIRED.replace("- ", "* ") + "* **Last Updated:** 2000-01-01",
    REQUIRED + "\n> > **Last Updated:** 2000-01-01",
    REQUIRED + "- Note\n  **Last Updated:** 2000-01-01",
    REQUIRED + "- Note\n\n  **Last Updated:** 2000-01-01",
], ids=["div-block", "pre-block", "block-quote", "nested-list", "star-bullet", "paragraph-at-list-depth",
        "continuation-line", "second-paragraph"])
def test_field_like_line_outside_a_top_level_dash_item_is_not_the_field(repo: Repo, block: str) -> None:
    repo.write("docs/plain.md", "# No metadata\n\n" + block + "\n\nText changed.\n")
    repo.commit("example only", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def publish(repo: Repo, text: str, date: str, path: str = "docs/a.md") -> None:
    """Commit `text` on the pr branch and fast-forward main to it: the published baseline."""
    repo.write(path, text)
    repo.commit("publish", date)
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")


def test_example_bullet_later_in_the_body_is_not_the_field(repo: Repo) -> None:
    repo.write("docs/plain.md", "# No metadata\n\nIntro changed.\n\n- **Last Updated:** 2000-01-01\n")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_real_block_after_front_matter_without_an_h1_is_found(repo: Repo) -> None:
    rule = "---\ndescription: Test rule.\n---\n- **Status:** Active\n- **Owner:** Maintainers\n- **Last Updated:** 2026-01-01\n- **Scope:** Test.\n\n%s\n"
    publish(repo, rule % "Body.", "2026-01-01T12:00:00+00:00", "docs/rule.mdc")
    repo.write("docs/rule.mdc", rule % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/rule.mdc" in problems[0] and "Set it to 2026-03-05" in problems[0]


def test_block_at_the_top_of_a_body_without_an_h1_is_found(repo: Repo) -> None:
    text = "<!-- markdownlint-disable MD013 -->\n\n- **Status:** Active\n- **Owner:** Maintainers\n- **Last Updated:** 2026-01-01\n- **Scope:** Test.\n\n%s\n"
    publish(repo, text % "Body.", "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", text % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_leading_thematic_break_is_not_front_matter(repo: Repo) -> None:
    # A document may open with a thematic break and have another later; only YAML is front matter.
    text = "---\n" + doc("2026-01-01", "%s") + "\n---\n\nMore.\n"
    publish(repo, text % "Body.", "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", text % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_prose_between_thematic_breaks_is_not_front_matter(repo: Repo) -> None:
    # "Intro." parses as a YAML string, not a mapping, so both breaks stay in the body. The list
    # after them is then not at the top of the body, where a block without an H1 must be.
    meta = "- **Status:** Active\n- **Owner:** Maintainers\n- **Last Updated:** 2026-01-01\n- **Scope:** Test.\n\n%s\n"
    text = "---\n\nIntro.\n\n---\n\n" + meta
    publish(repo, text % "Body.", "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", text % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_list_without_the_required_fields_is_not_the_block(repo: Repo) -> None:
    listed = "# No metadata\n\n- **Status:** Active\n- **Last Updated:** 2000-01-01\n\n%s\n"
    publish(repo, listed % "Text.", "2026-01-01T12:00:00+00:00", "docs/plain.md")
    repo.write("docs/plain.md", listed % "Text changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_unrelated_histories_merge_is_checked(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    repo.git("switch", "-q", "--orphan", "other")   # starts with an empty index and tree
    repo.write("docs/other.md", doc("2026-03-05", "Other."))   # added by a root commit, so it needs its date
    repo.commit("other root", "2026-03-05T11:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.git("merge", "-q", "--no-ff", "--allow-unrelated-histories", "-m", "merge other", "other",
             date="2026-03-06T10:00:00+00:00")
    assert run(repo) == []


@pytest.mark.parametrize("raw", [
    '<a href="https&#58;//example.com/x.md">x</a>',
    '<a href="https&#58//example.com/x.md">x</a>',      # a numeric reference decodes without its semicolon
    '<a href="https&#x3a;//example.com/x.md">x</a>',
], ids=["decimal", "no-semicolon", "hex"])
def test_entity_encoded_absolute_url_is_not_relative(repo: Repo, raw: str) -> None:
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_h1_after_line_30_does_not_move_the_block(repo: Repo) -> None:
    # The guide looks after the H1 only when it starts in the first 30 lines of the body.
    text = ("- **Status:** Active\n- **Owner:** Maintainers\n- **Last Updated:** 2026-01-01\n- **Scope:** Test.\n" + "\n" * 30
            + "# Title\n\n- **Last Updated:** 2000-01-01\n\n%s\n")
    publish(repo, text % "Body.", "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", text % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Last Updated is 2026-01-01" in problems[0]


def test_block_moved_below_the_introduction_is_reported(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05").replace("# Title\n", "# Title\n\nIntroduction.\n"))
    repo.commit("move the block", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "moved it out of that block" in problems[0]


def test_comment_between_the_h1_and_the_block_is_skipped(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-01-01", "Changed.").replace("## Metadata", "<!-- note -->\n\n## Metadata"))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


LINKED = "See [other](%sother.md), ![pic](%spic.png), [site](https://example.com/x.md), [top](#top) and [root](/README.md)."


def test_moving_a_file_with_a_relative_link_needs_a_bump(repo: Repo) -> None:
    publish(repo, doc("2026-01-01", LINKED % ("", "")), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "docs/sub/a.md" in problems[0] and "Set it to 2026-03-05" in problems[0]


@pytest.mark.parametrize("raw", [
    "<img src=pic.png>",
    "<img src='pic.png'>",
    '<a HREF = "other.md">x</a>',
    '<p>\n<img alt="a" src=pic.png />\n</p>',
    '<picture><source srcset="dark.png 1x, dark2.png 2x"></picture>',
    '<img srcset="data:image/png;base64,AAAA 1x, pic.png 2x">',
    '<a href="#top" ping="https://example.com/p audit">top</a>',
    '<div itemscope itemid="thing.md">x</div>',
    '<link rel="preload" as="image" href="/abs.png" imagesrcset="pic.png 1x">',
    '<svg><image xlink:href="pic.png" /></svg>',
    # The helper parses none of these, so each ties the tag to the file's directory.
    '<span style="background-image: url(pic.png)">x</span>',
    '<style>\n.x { background: url(pic.png); }\n</style>',
    '<iframe srcdoc="&lt;img src=pic.png&gt;"></iframe>',
    '<meta http-equiv="refresh" content="0; url=other.md">',
    '<a href="/abs.md" onclick="location = \'other.md\'">x</a>',
    # In an HTML block the tag reaches the browser as written, and it reads srcset despite the
    # missing space; the helper's attribute grammar stops at it.
    '<div>\n<img src="/abs.png"srcset="pic.png 1x">\n</div>',
    '<a href="&nbsp;https://example.com/x.md">x</a>',   # the URL parser keeps a leading U+00A0
], ids=["unquoted", "single-quoted", "uppercase-spaced", "in-a-block", "srcset", "srcset-after-data-url", "ping",
        "itemid", "imagesrcset", "xlink-href", "style-attribute", "style-element", "srcdoc", "meta-refresh",
        "event-handler", "unread-attribute", "nbsp-before-scheme"])
def test_moving_a_file_with_a_relative_raw_html_reference_needs_a_bump(repo: Repo, raw: str) -> None:
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


@pytest.mark.parametrize("body", [
    "```html\n<img src=pic.png>\n```",                              # code shows the tag as text
    '<a title="see href=x.md" href="https://example.com/">x</a>',   # a lookalike inside a value
    "<!-- <img src=\"pic.png\"> -->",                               # a commented-out tag
    '<img srcset="data:image/png;base64,AAAA 1x">',                 # a data URL keeps its comma
    '<a href="ht&#10;tps://example.com/x.md">x</a>',                # the URL parser drops a newline
    '<a href="\\x.md">x</a>',                                       # a browser reads \ as /
    '<img srcset="https://example.com/a.png&nbsp;,pic.png 2x">',    # U+00A0 does not split candidates
    '<a href="/x.md" ping="https://example.com/p&nbsp;q.md">x</a>', # nor ping URLs
], ids=["code-block", "value-lookalike", "comment", "srcset-data-url", "newline-in-scheme", "backslash-root",
        "srcset-nbsp", "ping-nbsp"])
def test_raw_html_lookalikes_are_not_references(repo: Repo, body: str) -> None:
    publish(repo, doc("2026-01-01", "Text.\n\n" + body), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


@pytest.mark.parametrize("raw", [
    "<img src={up}pic.png>",
    "<img src='{up}pic.png'>",
    '<a href="{up}x.md" ping="{up}p https://example.com/q">x</a>',
    '<div itemscope itemid="{up}thing.md">x</div>',
    '<blockquote cite="{up}source.md">q</blockquote>',
    '<object data="{up}file.pdf"></object>',
    '<form action="{up}f"><button formaction="{up}g">b</button></form>',
    '<video poster="{up}poster.png"></video>',
    '<table background="{up}bg.png"><tr><td>x</td></tr></table>',
    '<img src="/a.png" alt="a" longdesc="{up}d.md">',
    '<svg><image xlink:href="{up}pic.png" /></svg>',
], ids=["unquoted", "single-quoted", "href-and-ping", "itemid", "cite", "data", "action-and-formaction", "poster",
        "background", "longdesc", "xlink-href"])
def test_move_that_keeps_every_url_attribute_target_needs_no_bump(repo: Repo, raw: str) -> None:
    # Each URL attribute is resolved, so a move that keeps its target is mechanical. Were one not
    # resolved, it would tie the tag to the directory, and the move would need a bump.
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw.replace("{up}", "")), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.write("docs/sub/a.md", doc("2026-01-01", "Text.\n\n" + raw.replace("{up}", "../")))
    repo.commit("move and keep targets", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_attribute_after_a_non_ascii_space_is_not_read_as_a_url(repo: Repo) -> None:
    # A browser separates attributes only with ASCII whitespace, so after U+00A0 the name is
    # " src", not src; its value is text, and changing it is a content change.
    raw = '<div>\n<img alt="x" src="{up}pic.png">\n</div>'
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw.replace("{up}", "")), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.write("docs/sub/a.md", doc("2026-01-01", "Text.\n\n" + raw.replace("{up}", "../")))
    repo.commit("move and edit the value", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_visible_text_after_a_comment_is_not_skipped(repo: Repo) -> None:
    # The comment block renders "Visible introduction", so the list after it is not at the top
    # of the body, and this page has no metadata block.
    listed = ("<!-- note -->Visible introduction\n\n- **Status:** Active\n- **Owner:** Maintainers\n"
              "- **Last Updated:** 2000-01-01\n- **Scope:** Example.\n\n%s\n")
    publish(repo, listed % "Text.", "2026-01-01T12:00:00+00:00", "docs/plain.md")
    repo.write("docs/plain.md", listed % "Text changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


@pytest.mark.parametrize("comments", ["<!-- one --> <!-- two -->", "<!-->", "<!--->"],
                         ids=["two-on-a-line", "empty", "empty-dash"])
def test_a_block_of_only_comments_is_skipped(repo: Repo, comments: str) -> None:
    text = (comments + "\n\n- **Status:** Active\n- **Owner:** Maintainers\n- **Last Updated:** 2026-01-01\n"
            "- **Scope:** Test.\n\n%s\n")
    publish(repo, text % "Body.", "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", text % "Body changed.")
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


@pytest.mark.parametrize("raw", [
    '<a href="%2e%2e/shared.md">x</a>',
    '<a href="%2E%2e/shared.md">x</a>',
    '<a href="..\\shared.md">x</a>',
    '<a href="../../../shared.md">x</a>',
], ids=["percent-dots", "percent-dots-mixed-case", "backslash", "above-the-root"])
def test_url_path_rules_keep_a_target_across_a_sibling_move(repo: Repo, raw: str) -> None:
    # From docs/ and from other/, each reference resolves to /shared.md under the URL Standard's
    # path rules, so moving the file between the two needs no bump.
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw), "2026-01-01T12:00:00+00:00")
    (repo.root / "other").mkdir()
    repo.git("mv", "docs/a.md", "other/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


SLASH = chr(92)   # a backslash, built so no escaping layer can change it


@pytest.mark.parametrize("before, after", [
    ('<a href="ht&#10;tps://a.example/x.md">x</a>', '<a href="ht&#10;tps://b.example/x.md">x</a>'),
    ('<a href="' + SLASH * 2 + "a.example" + SLASH + 'x.md">x</a>',
     '<a href="' + SLASH * 2 + "b.example" + SLASH + 'x.md">x</a>'),
], ids=["newline-in-scheme", "backslash-host"])
def test_changing_the_host_of_an_absolute_reference_is_content(repo: Repo, before: str, after: str) -> None:
    # A browser reads both forms as absolute URLs, so the host is part of what the page links to.
    publish(repo, doc("2026-01-01", "Text.\n\n" + before), "2026-01-01T12:00:00+00:00")
    repo.write("docs/a.md", doc("2026-01-01", "Text.\n\n" + after))
    repo.commit("change the host", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_directory_name_with_a_hash_stays_part_of_the_path(repo: Repo) -> None:
    # "c#1" is a directory name, not a URL fragment, so the move into its subfolder keeps the target.
    publish(repo, doc("2026-01-01", "Text.\n\n[x](x.md)"), "2026-01-01T12:00:00+00:00", "docs/c#1/a.md")
    (repo.root / "docs" / "c#1" / "sub").mkdir()
    repo.git("mv", "docs/c#1/a.md", "docs/c#1/sub/a.md")
    repo.write("docs/c#1/sub/a.md", doc("2026-01-01", "Text.\n\n[x](../x.md)"))
    repo.commit("move and keep the target", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_moving_html_the_helper_fully_resolves_needs_no_bump(repo: Repo) -> None:
    # Every attribute here is a resolved URL or one that never holds a URL, so nothing is tied
    # to the directory, and every URL is absolute or a fragment.
    body = ('<a id="top"></a>\n\n<img src="/abs.png" alt="A" width="10" class="x" data-note="y" aria-label="z">\n\n'
            '<details open><summary>More</summary>Text.</details>\n\n<a href="#top" title="Top">up</a><br>')
    publish(repo, doc("2026-01-01", "Text.\n\n" + body), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


@pytest.mark.parametrize("raw", [
    '<picture><source srcset="%sdark.png 1x, %sdark2.png 2x"><img src="%spic.png"></picture>',
    '<link rel="preload" as="image" imagesrcset="%sdark.png 1x, %sdark2.png 2x" href="%spic.png">',
    '<IMG SRC="%sdark.png" ALT="x"><A HREF="%sdark2.png">x</A><img src="%spic.png">',   # names are case-insensitive
], ids=["srcset", "imagesrcset", "uppercase-names"])
def test_move_that_keeps_every_srcset_target_needs_no_bump(repo: Repo, raw: str) -> None:
    publish(repo, doc("2026-01-01", "Text.\n\n" + raw % ("", "", "")), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.write("docs/sub/a.md", doc("2026-01-01", "Text.\n\n" + raw % ("../", "../", "../")))
    repo.commit("move and keep targets", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_edit_before_a_copy_then_delete_rename_sets_the_date(repo: Repo) -> None:
    # A reordering rebase can leave later commits with earlier author dates.
    repo.write("docs/a.md", doc("2026-03-05", "Edited."))
    repo.commit("edit", "2026-03-06T10:00:00+00:00")
    repo.write("docs/b.md", doc("2026-03-05", "Edited."))
    repo.commit("copy", "2026-03-05T11:00:00+00:00")
    repo.git("rm", "-q", "docs/a.md")
    repo.commit("delete", "2026-03-05T12:00:00+00:00")
    assert repo.git("diff", "--name-status", "-M", "main..HEAD").startswith("R")
    problems = run(repo)
    assert len(problems) == 1 and "docs/b.md" in problems[0] and "Set it to 2026-03-06" in problems[0]


def test_edit_before_a_deletion_and_restoration_sets_the_date(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Edited."))
    repo.commit("edit", "2026-03-06T10:00:00+00:00")
    repo.git("rm", "-q", "docs/a.md")
    repo.commit("delete", "2026-03-05T11:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Edited."))
    repo.commit("restore", "2026-03-05T12:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-06" in problems[0]


def test_date_later_than_the_change_fails(repo: Repo) -> None:
    repo.write("docs/new.md", doc("2099-01-01", version="20990101"))
    repo.commit("add", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "later than the last commit" in problems[0] and "Set it to 2026-03-05" in problems[0]


def test_amended_commit_may_carry_its_commit_day(repo: Repo) -> None:
    # An amend keeps the author date but records a new commit date, the day the change was made.
    repo.write("docs/a.md", doc("2026-03-06", "Changed."))
    repo.git("add", "-A")
    env = dict(os.environ, GIT_AUTHOR_DATE="2026-03-05T23:00:00+00:00", GIT_COMMITTER_DATE="2026-03-06T09:00:00+00:00")
    subprocess.run(["git", "commit", "-q", "-m", "amended"], cwd=repo.root, env=env, check=True)
    assert run(repo) == []


def test_unchanged_later_base_date_is_allowed(repo: Repo) -> None:
    # The base's own date was not set by this pull request, so a later value is not its error.
    publish(repo, doc("2026-03-10"), "2026-03-10T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-10", "An older change, rebased."))
    repo.commit("rebased", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_move_that_keeps_every_target_needs_no_bump(repo: Repo) -> None:
    publish(repo, doc("2026-01-01", LINKED % ("", "")), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.write("docs/sub/a.md", doc("2026-01-01", LINKED % ("../", "../")))
    repo.commit("move and keep targets", "2026-03-05T10:00:00+00:00")
    assert "R" in repo.git("diff", "--name-status", "-M", "main..HEAD")
    assert run(repo) == []


def test_move_without_relative_references_needs_no_bump(repo: Repo) -> None:
    body = "See [site](https://example.com/x.md), [top](#top), [query](?tab=1) and [root](/README.md)."
    publish(repo, doc("2026-01-01", body), "2026-01-01T12:00:00+00:00")
    (repo.root / "docs" / "sub").mkdir()
    repo.git("mv", "docs/a.md", "docs/sub/a.md")
    repo.commit("move", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_same_day_edit_needs_the_next_revision(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305"), "2026-03-05T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305"))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "already has 1.0.20260305.0, so the revision must be 1" in problems[0]
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305", revision=1))
    repo.commit("next revision", "2026-03-05T10:05:00+00:00")
    assert run(repo) == []


def test_next_day_edit_resets_the_revision(repo: Repo) -> None:
    publish(repo, doc("2026-03-04", version="20260304", revision=2), "2026-03-04T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305", revision=3))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "so the revision must be 0" in problems[0]
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305"))
    repo.commit("reset", "2026-03-05T10:05:00+00:00")
    assert run(repo) == []


def test_minor_change_resets_the_revision(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305", revision=1), "2026-03-05T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305", minor=1))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_new_file_version_starts_at_revision_zero(repo: Repo) -> None:
    repo.write("docs/new.md", doc("2026-03-05", version="20260305", revision=1))
    repo.commit("add", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "no Version for this file, so the revision must be 0" in problems[0]


def test_published_baseline_is_the_base_branch_tip(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305"), "2026-03-05T08:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.write("docs/a.md", doc("2026-03-05", "Main's change.", version="20260305", revision=1))
    repo.commit("main publishes revision 1", "2026-03-05T09:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-03-05", "The PR's change.", version="20260305", revision=1))
    repo.commit("pr also picks revision 1", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "already has 1.0.20260305.1, so the revision must be 2" in problems[0]


def test_stale_date_is_reported_before_the_revision(repo: Repo) -> None:
    # Once the date is bumped, the revision resets to 0, so asking for N + 1 now would mislead.
    publish(repo, doc("2026-03-04", version="20260304"), "2026-03-04T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-04", "Changed.", version="20260304"))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


def test_version_date_mismatch_is_reported_alone(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "New.", version="20260304", revision=1))
    repo.commit("change", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Version date segment is 20260304" in problems[0]


def test_published_baseline_follows_a_base_branch_rename(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305"), "2026-03-05T08:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("mv", "docs/a.md", "docs/renamed.md")
    repo.commit("main renames the file", "2026-03-05T09:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305"))
    repo.commit("edit under the old name", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "already has 1.0.20260305.0, so the revision must be 1" in problems[0]
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305", revision=1))
    repo.commit("next revision", "2026-03-05T10:05:00+00:00")
    assert run(repo) == []


def test_base_branch_deletion_leaves_no_published_baseline(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305"), "2026-03-05T08:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("rm", "-q", "docs/a.md")
    repo.commit("main deletes the file", "2026-03-05T09:00:00+00:00")
    repo.git("switch", "-q", "pr")
    repo.write("docs/a.md", doc("2026-03-05", "Changed.", version="20260305", revision=1))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "no Version for this file, so the revision must be 0" in problems[0]


def test_mechanical_change_does_not_need_a_new_revision(repo: Repo) -> None:
    publish(repo, doc("2026-03-05", version="20260305"), "2026-03-05T08:00:00+00:00")
    repo.write("docs/a.md", doc("2026-03-05", "Body text. ", version="20260305"))
    repo.commit("whitespace", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_version_line_inside_a_block_quote_is_not_the_version(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "> **Version:** 1.0.20000101.0\n\nChanged."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def test_version_line_outside_the_header_is_not_the_version(repo: Repo) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "**Version:** 1.0.20000101.0\n\nChanged."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    assert run(repo) == []


def fresh_renderer(monkeypatch: Any, **overrides: str) -> None:
    for name, value in overrides.items():
        monkeypatch.setattr(last_updated, name, value)
    monkeypatch.setattr(last_updated, "render", last_updated.Renderer())


def test_missing_renderer_helper_is_exit_2(repo: Repo, monkeypatch: Any, tmp_path_factory: Any) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    fresh_renderer(monkeypatch, HELPER=str(tmp_path_factory.mktemp("helper") / "missing.js"))
    assert last_updated.main(["--base", "main"]) == 2


def test_missing_node_is_exit_2(repo: Repo, monkeypatch: Any) -> None:
    repo.write("docs/a.md", doc("2026-03-05", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    fresh_renderer(monkeypatch, NODE="node-that-does-not-exist")
    assert last_updated.main(["--base", "main"]) == 2


@pytest.mark.parametrize("reply", [
    b"JSON.stringify({ html: 'x', version: null }) + '\\n'",                        # `lastUpdated` missing
    b"JSON.stringify({ html: 'x', lastUpdated: 20260305, version: null }) + '\\n'",  # not a string
    b"'not json\\n'",
    b"process.exit(3)",                                                              # no answer at all
], ids=["missing-key", "wrong-type", "not-json", "no-answer"])
def test_unusable_renderer_answer_is_exit_2(repo: Repo, monkeypatch: Any, tmp_path_factory: Any, reply: bytes) -> None:
    # A helper that forgets `lastUpdated`, for example, must not make every file look field-less.
    fake = tmp_path_factory.mktemp("helper") / "fake.js"
    fake.write_bytes(b"require('readline').createInterface({ input: process.stdin }).on('line', () => "
                     b"process.stdout.write(" + reply + b"));\n")
    repo.write("docs/a.md", doc("2026-01-01", "Changed."))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    fresh_renderer(monkeypatch, HELPER=str(fake))
    assert last_updated.main(["--base", "main"]) == 2


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


def test_file_with_non_utf8_bytes_is_still_checked(repo: Repo) -> None:
    stale = doc("2026-01-01", "Caf\x00 changed.").encode("utf-8").replace(b"\x00", b"\xe9")
    (repo.root / "docs" / "a.md").write_bytes(stale)
    repo.commit("latin-1 byte", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


@pytest.mark.skipif(os.name == "nt", reason="Windows cannot pass a non-UTF-8 filename to git")
def test_non_utf8_filename_is_still_checked(repo: Repo) -> None:
    name = b"docs/caf\xe9.md"
    (repo.root / os.fsdecode(name)).write_bytes(doc("2026-01-01").encode("utf-8"))
    repo.commit("add", "2026-01-01T12:00:00+00:00")
    repo.git("switch", "-q", "main")
    repo.git("merge", "-q", "--ff-only", "pr")
    repo.git("switch", "-q", "pr")
    (repo.root / os.fsdecode(name)).write_bytes(doc("2026-01-01", "Changed.").encode("utf-8"))
    repo.commit("edit", "2026-03-05T10:00:00+00:00")
    problems = run(repo)
    assert len(problems) == 1 and "Set it to 2026-03-05" in problems[0]


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
    monkeypatch.setattr(last_updated, "content_changes", lambda base, head, path, origin=None: [])
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
