"""Tests for the `X, not Y` recount tool.

The script is loaded by file path because its filename is hyphenated, matching
the pattern used by `tests/test_check_readability.py`. Every test builds its own
small page or repository under `tmp_path`, so no test depends on the pages.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-x-not-y.py"
SPEC = importlib.util.spec_from_file_location("check_x_not_y", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load the recount script from {SCRIPT_PATH}")
_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _module
SPEC.loader.exec_module(_module)

cx = cast(Any, _module)

TICK = "`"
FENCE = TICK * 3


def candidates(text: str) -> list[Any]:
    """Return the candidates the script finds in one page."""
    page = cx.parse_text(text)
    return cx.find_candidates("page.md", page.prose, text.split("\n"))


def kinds(text: str) -> list[tuple[str, str]]:
    """Return (kind, text) for every candidate in one page."""
    return [(c.kind, c.text) for c in candidates(text)]


def write(root: Path, rel: str, text: str) -> None:
    """Write one page under a test repository root."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def judge_all(root: Path, judgment: str = "device") -> dict:
    """Return judgments that record every candidate under `root` as `judgment`."""
    out: dict = {}
    for rep in cx.scan(root, {}, {}):
        out[rep.path] = {c.key: {"line": c.lineno, "judgment": judgment, "reason": "test"} for c in rep.candidates}
    return out


def summary_for(root: Path, rel: str, judgments: dict, registers: dict | None = None) -> dict:
    """Return the summary row for one page."""
    for rep in cx.scan(root, judgments, registers or {}):
        if rep.path == rel:
            return cast(dict, cx.summarize(rep))
    raise AssertionError(f"{rel} was not scanned")


# ---------------------------------------------------------------------------
# What counts as prose
# ---------------------------------------------------------------------------


def test_code_spans_fences_tables_and_comment_lines_are_skipped() -> None:
    text = "\n".join([
        "# Title",
        "",
        "Use " + TICK + "a label, not a list" + TICK + " here.",
        "",
        FENCE + "text",
        "This is a fact, not a guess.",
        FENCE,
        "",
        "| Prompt | Answer |",
        "| --- | --- |",
        "| A row, not a sentence | |",
        "",
        "<!-- a comment, not prose -->",
    ])
    assert kinds(text) == []


def test_a_comment_inside_a_code_span_does_not_hide_later_text() -> None:
    text = "Show " + TICK + "<!-- marker -->" + TICK + " as it is. It is a map, not a list."
    assert [k for k, _ in kinds(text)] == ["device"]


def test_headings_are_never_counted() -> None:
    assert kinds("## A heading, not a sentence\n\nPlain text.") == []


def test_a_thematic_break_is_not_prose() -> None:
    assert kinds("One line.\n\n---\n\nDo not copy it.") == []


# ---------------------------------------------------------------------------
# Candidate patterns
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sentence",
    [
        "It is a first guess, not a final call.",
        "Draw it rather than fill it in.",
        "Take a break instead of quitting.",
        "Keep it cooperative, and never scored.",
        "A filter reduces exposure but does not remove it.",
        "Coach; do not do the work for them.",
    ],
)
def test_each_listed_form_is_a_device_candidate(sentence: str) -> None:
    assert [k for k, _ in kinds(sentence)] == ["device"]


def test_a_fragment_counts_only_after_a_claim() -> None:
    assert [k for k, _ in kinds("Break a rule gently. Not a failure.")] == ["device"]
    assert kinds("Not every station has an elevator.") == []


def test_emphasis_does_not_hide_a_contrast() -> None:
    assert [k for k, _ in kinds("It is a quick self-check, **not a grade.**")] == ["device"]


def test_a_short_negation_after_a_claim_is_a_split_candidate() -> None:
    found = kinds("You move a block. You don't start over.")
    assert ("split", "You move a block. → You don't start over.") in found


def test_the_banned_shape_is_a_candidate() -> None:
    found = [k for k, _ in kinds("It isn't just a binder page. It's a tool you'll use.")]
    assert "banned" in found


def test_the_banned_shape_across_a_paragraph_break_is_a_candidate() -> None:
    found = [k for k, _ in kinds("This is not a ban on open research.\n\nIt's a list of where to sit.")]
    assert "banned" in found


def test_candidate_keys_hold_kind_text_and_occurrence() -> None:
    found = candidates("It is a map, not a list. It is a map, not a list.")
    assert [c.key for c in found] == [
        "device|It is a map, not a list.|1",
        "device|It is a map, not a list.|2",
    ]


# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------


def scoped(text: str) -> list[Any]:
    """Return the page's markers with their scopes set."""
    page = cx.parse_text(text)
    lines = text.split("\n")
    for mk in page.markers:
        cx.marker_scope(mk, lines, page.heading_lines)
    return cast(list, page.markers)


def test_a_marker_covers_the_next_paragraph_only() -> None:
    text = "<!-- density-exempt: X, not Y -- required -->\nFirst line.\nSecond line.\n\nLater paragraph."
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end) == (2, 3)


def test_a_marker_above_a_heading_covers_its_section() -> None:
    text = "\n".join([
        "<!-- density-exempt: X, not Y -- required -->",
        "## Rule",
        "",
        "Text.",
        "",
        "### Detail",
        "",
        "More.",
        "",
        "## Next",
        "",
        "Other.",
    ])
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end) == (2, 9)


def test_stacked_markers_cover_the_same_list() -> None:
    text = "\n".join([
        "<!-- density-exempt: spaced dash -- required -->",
        "<!-- density-exempt: X, not Y -- required -->",
        "",
        "- one",
        "- two",
    ])
    first, second = scoped(text)
    assert (first.scope_start, first.scope_end) == (4, 5)
    assert (second.scope_start, second.scope_end) == (4, 5)


@pytest.mark.parametrize(("device", "applies"), [
    ("X, not Y", True),
    ("X-not-Y", True),
    ("x-not-y", True),
    ("spaced dash", False),
    ("real", False),
])
def test_only_x_not_y_markers_apply(device: str, applies: bool) -> None:
    (mk,) = scoped(f"<!-- density-exempt: {device} -- a reason -->\nText.")
    assert mk.applies is applies


# ---------------------------------------------------------------------------
# Registers
# ---------------------------------------------------------------------------


def test_register_comes_from_the_audience_marker_first() -> None:
    page = cx.parse_text("<!-- markdownlint-disable MD013 -->\n<!-- audience: parent -->\n\n# Page")
    assert cx.resolve_register("framework/templates/x.md", page.audience, {})[0] == "parent"


def test_an_audience_marker_shown_in_a_code_span_is_ignored() -> None:
    page = cx.parse_text("Write " + TICK + "<!-- audience: builder -->" + TICK + " on line 2.")
    assert page.audience is None


@pytest.mark.parametrize(("rel", "expected"), [
    ("framework/parent_guide/a.md", "parent"),
    ("framework/sessions/phase_00_setup/01_a.md", "child"),
    ("framework/templates/a.md", "child"),
    ("destinations/pack/session_inserts/a.md", "child"),
    ("destinations/pack/reference/a.md", "child"),
    ("framework/docs/a.md", "undetermined"),
])
def test_register_falls_back_to_the_tree(rel: str, expected: str) -> None:
    assert cx.resolve_register(rel, None, {})[0] == expected


def test_a_registers_entry_decides_an_unmarked_page() -> None:
    entry = {"framework/docs/a.md": {"register": "parent", "basis": "test"}}
    assert cx.resolve_register("framework/docs/a.md", None, entry) == ("parent", "test")


# ---------------------------------------------------------------------------
# Caps
# ---------------------------------------------------------------------------

THREE = "## One\n\nIt is a map, not a list.\n\n## Two\n\nDraw it rather than fill it in.\n\n## Three\n\nRest instead of quitting.\n"


def test_a_child_page_over_its_file_cap_is_over(tmp_path: Path) -> None:
    write(tmp_path, "framework/templates/a.md", THREE)
    row = summary_for(tmp_path, "framework/templates/a.md", judge_all(tmp_path))
    assert (row["counted"], row["cap"], row["status"]) == (3, 2, "OVER")


def test_a_parent_page_allows_three(tmp_path: Path) -> None:
    write(tmp_path, "framework/parent_guide/a.md", THREE)
    row = summary_for(tmp_path, "framework/parent_guide/a.md", judge_all(tmp_path))
    assert (row["counted"], row["cap"], row["status"]) == (3, 3, "PASS")


def test_a_marker_makes_a_page_exempt(tmp_path: Path) -> None:
    text = THREE.replace("## Three\n", "<!-- density-exempt: X, not Y -- required -->\n## Three\n")
    write(tmp_path, "framework/templates/a.md", text)
    row = summary_for(tmp_path, "framework/templates/a.md", judge_all(tmp_path))
    assert (row["raw"], row["counted"], row["status"]) == (3, 2, "EXEMPT")


def test_two_in_one_section_are_over_for_child_and_parent_pages(tmp_path: Path) -> None:
    text = "## One\n\nIt is a map, not a list. Draw it rather than fill it in.\n"
    write(tmp_path, "framework/parent_guide/a.md", text)
    row = summary_for(tmp_path, "framework/parent_guide/a.md", judge_all(tmp_path))
    assert [r["status"] for r in row["sections"] if r["section"] == "One"] == ["OVER"]


def test_builder_sections_carry_no_section_cap(tmp_path: Path) -> None:
    text = "<!-- audience: builder -->\n\n## One\n\nIt is a map, not a list. Draw it rather than fill it in.\n"
    write(tmp_path, "framework/docs/a.md", text)
    row = summary_for(tmp_path, "framework/docs/a.md", judge_all(tmp_path))
    assert [r["status"] for r in row["sections"] if r["section"] == "One"] == ["n/a"]
    assert row["status"] == "PASS"


def test_text_above_the_first_heading_is_not_a_section(tmp_path: Path) -> None:
    text = "# Card\n\nIt is a map, not a list. Draw it rather than fill it in.\n"
    write(tmp_path, "framework/templates/a.md", text)
    row = summary_for(tmp_path, "framework/templates/a.md", judge_all(tmp_path))
    assert [r["status"] for r in row["sections"]] == ["n/a"]
    assert row["status"] == "PASS"


def test_a_second_split_negation_is_over(tmp_path: Path) -> None:
    text = "## A\n\nYou move a block. You don't start over.\n\n## B\n\nLook it up. Do not guess.\n"
    write(tmp_path, "framework/templates/a.md", text)
    judged = judge_all(tmp_path, "split")
    row = summary_for(tmp_path, "framework/templates/a.md", judged)
    assert (row["splits_counted"], row["split_status"]) == (2, "OVER")


# ---------------------------------------------------------------------------
# The command line
# ---------------------------------------------------------------------------


def repo_with(tmp_path: Path, text: str) -> Path:
    """Return a test repository holding one child page."""
    write(tmp_path, "framework/templates/a.md", text)
    return tmp_path


def run(tmp_path: Path, judgments: dict, capsys: Any) -> int:
    """Run the script's main() on a test repository with a judgments file."""
    jpath = tmp_path / "judgments.json"
    jpath.write_text(json.dumps(judgments), encoding="utf-8")
    code = cx.main([str(tmp_path), "--judgments", str(jpath), "--registers", str(tmp_path / "none.json")])
    capsys.readouterr()
    return cast(int, code)


def test_an_unjudged_candidate_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\nIt is a map, not a list.\n")
    assert run(root, {}, capsys) == 1


def test_a_judged_page_within_its_caps_passes(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\nIt is a map, not a list.\n")
    assert run(root, judge_all(root), capsys) == 0


def test_a_banned_shape_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\nIt isn't just a page. It's a tool.\n")
    judged = judge_all(root, "no")
    for page in judged.values():
        for entry in page.values():
            entry["judgment"] = "banned"
    assert run(root, judged, capsys) == 1


def test_a_root_without_framework_is_refused(tmp_path: Path, capsys: Any) -> None:
    assert cx.main([str(tmp_path)]) == 2
    capsys.readouterr()


def test_symlinked_pages_are_not_read(tmp_path: Path) -> None:
    write(tmp_path, "outside.md", "It is a map, not a list.\n")
    (tmp_path / "framework").mkdir()
    try:
        (tmp_path / "framework" / "link.md").symlink_to(tmp_path / "outside.md")
    except (OSError, NotImplementedError):
        pytest.skip("this platform cannot create a symlink here")
    assert cx.page_paths(tmp_path) == []


# ---------------------------------------------------------------------------
# The data files beside the script
# ---------------------------------------------------------------------------


def test_the_judgments_file_is_well_formed() -> None:
    data = cx.load_json(cx.DEFAULT_JUDGMENTS)
    assert data
    for rel, entries in data.items():
        assert rel.endswith(".md")
        for key, entry in entries.items():
            kind, _, rest = key.partition("|")
            assert kind in ("device", "split", "banned")
            assert rest.rsplit("|", 1)[1].isdigit()
            assert entry["judgment"] in cx.VALID_JUDGMENTS
            assert entry["reason"]


def test_the_registers_file_is_well_formed() -> None:
    data = cx.load_json(cx.DEFAULT_REGISTERS)
    for rel, entry in data.items():
        assert rel.endswith(".md")
        assert entry["register"] in cx.FILE_CAP
        assert entry["basis"]
