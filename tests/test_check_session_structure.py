"""Tests for the session-structure check.

The script is loaded by file path because its filename is hyphenated, matching
the pattern used by `tests/test_check_prohibited_placeholders.py`.
"""

from __future__ import annotations

import importlib.util
import os
import pathlib
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

SCRIPT_PATH = (
    Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-session-structure.py"
)
SPEC = importlib.util.spec_from_file_location("check_session_structure", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load session-structure script from {SCRIPT_PATH}")
_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _module
SPEC.loader.exec_module(_module)

structure = cast(Any, _module)


def build_session(
    *,
    number: str = "07",
    title: str = "A Well-Formed Session",
    nav: bool = True,
    parents: bool = True,
    sections: tuple[str, ...] = (
        "Goal",
        "Start Here",
        "Steps",
        "Workspace",
        "Artifact Created",
        "Stop Point",
        "Source Check",
    ),
    empty_sections: tuple[str, ...] = (),
    markers: str = "",
    extra: str = "",
    parent_bullets: tuple[str, ...] = (
        "- Status: Core",
        "- Estimated time: 20-30 minutes",
        "- Parent involvement: 5-minute check-in",
    ),
) -> str:
    """Return a synthetic session document for a test."""
    parts = ["<!-- markdownlint-disable MD013 -->"]
    if markers:
        parts.append(markers)
    parts.append("")
    parts.append(f"# Session {number}: {title}")
    parts.append("")
    if nav:
        parts.append("You are here: Phase 0 (Setup). Previous: none | Next: 08 Something")
        parts.append("")
    if parents:
        parts.append("**For parents:**")
        parts.append("")
        parts.extend(parent_bullets)
        parts.append("")
    for section in sections:
        parts.append(f"## {section}")
        parts.append("")
        if section not in empty_sections:
            parts.append(f"Real content for {section}.")
            parts.append("")
    if extra:
        parts.append(extra)
    return "\n".join(parts) + "\n"


def check(text: str, name: str = "07_a_session.md") -> list[str]:
    """Return the violation messages for one document."""
    return [v.message for v in structure.check_text(text, name, name)]


# ---------------------------------------------------------------------------
# The happy path
# ---------------------------------------------------------------------------


def test_a_well_formed_session_has_no_violations() -> None:
    """A session with every required part passes."""
    assert check(build_session()) == []


def test_extra_sections_between_mandatory_ones_are_allowed() -> None:
    """Session 00 carries several extra sections; that is legal."""
    text = build_session(
        sections=(
            "Goal",
            "Start Here",
            "Steps",
            "Workspace",
            "An Extra Adult Section",
            "Artifact Created",
            "Stop Point",
            "Source Check",
        )
    )
    assert check(text) == []


# ---------------------------------------------------------------------------
# Mandatory sections
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "missing",
    ["Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point"],
)
def test_each_mandatory_section_is_required(missing: str) -> None:
    """Dropping any one of the six is a violation."""
    sections = tuple(
        s
        for s in (
            "Goal",
            "Start Here",
            "Steps",
            "Workspace",
            "Artifact Created",
            "Stop Point",
            "Source Check",
        )
        if s != missing
    )
    messages = check(build_session(sections=sections))
    assert any(f'missing mandatory section "## {missing}"' in m for m in messages)


def test_mandatory_sections_may_not_be_reordered() -> None:
    """The order is the scaffold, so reordering is a violation."""
    text = build_session(
        sections=(
            "Goal",
            "Steps",
            "Start Here",
            "Workspace",
            "Artifact Created",
            "Stop Point",
            "Source Check",
        )
    )
    assert any("out of order" in m for m in check(text))


def test_an_empty_mandatory_section_is_a_violation() -> None:
    """A heading with nothing under it is not a section."""
    text = build_session(empty_sections=("Stop Point",))
    assert any('"## Stop Point" is empty' in m for m in check(text))


# ---------------------------------------------------------------------------
# Source Check and its exemptions
# ---------------------------------------------------------------------------


def test_source_check_is_required_by_default() -> None:
    """Silence is not an exemption."""
    sections = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")
    assert any("Source Check" in m for m in check(build_session(sections=sections)))


def test_adult_audience_marker_exempts_source_check() -> None:
    """An adult-only setup session is not doing child research."""
    sections = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")
    text = build_session(sections=sections, markers="<!-- audience: adult -- setup only -->")
    assert check(text) == []


def test_explicit_no_source_check_marker_exempts_it() -> None:
    """A stated reason exempts the session."""
    sections = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")
    text = build_session(
        sections=sections, markers="<!-- no-source-check: no research step in this session -->"
    )
    assert check(text) == []


def test_a_marker_without_a_reason_does_not_exempt() -> None:
    """The marker must state why."""
    sections = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")
    text = build_session(sections=sections, markers="<!-- no-source-check: -->")
    assert any("Source Check" in m for m in check(text))


# ---------------------------------------------------------------------------
# Title, navigation, parent strip
# ---------------------------------------------------------------------------


def test_a_missing_title_is_a_violation() -> None:
    """Every session names itself."""
    text = build_session().replace("# Session 07: A Well-Formed Session", "# Some Other Title")
    assert any("no session title" in m for m in check(text))


def test_title_number_must_match_the_filename() -> None:
    """A renamed file with a stale title is a real and easy mistake."""
    messages = check(build_session(number="08"), name="07_a_session.md")
    assert any("must agree" in m for m in messages)


def test_a_missing_navigation_line_is_a_violation() -> None:
    """A child needs to see where they are in the sequence."""
    assert any("navigation line" in m for m in check(build_session(nav=False)))


def test_a_missing_parent_strip_is_a_violation() -> None:
    """Parent-facing metadata is mandatory."""
    assert any("parent metadata strip" in m for m in check(build_session(parents=False)))


# ---------------------------------------------------------------------------
# Worksheet form
# ---------------------------------------------------------------------------


def test_a_fenced_underscore_worksheet_is_rejected() -> None:
    """Worksheet fill-ins are Markdown tables, not fenced underscore blocks."""
    extra = "```text\nWhat I learned: ____________\n```"
    assert any("worksheet fill-in" in m for m in check(build_session(extra=extra)))


def test_a_normal_code_fence_is_allowed() -> None:
    """A real code block is not a worksheet."""
    extra = "```python\nprint('hello')\n```"
    assert check(build_session(extra=extra)) == []


def test_an_inline_underscore_blank_is_allowed() -> None:
    """Inline blanks in prose or a table cell are fine."""
    extra = "Write your home airport here: ______ (from your Trip-Basics card)."
    assert check(build_session(extra=extra)) == []


def test_headings_inside_a_fence_are_not_counted() -> None:
    """A fenced example containing '## Goal' must not satisfy the requirement."""
    sections = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")
    text = build_session(sections=sections, markers="<!-- no-source-check: none needed -->")
    fenced = text + "\n```markdown\n## Stop Point\n\nnot a real section\n```\n"
    # Removing the real Stop Point must still be caught even though a fenced copy exists.
    broken = fenced.replace("## Stop Point\n\nReal content for Stop Point.\n", "", 1)
    assert any('missing mandatory section "## Stop Point"' in m for m in check(broken))


# ---------------------------------------------------------------------------
# Path safety and end-to-end
# ---------------------------------------------------------------------------


def test_paths_outside_the_repository_root_are_refused(tmp_path: Path) -> None:
    """CLI input must not drive reads outside the allowlisted tree.

    The in-root file is the positive control. An empty result would also come
    from a `resolve_paths` that rejects everything, which would pass this test
    while breaking the checker.
    """
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    inside = session_dir / "01_inside.md"
    inside.write_text("# Session 01: Inside\n", encoding="utf-8")
    outside = tmp_path.parent / "outside.md"
    outside.write_text("# Session 01: Nope\n", encoding="utf-8")

    assert structure.resolve_paths([str(inside)], tmp_path) == [inside]
    assert structure.resolve_paths([str(outside)], tmp_path) == []


#: A floor, not the real count. The repository has more sessions than this, and
#: is about to have many more. The number exists so that a change which silently
#: stops matching any file fails loudly instead of reporting a clean corpus it
#: never looked at.
MINIMUM_SESSIONS = 10


def test_an_unparsable_filename_is_a_violation() -> None:
    """A filename with no session number cannot be checked, so it is a violation.

    Skipping the check for such a file would let a misnamed session pass the one
    invariant this check exists to hold.
    """
    messages = check(build_session(number="07"), name="session_seven.md")
    assert any("two-digit session number" in m for m in messages)


def test_a_hyphenated_filename_number_still_parses() -> None:
    """`07-name.md` is as valid a shape as `07_name.md`."""
    assert check(build_session(number="07"), name="07-a-session.md") == []


def test_a_nonexistent_explicit_path_is_refused(tmp_path: Path) -> None:
    """A typo must not let the run report success for a corpus it never opened."""
    (tmp_path / "framework" / "sessions").mkdir(parents=True)
    violations = structure.scan_files(["framework/sessions/99_typo.md"], root=tmp_path)
    assert any("nothing to check" in v.message for v in violations)
    assert structure.main(["framework/sessions/99_typo.md"], root=tmp_path) == 1


def test_a_non_markdown_explicit_path_is_refused(tmp_path: Path) -> None:
    """A file that is not Markdown cannot be checked, so it is refused, not skipped."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "notes.txt").write_text("not markdown", encoding="utf-8")
    violations = structure.scan_files(["framework/sessions/notes.txt"], root=tmp_path)
    assert any("nothing to check" in v.message for v in violations)


def test_the_real_session_corpus_is_well_formed() -> None:
    """The gate must be green on the real repository, or it is not a gate."""
    checked = structure.resolve_paths([], structure.REPO_ROOT)
    assert len(checked) >= MINIMUM_SESSIONS, (
        f"only {len(checked)} session file(s) were found. The gate is not looking at the "
        "corpus any more; check DEFAULT_SCAN_GLOB and the path guard."
    )

    violations = structure.scan_files([], root=structure.REPO_ROOT)
    assert not violations, "\n".join(v.format_message() for v in violations)


def test_main_returns_one_when_a_session_is_malformed(tmp_path: Path) -> None:
    """A malformed session fails the run."""
    session_dir = tmp_path / "framework" / "sessions" / "phase_00_setup"
    session_dir.mkdir(parents=True)
    (session_dir / "07_broken.md").write_text(
        build_session(sections=("Goal", "Start Here")), encoding="utf-8"
    )
    assert structure.main([], root=tmp_path) == 1


def test_main_returns_zero_on_a_clean_tree(tmp_path: Path) -> None:
    """A well-formed session passes the run."""
    session_dir = tmp_path / "framework" / "sessions" / "phase_00_setup"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    assert structure.main([], root=tmp_path) == 0


# ---------------------------------------------------------------------------
# Source Check is the seventh field, and seventh is a position
# ---------------------------------------------------------------------------


def test_source_check_may_not_come_before_stop_point() -> None:
    """The style guide numbers Source Check seventh; that is a position, not a label."""
    text = build_session(
        sections=(
            "Goal",
            "Start Here",
            "Steps",
            "Workspace",
            "Artifact Created",
            "Source Check",
            "Stop Point",
        )
    )
    assert any("out of order" in m for m in check(text))


def test_source_check_may_not_come_first() -> None:
    """A session does not open with the record of what it read."""
    text = build_session(
        sections=(
            "Source Check",
            "Goal",
            "Start Here",
            "Steps",
            "Workspace",
            "Artifact Created",
            "Stop Point",
        )
    )
    assert any("out of order" in m for m in check(text))


# ---------------------------------------------------------------------------
# The title is a real heading, not a fenced example
# ---------------------------------------------------------------------------


def test_a_fenced_title_does_not_satisfy_the_title_check() -> None:
    """A title inside a fenced example is an example, not the name of the session."""
    text = build_session().replace("# Session 07: A Well-Formed Session", "# Some Other Title", 1)
    text += "\n```markdown\n# Session 07: Example Session\n```\n"
    assert any("no session title" in m for m in check(text))


def test_a_fenced_title_does_not_mask_a_filename_mismatch() -> None:
    """The number that must match the filename is the real title's, not an example's."""
    text = build_session(number="08").replace(
        "<!-- markdownlint-disable MD013 -->",
        "<!-- markdownlint-disable MD013 -->\n\n```markdown\n# Session 07: Fenced Example\n```",
        1,
    )
    assert any("must agree" in m for m in check(text, name="07_a_session.md"))


def test_the_title_must_be_the_first_heading() -> None:
    """A session names itself before it says anything else."""
    text = build_session().replace(
        "# Session 07: A Well-Formed Session",
        "## Before The Title\n\nStray content.\n\n# Session 07: A Well-Formed Session",
        1,
    )
    assert any("no session title" in m for m in check(text))


def test_a_level_one_heading_does_not_satisfy_a_section_requirement() -> None:
    """The scaffold sections are level-2 headings; one parser must not blur the levels."""
    text = build_session().replace("## Goal", "# Goal", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


# ---------------------------------------------------------------------------
# Symbolic links and the allowlisted tree
# ---------------------------------------------------------------------------


def make_session_dir(tmp_path: Path) -> Path:
    """Return a session directory inside a synthetic repository root."""
    session_dir = tmp_path / "repo" / "framework" / "sessions" / "phase_00_setup"
    session_dir.mkdir(parents=True)
    return session_dir


def link_or_skip(link: Path, target: Path) -> None:
    """Create a symbolic link, or skip the test where the platform forbids one."""
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError) as error:  # pragma: no cover - platform guard
        pytest.skip(f"this platform does not allow symbolic links: {error}")


def test_a_symlinked_session_is_refused_by_the_default_scan(tmp_path: Path) -> None:
    """The default scan is the path CI uses, so the default scan is what must be guarded."""
    outside = tmp_path / "outside.md"
    outside.write_text("## Secret Heading\n\nnot repository content\n", encoding="utf-8")
    session_dir = make_session_dir(tmp_path)
    link_or_skip(session_dir / "08_link.md", outside)
    root = tmp_path / "repo"
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")

    messages = [v.format_message() for v in structure.scan_files([], root=root)]
    assert any("symbolic link" in m for m in messages)
    assert not any("Secret Heading" in m for m in messages)
    assert structure.resolve_paths([], root) == [session_dir / "07_a_session.md"]
    assert structure.main([], root=root) == 1


def test_a_symlinked_session_in_a_directory_argument_is_refused(tmp_path: Path) -> None:
    """A directory argument walks the tree, so the walk needs the same guard."""
    outside = tmp_path / "outside.md"
    outside.write_text("# Session 08: Elsewhere\n", encoding="utf-8")
    session_dir = make_session_dir(tmp_path)
    link_or_skip(session_dir / "08_link.md", outside)
    root = tmp_path / "repo"

    assert structure.resolve_paths([str(session_dir)], root) == []
    assert any(
        "symbolic link" in v.format_message()
        for v in structure.scan_files([str(session_dir)], root=root)
    )


def test_a_path_outside_the_root_fails_the_run(tmp_path: Path) -> None:
    """Refusing to read a path is a verdict, not a silent skip."""
    outside = tmp_path / "outside.md"
    outside.write_text("# Session 01: Nope\n", encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    assert structure.main([str(outside)], root=root) == 1


# ---------------------------------------------------------------------------
# One fence parser governs every structural search
# ---------------------------------------------------------------------------

FENCE = "```"
SIX_SECTIONS = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created", "Stop Point")


def test_a_fenced_no_source_check_marker_does_not_exempt() -> None:
    """An exemption printed in an example is an example, not an exemption."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Example\n\n{FENCE}markdown\n<!-- no-source-check: none -->\n{FENCE}\n",
    )
    assert any("Source Check" in m for m in check(text))


def test_a_fenced_audience_marker_does_not_exempt() -> None:
    """The adult-audience marker is read under the same rule as the other marker."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Example\n\n{FENCE}markdown\n<!-- audience: adult -->\n{FENCE}\n",
    )
    assert any("Source Check" in m for m in check(text))


def test_a_fenced_navigation_line_does_not_satisfy_the_check() -> None:
    """A child cannot navigate by an example of a navigation line."""
    text = build_session(
        nav=False,
        extra=f"## Example\n\n{FENCE}markdown\nYou are here: Phase 1. Next: 06\n{FENCE}\n",
    )
    assert any("navigation line" in m for m in check(text))


def test_a_fenced_parent_strip_does_not_satisfy_the_check() -> None:
    """A parent cannot read an example of a strip."""
    text = build_session(
        parents=False,
        extra=f"## Example\n\n{FENCE}markdown\n**For parents:**\n{FENCE}\n",
    )
    assert any("parent metadata strip" in m for m in check(text))


def test_a_marker_in_a_blockquoted_fence_does_not_exempt() -> None:
    """A fence inside a blockquote is still a fence."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Example\n\n> {FENCE}markdown\n> <!-- no-source-check: none -->\n> {FENCE}\n",
    )
    assert any("Source Check" in m for m in check(text))


def test_a_marker_in_a_list_nested_fence_does_not_exempt() -> None:
    """A fence under a two-digit list item is still a fence."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra=(
            "## Example\n\n10. Like this:\n\n"
            f"    {FENCE}markdown\n    <!-- no-source-check: none -->\n    {FENCE}\n"
        ),
    )
    assert any("Source Check" in m for m in check(text))


# ---------------------------------------------------------------------------
# Fences inside Markdown containers
# ---------------------------------------------------------------------------


def test_a_worksheet_fence_under_a_two_digit_list_item_is_rejected() -> None:
    """Item `10.` puts its content at column four, which is still inside the item."""
    steps = (
        "## Steps\n\n"
        + "".join(f"{n}. Step {n}.\n" for n in range(1, 10))
        + "10. Write your answer.\n\n"
        + f"    {FENCE}text\n    My answer: ______________________\n    {FENCE}\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_worksheet_fence_in_a_blockquote_is_rejected() -> None:
    """A blockquote prefix does not hide a worksheet fence."""
    steps = f"## Steps\n\n> {FENCE}text\n> My answer: ______________________\n> {FENCE}\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_worksheet_fence_under_a_nested_bullet_is_rejected() -> None:
    """A second-level bullet puts its content at column four as well."""
    steps = (
        "## Steps\n\n- Outer.\n  - Inner.\n\n"
        f"    {FENCE}text\n    My answer: ______________________\n    {FENCE}\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_top_level_four_space_fence_marker_is_not_a_fence() -> None:
    """A positive control. At top level, four spaces make an indented code block."""
    steps = f"## Steps\n\n    {FENCE}text\n    plain\n    {FENCE}\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert not any("worksheet fill-in" in m for m in check(text))


def test_a_nested_fence_without_underscores_is_allowed() -> None:
    """A positive control. Container awareness must not reject an ordinary example."""
    steps = f"## Steps\n\n10. Example:\n\n    {FENCE}text\n    plain content\n    {FENCE}\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert check(text) == []


def test_trailing_prose_does_not_close_a_fence() -> None:
    """CommonMark closes a block only on a fence line that carries nothing else."""
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<!-- no-source-check: none -->",
        extra=f"## Example\n\n{FENCE}text\nplain\n{FENCE} and then prose\n## Stop Point\n{FENCE}\n",
    )
    assert check(text) == []


def test_an_info_string_does_not_close_a_fence() -> None:
    """A fence line with an info string opens a block; it never closes one."""
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<!-- no-source-check: none -->",
        extra=f"## Example\n\n{FENCE}text\n{FENCE}markdown\n## Stop Point\n{FENCE}\n",
    )
    assert check(text) == []


def test_an_unterminated_worksheet_fence_is_still_rejected() -> None:
    """A fence that is never closed still holds the underscores it holds."""
    text = build_session(extra=f"{FENCE}text\nMy answer: ______________________\n")
    assert any("worksheet fill-in" in m for m in check(text))


# ---------------------------------------------------------------------------
# The parent strip carries fields, not only a label
# ---------------------------------------------------------------------------


def test_a_parent_strip_with_only_a_label_is_a_violation() -> None:
    """A label with nothing under it tells a parent nothing."""
    messages = check(build_session(parent_bullets=()))
    assert any("Status, Estimated time, Parent involvement" in m for m in messages)


def test_a_parent_strip_missing_one_field_names_that_field() -> None:
    """The violation says which bullet to add."""
    messages = check(
        build_session(
            parent_bullets=("- Status: Core", "- Estimated time: 20-30 minutes")
        )
    )
    assert any(
        "these fields: Parent involvement" in m for m in messages
    ), messages


def test_a_parent_strip_of_prose_only_is_a_violation() -> None:
    """A paragraph under the label is not a field list."""
    messages = check(build_session(parent_bullets=("This session is short.",)))
    assert any("Status, Estimated time, Parent involvement" in m for m in messages)


def test_a_parent_strip_with_bold_field_labels_passes() -> None:
    """A positive control. Bold field labels are the same strip."""
    text = build_session(
        parent_bullets=(
            "- **Status:** Core",
            "- **Estimated time:** 20 minutes",
            "- **Parent involvement:** none",
        )
    )
    assert check(text) == []


def test_the_session_00_strip_shape_passes() -> None:
    """A positive control. Session 00 is adult-only and carries no Planner skill line."""
    text = build_session(
        parent_bullets=(
            "- Status: Core (adult-only setup)",
            "- Estimated time: about 1-2 hours, once",
            "- Parent involvement: adult-owned; the child does not do this session",
            "- Materials: this checklist",
        )
    )
    assert check(text) == []


# ---------------------------------------------------------------------------
# A section that prints nothing is empty
# ---------------------------------------------------------------------------


def test_a_comment_only_section_is_empty() -> None:
    """A drafting note is a bare heading to the child who opens the page."""
    text = build_session(empty_sections=("Stop Point",)).replace(
        "## Stop Point\n", "## Stop Point\n\n<!-- drafting note -->\n", 1
    )
    assert any('"## Stop Point" is empty' in m for m in check(text))


def test_a_markdownlint_disable_only_section_is_empty() -> None:
    """A lint directive is an HTML comment, so it needs no special case."""
    text = build_session(empty_sections=("Stop Point",)).replace(
        "## Stop Point\n", "## Stop Point\n\n<!-- markdownlint-disable -->\n", 1
    )
    assert any('"## Stop Point" is empty' in m for m in check(text))


def test_a_multi_line_comment_only_section_is_empty() -> None:
    """A comment across three lines prints as nothing, the same as one line."""
    text = build_session(empty_sections=("Stop Point",)).replace(
        "## Stop Point\n", "## Stop Point\n\n<!--\nwrite this\n-->\n", 1
    )
    assert any('"## Stop Point" is empty' in m for m in check(text))


def test_a_bare_list_marker_section_is_empty() -> None:
    """One empty bullet does not tell a child when to stop."""
    text = build_session(empty_sections=("Stop Point",)).replace(
        "## Stop Point\n", "## Stop Point\n\n-\n", 1
    )
    assert any('"## Stop Point" is empty' in m for m in check(text))


def test_a_comment_above_real_content_is_not_empty() -> None:
    """A positive control. A note beside real content is fine."""
    text = build_session(empty_sections=("Stop Point",)).replace(
        "## Stop Point\n",
        "## Stop Point\n\n<!-- note -->\n\nStop when the page is full.\n",
        1,
    )
    assert check(text) == []


def test_a_section_holding_only_a_fenced_block_is_not_empty() -> None:
    """A positive control. A code block is content, even though the scan removes it."""
    text = build_session(empty_sections=("Workspace",)).replace(
        "## Workspace\n", f"## Workspace\n\n{FENCE}text\nnotes here\n{FENCE}\n", 1
    )
    assert check(text) == []


# ---------------------------------------------------------------------------
# A commented-out heading is not a heading
# ---------------------------------------------------------------------------


def test_a_heading_inside_a_multiline_comment_is_not_a_section() -> None:
    """A section commented out with `<!-- ... -->` is not on the page at all."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "<!--\n## Goal\n\nReal content for Goal.\n-->\n",
        1,
    )
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_commented_out_heading_alone_is_not_a_section() -> None:
    """The shortest form of the same mistake: only the heading is commented out."""
    text = build_session().replace(
        "## Stop Point\n\nReal content for Stop Point.\n",
        "<!--\n## Stop Point\n-->\n\nReal content for Stop Point.\n",
        1,
    )
    assert any('missing mandatory section "## Stop Point"' in m for m in check(text))


def test_a_commented_out_title_does_not_name_the_session() -> None:
    """A session names itself in words a child can read, not in a comment."""
    text = build_session().replace(
        "# Session 07: A Well-Formed Session",
        "<!--\n# Session 07: A Well-Formed Session\n-->",
        1,
    )
    assert any("no session title" in m for m in check(text))


def test_a_commented_out_navigation_line_does_not_satisfy_the_check() -> None:
    """A navigation line that prints as nothing navigates nobody."""
    text = build_session(nav=False).replace(
        "**For parents:**",
        "<!--\nYou are here: Phase 0 (Setup). Previous: none | Next: 08\n-->\n\n**For parents:**",
        1,
    )
    assert any("navigation line" in m for m in check(text))


def test_a_commented_out_parent_strip_does_not_satisfy_the_check() -> None:
    """A parent cannot read a strip that is inside a comment."""
    text = build_session(parents=False).replace(
        "## Goal",
        "<!--\n**For parents:**\n\n- Status: Core\n- Estimated time: 20 minutes\n"
        "- Parent involvement: none\n-->\n\n## Goal",
        1,
    )
    assert any("parent metadata strip" in m for m in check(text))


def test_a_real_exemption_marker_survives_comment_stripping() -> None:
    """A positive control. The two exemption markers *are* comments, so they must survive."""
    text = build_session(
        sections=SIX_SECTIONS, markers="<!-- no-source-check: no research step here -->"
    )
    assert check(text) == []


def test_a_real_audience_marker_survives_comment_stripping() -> None:
    """A positive control for the other marker."""
    text = build_session(sections=SIX_SECTIONS, markers="<!-- audience: adult -- setup only -->")
    assert check(text) == []


def test_a_fence_inside_a_comment_is_not_a_fence() -> None:
    """A positive control. A commented-out example prints as nothing, fence and all.

    The sibling hook reads a commented-out fence the same way, so the two
    scripts do not disagree about which fences exist.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<!-- no-source-check: none -->",
        extra=f"## Example\n\n<!--\n{FENCE}text\nMy answer: ______________________\n{FENCE}\n-->\n",
    )
    assert check(text) == []


def test_a_heading_after_an_inline_comment_on_one_line_is_not_a_heading() -> None:
    """A positive control. CommonMark makes the whole line raw HTML.

    ``<!-- note -->## Goal`` prints the literal characters ``## Goal``; it is
    not a section. See <https://spec.commonmark.org/0.31.2/#html-blocks>.
    """
    text = build_session().replace("## Goal\n", "<!-- note -->## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


# ---------------------------------------------------------------------------
# A worksheet blank is a blank, not every underscore
# ---------------------------------------------------------------------------


def test_an_identifier_with_embedded_underscores_is_not_a_worksheet() -> None:
    """`A____B` renders as code. The rule prohibits underscore forms, not underscores."""
    extra = f"{FENCE}text\nA____B\n{FENCE}"
    assert check(build_session(extra=extra)) == []


def test_a_long_embedded_underscore_run_is_not_a_worksheet() -> None:
    """Run length does not turn an identifier into a form."""
    extra = f"{FENCE}python\nMAX______________VALUE = 3\n{FENCE}"
    assert check(build_session(extra=extra)) == []


@pytest.mark.parametrize(
    "blank_line",
    [
        "____",
        "What I learned: ____________",
        "Name:____",
        "$____ per night x ____ nights",
        "| ____ | ____ |",
        "Total days ____ - 1 arrival day = ____ real days",
        "____ of 13",
    ],
)
def test_a_blank_that_starts_or_ends_a_token_is_still_a_worksheet(blank_line: str) -> None:
    """A positive-control set. Narrowing the rule must not switch it off."""
    extra = f"{FENCE}text\n{blank_line}\n{FENCE}"
    assert any("worksheet fill-in" in m for m in check(build_session(extra=extra)))


# ---------------------------------------------------------------------------
# A fence ends with the container that holds it
# ---------------------------------------------------------------------------


def test_an_unclosed_blockquote_fence_ends_with_its_blockquote() -> None:
    """CommonMark ends a fenced block at the end of its containing block.

    <https://spec.commonmark.org/0.31.2/#fenced-code-blocks>
    """
    steps = f"## Steps\n\nLike this:\n\n> {FENCE}markdown\n> # Session 01: Example\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert check(text) == []


def test_an_unclosed_list_fence_ends_with_its_list_item() -> None:
    """A fence under a list item does not swallow the rest of the document."""
    steps = f"## Steps\n\n1. Like this:\n\n   {FENCE}markdown\n   # Session 01: Example\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert check(text) == []


def test_an_unclosed_blockquote_fence_ends_at_a_blank_line() -> None:
    """A blank line ends a blockquote, so it ends the fence the blockquote holds."""
    steps = f"## Steps\n\n> {FENCE}markdown\n> # Session 01: Example\n\nBack to prose.\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert check(text) == []


def test_a_blank_line_does_not_end_a_list_nested_fence() -> None:
    """A positive control. Inside a list item a blank line is ordinary fence content."""
    extra = (
        f"## Example\n\n1. Like this:\n\n   {FENCE}markdown\n   first line\n\n"
        f"   <!-- no-source-check: none -->\n   {FENCE}\n"
    )
    text = build_session(sections=SIX_SECTIONS, extra=extra)
    assert any("Source Check" in m for m in check(text))


def test_a_worksheet_fence_that_ends_with_its_blockquote_is_still_rejected() -> None:
    """A positive control. The fence is over, but it still held what it held."""
    steps = f"## Steps\n\n> {FENCE}text\n> My answer: ______________________\n\nBack to prose.\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


# ---------------------------------------------------------------------------
# A run that opened no file has checked nothing
# ---------------------------------------------------------------------------


def test_an_empty_directory_argument_is_refused(tmp_path: Path) -> None:
    """A directory with no session file in it is a run that checked nothing."""
    (tmp_path / "framework" / "sessions" / "phase_09_empty").mkdir(parents=True)
    violations = structure.scan_files(["framework/sessions/phase_09_empty"], root=tmp_path)
    assert any("checked nothing" in v.message for v in violations)
    assert structure.main(["framework/sessions/phase_09_empty"], root=tmp_path) == 1


def test_a_directory_holding_no_markdown_is_refused(tmp_path: Path) -> None:
    """A walk that finds no Markdown has no evidence either."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "notes.txt").write_text("not markdown", encoding="utf-8")
    assert structure.main(["framework/sessions"], root=tmp_path) == 1


def test_a_default_scan_that_matches_nothing_is_refused(tmp_path: Path) -> None:
    """The default glob is the path CI uses, so a glob that stops matching must fail."""
    violations = structure.scan_files([], root=tmp_path)
    assert any("checked nothing" in v.message for v in violations)
    assert structure.main([], root=tmp_path) == 1


def test_the_zero_target_guard_does_not_fire_beside_another_refusal(tmp_path: Path) -> None:
    """A positive control. One refusal is enough; the guard must not double-report."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    violations = structure.scan_files(["framework/sessions/99_typo.md"], root=tmp_path)
    assert len(violations) == 1
    assert "nothing to check" in violations[0].message


def test_the_reported_file_count_comes_from_the_traversal_that_checked(
    tmp_path: Path, capsys: Any
) -> None:
    """A positive control. The count in the summary is the count that was read."""
    session_dir = tmp_path / "framework" / "sessions" / "phase_00_setup"
    session_dir.mkdir(parents=True)
    for number in ("07", "08"):
        (session_dir / f"{number}_a_session.md").write_text(
            build_session(number=number), encoding="utf-8"
        )
    assert structure.main([], root=tmp_path) == 0
    assert "2 file(s) checked, all well-formed" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# A metadata label with no value is not metadata
# ---------------------------------------------------------------------------


def test_a_metadata_field_with_no_value_is_a_violation() -> None:
    """`- Status:` states a label and no fact. A parent learns nothing from it."""
    text = build_session(
        parent_bullets=("- Status:", "- Estimated time:", "- Parent involvement:")
    )
    assert any("Status, Estimated time, Parent involvement" in m for m in check(text))


def test_one_emptied_metadata_field_names_that_field() -> None:
    """The value must be on the field's own line, not borrowed from the next bullet."""
    text = build_session(
        parent_bullets=(
            "- Status:",
            "- Estimated time: 20 minutes",
            "- Parent involvement: none",
        )
    )
    messages = check(text)
    assert any("fields: Status." in m for m in messages), messages


def test_a_bold_metadata_label_with_no_value_is_a_violation() -> None:
    """In `- **Status:**` the only thing after the colon is the label's own emphasis."""
    text = build_session(
        parent_bullets=(
            "- **Status:**",
            "- **Estimated time:**",
            "- **Parent involvement:**",
        )
    )
    assert any("Status, Estimated time, Parent involvement" in m for m in check(text))


def test_a_metadata_value_of_only_an_html_comment_is_a_violation() -> None:
    """A comment prints as nothing, so a field whose value is one has no value."""
    text = build_session(
        parent_bullets=(
            "- Status: <!-- decide later -->",
            "- Estimated time: 20 minutes",
            "- Parent involvement: none",
        )
    )
    assert any("fields: Status." in m for m in check(text))


def test_a_metadata_field_whose_value_holds_a_colon_still_passes() -> None:
    """A positive control. Requiring a value must not confuse the value for the label."""
    text = build_session(
        parent_bullets=(
            "- Status: Core -- Checkpoint 1: a real review",
            "- Estimated time: 20:30 to 21:00",
            "- Parent involvement: none",
        )
    )
    assert check(text) == []


def test_a_metadata_value_wrapped_in_emphasis_still_passes() -> None:
    """A positive control. Excluding the label's asterisks must not exclude the value's."""
    text = build_session(
        parent_bullets=(
            "- Status: ***Core***",
            "- **Estimated time:** *20 minutes*",
            "- Parent involvement: _none_",
        )
    )
    assert check(text) == []


def test_every_metadata_pattern_rejects_its_own_valueless_form() -> None:
    """The A6 meta-test: a presence check that a null instance satisfies is no check.

    This is the only guard this repository has against the next vacuous
    pattern, and it is a tripwire rather than a cure: it covers the patterns
    enrolled in PARENT_STRIP_FIELDS and nothing else.
    """
    for name, pattern in structure.PARENT_STRIP_FIELDS:
        for empty in (f"- {name}:", f"- **{name}:**", f"- **{name}**:", f"- {name}:   "):
            assert pattern.search(empty) is None, (name, empty)
        assert pattern.search(f"- {name}: a real value") is not None, name


# ---------------------------------------------------------------------------
# The walk sees every entry, and says what became of each one
# ---------------------------------------------------------------------------


def test_a_symlinked_phase_directory_is_refused_by_the_default_scan(tmp_path: Path) -> None:
    """A pattern does not descend into a linked directory, so the subtree is unread.

    The zero-target guard cannot catch this: ordinary sessions exist, so the
    run has targets and reports success for a corpus missing a whole subtree.
    """
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    outside = tmp_path / "elsewhere" / "phase_09_linked"
    outside.mkdir(parents=True)
    (outside / "08_broken.md").write_text("no structure at all\n", encoding="utf-8")
    root = tmp_path / "repo"
    link_or_skip(root / "framework" / "sessions" / "phase_09_linked", outside)

    messages = [v.format_message() for v in structure.scan_files([], root=root)]
    assert any("phase_09_linked" in m for m in messages), messages
    assert structure.main([], root=root) == 1


def test_a_symlinked_phase_directory_is_refused_in_a_directory_argument(
    tmp_path: Path,
) -> None:
    """A directory argument walks the same tree, so it needs the same answer."""
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    outside = tmp_path / "elsewhere" / "phase_09_linked"
    outside.mkdir(parents=True)
    (outside / "08_broken.md").write_text("no structure at all\n", encoding="utf-8")
    root = tmp_path / "repo"
    link_or_skip(root / "framework" / "sessions" / "phase_09_linked", outside)

    assert structure.main(["framework/sessions"], root=root) == 1


def test_a_nested_phase_directory_is_still_walked(tmp_path: Path) -> None:
    """A positive control. Refusing links must not stop the walk descending."""
    deep = tmp_path / "repo" / "framework" / "sessions" / "phase_00_setup" / "extra"
    deep.mkdir(parents=True)
    (deep / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    root = tmp_path / "repo"
    assert [p.name for p in structure.resolve_paths([], root)] == ["07_a_session.md"]
    assert structure.main([], root=root) == 0


def test_an_uppercase_markdown_extension_is_checked(tmp_path: Path) -> None:
    """`02_bad.MD` is a session file. A lowercase pattern misses it on CI.

    This fails at 7e4463f only on a case-sensitive filesystem -- which is the
    Linux runner CI uses, and is the reason the bug is invisible on Windows.
    """
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (session_dir / "02_bad.MD").write_text("no structure at all\n", encoding="utf-8")
    root = tmp_path / "repo"

    assert sorted(p.name for p in structure.resolve_paths([], root)) == [
        "02_bad.MD",
        "07_a_session.md",
    ]
    assert structure.main([], root=root) == 1


def test_an_uppercase_extension_is_checked_where_patterns_are_case_sensitive(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """The same fact, forced to hold on every platform.

    Pattern matching is made case-sensitive here so the test reproduces the CI
    runner's filesystem on the developer's. The fixed walk never consults a
    pattern, so the substitution has nothing to act on -- which is the point.
    """
    real_glob, real_rglob = pathlib.Path.glob, pathlib.Path.rglob
    monkeypatch.setattr(
        pathlib.Path,
        "glob",
        lambda self, pat, **kw: real_glob(self, pat, **{"case_sensitive": True, **kw}),
    )
    monkeypatch.setattr(
        pathlib.Path,
        "rglob",
        lambda self, pat, **kw: real_rglob(self, pat, **{"case_sensitive": True, **kw}),
    )
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (session_dir / "02_bad.MD").write_text("no structure at all\n", encoding="utf-8")
    root = tmp_path / "repo"

    assert structure.main([], root=root) == 1


def test_an_unreadable_directory_is_refused_not_treated_as_empty(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """A directory that cannot be listed is not an empty directory.

    `Path.glob` swallows the OSError and yields nothing, so an unreadable
    subtree reads as an absent one and the run reports what it did not see.
    """
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    locked = tmp_path / "repo" / "framework" / "sessions" / "phase_01_locked"
    locked.mkdir()
    (locked / "08_broken.md").write_text("no structure at all\n", encoding="utf-8")
    root = tmp_path / "repo"

    real_iterdir, real_scandir = pathlib.Path.iterdir, os.scandir

    def guarded_iterdir(self: Path):
        if self.name == "phase_01_locked":
            raise PermissionError(13, "Permission denied", str(self))
        return real_iterdir(self)

    def guarded_scandir(path=None, *args, **kwargs):
        if path is not None and "phase_01_locked" in str(path):
            raise PermissionError(13, "Permission denied", str(path))
        return real_scandir(path, *args, **kwargs)

    monkeypatch.setattr(pathlib.Path, "iterdir", guarded_iterdir)
    monkeypatch.setattr(os, "scandir", guarded_scandir)

    assert structure.main([], root=root) == 1


def test_a_non_markdown_file_is_recorded_as_skipped(tmp_path: Path) -> None:
    """A skip is a decision the walk writes down, not an entry that vanishes."""
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (session_dir / "notes.txt").write_text("not markdown", encoding="utf-8")
    root = tmp_path / "repo"

    targets = structure.collect_targets([], root)
    assert [s.display_path for s in targets.skipped] == [
        "framework/sessions/phase_00_setup/notes.txt"
    ]
    assert structure.main([], root=root) == 0


def test_the_walk_accounts_for_every_entry_it_sees(tmp_path: Path) -> None:
    """The reconciliation itself: checked + refused + descended + skipped == seen."""
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (session_dir / "08_b.MD").write_text(build_session(number="08"), encoding="utf-8")
    (session_dir / "notes.txt").write_text("not markdown", encoding="utf-8")
    root = tmp_path / "repo"

    tally = structure.WalkTally()
    structure.walk_session_directory(
        root / structure.DEFAULT_SCAN_ROOT, root.resolve(), [], [], [], tally
    )
    assert tally.balances(), tally
    assert (tally.seen, tally.checked, tally.descended, tally.skipped) == (4, 2, 1, 1)


def test_an_unbalanced_walk_fails_the_run(tmp_path: Path) -> None:
    """A negative control for the reconciliation: it must actually fail a run.

    A guard that has never been seen to fire is a guard nobody knows works.
    """
    session_dir = make_session_dir(tmp_path)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    root = tmp_path / "repo"

    real_walk = structure.walk_session_directory

    def losing_walk(directory, walk_root, paths, refusals, skipped, tally):
        real_walk(directory, walk_root, paths, refusals, skipped, tally)
        tally.seen += 1  # an entry seen and given no disposition

    structure.walk_session_directory = losing_walk
    try:
        violations = structure.scan_files([], root=root)
    finally:
        structure.walk_session_directory = real_walk

    assert any("gone missing" in v.message for v in violations), violations


# ---------------------------------------------------------------------------
# A marker is a marker only where CommonMark reads it as a comment
# ---------------------------------------------------------------------------


def _session_with(body: str) -> str:
    return build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("code span", "Use `<!-- no-source-check: explain why -->` when needed."),
        ("code span, audience", "Write `<!-- audience: adult -->` at the top."),
        ("double-backtick span", "Use ``<!-- no-source-check: reason -->`` here."),
        ("backslash escape", "\\<!-- no-source-check: this renders literally -->"),
        ("html attribute", '<span title="<!-- no-source-check: x -->">hi</span>'),
        ("indented code block", "    <!-- no-source-check: an indented example -->"),
        ("link text", "[see `<!-- no-source-check: x -->`](https://example.com)"),
        ("image alt text", "![a note <!-- no-source-check: x -->](picture.png)"),
    ],
)
def test_a_marker_that_is_not_a_comment_does_not_exempt(label: str, body: str) -> None:
    """Prose *about* the marker prints as characters, so it exempts nothing.

    None of these is an HTML comment. Six render the marker visibly -- the two
    code spans, the backslash escape, the indented code block, the code span
    inside link text, and the image whose alt text is escaped into an
    attribute. The remaining one, ``<span title="...">``, puts the characters
    inside a tag's attribute value, where CommonMark reads them as part of the
    attribute rather than as a comment; measured against markdown-it 14.3.0,
    that is invisible but it is still not a comment. Either way the session
    has said nothing about why it has no research step.
    """
    messages = check(_session_with(body))
    assert any("Source Check" in m for m in messages), (label, messages)


def test_a_real_marker_beside_other_comments_on_one_line_still_exempts() -> None:
    """A positive control. The line starts an HTML block, so the marker is real."""
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<!-- markdownlint-disable MD033 --> <!-- audience: adult -->",
    )
    assert check(text) == []
# --- a file that cannot be read is not a file that is well-formed ----------


def test_a_non_utf8_session_is_a_violation_not_a_crash(tmp_path: Path) -> None:
    """UnicodeDecodeError is a ValueError, so an OSError-only guard misses it.

    Before the fix this script had no guard at all: one Latin-1 byte in one
    session ended the run in a traceback. In CI a traceback reads as the gate
    being broken rather than as one bad file, which is the reading that gets a
    gate switched off.
    """
    session_dir = tmp_path / "framework" / "sessions" / "phase_00_setup"
    session_dir.mkdir(parents=True)
    good = session_dir / "01_good.md"
    good.write_text("# Session 01: Good\n", encoding="utf-8")
    bad = session_dir / "02_bad.md"
    bad.write_bytes(
        b"# Session 02: Bad\n\ncaf\xe9 is not UTF-8\n"
    )

    targets = structure.ScanTargets((good, bad), ())
    violations = structure.check_targets(targets, tmp_path)
    messages = [v.format_message() for v in violations]
    unreadable = [m for m in messages if "could not be read" in m]
    assert len(unreadable) == 1, messages
    assert "02_bad.md" in unreadable[0]
    assert "UnicodeDecodeError" in unreadable[0]
    # The positive control: the readable sibling was still checked, so the
    # refusal did not abort the whole scan.
    assert any("01_good.md" in m for m in messages)


# ---------------------------------------------------------------------------
# Round 6: the scan roots themselves, and three CommonMark defects
# ---------------------------------------------------------------------------


def test_a_symlinked_default_scan_root_is_refused(tmp_path: Path) -> None:
    """The scan root is a path too, and it was the one path never guarded.

    A link here is the whole corpus redirected. The run reads whatever the
    link points at and reports success for the directory it was asked for,
    which is the gate's own promise -- "a linked directory is a subtree this
    run would otherwise never open" -- falsified at the root.
    """
    root = tmp_path / "repo"
    real = root / "framework" / "curated"
    real.mkdir(parents=True)
    (real / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (root / "framework" / "sessions").parent.mkdir(parents=True, exist_ok=True)
    link_or_skip(root / "framework" / "sessions", real)

    messages = [v.format_message() for v in structure.scan_files([], root=root)]
    assert any("symbolic link" in m for m in messages), messages
    assert structure.resolve_paths([], root) == []
    assert structure.main([], root=root) == 1


def test_a_linked_scan_root_is_not_enumerated_before_its_children_are_refused(
    tmp_path: Path,
) -> None:
    """Refusing the children is not enough: listing the directory already left the tree.

    A link pointing outside the repository made the run call ``iterdir()`` on
    an out-of-bounds directory and only then refuse what it found there. The
    refusal must come first, so nothing outside the root is ever listed.
    """
    root = tmp_path / "repo"
    (root / "framework").mkdir(parents=True)
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    (outside / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    link_or_skip(root / "framework" / "sessions", outside)

    walked: list[Path] = []
    real_walk = structure.walk_session_directory

    def recording_walk(directory, walk_root, paths, refusals, skipped, tally):
        walked.append(Path(directory))
        real_walk(directory, walk_root, paths, refusals, skipped, tally)

    structure.walk_session_directory = recording_walk
    try:
        assert structure.main([], root=root) == 1
    finally:
        structure.walk_session_directory = real_walk

    assert walked == [], f"an out-of-bounds directory was enumerated: {walked}"


def test_an_empty_directory_argument_is_refused_beside_a_real_file(tmp_path: Path) -> None:
    """A mistyped directory must not vanish because another argument had a target.

    The run-wide zero-target guard fires only when the whole run opened
    nothing, so one real file silences it and the directory beside it is
    dropped without a word.
    """
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (tmp_path / "framework" / "sessions_v2").mkdir()

    violations = structure.scan_files(
        ["framework/sessions_v2", "framework/sessions/07_a_session.md"], root=tmp_path
    )
    assert any("sessions_v2" in v.display_path for v in violations), violations
    assert (
        structure.main(
            ["framework/sessions_v2", "framework/sessions/07_a_session.md"], root=tmp_path
        )
        == 1
    )


def test_a_directory_argument_of_non_markdown_is_refused_beside_a_real_file(
    tmp_path: Path,
) -> None:
    """A directory whose entries were all skipped still contributed no target.

    The entries are accounted for -- the walk says "skipped, not Markdown" --
    but the *argument* produced nothing, and the reader was told the run was
    clean.
    """
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    notes = tmp_path / "framework" / "notes"
    notes.mkdir()
    (notes / "readme.txt").write_text("not markdown", encoding="utf-8")

    assert (
        structure.main(
            ["framework/notes", "framework/sessions/07_a_session.md"], root=tmp_path
        )
        == 1
    )


def test_the_run_accounts_for_every_scan_root_it_was_given(tmp_path: Path) -> None:
    """The reconciliation one level up: walked + checked + refused == requested."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    (tmp_path / "framework" / "sessions_v2").mkdir()

    roots = structure.RootTally()
    assert roots.balances()
    roots.requested = 3
    roots.walked, roots.checked, roots.refused = 1, 1, 1
    assert roots.balances()
    roots.requested = 4
    assert not roots.balances()


def test_an_unaccounted_scan_root_fails_the_run(tmp_path: Path) -> None:
    """A negative control for the root reconciliation: it must actually fail a run."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")

    real_collect = structure.collect_directory_root

    def losing_collect(requested, directory, walk_root, paths, refusals, skipped, tally, roots):
        real_collect(requested, directory, walk_root, paths, refusals, skipped, tally, roots)
        roots.requested += 1  # a root requested and given no disposition

    structure.collect_directory_root = losing_collect
    try:
        violations = structure.scan_files([], root=tmp_path)
    finally:
        structure.collect_directory_root = real_collect

    assert any("gone missing" in v.message for v in violations), violations


def test_a_directory_argument_that_yields_a_refusal_is_not_double_reported(
    tmp_path: Path,
) -> None:
    """A positive control. A root that produced a refusal has accounted for itself."""
    session_dir = tmp_path / "repo" / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    outside = tmp_path / "outside.md"
    outside.write_text("# Session 08: Elsewhere\n", encoding="utf-8")
    link_or_skip(session_dir / "08_link.md", outside)
    root = tmp_path / "repo"

    violations = structure.scan_files(["framework/sessions"], root=root)
    assert len(violations) == 1, [v.format_message() for v in violations]
    assert "symbolic link" in violations[0].message


def test_a_directory_argument_holding_sessions_is_still_accepted(tmp_path: Path) -> None:
    """A positive control. Per-root accounting must not refuse a productive root."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "07_a_session.md").write_text(build_session(), encoding="utf-8")
    assert structure.main(["framework/sessions"], root=tmp_path) == 0


def test_a_worksheet_fence_under_two_list_markers_on_one_line_is_rejected() -> None:
    """``- - `` opens two list items on one physical line, and the fence is inside both."""
    steps = (
        "## Steps\n\n- - ```text\n    My answer: ______________________\n    ```\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_worksheet_fence_under_a_bullet_and_a_blockquote_on_one_line_is_rejected() -> None:
    """``- > `` alternates the two container kinds on one line; both must be peeled."""
    steps = (
        "## Steps\n\n- > ```text\n  > My answer: ______________________\n  > ```\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_worksheet_fence_under_three_markers_on_one_line_is_rejected() -> None:
    """The peel is a loop, not two special cases: ``> - - `` must work too."""
    steps = (
        "## Steps\n\n> - - ```text\n>     My answer: ______________________\n>     ```\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_compact_nested_fence_without_underscores_is_allowed() -> None:
    """A positive control. Peeling more markers must not invent a worksheet."""
    steps = "## Steps\n\n- - ```text\n    plain content\n    ```\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert check(text) == []


def test_an_html_block_line_with_trailing_backticks_opens_no_fence() -> None:
    """An HTML block runs to its ``-->``; the characters after it are raw HTML.

    Treating the comment-stripped remainder as a fence blanks every heading
    from there to EOF, so a valid session is reported as missing all of them.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n<!-- note --> ```\n\nReal content for Goal.\n",
        1,
    )
    assert check(text) == []


def test_the_closing_line_of_a_multiline_comment_opens_no_fence() -> None:
    """The line carrying ``-->`` is the block's last line, so it is raw HTML too."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n<!-- note\nstill the comment --> ```\n\nReal content for Goal.\n",
        1,
    )
    assert check(text) == []


def test_the_real_fence_after_an_html_block_line_is_the_one_reported() -> None:
    """The block that opens is the real fence, not the HTML-block line before it.

    Both lines carry backticks, so both builds report *a* worksheet. Only the
    reported line number says which line the parser thought the block began on.
    """
    steps = (
        "## Steps\n\n<!-- note --> ```\n\n"
        "```text\nMy answer: ______________________\n```\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    violations = [
        v
        for v in structure.check_text(text, "07_a_session.md", "07_a_session.md")
        if "worksheet fill-in" in v.message
    ]
    assert len(violations) == 1, violations
    opened_on = text.split("\n")[violations[0].line_number - 1]
    assert opened_on.startswith("```text"), f"the block was opened on {opened_on!r}"


def test_a_fence_on_the_line_after_a_comment_still_opens() -> None:
    """A positive control. Only the HTML-block line itself is exempt."""
    steps = (
        "## Steps\n\n<!-- note -->\n\n```text\nMy answer: ______________________\n```\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_backtick_in_a_backtick_info_string_opens_no_fence() -> None:
    """CommonMark forbids it, so the line is an ordinary paragraph.

    Accepting it leaves the scan fenced to EOF and every real heading after it
    disappears, failing a session that is well formed.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n```js `x`\n\nReal content for Goal.\n",
        1,
    )
    assert check(text) == []


def test_a_backtick_in_a_long_backtick_info_string_opens_no_fence() -> None:
    """The rule is about the marker character, not the marker length."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n````js `x`\n\nReal content for Goal.\n",
        1,
    )
    assert check(text) == []


def test_a_backtick_in_a_tilde_info_string_still_opens_a_fence() -> None:
    """A positive control. A tilde fence carries no such restriction."""
    steps = (
        "## Steps\n\n~~~text `x`\nMy answer: ______________________\n~~~\n"
    )
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_an_ordinary_backtick_info_string_still_opens_a_fence() -> None:
    """A positive control. Only a backtick in the info string disqualifies the line."""
    steps = "## Steps\n\n```text\nMy answer: ______________________\n```\n"
    text = build_session().replace("## Steps\n\nReal content for Steps.\n", steps, 1)
    assert any("worksheet fill-in" in m for m in check(text))


# ---------------------------------------------------------------------------
# Round 7: a container prefix does not stop a comment from being a comment
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "marker"),
    [
        ("blockquote", "> <!-- no-source-check: adult-only setup -->"),
        ("blockquote, audience", "> <!-- audience: adult -->"),
        ("bullet", "- <!-- no-source-check: adult-only setup -->"),
        ("ordered item", "1. <!-- no-source-check: adult-only setup -->"),
        ("nested blockquote", "> > <!-- no-source-check: adult-only setup -->"),
        ("bullet in a blockquote", "> - <!-- no-source-check: adult-only setup -->"),
        ("indented bullet", "  - <!-- no-source-check: adult-only setup -->"),
    ],
)
def test_a_marker_inside_a_markdown_container_still_exempts(label: str, marker: str) -> None:
    """CommonMark decides the block after the container prefix comes off.

    A blockquote or a list item does not turn a comment into prose. The child
    sees nothing on the line either way, and the session has said in the file
    why it has no research step -- which is the whole point of the marker.
    """
    text = build_session(sections=SIX_SECTIONS, markers=marker)
    messages = check(text)
    assert messages == [], (label, messages)


def test_a_marker_indented_four_spaces_is_still_an_example() -> None:
    """A negative control. Four spaces is an indented code block, not a comment."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\n    <!-- no-source-check: an indented example -->\n",
    )
    assert any("Source Check" in m for m in check(text))


def test_a_container_nested_marker_inside_a_fence_is_still_an_example() -> None:
    """A negative control. Round 4 holds: a fenced marker exempts nothing."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\n```\n> <!-- no-source-check: printed, not declared -->\n```\n",
    )
    assert any("Source Check" in m for m in check(text))


def test_a_blockquoted_comment_with_trailing_backticks_opens_no_fence() -> None:
    """The same line, read as a fence, invented a worksheet that is not there.

    The blockquote prefix hid the HTML block from the round-6 test, so the
    backticks after the comment opened a fence, and the quoted underscores
    inside it were reported as a worksheet fill-in. CommonMark opens no fence
    there: the whole line is one HTML block.
    """
    goal = "## Goal\n\n> <!-- a note --> ```\n> Name: ____\n"
    text = build_session().replace("## Goal\n\nReal content for Goal.\n", goal, 1)
    assert check(text) == []


def test_a_real_fence_inside_a_blockquote_still_holds_what_it_holds() -> None:
    """A positive control. Only the HTML-block line is exempt from opening one."""
    goal = "## Goal\n\n> ```\n> Name: ____\n> ```\n"
    text = build_session().replace("## Goal\n\nReal content for Goal.\n", goal, 1)
    assert any("worksheet fill-in" in m for m in check(text))


def test_a_fence_after_a_blockquoted_comment_line_still_opens() -> None:
    """A positive control. The HTML block ends on the line carrying ``-->``."""
    goal = "## Goal\n\n> <!-- a note -->\n> ```\n> Name: ____\n> ```\n"
    text = build_session().replace("## Goal\n\nReal content for Goal.\n", goal, 1)
    assert any("worksheet fill-in" in m for m in check(text))


# ---------------------------------------------------------------------------
# Round 7: a link reference definition prints nothing
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("bare destination", "[shared]: https://example.com"),
        ("angle-bracket destination", "[shared]: <https://example.com>"),
        ("double-quoted title", '[shared]: https://example.com "Why it matters"'),
        ("single-quoted title", "[shared]: https://example.com 'Why it matters'"),
        ("parenthesised title", "[shared]: https://example.com (Why it matters)"),
        ("three spaces of indent", "   [shared]: https://example.com"),
        ("two definitions", "[a]: https://example.com/a\n[b]: https://example.com/b"),
        ("label with a space", "[shared source]: https://example.com"),
    ],
)
def test_a_section_holding_only_reference_definitions_is_empty(label: str, body: str) -> None:
    """A definition is a line in the file and nothing on the page.

    The child opening the session sees a heading with no words under it,
    whether or not a link in some later section resolves through it.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert any('section "## Goal" is empty' in m for m in check(text))


def test_a_definition_used_by_a_later_section_does_not_fill_its_own_section() -> None:
    """Being useful elsewhere does not put words under this heading."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n[shared]: https://example.com\n",
        1,
    ).replace(
        "Real content for Steps.",
        "Read the [shared] page first.",
        1,
    )
    assert any('section "## Goal" is empty' in m for m in check(text))


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a definition beside a sentence", "[shared]: https://example.com\n\nReal words."),
        ("an inline link", "[shared](https://example.com) is the page to read."),
        ("bracket-colon prose", "[shared]: not a url but still a definition?"),
        ("an unterminated title", '[shared]: https://example.com "Why it matters'),
        ("trailing words after a title", '[shared]: https://example.com "Title" and more'),
        ("four spaces, so a code block", "    [shared]: https://example.com"),
        ("a comment first, so an HTML block", "<!-- a note -->[shared]: https://example.com"),
        ("a comment last, so a paragraph", "[shared]: https://example.com <!-- a note -->"),
        ("an empty label", "[]: https://example.com"),
        ("no destination", "[shared]:"),
        ("a quoted definition", "> [shared]: https://example.com"),
    ],
)
def test_a_line_that_is_not_a_reference_definition_is_still_content(
    label: str, body: str
) -> None:
    """Negative controls. Each of these puts characters on the page.

    The last two are the conservative direction on purpose: a blockquote round
    a definition renders an empty quote box, and this checker has never peeled
    containers when asking whether a section is empty. Calling them content
    cannot fail a session that is fine.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    messages = check(text)
    assert not any('section "## Goal" is empty' in m for m in messages), (label, messages)


def test_the_emptiness_rule_still_reads_comments_and_bare_markers_as_empty() -> None:
    """A negative control for round 4: the comment rule is untouched."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "## Goal\n\n<!-- markdownlint-disable -->\n\n-\n",
        1,
    )
    assert any('section "## Goal" is empty' in m for m in check(text))


# ---------------------------------------------------------------------------
# Round 8: a comment is a comment where it sits, not only on a line of its own
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("after prose", "No research is needed. <!-- no-source-check: offline exercise -->"),
        ("before prose", "<!-- no-source-check: offline exercise --> No research is needed."),
        ("mid sentence", "No research. <!-- no-source-check: offline exercise --> Really."),
        ("no space before it", "No research is needed.<!-- no-source-check: offline -->"),
        ("beside another comment", "No research. <!-- a note --> <!-- no-source-check: r -->"),
        ("in a list item", "- No research is needed. <!-- no-source-check: offline -->"),
        ("in a blockquote", "> No research is needed. <!-- no-source-check: offline -->"),
        ("after a closed code span", "Use `x` first. <!-- no-source-check: offline -->"),
        ("after a complete html tag", "<span>hi</span> <!-- no-source-check: offline -->"),
        ("after an unmatched backtick", "Use ` here. <!-- no-source-check: offline -->"),
        ("after an image", "![alt](p.png) <!-- no-source-check: offline -->"),
        ("the audience marker", "This is an adult setup step. <!-- audience: adult -->"),
        ("three spaces of indent", "   <!-- no-source-check: offline exercise -->"),
    ],
)
def test_an_inline_marker_still_exempts(label: str, body: str) -> None:
    """An exemption marker is a comment wherever CommonMark reads one.

    ``No research is needed. <!-- no-source-check: offline exercise -->`` is an
    inline raw-HTML comment span; markdown-it 14.3.0 renders it as a comment,
    not as characters. Requiring the marker to occupy a line by itself is a
    placement rule the exemption syntax never stated, and the sibling
    placeholder hook documents the opposite placement for its own suppression
    marker.
    """
    assert check(_session_with(body)) == [], label


def test_an_inline_marker_inside_a_mandatory_section_exempts() -> None:
    """The marker is read from the whole document, section bodies included."""
    text = build_session(sections=SIX_SECTIONS).replace(
        "Real content for Stop Point.",
        "Stop when the page is full. <!-- no-source-check: offline exercise -->",
        1,
    )
    assert check(text) == []


def test_a_marker_split_across_two_lines_still_exempts() -> None:
    """A comment spans lines, so the marker view has to as well."""
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\nNo research. <!-- no-source-check:\nan offline exercise -->\n",
    )
    assert check(text) == []


def test_an_inline_marker_five_spaces_into_a_list_item_is_still_an_example() -> None:
    """A negative control on the peel, not the scan.

    Five spaces after the bullet put the content at relative indent four, which
    is an indented code block inside the list item. The marker prints there.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\n-     <!-- no-source-check: an indented example -->\n",
    )
    assert any("Source Check" in m for m in check(text))


# ---------------------------------------------------------------------------
# Round 8: a heading inside any raw HTML block is not a heading
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("a div", "<div>"),
        ("a table", "<table>"),
        ("a section", "<section>"),
        ("a list element", "<ul>"),
        ("a closing tag", "</div>"),
        ("a div with attributes", '<div class="note">'),
    ],
)
def test_a_heading_inside_a_raw_html_block_is_not_a_section(label: str, opener: str) -> None:
    """CommonMark opens an HTML block on a block-level element name.

    Every line of that block is raw HTML until the blank line that ends it, so
    the ``## Goal`` below the opener is not a heading and the session has no
    Goal. Measured against markdown-it 14.3.0: ``<div>`` followed by
    ``## Goal`` parses as ``html_block``, with no ``heading_open`` in it.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """
    text = build_session().replace("## Goal\n", f"{opener}\n## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text)), label


def test_a_heading_inside_a_script_block_is_not_a_section() -> None:
    """Start condition 1 runs to the line carrying the matching closing tag."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "<script>\n## Goal\n</script>\n\nReal content for Goal.\n",
        1,
    )
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_heading_inside_a_processing_instruction_is_not_a_section() -> None:
    """Start condition 3 runs to ``?>``."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "<?php\n## Goal\n?>\n\nReal content for Goal.\n",
        1,
    )
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_heading_inside_a_cdata_section_is_not_a_section() -> None:
    """Start condition 5 runs to ``]]>``."""
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "<![CDATA[\n## Goal\n]]>\n\nReal content for Goal.\n",
        1,
    )
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_blockquoted_html_block_leaves_no_section_behind() -> None:
    """A control on the container peel, and on an older behaviour it meets.

    ``> <div>`` opens an HTML block once the blockquote prefix is peeled, so
    ``> ## Goal`` is raw HTML. It was not a section before this change either:
    the heading scan has never peeled container prefixes, so a blockquoted ATX
    heading has never counted as one. The verdict is the same on both sides.
    What this pins is that the new classifier reaches that same answer instead
    of a different one.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        "> <div>\n> ## Goal\n\nReal content for Goal.\n",
        1,
    )
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_heading_after_a_blank_line_ends_the_html_block() -> None:
    """A positive control. A blank line ends the conditions that have no end tag."""
    text = build_session().replace("## Goal\n", "<div>\n\n## Goal\n", 1)
    assert check(text) == []


def test_a_heading_after_a_closed_script_block_is_a_section() -> None:
    """A positive control. The block ends on the line carrying ``</script>``."""
    text = build_session().replace("## Goal\n", "<script>\nx\n</script>\n## Goal\n", 1)
    assert check(text) == []


def test_a_heading_after_a_document_type_declaration_is_a_section() -> None:
    """A positive control. Condition 4 ends on the line carrying ``>``, which is its own."""
    text = build_session().replace("## Goal\n", "<!DOCTYPE html>\n## Goal\n", 1)
    assert check(text) == []


def test_a_heading_after_a_one_line_comment_is_still_a_section() -> None:
    """A negative control for round 4. A closed comment does not swallow the next line."""
    text = build_session().replace("## Goal\n", "<!-- a note -->\n## Goal\n", 1)
    assert check(text) == []


def test_a_fence_line_inside_a_raw_html_block_opens_no_fence() -> None:
    """Round 6's rule, extended: raw HTML is raw HTML whichever condition opened it.

    The backticks inside the ``<div>`` are characters in an HTML block, not a
    fence. Before this they opened one that nothing closed, and every heading
    below it was swallowed, so a well-formed session lost all seven sections.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n",
        f"<div>\n{FENCE}\n</div>\n\n## Goal\n\nReal content for Goal.\n",
        1,
    )
    assert check(text) == []


# ---------------------------------------------------------------------------
# Round 8: the navigation line belongs in the session header
# ---------------------------------------------------------------------------


def test_a_navigation_line_below_the_first_section_is_a_violation() -> None:
    """Orientation the child reaches after the work is orientation nobody reads."""
    text = build_session(nav=False, extra="You are here: Phase 0. Previous: none | Next: 08\n")
    messages = check(text)
    assert any("navigation line sits below the first section" in m for m in messages), messages


def test_a_misplaced_navigation_line_is_reported_where_it_sits() -> None:
    """The violation points at the line to move, not at line one."""
    text = build_session(nav=False, extra="You are here: Phase 0. Previous: none | Next: 08\n")
    misplaced = [
        v for v in structure.check_text(text, "07_a.md", "07_a.md")
        if "navigation line" in v.message
    ]
    assert len(misplaced) == 1
    assert misplaced[0].line_number == text.split("\n").index(
        "You are here: Phase 0. Previous: none | Next: 08"
    ) + 1


def test_a_missing_navigation_line_still_reads_as_missing() -> None:
    """A negative control. Absent and misplaced are different problems."""
    messages = check(build_session(nav=False))
    assert any("no navigation line" in m for m in messages), messages
    assert not any("sits below" in m for m in messages), messages


def test_a_navigation_line_in_a_document_with_no_sections_is_still_found() -> None:
    """A positive control, and the safe direction.

    With no level-two heading the header is the whole document, so the search
    looks at more text rather than less. The missing sections are reported on
    their own account.
    """
    messages = check(build_session(sections=()))
    assert not any("navigation line" in m for m in messages), messages


def test_a_parent_strip_below_the_first_section_is_allowed() -> None:
    """A negative control, and the reason the strip is not bounded.

    The specification says the parent-facing meta-fields "may be shown in a
    compact strip near the top, as above, or grouped at the bottom". A gate
    that demanded the header would reject a session the curriculum allows.
    """
    text = build_session(
        parents=False,
        extra=(
            "**For parents:**\n\n- Status: Core\n- Estimated time: 20 minutes\n"
            "- Parent involvement: none\n"
        ),
    )
    assert check(text) == []


def test_the_navigation_line_in_the_header_still_passes() -> None:
    """A positive control for the ordinary shape every session already uses."""
    assert check(build_session()) == []


# ---------------------------------------------------------------------------
# Issue 27: the findings PR #23 deferred
# ---------------------------------------------------------------------------

FIVE_SECTIONS = ("Goal", "Start Here", "Steps", "Workspace", "Artifact Created")


def test_a_marker_in_a_block_level_tag_attribute_does_not_exempt() -> None:
    """An attribute value is not a comment, even on a raw HTML block's own line.

    ``<div>`` opens an HTML block, and the whole raw line went into the marker
    view, so the delimiters inside the attribute exempted a session that had
    said nothing about why it has no research step. Measured against
    markdown-it 14.3.0: the text lands in the ``title`` attribute.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra='## Notes\n\n<div title="<!-- no-source-check: x -->">\nhi\n</div>\n',
    )
    assert any("Source Check" in m for m in check(text))


@pytest.mark.parametrize(
    ("label", "marker_line"),
    [
        ("at the margin", "<!-- no-source-check: an offline exercise -->"),
        ("four spaces in", "    <!-- no-source-check: an offline exercise -->"),
    ],
)
def test_a_real_comment_inside_a_raw_html_block_still_exempts(
    label: str, marker_line: str
) -> None:
    """A negative control. A raw HTML block is passed through to the page.

    A comment inside one is still a comment, and four spaces of indent inside
    one is not an indented code block: the block is raw HTML end to end.
    Measured against markdown-it 14.3.0.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Notes\n\n<div>\n{marker_line}\n</div>\n",
    )
    assert check(text) == [], label


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("a blockquoted div", "> <div>\n"),
        ("a blockquoted div over a blank line", "> <div>\n\n"),
        ("a listed div", "- <div>\n\n"),
    ],
)
def test_an_unclosed_html_block_ends_with_its_container(label: str, opener: str) -> None:
    """A leaf block ends with the block that holds it, as an unclosed fence does.

    The HTML-block state had no containment path, so an unclosed ``<div>``
    inside a blockquote stayed open to its own terminator and blanked every
    heading the document outdented to -- all six mandatory sections reported
    missing on a session that is fine. Measured with markdown-it 14.3.0 read by
    ``html.parser``: the block closes with its container, the page paints
    ``<h2>Goal</h2>``, and ``## Goal`` is a heading.

    The three raw-text parameters this test used to carry are now the test
    below, with the opposite verdict and the measurement that changed it.
    """
    text = build_session().replace("## Goal\n", f"{opener}## Goal\n", 1)
    assert check(text) == [], label


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("a blockquoted script", "> <script>\n"),
        ("a blockquoted script over a blank line", "> <script>\n\n"),
        ("a listed script", "- <script>\n\n"),
    ],
)
def test_a_run_outlives_the_container_its_block_died_with(label: str, opener: str) -> None:
    """The block ends with its container; the element does not.

    A raw-text run is not CommonMark's construct -- it is the page's. The
    renderer writes the ``<script>`` into the output and an HTML parser reading
    that output stays in raw text until a closing tag that never comes, so
    everything below is script data: no comment is a comment and no heading is
    painted. Measured with markdown-it 14.3.0 read by ``html.parser``: the
    rendered page carries no ``<h2>`` at all, and this session really has no
    visible Goal.

    A previous round asserted the opposite here, from the Markdown layer alone
    -- markdown-it does emit ``<h2>Goal</h2>`` into a document nothing will
    ever read as markup. Both layers have to agree before a heading is a
    heading, which is the same lesson the front-matter rule learned from
    PyYAML.
    """
    text = build_session().replace("## Goal\n", f"{opener}## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text)), label


def test_a_container_that_ends_a_div_block_still_frees_the_heading() -> None:
    """The control in the other direction, and the reason the clearing exists.

    ``<div>`` is not a raw-text element, so nothing survives the container: the
    page paints the heading below it and a rule that blanked every line under
    any unclosed block would fail a session that is fine.
    """
    text = build_session().replace("## Goal\n", "> <div>\n## Goal\n", 1)
    assert check(text) == []


def test_a_script_line_inside_a_comment_opens_no_block() -> None:
    """No start condition is tried while an HTML block is open.

    A ``<script>`` written inside a multiline comment opened a second state
    that outlived the ``-->``, and every heading below it was hidden until a
    ``</script>`` that does not exist. Measured against markdown-it 14.3.0: the
    comment is one block and ``## Goal`` below it is a heading.
    """
    text = build_session().replace("## Goal\n", "<!-- a note\n<script>\n-->\n\n## Goal\n", 1)
    assert check(text) == []


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("an open tag", "<x-session>"),
        ("an open tag with attributes", '<x-session data-id="1">'),
        ("a self-closing tag", "<x-session />"),
        ("a closing tag", "</x-session>"),
    ],
)
def test_a_heading_inside_a_type_seven_html_block_is_not_a_section(
    label: str, opener: str
) -> None:
    """Start condition 7 is a condition like the other six.

    A complete tag alone on its line, at a block boundary, opens a raw HTML
    block that runs to the next blank line, so the ``## Goal`` under it is not
    a heading and the session has no visible Goal. The scan omitted the
    condition because deciding it needs paragraph state; it keeps that state
    now. Measured against markdown-it 14.3.0.
    """
    text = build_session().replace("## Goal\n", f"{opener}\n## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text)), label


@pytest.mark.parametrize(
    ("label", "lines"),
    [
        ("a tag on the second line of a paragraph", "Some prose first.\n<x-session>\n"),
        ("an incomplete tag", "<x-session\n"),
        ("a tag with text after it", "<b>bold</b>\n"),
    ],
)
def test_a_shape_that_is_not_condition_seven_leaves_the_heading_below_it(
    label: str, lines: str
) -> None:
    """Negative controls. Condition 7 needs a complete tag, alone, at a boundary.

    The first is the one condition a paragraph blocks, which is why the
    paragraph tracker exists at all. Measured against markdown-it 14.3.0.
    """
    text = build_session().replace("## Goal\n", f"{lines}## Goal\n", 1)
    assert check(text) == [], label


def test_a_fence_after_a_paragraph_that_starts_with_a_tag_still_opens() -> None:
    """A negative control, restating the sibling hook's round-eight control.

    A paragraph is open, so the tag opens no block, so the backticks under it
    are a fence and the heading inside it is an example.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\nProse first.\n<x-session>\n```\n## Stop Point\n```\n",
    )
    messages = check(text)
    assert any("Source Check" in m for m in messages)
    assert not any('missing mandatory section "## Stop Point"' in m for m in messages)


def test_a_marker_inside_a_multiline_code_span_does_not_exempt() -> None:
    """A code span closes on a run of its own length anywhere in its paragraph.

    The finding that raised this gave an example that does not reproduce: a
    line beginning ``<!--`` opens HTML block condition 2, which may interrupt a
    paragraph, so the span never forms and the marker there is a real comment.
    This is the shape that does reproduce, and markdown-it 14.3.0 renders the
    whole of it as one ``<code>`` element.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\nUse `a\nb <!-- no-source-check: x --> c\nd` here.\n",
    )
    assert any("Source Check" in m for m in check(text))


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("the run never closes", "Use `a\nb <!-- no-source-check: x --> c\nd here."),
        (
            "the run closes past a blank line",
            "Use `a\nb <!-- no-source-check: x --> c\n\nd` here.",
        ),
        ("the marker opens a block of its own", "Use `\n<!-- no-source-check: x -->\n` here."),
    ],
)
def test_a_code_span_that_does_not_form_leaves_a_real_marker(label: str, body: str) -> None:
    """Negative controls. Each of these is a comment on the page.

    The third is the shape the finding gave. Its middle line opens an HTML
    block of its own, which ends the paragraph, so the backticks around it are
    literal text. All three measured against markdown-it 14.3.0.
    """
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == [], label


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a link title", '[help](page.md "<!-- no-source-check: x -->")'),
        ("a link destination", "[help](<!-- no-source-check: x -->)"),
        ("a single-quoted title", "[help](page.md '<!-- no-source-check: x -->')"),
        ("an angle-bracket destination", '[help](<page.md> "<!-- no-source-check: x -->")'),
        ("a parenthesised title", "[help](page.md (<!-- no-source-check: x -->))"),
        ("an image title", '![alt](p.png "<!-- no-source-check: x -->")'),
        ("image alt text", "![a note <!-- no-source-check: x -->](p.png)"),
        (
            "a defined reference label",
            "[help][<!-- no-source-check: x -->]\n\n[<!-- no-source-check: x -->]: p.md",
        ),
        ("a reference definition", '[a]: p.md "<!-- no-source-check: x -->"'),
    ],
)
def test_a_marker_in_link_metadata_does_not_exempt(label: str, body: str) -> None:
    """Link metadata becomes an attribute of an element, or nothing at all.

    A destination becomes ``href`` or ``src``, a title becomes ``title``, an
    image's alt text becomes ``alt``, a resolved reference label becomes
    nothing, and a reference definition renders nothing end to end. None of
    them is a comment. Every row measured against markdown-it 14.3.0.
    """
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert any("Source Check" in m for m in check(text)), label


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("link text", "[see <!-- no-source-check: x --> here](page.md)"),
        ("an undefined reference label", "![a note <!-- no-source-check: x -->][lbl]"),
        ("brackets that are not a link", '[help] (page.md "<!-- no-source-check: x -->")'),
        (
            "an outer link that cannot nest",
            '[a [b](u.md) c](v.md "<!-- no-source-check: x -->")',
        ),
    ],
)
def test_a_marker_outside_link_metadata_still_exempts(label: str, body: str) -> None:
    """Negative controls. markdown-it 14.3.0 renders a comment in every one.

    A link's text is inline content. An undefined reference is the brackets the
    author typed. A space between ``]`` and ``(`` is not a link. And links may
    not nest, so the inner link of the last row wins and the outer brackets are
    literal -- which is why the region pass keeps a bracket stack rather than
    matching brackets where it finds them.
    """
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == [], label


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a destination on the next line", "[shared]:\n    https://example.com"),
        ("a title on a third line", '[shared]:\n    https://example.com\n    "A title"'),
        ("an angle-bracket destination", "[shared]:\n  <https://example.com>"),
        ("a title under a one-line definition", '[shared]: https://example.com\n  "A title"'),
    ],
)
def test_a_multiline_reference_definition_is_an_empty_section(label: str, body: str) -> None:
    """A definition renders nothing at all, however many lines it took to write.

    The emptiness rule read one line at a time, so it matched neither half of
    ``[shared]:`` with its destination indented underneath, and a session whose
    Goal printed as a bare heading passed. Measured against markdown-it 14.3.0:
    each of these renders an empty section.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert any('section "## Goal" is empty' in m for m in check(text)), label


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a label with no destination", "[shared]:"),
        ("prose under a label line", "[shared]:\nReal visible prose here."),
        (
            "prose under a complete definition",
            "[shared]:\n  https://example.com\n  Real visible prose.",
        ),
    ],
)
def test_a_reference_definition_that_does_not_parse_is_still_content(
    label: str, body: str
) -> None:
    """Negative controls. markdown-it 14.3.0 puts every one of these on the page.

    The last is the greedy rule doing its work: two lines are the definition,
    and the third is an indented code block the child sees.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert not any('section "## Goal" is empty' in m for m in check(text)), label


def test_a_nonbreaking_space_does_not_close_a_fence() -> None:
    """CommonMark permits spaces and tabs after a closing fence and nothing else.

    Python reads a whitespace class as Unicode whitespace, so a fence closed
    with a nonbreaking space ended the block here while the renderer kept every
    line below it inside the code -- and the fake ``## Stop Point`` under it counted
    as structure. Measured against markdown-it 14.3.0: the block runs on.
    """
    text = build_session(
        sections=FIVE_SECTIONS,
        extra="## Notes\n\n```\ncode\n```\u00a0\n\n## Stop Point\n\nNot a real one.\n",
    )
    assert any('missing mandatory section "## Stop Point"' in m for m in check(text))


def test_a_tab_after_a_closing_fence_still_closes_it() -> None:
    """A positive control. A tab is one of the two characters CommonMark allows."""
    text = build_session(
        sections=FIVE_SECTIONS,
        extra="## Notes\n\n```\ncode\n```\t\n\n## Stop Point\n\nA real one.\n",
    )
    assert not any('missing mandatory section "## Stop Point"' in m for m in check(text))


def test_a_navigation_label_with_no_value_is_not_a_navigation_line() -> None:
    """The value belongs on the navigation line, not on whatever line follows.

    A plain whitespace run crossed the line break and took the next line's
    first character as the value, so a session whose location had been deleted
    passed on the strength of the parent strip's own asterisk below it. markdown-it 14.3.0
    renders the label as a paragraph with no location in it.
    """
    text = build_session(nav=False).replace(
        "**For parents:**", "You are here:\n\n**For parents:**", 1
    )
    assert any("no navigation line" in m for m in check(text))


def test_a_navigation_value_after_a_tab_is_still_a_navigation_line() -> None:
    """A positive control. Horizontal whitespace sits between the colon and the value."""
    text = build_session(nav=False).replace(
        "**For parents:**", "You are here:\tPhase 0 (Setup).\n\n**For parents:**", 1
    )
    assert check(text) == []


#: One backtick. Spelled through a name so a test that puts a code span beside
#: an HTML comment never has to embed the character in a literal, where a stray
#: one is easy to miss.
TICK = FENCE[0]

#: The exemption marker, spelled once for the tests that place it on one side
#: or the other of a block boundary.
OFFLINE_MARKER = "<!-- no-source-check: an offline exercise -->"


def test_a_code_span_does_not_reach_across_a_list_item_into_a_marker() -> None:
    """A list item interrupts a paragraph, so the run above it closes nothing.

    The lookahead stopped at a blank line, a heading and a thematic break and
    at nothing else, so an unclosed run paired with the first run inside the
    list item and swallowed the marker between them -- and a session that had
    declared itself was reported as missing its Source Check. Measured against
    markdown-it 14.3.0: the paragraph ends before the list and the marker
    renders as a comment.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=(
            f"## Notes\n\nUse {TICK}open on one line and\n"
            f"- item {OFFLINE_MARKER} {TICK}x{TICK}\n"
        ),
    )
    assert check(text) == []


def test_a_code_span_does_not_reach_across_a_blockquote_into_a_marker() -> None:
    """A blockquote interrupts a paragraph exactly as a list item does.

    Measured against markdown-it 14.3.0: the quoted line is its own block and
    the marker inside it renders as a comment.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=(
            f"## Notes\n\nUse {TICK}open on one line and\n"
            f"> quoted {OFFLINE_MARKER} {TICK}x{TICK}\n"
        ),
    )
    assert check(text) == []


def test_a_code_span_inside_one_paragraph_still_swallows_a_marker() -> None:
    """A negative control. A span really does cross a soft line break.

    Nothing between the two runs opens a block, so the marker is inside the
    span, is printed rather than read, and exempts nothing. Measured against
    markdown-it 14.3.0.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Notes\n\nUse {TICK}open and\nmore {OFFLINE_MARKER} here{TICK} today.\n",
    )
    assert any('missing "## Source Check"' in message for message in check(text))


def test_a_setext_underline_closes_the_paragraph_above_a_raw_html_block() -> None:
    """A Setext underline turns the paragraph above it into a heading.

    The paragraph tracker recognized an ATX heading and a thematic break and
    stopped there, so an open paragraph was still claimed under the underline
    and the complete tag below it was refused HTML block condition 7. The
    heading inside that block then counted as a mandatory section the page
    never shows. Measured against markdown-it 14.3.0: the block opens and
    swallows the heading.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\nHeading\n=====\n<x-session>\n## Source Check\n",
    )
    assert any('missing "## Source Check"' in message for message in check(text))


# ---------------------------------------------------------------------------
# Round 2: which labels a document defines, and where a line ends
# ---------------------------------------------------------------------------


def test_an_incomplete_reference_definition_does_not_define_its_label() -> None:
    """A label with no destination defines nothing, so the reference is text.

    The collector read the label off the front of the line without asking
    whether the definition parsed, so a reference to it was treated as an image
    and the marker in its alt text was thrown away with the rest of the link
    metadata. Measured against markdown-it 14.3.0: the brackets are on the page
    and the marker inside them is a comment.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Notes\n\n[x]:\n![a {OFFLINE_MARKER}][x]\n",
    )
    assert check(text) == []


def test_a_complete_reference_definition_still_defines_its_label() -> None:
    """A negative control. A definition that parses makes the reference an image.

    The alt text is then an attribute rather than a page, so the marker inside
    it declares nothing and the session still owes a Source Check. Measured
    against markdown-it 14.3.0.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Notes\n\n[x]: /y\n\n![a {OFFLINE_MARKER}][x]\n",
    )
    assert any('missing "## Source Check"' in message for message in check(text))


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("an unbalanced closer, next line", "[shared]:\n  https://example.com/x)"),
        ("an unclosed opener, next line", "[shared]:\n  https://example.com/x("),
        ("an unbalanced closer, one line", "[shared]: https://example.com/x)"),
        ("an unclosed opener, one line", "[shared]: https://example.com/x("),
    ],
)
def test_a_reference_destination_must_balance_its_parentheses(label: str, body: str) -> None:
    """A bare destination takes parentheses only in balanced pairs.

    Both destination patterns accepted any run of nonblank characters, so a
    section holding a stray parenthesis was called empty while the renderer put
    every character of it on the page. Measured against markdown-it 14.3.0:
    each of these is a paragraph.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert not any('section "## Goal" is empty' in m for m in check(text)), label


#: One backslash. Spelled through a name so a test that escapes a parenthesis
#: never has to embed the character in a literal, where a stray one is easy to
#: miss. Kept as the readability suite spells it.
BACKSLASH = "\\"


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a balanced pair, next line", "[shared]:\n  https://example.com/x(y)"),
        ("a balanced pair, one line", "[shared]: https://example.com/x(y)"),
        ("a nested balanced pair", "[shared]: https://example.com/a(b(c))"),
        ("an escaped closer", "[shared]: https://example.com/x" + BACKSLASH + ")"),
    ],
)
def test_a_balanced_reference_destination_still_renders_nothing(label: str, body: str) -> None:
    """Negative controls. A parenthesis that balances, or is escaped, is allowed.

    Measured against markdown-it 14.3.0: each of these renders an empty
    section, so narrowing the destination must not have cost them.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert any('section "## Goal" is empty' in m for m in check(text)), label


def test_a_document_with_crlf_line_endings_keeps_its_sections() -> None:
    """A carriage return is a line ending, not a character on the line.

    The closing fence carried a stray ``\\r``, so it did not close, and every
    mandatory heading below it disappeared into the code block that never
    ended. Measured against markdown-it 14.3.0, which reads the three CommonMark
    line endings alike.
    """
    text = (
        build_session(empty_sections=("Workspace",))
        .replace("## Workspace\n", f"## Workspace\n\n{FENCE}text\nnotes here\n{FENCE}\n", 1)
        .replace("\n", "\r\n")
    )
    assert check(text) == []
# --- round 3: declarations, code spans before links, and label length -------


def test_a_lowercase_declaration_does_not_open_an_html_block() -> None:
    """``<!foo>`` is a declaration to micromark and prose to markdown-it.

    Condition 4 accepted any ASCII letter, so a lowercase declaration inside a
    paragraph closed it, the complete tag on the next line opened a type-seven
    block, and every mandatory heading down to the blank line disappeared into
    it. Measured against markdown-it 14.3.0, which is what this repository
    reads a rendered page by: both lines stay in the paragraph and the heading
    below them is a heading.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra="## Notes\n\nPack a snack for the walk.\n<!foo>\n<x>\n## Source Check\n\nWe read it.\n",
    )
    assert check(text) == []


def test_an_uppercase_declaration_still_opens_an_html_block() -> None:
    """A negative control. Condition 4 is a real condition; it just wants a capital.

    Measured against markdown-it 14.3.0: the declaration closes the paragraph,
    the tag below it opens a block, and the heading inside that block is raw
    HTML rather than a heading.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=(
            "## Notes\n\nPack a snack for the walk.\n<!DOCTYPE html>\n<x>\n"
            "## Source Check\n\nWe read it.\n"
        ),
    )
    assert any('missing "## Source Check"' in message for message in check(text))


def test_a_code_span_shaped_like_an_image_does_not_hide_a_marker() -> None:
    """The link metadata was computed over the raw line, before the code spans.

    ``` `![alt](url` "<!-- no-source-check: x -->") ``` looked like an image
    running to the final ``)``, so the marker inside it was thrown away and a
    session that had declared its exemption was failed for not declaring one.
    Measured against markdown-it 14.3.0: the code span wins, and what follows
    it is a comment on the page.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f'## Notes\n\n{TICK}![alt](url{TICK} "{OFFLINE_MARKER}")\n',
    )
    assert check(text) == []


def test_a_real_image_title_still_hides_a_marker() -> None:
    """A negative control. An image's title is an attribute, not a comment.

    Measured against markdown-it 14.3.0: the marker becomes the ``title`` of an
    ``<img>`` and the page carries no comment at all.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f'## Notes\n\n![alt](url "{OFFLINE_MARKER}")\n',
    )
    assert any('missing "## Source Check"' in message for message in check(text))


def test_a_code_span_opening_inside_alt_text_hides_the_marker_after_it() -> None:
    """The same defect the other way round, and the dangerous way round.

    A raw-line pass read ``![a`b](u) <!-- ... --> c` `` as an image ending at
    ``)``, so the marker after it looked like ordinary text and exempted the
    session. Measured against markdown-it 14.3.0: the code span opens inside
    the alt text, swallows the ``]``, and the marker is printed rather than
    read. The exemption was one the page never carried.
    """
    text = build_session(
        sections=SIX_SECTIONS,
        extra=f"## Notes\n\n![a{TICK}b](u) {OFFLINE_MARKER} c{TICK}\n",
    )
    assert any('missing "## Source Check"' in message for message in check(text))


#: A label one character past what CommonMark allows between the brackets, and
#: the longest one it does allow. Spelled here so the two tests below cannot
#: drift apart by a character.
LABEL_TOO_LONG = "a" * 1000
LABEL_LONGEST_ALLOWED = "a" * 999


@pytest.mark.parametrize(
    ("label", "body"),
    [
        ("a label line over an indented destination", f"[{LABEL_TOO_LONG}]:\n    /destination"),
        ("a one-line definition", f"[{LABEL_TOO_LONG}]: /destination"),
    ],
)
def test_a_label_of_a_thousand_characters_is_not_a_definition(label: str, body: str) -> None:
    """CommonMark caps a link label at 999 characters between the brackets.

    Both definition patterns took a label of any length, so a section holding a
    1,000-character label was consumed as a definition and reported empty.
    Measured against micromark 4.0.2, which implements the cap: the brackets
    and the destination are a paragraph the child reads. markdown-it 14.3.0
    does not implement the cap, which is why this one rule is measured
    elsewhere.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert not any('section "## Goal" is empty' in m for m in check(text)), label


@pytest.mark.parametrize(
    ("label", "body"),
    [
        (
            "a label line over an indented destination",
            f"[{LABEL_LONGEST_ALLOWED}]:\n    /destination",
        ),
        ("a one-line definition", f"[{LABEL_LONGEST_ALLOWED}]: /destination"),
    ],
)
def test_a_label_of_nine_hundred_ninety_nine_characters_still_renders_nothing(
    label: str, body: str
) -> None:
    """A negative control, and the one that keeps the cap off by no characters.

    Measured against micromark 4.0.2: at 999 the definition parses and the
    section prints to the child as a bare heading.
    """
    text = build_session().replace(
        "## Goal\n\nReal content for Goal.\n", f"## Goal\n\n{body}\n", 1
    )
    assert any('section "## Goal" is empty' in m for m in check(text)), label


# ---------------------------------------------------------------------------
# A backtick inside a parsed link target is not a delimiter
# ---------------------------------------------------------------------------


#: One ASCII control character, and the delete character beside it. Spelled
#: through ``chr`` so no test has to embed a byte an editor can eat.
CONTROL_CHARACTER = chr(1)
DELETE_CHARACTER = chr(127)


@pytest.mark.parametrize(
    ("label", "first_line"),
    [
        ("a link title", f'[x](u "t {TICK}")'),
        ("a link destination", f"[x](u{TICK}v)"),
        ("an image title", f'![x](p.png "t {TICK}")'),
        ("a single-quoted title", f"[x](u 't {TICK}')"),
        ("a parenthesised title", f"[x](u (t {TICK}))"),
        ("an angle-bracket destination", f'[x](<u> "t {TICK}")'),
    ],
)
def test_a_backtick_in_a_link_target_opens_no_code_span(label: str, first_line: str) -> None:
    """A destination and a title are scanned as characters, not as inline content.

    The bracket comes first, so the target is consumed whole and the backtick
    in it is metadata. The pass that finds the code spans had no link model at
    all, so it paired that backtick with the one on the next line and masked
    the marker between them -- and a session that had declared its exemption
    was failed for not declaring one. Every row measured against markdown-it
    14.3.0.
    """
    body = f"{first_line}\nText <!-- no-source-check: an offline exercise --> tail{TICK}"
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == [], label


def test_a_code_span_that_opens_before_a_link_still_swallows_it() -> None:
    """A negative control. Whichever construct starts first takes the rest.

    The backtick opens before the ``[``, so the bracket and the ``]`` after it
    are both inside the code span and neither is ever counted. There is no link
    to have a target, the span closes on the backtick inside those
    parentheses, and the marker after it is a comment on the page. Measured
    against markdown-it 14.3.0.
    """
    body = f"{TICK}[a](u{TICK} x) <!-- no-source-check: an offline exercise --> y{TICK}"
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == []


def test_an_outer_link_that_cannot_nest_keeps_its_marker() -> None:
    """A negative control, and the reason the bracket walk runs in one pass only.

    Links may not nest, so the inner link wins and the outer brackets are
    literal text: the marker in those parentheses is a comment the page
    carries. ``link_metadata_regions`` models that, and the pass that reads its
    answer must not be second-guessed by a walk that counts brackets and
    nothing else. Measured against markdown-it 14.3.0.
    """
    body = "[a [b](u.md) c](v.md \"<!-- no-source-check: an offline exercise -->\")"
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == []


def test_a_bracket_with_no_opener_skips_nothing() -> None:
    """A negative control. A ``]`` that closes nothing is an ordinary character."""
    body = f"a](u{TICK} x) <!-- no-source-check: an offline exercise --> y{TICK}"
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert any("Source Check" in m for m in check(text))


# ---------------------------------------------------------------------------
# What a bare link destination may hold
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "body"),
    [
        (
            "an inline link",
            f'[x](fo{CONTROL_CHARACTER}o "<!-- no-source-check: an offline exercise -->")',
        ),
        (
            "an inline link, delete character",
            f'[x](fo{DELETE_CHARACTER}o "<!-- no-source-check: an offline exercise -->")',
        ),
        (
            "an image",
            f'![x](fo{CONTROL_CHARACTER}o "<!-- no-source-check: an offline exercise -->")',
        ),
        (
            "a reference definition",
            f'[a]: fo{DELETE_CHARACTER}o "<!-- no-source-check: an offline exercise -->"',
        ),
    ],
)
def test_a_control_character_is_not_a_destination_character(label: str, body: str) -> None:
    """CommonMark forbids an ASCII control character in a bare destination.

    Neither markdown-it 14.3.0 nor micromark 4.0.2 forms a link or a
    definition, so the marker in the quotes is an ordinary HTML comment on the
    page and the session really has declared its exemption. ``inline_link_end``
    stopped only at a space and a tab, and the destination class reached only
    to U+001F, so both read the whole thing as metadata and masked it.
    """
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == [], label


def test_a_less_than_part_way_into_a_bare_destination_is_still_a_destination() -> None:
    """A negative control, and the mirror of the finding that prompted this.

    A bare destination may not *start* with ``<`` and may hold one further
    along: markdown-it 14.3.0 and micromark 4.0.2 both read ``[a]: foo< "t"``
    as a definition, which renders nothing at all. The class excluded ``<``
    outright, so this hook read the line as prose and honoured a marker the
    page never shows.
    """
    body = '[a]: foo< "<!-- no-source-check: an offline exercise -->"'
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert any("Source Check" in m for m in check(text))


def test_a_bare_destination_may_not_start_with_a_less_than() -> None:
    """A negative control the lookahead protects.

    ``[a]: <foo "t"`` opens the angle-bracket form and never closes it, so
    neither renderer forms a definition and the marker in it is a comment.
    """
    body = '[a]: <foo "<!-- no-source-check: an offline exercise -->"'
    text = build_session(sections=SIX_SECTIONS, extra=f"## Notes\n\n{body}\n")
    assert check(text) == []


#: One non-breaking space, spelled through a name for the reason the sibling
#: test module spells it through one: an editor or a patch tool can turn the
#: character back into an ordinary space without anyone noticing.
NONBREAKING_SPACE = "\u00a0"


def test_a_nonbreaking_space_body_renders_as_content() -> None:
    """A section body of one U+00A0 puts a paragraph on the page.

    markdown-it 14.3.0 renders it as one, so the section is not the bare
    heading the checker called it. ``str.strip`` with no argument removed the
    character and read the body as empty.
    https://spec.commonmark.org/0.31.2/#blank-line
    """
    assert structure.renders_as_content(f"{NONBREAKING_SPACE}\n")


@pytest.mark.parametrize(
    ("label", "body"),
    [("an empty body", ""), ("three spaces", "   \n"), ("a tab", "\t\n")],
)
def test_a_blank_body_renders_as_nothing(label: str, body: str) -> None:
    """The negative control. Spaces and tabs really do render as nothing."""
    assert not structure.renders_as_content(body), label


def test_a_nonbreaking_space_line_keeps_a_paragraph_open() -> None:
    """A line of one U+00A0 leaves a paragraph open below it.

    HTML block condition 7 is the one condition that may not interrupt a
    paragraph, so clearing the paragraph state on this line opened a block
    markdown-it 14.3.0 does not open.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    assert structure.opens_a_paragraph(NONBREAKING_SPACE, False)


@pytest.mark.parametrize(
    ("label", "content"), [("an empty line", ""), ("three spaces", "   "), ("a tab", "\t")]
)
def test_a_blank_line_opens_no_paragraph(label: str, content: str) -> None:
    """The negative control. A real blank line still closes the paragraph."""
    assert not structure.opens_a_paragraph(content, False), label


def test_a_nonbreaking_space_line_does_not_close_an_html_block() -> None:
    """Only a blank line closes an HTML block whose condition has no end tag.

    A line of one U+00A0 is not blank, so condition 6 is still open below it
    and the backticks under it are raw HTML rather than a fence. markdown-it
    14.3.0 prints them, and the comment inside is the comment it looks like.
    Closing the block early made the fence real and buried the marker in a
    code block.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    text = (
        f"<div>\nnote\n{NONBREAKING_SPACE}\n{FENCE}\n"
        f"<!-- no-source-check: an exercise -->\n{FENCE}\n"
    )
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def test_a_blank_line_closes_an_html_block() -> None:
    """The negative control. A real blank line still closes condition 6."""
    text = (
        f"<div>\nnote\n\n{FENCE}\n"
        f"<!-- no-source-check: an exercise -->\n{FENCE}\n"
    )
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


def test_a_nonbreaking_space_does_not_open_an_atx_heading() -> None:
    """CommonMark requires a space or a tab after the opening hash run.

    ``#`` followed by U+00A0 is a paragraph to markdown-it 14.3.0, so the
    document holds no heading at all and a scaffold section named this way is
    missing rather than present.
    https://spec.commonmark.org/0.31.2/#atx-headings
    """
    scan = structure.scan_document(f"#{NONBREAKING_SPACE}Goal\n")
    assert structure.find_headings(scan) == []


def test_a_space_after_the_hashes_opens_an_atx_heading() -> None:
    """The negative control. A real heading is still found."""
    scan = structure.scan_document("# Goal\n")
    assert [(h.level, h.title) for h in structure.find_headings(scan)] == [(1, "Goal")]


# ---------------------------------------------------------------------------
# An autolink is destination data
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "autolink"),
    [
        ("a URI autolink", "<http://example.com/`>"),
        ("an email autolink", "<a`b@example.com>"),
    ],
)
def test_a_backtick_inside_an_autolink_opens_no_code_span(
    label: str, autolink: str
) -> None:
    """Everything between the angle brackets is the destination.

    It becomes the element's ``href`` and is printed as the link's text, so a
    backtick in one is a character rather than a delimiter. The scan skipped
    comments and tags and knew nothing of autolinks, so it paired that backtick
    with the next one and blanked the Source Check marker between them -- and a
    session that had declared its exemption was failed for not declaring one.
    Measured against markdown-it 14.3.0, which renders the marker as a comment.
    Kept in step with the case of the same name in
    ``tests/test_check_readability.py``.
    <https://spec.commonmark.org/0.31.2/#autolinks>
    """
    text = f"{autolink} <!-- no-source-check: an offline exercise --> `end`\n"
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None, label


def test_an_angle_run_that_is_no_autolink_keeps_its_backtick() -> None:
    """The negative control. A run holding spaces is no autolink at all.

    The backtick inside it really is an opening run, the code span reaches the
    marker, and the session has declared nothing.
    """
    text = "<no spaces allowed`> <!-- no-source-check: an offline exercise --> `end`\n"
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


# --- round 7: a block start clears the paragraph above condition 7 ----------

#: The Source Check exemption marker, spelled once for the round-7 cases.


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "a list item opening on the line",
            f"Words above the list.\n- <x-session>\n  {FENCE}\n"
            f"  {OFFLINE_MARKER}\n  {FENCE}\n",
        ),
        (
            "a blockquote opening on the line",
            f"Words above the quote.\n> <x-session>\n> {FENCE}\n"
            f"> {OFFLINE_MARKER}\n> {FENCE}\n",
        ),
    ],
)
def test_a_container_opening_on_a_line_lets_condition_seven_open(
    label: str, document: str
) -> None:
    """A container that opens on a line has closed the paragraph above it.

    Condition 7 may not interrupt a paragraph, and this hook asked
    ``opens_a_paragraph`` alone, which answers for the line *below* the one it
    reads. So a container opening on this line inherited the paragraph above it
    and refused the block CommonMark opens inside the new container; the
    backtick runs under it were read as a fence, and the exemption marker
    between them -- which markdown-it 14.3.0 renders as a comment on the page --
    was never found. ``starts_a_block`` was already in this module, asked of the
    inline model only; it is now asked here too. Kept in step with the case of
    the same name in ``tests/test_check_prohibited_placeholders.py``.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None, label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "a tag under a root paragraph",
            f"Words above.\n<x-session>\n{FENCE}\n{OFFLINE_MARKER}\n{FENCE}\n",
        ),
        (
            "a tag outdented out of a list item",
            f"- Words in a list item.\n<x-session>\n{FENCE}\n{OFFLINE_MARKER}\n{FENCE}\n",
        ),
    ],
)
def test_condition_seven_still_may_not_interrupt_a_paragraph(
    label: str, document: str
) -> None:
    """The negative controls, and the ones round 6 measured.

    A line that merely outdents out of a container has not started a block, so
    no type-seven block opens, the backtick runs really are a fence, and the
    marker inside them declares nothing. Refusing to exempt is the safe
    direction and it is the one the renderer takes here too.
    """
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None, label


# --- round 7: raw HTML before the bracket stack (4003802121) ----------------


@pytest.mark.parametrize(
    ("label", "prefix"),
    [
        ("an attribute value", '<span title="[">'),
        ("an autolink destination", "<http://example.com/[>"),
    ],
)
def test_a_bracket_inside_raw_html_is_no_link_opener(label: str, prefix: str) -> None:
    """A tag's attribute and an autolink's destination are data, not markup.

    CommonMark consumes the bracket with the tag or the autolink, so the later
    ``](`` is literal text and the comment in the parentheses is a comment the
    page prints. The bracket stack recorded that bracket as a link opener,
    masked the parentheses as a link target, and failed a session that had
    declared its exemption. Measured against markdown-it 14.3.0. Kept in step
    with the case of the same name in ``tests/test_check_readability.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    text = f'{prefix}text](url "{OFFLINE_MARKER}")\n'
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None, label


def test_a_marker_in_a_real_link_target_still_declares_nothing() -> None:
    """The negative control. A real link's title is an attribute.

    With no tag in front of it the bracket is an opener, the target parses, and
    the marker inside it is not a comment the page shows.
    """
    text = f'<span title="x">[text](url "{OFFLINE_MARKER}")\n'
    scan = structure.scan_document(text)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


# --- round 8: raw HTML runs, list interruption, lazy Setext, leaf blocks
# --- (4004076349, 4004076354, 4004076360, 4004076363, 4004076367) -----------


def _marker_found(document: str) -> bool:
    """Return whether the scan reads a Source Check exemption in ``document``."""
    scan = structure.scan_document(document)
    return structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def _goal_found(document: str) -> bool:
    """Return whether the scan leaves a ``## Goal`` heading to be counted."""
    scan = structure.scan_document(document)
    return any(line.strip().lower().startswith("## goal") for line in scan.content_lines)


@pytest.mark.parametrize(
    ("label", "run"),
    [
        ("a processing instruction", "<?foo ` ?>"),
        ("a declaration", "<!DOCTYPE ` html>"),
        ("a CDATA section", "<![CDATA[ ` ]]>"),
    ],
)
def test_a_raw_html_run_hides_no_marker(label: str, run: str) -> None:
    """A processing instruction, a declaration and a CDATA section are raw HTML.

    CommonMark takes whichever of a code span and a raw HTML form opens first,
    so a backtick inside one of these three is data and opens no span. The
    inline walk knew a comment, an autolink and a tag and not these, so it
    paired that backtick with the next real run and swallowed the marker
    between them -- and a session that had declared its exemption was failed
    for not declaring one. Measured against markdown-it 14.3.0. Kept in step
    with the case of the same name in ``tests/test_check_readability.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    assert _marker_found(f"Text {run} more {OFFLINE_MARKER} `end`\n"), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("an opener that never closes", f"Text <?foo ` more {OFFLINE_MARKER} `end`\n"),
        ("a lone angle bracket", f"Choose < 5 days ` and more {OFFLINE_MARKER} `end`\n"),
    ],
)
def test_an_unclosed_raw_html_run_is_still_ordinary_text(
    label: str, document: str
) -> None:
    """The positive control: without the closer there is no raw HTML at all.

    The backticks then pair across the marker and the session declares nothing,
    which is what markdown-it 14.3.0 does with both of these.
    """
    assert not _marker_found(document), label


def test_an_ordered_list_above_one_does_not_interrupt_a_paragraph() -> None:
    """A list may interrupt a paragraph only when an ordered one starts at 1.

    So ``2.`` under an open sentence is that sentence's own text, the paragraph
    runs on, and the code span opened above it closes past the marker. The scan
    split the paragraph at the marker instead and granted an exemption the page
    never shows. Measured against markdown-it 14.3.0.
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
    assert not _marker_found(f"Use `open\n2. continuation {OFFLINE_MARKER} `close`\n")


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "an ordered list starting at 1",
            f"Use `open\n1. continuation {OFFLINE_MARKER} `close`\n",
        ),
        ("a bullet list", f"Use `open\n- continuation {OFFLINE_MARKER} `close`\n"),
        (
            "a list already open above the line",
            f"2. Use `open\n3. continuation {OFFLINE_MARKER} `close`\n",
        ),
        (
            "nothing open above the line",
            f"# A heading\n2. continuation {OFFLINE_MARKER} `close`\n",
        ),
    ],
)
def test_a_list_that_may_interrupt_still_starts_a_block(label: str, document: str) -> None:
    """The positive controls the rule has to leave standing.

    The restriction is the *list's* and not the item's: a ``3.`` under a list
    already open is that list's next item and does start a block, and the
    marker really is a comment in all four.
    """
    assert _marker_found(document), label


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("out of a block quote", "> Use `open"),
        ("out of a list item", "- Use `open"),
    ],
)
def test_a_lazy_setext_underline_stays_in_its_paragraph(label: str, opener: str) -> None:
    """A Setext underline may never be a lazy continuation line.

    An outdented ``===`` under a quoted or listed paragraph has no root
    paragraph to underline, so it is that paragraph's own text and the code
    span opened above it closes past the marker. Ending the paragraph there
    exposed the marker and exempted a session the page never exempts. Measured
    against markdown-it 14.3.0.
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    """
    assert not _marker_found(f"{opener}\n===\nmore {OFFLINE_MARKER} `close`\n"), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "a Setext underline at the root",
            f"Use `open\n===\nmore {OFFLINE_MARKER} `close`\n",
        ),
        (
            "a Setext underline inside the quote",
            f"> Use `open\n> ===\n> more {OFFLINE_MARKER} `close`\n",
        ),
        (
            "a lazy line with no paragraph to underline",
            f"> # A heading `open\n===\nmore {OFFLINE_MARKER} `close`\n",
        ),
        (
            "a lazy thematic break, which may interrupt",
            f"> Use `open\n---\nmore {OFFLINE_MARKER} `close`\n",
        ),
    ],
)
def test_a_setext_underline_that_is_not_lazy_still_ends_the_paragraph(
    label: str, document: str
) -> None:
    """The positive controls. Only the lazy line changes."""
    assert _marker_found(document), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a textarea", f"<textarea>\n{OFFLINE_MARKER}\n</textarea>\n"),
        ("a script", f"<script>\n{OFFLINE_MARKER}\n</script>\n"),
        ("a style", f"<style>\n{OFFLINE_MARKER}\n</style>\n"),
        (
            "a textarea inside a div",
            f"<div>\n<textarea>\n{OFFLINE_MARKER}\n</textarea>\n</div>\n",
        ),
        ("a processing instruction block", f"<?php\n{OFFLINE_MARKER}\n?>\n"),
        ("a CDATA block", f"<![CDATA[\n{OFFLINE_MARKER}\n]]>\n"),
    ],
)
def test_a_raw_text_run_holds_no_marker(label: str, document: str) -> None:
    """Comment-shaped text inside a raw HTML run is not a comment.

    CommonMark passes a raw HTML block through untouched, and what its content
    *is* is then HTML's question. Inside ``script``, ``style`` and ``textarea``
    the content is raw text, and a processing instruction and a CDATA section
    are one token each, so none of these exempts a session from the Source
    Check. Python's ``html.parser`` reports the run as data for every document
    here. Kept in step with the case of the same name in
    ``tests/test_check_readability.py``.
    <https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state>
    """
    assert not _marker_found(document), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a div, whose content is markup", f"<div>\n{OFFLINE_MARKER}\n</div>\n"),
        ("a pre, whose content is markup", f"<pre>\n{OFFLINE_MARKER}\n</pre>\n"),
        (
            "the line after the element closes",
            f"<textarea>\nx\n</textarea>\n{OFFLINE_MARKER}\n",
        ),
        (
            "a script name written inside a comment",
            f"<!-- a note\n<script>\n-->\n\n{OFFLINE_MARKER}\n",
        ),
    ],
)
def test_a_comment_outside_a_raw_text_run_still_exempts(label: str, document: str) -> None:
    """The positive controls, and the two that bound the new state.

    ``pre`` and ``div`` hold markup, which ``html.parser`` confirms by
    reporting a comment for both. The run ends at its closing tag, and a
    ``<script>`` written inside a comment opens no run at all -- a raw HTML
    block may not start inside another one.
    """
    assert _marker_found(document), label


@pytest.mark.parametrize(
    ("label", "definition"),
    [
        ("a bare destination", "[x]: /url"),
        ("a destination and a title", '[x]: /url "a title"'),
        ("two definitions", "[x]: /url\n[y]: /url2"),
    ],
)
def test_a_link_reference_definition_opens_no_paragraph(
    label: str, definition: str
) -> None:
    """A definition is a leaf block, so condition 7 may open under it.

    ``<custom>`` then opens a type-seven HTML block that runs to the next blank
    line, and the ``## Goal`` inside it is raw HTML rather than a heading. The
    liberal fallback called the definition a paragraph, held the block shut,
    and counted a heading the page never shows -- so a session with no visible
    Goal passed. Measured against markdown-it 14.3.0.
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
    """
    assert not _goal_found(f"{definition}\n<custom>\n## Goal\n"), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a paragraph above the definition", "Words above.\n[x]: /url\n<custom>\n## Goal\n"),
        ("a paragraph above the tag", "Words above.\n<custom>\n## Goal\n"),
        ("a label with no destination", "[x]:\n<custom>\n## Goal\n"),
    ],
)
def test_a_line_that_is_not_a_definition_still_opens_a_paragraph(
    label: str, document: str
) -> None:
    """The positive controls. A definition may not interrupt a paragraph either.

    With one open above it, ``[x]: /url`` is paragraph text and the paragraph
    holds condition 7 shut, so the heading is a heading. A label with no
    destination is no definition at all. Without these the rule above could be
    written as "a bracket and a colon are never a paragraph" and still pass.
    """
    assert _goal_found(document), label


def test_raw_text_run_state_names_the_run_the_line_is_in() -> None:
    """The helper's contract, kept identical across the three hooks.

    It returns the run below the line and the run the line is *in*, the pair
    ``html_block_state`` returns. This hook asks only the first question of it
    -- are these characters text rather than markup -- and reads the answer
    through ``raw_text_run_holds_text``.
    """
    state, line_run = structure.raw_text_run_state("<textarea>", None, True)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = structure.raw_text_run_state("some words", "textarea", False)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = structure.raw_text_run_state("</textarea>", "textarea", False)
    assert (state, line_run) == (None, "textarea")
    # A run that opens and closes on one line is the run that line is in.
    state, line_run = structure.raw_text_run_state("<script>a</script>", None, True)
    assert (state, line_run) == (None, "script")
    # A line CommonMark keeps inside the paragraph above it opens no run.
    state, line_run = structure.raw_text_run_state("<xmp>", None, False)
    assert (state, line_run) == (None, None)
    # The comment may open part way along a line, and may close and open again.
    state, line_run = structure.raw_text_run_state("<!-- one --> x <!-- two", None, True)
    assert (state, line_run) == (structure.COMMENT_RUN, None)
    state, line_run = structure.raw_text_run_state("<!-- one -->", None, True)
    assert (state, line_run) == (None, None)
    assert structure.raw_text_run_holds_text("textarea")
    assert structure.raw_text_run_holds_text("script")
    assert not structure.raw_text_run_holds_text(structure.HTML_BLOCK_COMMENT)
    assert not structure.raw_text_run_holds_text(None)


def test_a_comment_shaped_run_inside_a_script_blanks_no_heading() -> None:
    """A ``<!--`` that a ``<script>`` prints opens no comment.

    Stripping comments before classifying the run read it as a real comment,
    which then ran to the end of the file and blanked every heading below it --
    including the ``## Goal`` a session must carry.
    """
    document = (
        "# Session 01\n\n<script>\n<!-- not really a comment\n</script>\n\n"
        "## Goal\n\nWords here.\n"
    )
    scan = structure.scan_document(document)
    titles = [heading.title for heading in structure.find_headings(scan)]
    assert "Goal" in titles


def test_a_real_comment_still_blanks_the_heading_inside_it() -> None:
    """The over-application control for the test above.

    A ``## Goal`` written inside an ordinary comment is not a heading, and a
    rule that refused to strip comments at all would find one here.
    """
    document = (
        "# Session 01\n\n<!-- a note\n## Goal\n-->\n\nWords here.\n"
    )
    scan = structure.scan_document(document)
    titles = [heading.title for heading in structure.find_headings(scan)]
    assert "Goal" not in titles


def test_a_one_line_raw_text_element_grants_no_exemption() -> None:
    """``<script><!-- no-source-check: ... --></script>`` is script data.

    The run opens and closes on the same line. Answering "no run at all" for it
    let the marker inside be read as a comment and granted an exemption the page
    never shows.
    """
    document = (
        "# Session 01\n\n<script><!-- no-source-check: offline --></script>\n"
    )
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


def test_a_one_line_ordinary_element_still_grants_the_exemption() -> None:
    """The over-application control: ``<div>`` holds markup, not raw text."""
    document = "# Session 01\n\n<div><!-- no-source-check: offline --></div>\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def test_a_whitespace_only_reference_label_is_not_a_definition() -> None:
    """``[\u00a0]: /url`` is a paragraph, so the line below it opens no block.

    A link label must hold one character the renderer does not fold away, and
    markdown-it 14.3.0 folds a non-breaking space. Reading the line as a leaf
    definition let a ``<custom>`` under it open HTML block condition 7, which
    then swallowed a real ``## Goal``.
    """
    document = (
        "# Session 01\n\n[\u00a0]: /url\n<custom>\n## Goal\n\nWords here.\n"
    )
    scan = structure.scan_document(document)
    titles = [heading.title for heading in structure.find_headings(scan)]
    assert "Goal" in titles


def test_an_ordinary_reference_label_is_still_a_definition() -> None:
    """The over-application control for the test above.

    ``[x]: /url`` really is a definition, so the ``<custom>`` below it really
    does open condition 7 and the ``## Goal`` inside that block is not a
    heading. A rule that rejected every label fails here.
    """
    document = "# Session 01\n\n[x]: /url\n<custom>\n## Goal\n\nWords here.\n"
    scan = structure.scan_document(document)
    titles = [heading.title for heading in structure.find_headings(scan)]
    assert "Goal" not in titles


def test_a_link_label_folds_the_blanks_the_renderer_folds() -> None:
    """And keeps the ones it keeps.

    markdown-it 14.3.0 normalizes a label with a JavaScript trim and collapse.
    ``str.split`` is a different set in both directions: it folds U+0085, which
    the renderer keeps as part of the label, and keeps U+FEFF, which the
    renderer folds. Measured one character at a time against the renderer.
    """
    assert structure.normalize_link_label("a\ufeffb") == "a b"
    assert structure.normalize_link_label("a\u0085b") == "a\u0085b"
    assert structure.normalize_link_label("  a   b  ") == "a b"
    assert structure.normalize_link_label("A\u00a0B") == "a b"


# ---------------------------------------------------------------------------
# Round 11: spaces or tabs, an opener line, and raw HTML productions
# ---------------------------------------------------------------------------


def test_a_tab_separated_reference_definition_is_a_definition() -> None:
    """The structure copy, kept identical to the sibling's.

    A definition is a leaf block, so what follows it opens HTML block
    condition 7 where a paragraph would not. Reading a tab-separated
    definition as a paragraph found a ``## Goal`` the page never shows.
    """
    assert structure.LINK_REFERENCE_DEFINITION_PATTERN.match("[a]:\t/url")
    assert structure.LINK_REFERENCE_DEFINITION_PATTERN.match('[a]: /url\t"t"\t')
    document = "[a]:\t/url\n<custom>\n## Goal\n"
    scan = structure.scan_document(document)
    assert not any(h.title == "Goal" for h in structure.find_headings(scan))


def test_a_tab_indented_reference_definition_is_not_a_definition() -> None:
    """The control in the other direction: a leading tab is four columns."""
    assert structure.LINK_REFERENCE_DEFINITION_PATTERN.match("\t[a]: /url") is None
    assert structure.LINK_REFERENCE_DEFINITION_PATTERN.match("   [a]: /url")


def test_a_tab_after_a_block_quote_marker_is_peeled() -> None:
    """The structure copy of the container rule."""
    assert structure.BLOCK_QUOTE_PREFIX_PATTERN.match(">\tquoted").end() == 2
    assert structure.BLOCK_QUOTE_PREFIX_PATTERN.match("> quoted").end() == 2
    assert structure.BLOCK_QUOTE_PREFIX_PATTERN.match(">quoted").end() == 1


def test_an_opener_line_belongs_to_the_run_it_opens() -> None:
    """``<script>`` and its marker on one line, the closer two lines down.

    ``html.parser`` reports no comment there, so the offline marker is script
    data and grants no exemption. Round eight closed the run that opens and
    closes on one line; this is the branch with no closer on its line.
    """
    assert structure.raw_text_run_state("<script><!-- x -->", None, True) == (
        "script",
        "script",
    )
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<script>" + OFFLINE_MARKER + "\nx\n</script>",
    )
    assert any("Source Check" in message for message in check(text))


def test_a_marker_beside_a_real_element_still_exempts() -> None:
    """The control in the other direction: a ``<div>`` holds inline content."""
    text = build_session(
        sections=SIX_SECTIONS,
        markers="<div>" + OFFLINE_MARKER + "\nx\n</div>",
    )
    assert not any("Source Check" in message for message in check(text))


def test_a_bracket_inside_raw_html_opens_no_link() -> None:
    """The structure copy, kept identical to the sibling's.

    A ``[`` inside a comment, a processing instruction, a declaration or a
    CDATA section is data, so no link forms and a marker in the parentheses
    beside it is a comment the page prints.
    """
    for opener, closer in (
        ("<!--", "-->"),
        ("<?php", "?>"),
        ("<![CDATA[", "]]>"),
        ("<!DOC", ">"),
    ):
        line = f'Text {opener}[{closer}text](u "{OFFLINE_MARKER}")'
        assert structure.link_metadata_regions(line, frozenset()) == (), opener


def test_a_bracket_inside_a_real_link_still_masks_its_title() -> None:
    """The control in the other direction: a real link's title is metadata."""
    line = f'Text [text](u "{OFFLINE_MARKER}")'
    assert structure.link_metadata_regions(line, frozenset()) != ()


def test_a_declaration_that_never_closes_is_not_raw_html() -> None:
    """The structure copy, kept identical to the sibling's."""
    line = 'Text <!DOC [text](u "t")'
    assert structure.raw_html_run_end(line, 5) == -1
    assert structure.link_metadata_regions(line, frozenset()) != ()


def test_a_heading_a_run_holds_is_no_heading() -> None:
    """A line a raw-text run holds is the element's content, block or no block.

    The block and the run part company when the block ends first: a type 7
    block meets its blank line while the ``<xmp>`` that opened it is still
    unclosed. The content walk read only the block, so the ``## Goal`` below
    was a heading here while the page painted nothing at all -- measured with
    markdown-it 14.3.0 read by ``html.parser``, which reports no ``<h2>``.
    """
    text = build_session().replace("## Goal\n", "<xmp>\nsome text\n\n## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_a_heading_below_a_closed_run_is_still_a_heading() -> None:
    """The over-application control: a run that closes frees its lines again."""
    text = build_session().replace(
        "## Goal\n", "<xmp>\nsome text\n</xmp>\n\n## Goal\n", 1
    )
    assert check(text) == []


def test_an_unclosed_inline_comment_does_not_reach_the_next_block() -> None:
    """An inline comment that never closes is no comment at all.

    ``Text <!-- unfinished`` with no ``-->`` before the block ends is text:
    markdown-it 14.3.0 escapes it into ``&lt;!-- unfinished``. Collecting it
    anyway carried an open comment into the next block, where the marker
    written in a code span became a real comment and exempted the session from
    Source Check on a declaration the page never shows.
    """
    document = (
        "# Session 01\n\nText <!-- unfinished\n\n"
        + TICK
        + "<!-- no-source-check: offline -->"
        + TICK
        + "\n"
    )
    scan = structure.scan_document(document)
    assert "no-source-check" not in scan.marker_text
    assert "unfinished" not in scan.marker_text


def test_an_unclosed_inline_comment_bridges_to_no_later_closer() -> None:
    """The same rule, in the shape that costs an exemption.

    The characters of an opener that never closes are on the page, so putting
    them in the marker text let a reason-less ``no-source-check:`` reach across
    a blank line to the ``-->`` of an unrelated comment below it. Measured with
    markdown-it 14.3.0: the first line renders as
    ``<p>Text &lt;!-- no-source-check: offline</p>``.
    """
    document = "Text <!-- no-source-check: offline\n\n<!-- audience: adult -->\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


def test_a_comment_across_a_soft_line_break_is_still_one_comment() -> None:
    """The control in the other direction: inside one paragraph a comment does
    cross a line ending, and the marker in it is a real marker."""
    document = "# Session 01\n\nText <!-- no-source-check:\noffline --> tail words.\n"
    scan = structure.scan_document(document)
    assert "no-source-check" in scan.marker_text


def test_a_block_comment_still_reaches_the_run_below_it() -> None:
    """The control for the other scope: a comment a raw HTML block opened is
    genuinely open, so it does reach the text run under it.

    A blank line ends the blockquote and with it the block, but not the
    comment: an HTML parser reading the page stays inside it until the
    ``-->``, so the marker written across the boundary is one marker.
    """
    document = "> <!-- no-source-check: offline\n\nstill open -->\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def test_a_closing_line_is_still_the_runs_last_line() -> None:
    """The control for the blanking rule: the run holds the line that closes it.

    A previous round settled that a line carrying the closing delimiter is
    still the run's last line. Reading the state the line *leaves* rather than
    the state it is *in* would free that line again, and the ``## Goal`` on it
    would be a heading the page never paints.
    """
    document = "# Session 01\n\n> <script>\n\n## Goal</script>\n\nWords.\n"
    scan = structure.scan_document(document)
    titles = [heading.title for heading in structure.find_headings(scan)]
    assert not any("Goal" in title for title in titles), titles


def test_a_marker_whose_comment_spans_lines_is_still_a_marker() -> None:
    """A comment may hold a line ending and still be one comment.

    Found by this round's sweep rather than by a reviewer. The marker patterns
    used ``.*?``, which stops at a line ending, so a marker written over two
    lines of one comment exempted nothing. Measured with markdown-it 14.3.0
    read by ``html.parser``: the page holds one comment, and its text is
    ``no-source-check: offline\nstill open``.
    """
    document = "<div>\n<!-- no-source-check: offline\nstill open -->\n</div>\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def test_a_marker_split_across_two_comments_is_no_marker() -> None:
    """The control: the reluctant quantifier still stops at the first ``-->``,
    so a match cannot run from one comment into the next."""
    document = "<div>\n<!-- no-source-check: -->\n<!-- offline -->\n</div>\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None


def test_a_tag_that_spans_lines_inside_a_block_is_still_a_tag() -> None:
    """Inside a raw HTML block a tag may hold a line ending.

    ``<span`` on one line and ``title="<!-- ... -->">`` on the next is one tag
    and the marker is attribute data -- measured with markdown-it 14.3.0 read
    by ``html.parser``, which reports no comment at all. Reading the
    continuation line on its own read the delimiters as a comment, and the
    session was exempted on what the renderer puts in a ``title`` attribute.
    """
    document = (
        '<div>\n<span\ntitle="<!-- no-source-check: offline -->">\n</div>\n'
    )
    scan = structure.scan_document(document)
    assert "no-source-check" not in scan.marker_text


def test_a_comment_that_spans_lines_inside_a_block_is_still_a_comment() -> None:
    """The control in the other direction: the comment state still crosses lines
    inside a raw HTML block, and a real marker written over two lines exempts."""
    document = "<div>\n<!-- no-source-check:\noffline -->\n</div>\n"
    scan = structure.scan_document(document)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None


def test_an_angle_run_that_is_no_tag_stays_text_across_lines() -> None:
    """The control for the tag continuation: a ``<`` that begins no tag opens no
    run, so its backtick still pairs and the marker inside stays masked."""
    line = "Text <no spaces allowed" + TICK
    assert structure.html_tag_prefix(line, 5) is None


def test_an_empty_list_item_does_not_interrupt_a_paragraph() -> None:
    """CommonMark forbids an empty list item from interrupting a paragraph.

    ``Words`` then ``*`` then ``<x>`` is one paragraph of three lines --
    measured with markdown-it 14.3.0 -- so the tag is paragraph text, opens no
    type 7 block, and the ``## Goal`` below it is a visible heading. The
    machine closed the paragraph at the empty marker and hid the heading.
    """
    for marker in ("*", "+"):
        text = build_session().replace(
            "## Goal\n", f"Words\n{marker} \n<x>\n## Goal\n", 1
        )
        assert check(text) == [], marker


def test_an_item_with_content_still_interrupts_a_paragraph() -> None:
    """The over-application control, read off the rule itself.

    An item with content interrupts and an empty one does not, in both list
    kinds; the dash is the exception the test below measures end to end. It is
    asserted on the helper rather than on a document because an ATX heading
    ends a list whatever the item held, so both documents paint the heading and
    no document can tell the two answers apart.
    """
    star = structure.Container(kind=structure.CONTAINER_KIND_LIST, bullet="*")
    dash = structure.Container(kind=structure.CONTAINER_KIND_LIST, bullet="-")
    first = structure.Container(kind=structure.CONTAINER_KIND_LIST, ordered_start=1)
    second = structure.Container(kind=structure.CONTAINER_KIND_LIST, ordered_start=2)
    quote = structure.Container(kind=structure.CONTAINER_KIND_BLOCK_QUOTE)
    assert not structure.container_interrupts_paragraph(star, "")
    assert structure.container_interrupts_paragraph(star, "item")
    assert structure.container_interrupts_paragraph(dash, "")
    assert not structure.container_interrupts_paragraph(first, "")
    assert structure.container_interrupts_paragraph(first, "item")
    assert not structure.container_interrupts_paragraph(second, "item")
    assert structure.container_interrupts_paragraph(quote, "")


def test_an_empty_dash_item_is_a_setext_underline() -> None:
    """The one bullet that is also a heading.

    ``-`` with nothing after it underlines the paragraph above it, and
    markdown-it 14.3.0 renders ``Words`` over ``-`` as an ``<h2>``. A heading
    starts a block, so the tag below it does open a type 7 block and the Goal
    below that is hidden -- the opposite answer from ``*`` and ``+`` on the
    same shape.
    """
    text = build_session().replace("## Goal\n", "Words\n- \n<x>\n## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text))


def test_an_empty_item_with_no_paragraph_above_it_still_opens_a_list() -> None:
    """The control for the paragraph half: the rule is about interrupting, so an
    empty item under a blank line opens its list as it always did."""
    text = build_session().replace("## Goal\n", "* \n<x>\n## Goal\n", 1)
    assert any('missing mandatory section "## Goal"' in m for m in check(text))
