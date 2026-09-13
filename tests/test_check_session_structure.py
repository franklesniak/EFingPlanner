"""Tests for the session-structure check.

The script is loaded by file path because its filename is hyphenated, matching
the pattern used by `tests/test_check_prohibited_placeholders.py`.
"""

from __future__ import annotations

import importlib.util
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
        parts.append("- Status: Core")
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
    text = text.replace("## Goal", "## Goal", 1)
    fenced = text + "\n```markdown\n## Stop Point\n\nnot a real section\n```\n"
    # Removing the real Stop Point must still be caught even though a fenced copy exists.
    broken = fenced.replace("## Stop Point\n\nReal content for Stop Point.\n", "", 1)
    assert any('missing mandatory section "## Stop Point"' in m for m in check(broken))


# ---------------------------------------------------------------------------
# Path safety and end-to-end
# ---------------------------------------------------------------------------


def test_paths_outside_the_repository_root_are_refused(tmp_path: Path) -> None:
    """CLI input must not drive reads outside the allowlisted tree."""
    outside = tmp_path.parent / "outside.md"
    outside.write_text("# Session 01: Nope\n", encoding="utf-8")
    assert structure.resolve_paths([str(outside)], tmp_path) == []


def test_the_real_session_corpus_is_well_formed() -> None:
    """The gate must be green on the real repository, or it is not a gate."""
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
