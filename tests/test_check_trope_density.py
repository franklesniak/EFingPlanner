"""Tests for the trope-density gate.

The script is loaded by file path because its filename is hyphenated, as the
recount's suite loads the recount. Every test builds its own small page, or a
small repository under `tmp_path`, so no test depends on the curriculum. The
gate reads pages with markdown-it through Node, as the recount does, so the
suite needs Node.js and the repository's `node_modules` (`npm ci`).

Each fail rule has a failing and a passing test, and so does each counting
reading the gate applies: the label separator, the builder cap, the spaced em
dash, the smaller counting readings and the marker rules.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-trope-density.py"
SPEC = importlib.util.spec_from_file_location("check_trope_density", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load the trope-density gate from {SCRIPT_PATH}")
_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _module
SPEC.loader.exec_module(_module)

td = cast(Any, _module)

TICK = "`"
CHILD = "framework/sessions/phase_00_setup/99_test_session.md"
PARENT = "framework/parent_guide/test_page.md"
BUILDER = "framework/docs/test_page.md"
BUILDER_MARKER = "<!-- audience: builder -->"
EM = "\u2014"


def page(*lines: str) -> str:
    """Return a page built from its lines."""
    return "\n".join(lines) + "\n"


def filler(count: int, start: int = 1) -> list[str]:
    """Return `count` one-line paragraphs of plain prose, each a prose line with no device."""
    out: list[str] = []
    for n in range(start, start + count):
        out += [f"Plain line {n} is here.", ""]
    return out


def check(text: str, rel: str = CHILD, gated: bool = True) -> Any:
    """Measure one page."""
    return td.check_page(rel, text, {}, gated)


def fail_kinds(result: Any) -> list[str]:
    """Return the kind of each breach on a page."""
    return [n.kind for n in result.fails]


def advice_kinds(result: Any) -> list[str]:
    """Return the kind of each printed note on a page."""
    return [n.kind for n in result.advice]


def dashes(result: Any) -> list[Any]:
    """Return a page's spaced-dash devices, counted and exempted."""
    return [d for d in result.devices if d.family == "spaced dash"]


def write(root: Path, rel: str, text: str | bytes) -> Path:
    """Write one file under a test repository root."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(text, bytes):
        path.write_bytes(text)
    else:
        path.write_text(text, encoding="utf-8", newline="\n")
    return path


def run(root: Path, *args: str, capsys: Any) -> tuple[int, str]:
    """Run the gate's `main()` on a test repository and return its exit code and output."""
    code = td.main([str(root), *args])
    return code, capsys.readouterr().out


# ---------------------------------------------------------------------------
# Scope: which files are gated, which are reported, which are never read
# ---------------------------------------------------------------------------


def repository(tmp_path: Path) -> Path:
    """Return a small repository whose one gated page passes."""
    write(tmp_path, CHILD, page("# Session", "", *filler(5)))
    return tmp_path


def test_reported_files_are_measured_and_never_fail(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, "docs/build/batch9_build_prompt.md", page("# Brief", "", *[f"Line {n} -- aside." for n in range(9)]))
    write(root, "CONTRIBUTING.md", page("# Contributing", "", "One -- two.", "", "Three -- four."))
    code, out = run(root, capsys=capsys)
    assert code == 0
    assert "record docs/build/batch9_build_prompt.md: builder caps" in out
    assert "over on spaced dash, reported only" in out
    assert "record CONTRIBUTING.md" in out


def test_a_gated_page_over_its_cap_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, "destinations/demo/session_inserts/10_demo.md", page("# Insert", "", "One -- two.", "", "Three -- four."))
    code, out = run(root, capsys=capsys)
    assert code == 1
    assert "FAIL destinations/demo/session_inserts/10_demo.md" in out


def test_protected_files_github_and_templates_are_never_read(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    unreadable = b"\xff\xfe not UTF-8 -- at all\n"
    for rel in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".hermes.md", ".github/notes.md",
                "templates/adoption/_TEMPLATE.md"):
        write(root, rel, unreadable)
    code, out = run(root, "--format", "json", capsys=capsys)
    assert code == 0
    data = json.loads(out)
    paths = [p["path"] for p in data["pages"]] + [r["path"] for r in data["records"]]
    assert paths == [CHILD]


def test_the_root_pages_are_gated(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, "README.md", page("<!-- markdownlint-disable MD013 -->", "<!-- audience: parent -->", "", "# Read me",
                                  "", "One -- two.", "", "Three -- four."))
    code, out = run(root, capsys=capsys)
    assert code == 1
    assert "FAIL README.md" in out


def test_no_line_of_the_archived_spec_is_printed(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    secret = "Zanzibarquux"
    write(root, "docs/spec/specification.md", page(
        f"# {secret} spec", "", f"## {secret} section", "", *[f"{secret} line {n} -- aside, really." for n in range(9)],
        "", "<!-- density-exempt: real -- the spec page 12 wording -->", f"{secret} studies show it."))
    for args in ((), ("--format", "json")):
        code, out = run(root, *args, capsys=capsys)
        assert code == 0
        assert "docs/spec/specification.md" in out
        assert secret not in out


def test_a_gated_page_that_cannot_be_read_stops_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, "framework/sessions/phase_00_setup/95_bytes.md", b"# S\n\n\xff\xfe -- not UTF-8\n")
    code = td.main([str(root)])
    assert code == 3
    assert "95_bytes.md" in capsys.readouterr().err


def test_a_reader_that_cannot_run_stops_the_run(tmp_path: Path, capsys: Any, monkeypatch: Any) -> None:
    root = repository(tmp_path)

    class Broken:
        """A Markdown reader that cannot start, as with no Node.js installed."""

        def __call__(self, text: str) -> list[Any]:
            raise td.xny.ReadError("cannot start node", setup=True)

        def close(self) -> None:
            pass

    monkeypatch.setattr(td.xny, "read_blocks", Broken())
    code = td.main([str(root)])
    err = capsys.readouterr().err
    assert code == 3
    assert "needs Node.js and the repository's node_modules" in err


def test_a_link_under_a_gated_root_stops_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    target = write(root, "outside.md", "Plain.\n")
    link = root / "framework" / "linked.md"
    try:
        os.symlink(target, link)
    except (OSError, NotImplementedError):
        pytest.skip("this system cannot create a symbolic link")
    code = td.main([str(root)])
    err = capsys.readouterr().err
    assert code == 3
    assert "framework/linked.md is a symbolic link or a junction" in err


# ---------------------------------------------------------------------------
# Registers
# ---------------------------------------------------------------------------


def test_a_gated_page_with_no_register_fails() -> None:
    result = check(page("# Read me", "", "Plain text."), rel="README.md")
    assert result.register == "undetermined"
    assert fail_kinds(result) == ["register"]


def test_an_audience_marker_places_a_root_page() -> None:
    result = check(page("<!-- audience: parent -->", "", "# Read me", "", "Plain text."), rel="README.md")
    assert result.register == "parent"
    assert result.fails == []


def test_a_reported_file_is_measured_under_the_builder_caps() -> None:
    # Five `real` words: over the parent cap of 4, within the builder cap of 6.
    text = page("<!-- audience: parent -->", "", "# Prompts", "", *[f"It is real {n}." for n in range(5)])
    reported = check(text, rel="docs/PR_REVIEW_PROMPTS.md", gated=False)
    assert reported.caps == {"spaced dash": 1, "real": 6}
    assert "real file cap" not in fail_kinds(reported)
    assert "real file cap" in fail_kinds(check(text, rel=PARENT))


# ---------------------------------------------------------------------------
# Caps (each fail rule fails over its number and passes at it)
# ---------------------------------------------------------------------------


def test_child_file_dash_cap() -> None:
    # 10 prose lines: 10 // 5 = 2 dashes per file, all above the first `##`.
    at_cap = page("# S", "", "One -- two.", "", "Three -- four.", "", *filler(8))
    over = page("# S", "", "One -- two.", "", "Three -- four.", "", "Five -- six.", "", *filler(7))
    assert check(at_cap).caps["spaced dash"] == 2 and check(at_cap).fails == []
    assert fail_kinds(check(over)) == ["spaced dash file cap"]


def test_parent_file_dash_cap_stops_at_eight() -> None:
    lines = [f"Line {n} -- aside." for n in range(8)]
    at_cap = page("# P", "", *[x for line in lines for x in (line, "")], *filler(42))
    over = page("# P", "", *[x for line in lines + ["Line 9 -- aside."] for x in (line, "")], *filler(41))
    assert check(at_cap, rel=PARENT).caps["spaced dash"] == 8
    assert check(at_cap, rel=PARENT).fails == []
    assert fail_kinds(check(over, rel=PARENT)) == ["spaced dash file cap"]


def test_builder_cap_is_one_per_four_prose_lines_with_no_ceiling() -> None:
    # 40 prose lines: 40 // 4 = 10, above the child and parent ceiling of 8.
    ten = [f"Line {n} -- aside." for n in range(10)]
    at_cap = page(BUILDER_MARKER, "# B", "", *[x for line in ten for x in (line, "")], *filler(30))
    over = page(BUILDER_MARKER, "# B", "", *[x for line in ten + ["Line 11 -- aside."] for x in (line, "")],
                *filler(29))
    assert check(at_cap, rel=BUILDER).caps["spaced dash"] == 10
    assert check(at_cap, rel=BUILDER).fails == []
    assert fail_kinds(check(over, rel=BUILDER)) == ["spaced dash file cap"]


def test_builder_cap_has_a_floor_of_one() -> None:
    at_cap = page(BUILDER_MARKER, "# B", "", "One -- two.", "", "Plain.")
    over = page(BUILDER_MARKER, "# B", "", "One -- two.", "", "Three -- four.")
    assert check(at_cap, rel=BUILDER).caps["spaced dash"] == 1
    assert check(at_cap, rel=BUILDER).fails == []
    assert fail_kinds(check(over, rel=BUILDER)) == ["spaced dash file cap"]


def test_builder_and_parent_files_have_no_section_cap() -> None:
    body = ["## Chapter", "", "One -- two.", "", "Three -- four.", "", "Five -- six.", "", *filler(9)]
    assert check(page(BUILDER_MARKER, "# B", "", *body), rel=BUILDER).fails == []
    assert check(page("# P", "", *body, *filler(3, 20)), rel=PARENT).fails == []


def test_child_section_dash_cap_is_one() -> None:
    one = page("# S", "", *filler(20), "## Steps", "", "One -- two.", "", "Plain.")
    two = page("# S", "", *filler(20), "## Steps", "", "One -- two.", "", "Three -- four.")
    assert check(one).fails == []
    assert fail_kinds(check(two)) == ["spaced dash section cap"]


@pytest.mark.parametrize("title", ["Goal", "Start Here", "Stop Point"])
def test_goal_start_here_and_stop_point_hold_no_dash(title: str) -> None:
    assert fail_kinds(check(page("# S", "", *filler(20), f"## {title}", "", "One -- two."))) == [
        "spaced dash section cap"]
    assert check(page("# S", "", *filler(20), f"## {title}", "", "One, two.")).fails == []


def test_text_above_the_first_section_takes_only_the_file_cap() -> None:
    assert check(page("# S", "", "One -- two.", "", "Three -- four.", "", *filler(10))).fails == []


def test_the_section_cap_reads_only_child_facing_text() -> None:
    text = page("# S", "", *filler(20), "## Parent Notes", "", "One -- two.", "", "Three -- four.")
    assert check(text).fails == []


def test_real_file_caps_by_register() -> None:
    def reals(n: int) -> list[str]:
        return [x for k in range(n) for x in (f"It is real {k}.", "")]
    assert check(page("# S", "", *reals(4))).fails == []
    assert fail_kinds(check(page("# S", "", *reals(5)))) == ["real file cap"]
    assert check(page("# P", "", *reals(4)), rel=PARENT).fails == []
    assert fail_kinds(check(page("# P", "", *reals(5)), rel=PARENT)) == ["real file cap"]
    assert check(page(BUILDER_MARKER, "# B", "", *reals(6)), rel=BUILDER).fails == []
    assert fail_kinds(check(page(BUILDER_MARKER, "# B", "", *reals(7)), rel=BUILDER)) == ["real file cap"]


def test_child_section_real_cap_is_one() -> None:
    assert check(page("# S", "", "## Steps", "", "It is real.")).fails == []
    assert fail_kinds(check(page("# S", "", "## Steps", "", "It is real.", "", "It is really fine."))) == [
        "real section cap"]


def test_genuine_is_banned_in_child_facing_text() -> None:
    assert "child genuine" in fail_kinds(check(page("# S", "", "It is genuine.")))
    assert "child genuine" in fail_kinds(check(page("# S", "", "## Steps", "", "It genuinely helps.")))
    assert check(page("# S", "", "## Parent Notes", "", "It is genuine.")).fails == []
    assert check(page("# S", "", "**For parents:** it is genuine.")).fails == []
    assert check(page("# P", "", "It is genuine."), rel=PARENT).fails == []


def test_guardrails_is_banned_in_child_facing_text() -> None:
    assert fail_kinds(check(page("# S", "", "Mind the guardrails."))) == ["child guardrails"]
    assert check(page("# P", "", "The guardrails are budget and safety."), rel=PARENT).fails == []
    assert check(page("# S", "", "## Parent Notes", "", "The guardrails hold.")).fails == []


ZERO_TOLERANCE_SAMPLES = [
    ("T88", "I hope this helps you plan.", "Hope is a good thing to plan with."),
    ("T88", "Feel free to ask a grown-up.", "Feel free to pick the map."),
    ("T89", "Certainly, the map is ready.", "The map is certainly ready."),
    ("T89", "Here's a quick overview of the trip.", "Here is the overview of the trip."),
    ("T90", "As requested, the list is shorter.", "The list you asked for is shorter."),
    ("T91", "I have updated the page.", "The page was updated."),
    ("T91", "Below is the plan.", "The plan is below."),
    ("T92", "User: pick a city.", "Each user picks a city."),
    ("T92", "Fill in {{city_name}} here.", "Fill in the city name here."),
    ("T93", "As of my last update, it was open.", "Check that it is open."),
    ("T94", "After careful consideration, pick one.", "Consider it with care, then pick one."),
    ("T95", "I wanted to reach out about the trip.", "Reach out to a grown-up about the trip."),
    ("T96", "I hope this message finds you well.", "This message is for you."),
    ("T100", "Studies show that maps help.", "Your notes show that maps help."),
    ("SPEC-SECTION", "See the spec's section 31.", "See the Batch 4 build brief's section 8."),
]


@pytest.mark.parametrize(("family", "failing", "passing"), ZERO_TOLERANCE_SAMPLES)
def test_each_zero_tolerance_family_fails_on_a_hit(family: str, failing: str, passing: str) -> None:
    hit = check(page("# P", "", failing), rel=PARENT)
    assert [n.kind for n in hit.fails] == [family]
    assert hit.fails[0].lineno == 3
    assert check(page("# P", "", passing), rel=PARENT).fails == []


def test_each_zero_tolerance_pattern_keeps_its_flags_at_its_start() -> None:
    for family, (_, rx) in td.ZERO_TOLERANCE.items():
        assert rx.pattern.startswith("(?i)"), family
        assert "(?m)" not in rx.pattern and "\\x{" not in rx.pattern, family
    assert td.LOAD_BEARING[2].pattern.startswith("(?i)")


def test_a_line_start_pattern_is_anchored_at_the_paragraph_start() -> None:
    wrapped = page("# P", "", "The steps are written out and", "below is where they end.")
    assert check(wrapped, rel=PARENT).fails == []
    assert fail_kinds(check(page("# P", "", "Below is where they end."), rel=PARENT)) == ["T91"]


def test_zero_tolerance_skips_code_comments_and_quotations() -> None:
    text = page("# P", "", "Write " + TICK + "hope this helps" + TICK + " on the card.", "",
                "<!-- I hope this helps -->", "", "> \"I hope this helps,\" said the note.\"", "")
    assert check(text, rel=PARENT).fails == []


def test_zero_tolerance_reads_headings_and_table_cells() -> None:
    assert fail_kinds(check(page("# P", "", "## Studies show this"), rel=PARENT)) == ["T100"]
    table = page("# P", "", "| Prompt | Your answer |", "| --- | --- |", "| Experts say | |")
    assert fail_kinds(check(table, rel=PARENT)) == ["T100"]


@pytest.mark.parametrize(("text", "hit"), [
    ("See the spec's section 31.", True),
    ("See the spec\u2019s section 31.", True),
    ("The rule is in \u00a7 9.", True),
    ("The rule is in \u00a79.", True),
    ("As the specification section 4.2 says, pick one.", True),
    ("See Section 31 of the spec.", True),
    ("See section 31 of the specification.", True),
    ("See the design record's section 31.", True),
    ("See the archived record's section 31.", True),
    ("See the archived spec, section 31.", True),
    ("See the spec (section 31).", True),
    ("See the spec's own numbered section 31.", True),
    ("See the spec's own long numbered section 31.", False),
    ("See the spec's sections 3 and 4.", True),
    ("As the brief's section 10 says, pick one.", False),
    ("Session 10 has the rule.", False),
    ("Section 10 of the brief has the rule.", False),
    ("The design record fixes the titles.", False),
])
def test_spec_section_reads_each_citation_form(text: str, hit: bool) -> None:
    assert fail_kinds(check(page("# P", "", text), rel=PARENT)) == (["SPEC-SECTION"] if hit else [])


def test_load_bearing_fails_in_child_text_and_is_printed_elsewhere() -> None:
    assert fail_kinds(check(page("# S", "", "This is the load-bearing step."))) == ["T104"]
    builder = check(page(BUILDER_MARKER, "# B", "", "This is the load-bearing step."), rel=BUILDER)
    assert builder.fails == []
    assert advice_kinds(builder) == ["T104"]
    assert check(page("# S", "", "## Parent Notes", "", "This is the load-bearing step.")).fails == []


def test_an_html_block_the_page_model_cannot_read_fails() -> None:
    assert fail_kinds(check(page("# P", "", "<div>Hidden -- text.</div>"), rel=PARENT)) == ["unread HTML"]
    assert check(page("# P", "", "Shown text."), rel=PARENT).fails == []


# ---------------------------------------------------------------------------
# The label separator: a list item's label, one parenthetical, then the dash
# ---------------------------------------------------------------------------


def test_only_the_first_line_of_a_list_item_gives_a_separator() -> None:
    assert dashes(check(page("# P", "", "- **Term** -- the gloss."), rel=PARENT)) == []
    second_line = check(page("# P", "", "- Intro text", "  **Term** -- the gloss."), rel=PARENT)
    assert len(dashes(second_line)) == 1
    paragraph = check(page("# P", "", "**Term** -- the gloss."), rel=PARENT)
    assert len(dashes(paragraph)) == 1


@pytest.mark.parametrize("item", [
    "- **Term** -- the gloss.",
    "1. **Term** -- the gloss.",
    "- [Page](page.md) -- the gloss.",
    "- [Page][ref] -- the gloss.",
    f"- **Term** {EM} the gloss.",
    "- [ ] **Term** -- the gloss.",
])
def test_a_bold_run_or_a_link_opening_the_item_is_a_label(item: str) -> None:
    assert dashes(check(page("# P", "", item, "", "[ref]: page.md"), rel=PARENT)) == []


def test_one_parenthetical_may_stand_between_the_label_and_the_dash() -> None:
    assert dashes(check(page("# P", "", "- **Term** (a gloss) -- the rest."), rel=PARENT)) == []
    assert dashes(check(page("# P", "", "- [Page](page.md) (a gloss) -- the rest."), rel=PARENT)) == []
    two = check(page("# P", "", "- **Term** (a) (b) -- the rest."), rel=PARENT)
    assert len(dashes(two)) == 1


def test_the_separator_is_the_first_dash_after_the_label() -> None:
    result = check(page("# P", "", "- **Term** -- one thing. Then -- another."), rel=PARENT)
    assert [d.lineno for d in dashes(result)] == [3]
    assert len(dashes(result)) == 1
    link_dash = check(page("# P", "", "- [A -- B](page.md) -- the gloss."), rel=PARENT)
    assert len(dashes(link_dash)) == 1


def test_a_separator_is_neither_counted_nor_tested() -> None:
    result = check(page("# P", "", "- **Term** -- you have to pick one."), rel=PARENT)
    assert result.devices == []
    assert result.counts["spaced dash"] == 0


def test_a_bold_label_holding_its_own_dash_gives_no_separator() -> None:
    result = check(page("# P", "", "- **Pick one -- then stop.** -- The rest is here."), rel=PARENT)
    assert len(dashes(result)) == 2


@pytest.mark.parametrize("item", ["- Role: a value -- the rest.", "- the **term** -- the rest.",
                                  "- Pick the **term** -- the rest."])
def test_a_field_label_or_a_bold_run_inside_a_sentence_is_no_label(item: str) -> None:
    assert len(dashes(check(page("# P", "", item), rel=PARENT))) == 1


def test_every_other_dash_in_a_labelled_item_counts() -> None:
    result = check(page("# P", "", "- **Term** -- the gloss.", "  A second line -- an aside."), rel=PARENT)
    assert [d.lineno for d in dashes(result)] == [4]


# ---------------------------------------------------------------------------
# The spaced em dash
# ---------------------------------------------------------------------------


def test_a_spaced_em_dash_is_counted_as_a_spaced_dash() -> None:
    result = check(page("# P", "", f"One {EM} two."), rel=PARENT)
    assert [(d.word, d.paired) for d in dashes(result)] == [(EM, False)]
    assert check(page("# P", "", f"One{EM}two."), rel=PARENT).devices == []


def test_a_spaced_em_dash_meets_the_same_caps_and_pair_rule() -> None:
    two = page("# S", "", *filler(20), "## Steps", "", f"One {EM} two.", "", f"Three {EM} four.")
    assert fail_kinds(check(two)) == ["spaced dash section cap"]
    pair = check(page("# S", "", *filler(20), "## Steps", "", f"One {EM} like this {EM} two."))
    assert pair.fails == [] and [d.paired for d in dashes(pair)] == [True]
    mixed = check(page("# P", "", f"One -- like this {EM} two."), rel=PARENT)
    assert [d.paired for d in dashes(mixed)] == [True]


def test_both_glyphs_take_the_same_test() -> None:
    hyphens = check(page("# P", "", "Pick one -- you can change it later."), rel=PARENT)
    em_dash = check(page("# P", "", f"Pick one {EM} you can change it later."), rel=PARENT)
    assert dashes(hyphens)[0].test3 == dashes(em_dash)[0].test3 == "t3-finite"


def test_the_gate_changes_no_glyph(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    before = page("# S", "", f"One {EM} two.", "", "Three -- four.", "", *filler(10))
    path = write(root, "framework/sessions/phase_00_setup/98_glyphs.md", before)
    run(root, capsys=capsys)
    assert path.read_bytes() == before.encode("utf-8")


# ---------------------------------------------------------------------------
# The smaller counting readings
# ---------------------------------------------------------------------------


def test_text_in_inline_quotation_marks_is_counted() -> None:
    result = check(page("# P", "", 'Say "yes -- right now" to the plan.'), rel=PARENT)
    assert len(dashes(result)) == 1
    assert check(page("# P", "", "Say \"really\" to it."), rel=PARENT).counts["real"] == 1


def test_a_navigation_line_is_a_prose_line_and_its_dash_counts() -> None:
    result = check(page("# S", "", "You are here: Phase 1 | Previous: none | Next: none -- you made it"))
    assert result.prose_lines == 1
    assert len(dashes(result)) == 1


def test_a_parent_region_ends_at_the_next_heading_of_its_level_or_higher() -> None:
    inside = page("# S", "", "## Parent Notes", "", "### Coaching", "", "It is genuine.")
    assert check(inside).fails == []
    after = page("# S", "", "## Parent Notes", "", "Plain.", "", "## Next Steps", "", "It is genuine.")
    assert fail_kinds(check(after)) == ["child genuine"]


def test_child_genuine_fails_and_counts_in_the_family() -> None:
    result = check(page("# S", "", "It is genuine."))
    assert fail_kinds(result) == ["child genuine"]
    assert result.counts["real"] == 1


def test_a_real_marker_never_waives_the_child_genuine_ban() -> None:
    result = check(page("# S", "", "<!-- density-exempt: real -- the brief's wording for this line -->",
                        "It is genuine."))
    assert fail_kinds(result) == ["child genuine"]
    assert result.counts == {"spaced dash": 0, "spaced dash exempted": 0, "real": 0, "real exempted": 1}


def test_real_in_a_bold_label_lead_in_is_not_counted() -> None:
    assert check(page("# P", "", "**Progress is real.** Keep going."), rel=PARENT).counts["real"] == 0
    assert check(page("# P", "", "- **Progress is real** -- keep going."), rel=PARENT).counts["real"] == 0
    with_dash = check(page("# P", "", "**It is real -- truly.** Keep going."), rel=PARENT)
    assert with_dash.counts["real"] == 1
    with_contrast = check(page("# P", "", "**It is real, not pretend.** Keep going."), rel=PARENT)
    assert with_contrast.counts["real"] == 1
    assert check(page("# P", "", "Keep going, it is **real**."), rel=PARENT).counts["real"] == 1


def test_a_table_cell_dash_is_printed_and_never_counted() -> None:
    result = check(page("# S", "", "## Goal", "", "| Prompt | Your answer |", "| --- | --- |",
                        "| Pick one -- any one | |"))
    assert result.devices == [] and result.fails == []
    assert advice_kinds(result) == ["table cell dash"]


def test_a_heading_dash_is_printed_with_its_test_class_and_never_counted() -> None:
    result = check(page("# S", "", "## Stop -- you are done"))
    assert result.devices == [] and result.fails == []
    assert advice_kinds(result) == ["heading dash"]
    assert "(t3-finite)" in result.advice[0].message


@pytest.mark.parametrize(("register", "prose_lines", "cap"), [
    ("child", 4, 1), ("child", 9, 1), ("child", 14, 2), ("child", 60, 8),
    ("parent", 0, 1), ("parent", 49, 8), ("builder", 7, 1), ("builder", 8, 2), ("builder", 400, 100),
])
def test_a_ratio_divides_rounds_down_then_takes_the_floor(register: str, prose_lines: int, cap: int) -> None:
    assert td.dash_cap(register, prose_lines) == cap


def test_two_dashes_in_one_sentence_are_one_device() -> None:
    pair = check(page("# P", "", "One -- like this -- two."), rel=PARENT)
    assert [d.paired for d in dashes(pair)] == [True]
    wrapped = check(page("# P", "", "One -- like", "this -- two."), rel=PARENT)
    assert [(d.paired, d.lines) for d in dashes(wrapped)] == [(True, (3, 4))]
    two = check(page("# P", "", "One -- two. Three -- four."), rel=PARENT)
    assert [d.paired for d in dashes(two)] == [False, False]


def test_a_block_quote_is_exempt_only_when_matching_marks_enclose_it() -> None:
    quotation = check(page("# P", "", "> \"Pick one -- any one.\""), rel=PARENT)
    assert quotation.devices == [] and quotation.prose_lines == 0
    callout = check(page("# P", "", "> Pick one -- any one."), rel=PARENT)
    assert len(dashes(callout)) == 1 and callout.prose_lines == 1
    mismatched = check(page("# P", "", "> \"Pick one -- any one.\u201d"), rel=PARENT)
    assert len(dashes(mismatched)) == 1


def test_a_marker_skips_blank_lines_and_comments_and_covers_a_block_quote() -> None:
    result = check(page("# P", "", "<!-- density-exempt: spaced dash -- the brief's wording -->", "",
                        "<!-- a note -->", "", "> Pick one -- any one.", "> It is here -- still."), rel=PARENT)
    assert [d.exempt_by for d in dashes(result)] == [3, 3]
    assert result.markers[0].scope_desc == "next block (lines 7-8)"


def test_a_marker_above_a_heading_covers_its_section() -> None:
    result = check(page("# P", "", "<!-- density-exempt: spaced dash -- the brief's wording -->", "## Rules", "",
                        "One -- two.", "", "### Detail", "", "Three -- four.", "", "## Other", "", "Five -- six."),
                   rel=PARENT)
    assert [d.exempt_by for d in dashes(result)] == [3, 3, None]


def test_a_line_that_prints_no_word_is_not_a_prose_line() -> None:
    result = check(page("# S", "", "- [ ]", "- [ ] Pack the map.", "- " + TICK + "npm ci" + TICK, "- Plain."))
    assert result.prose_lines == 2


# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------


def test_markers_are_read_by_the_recount_parser_and_scope() -> None:
    result = check(page("# P", "", "<!-- density-exempt: spaced dash -- the batch 1 brief's wording -->",
                        "- One -- two.", "- Three -- four.", "", "Five -- six."), rel=PARENT)
    marker = result.markers[0]
    assert (marker.lineno, marker.device, marker.scope_start, marker.scope_end, marker.problem) == (3, "spaced dash",
                                                                                                    4, 5, "")
    assert marker.exempted == [4, 5]
    assert [d.exempt_by for d in dashes(result)] == [3, 3, None]


@pytest.mark.parametrize("device", ["dash", "spaced dashes", "Real", "genuine", "trope-cap"])
def test_a_marker_for_any_other_device_is_refused(device: str) -> None:
    result = check(page("# P", "", f"<!-- density-exempt: {device} -- the brief's wording -->", "One -- two."),
                   rel=PARENT)
    assert fail_kinds(result) == ["marker"]
    assert "is not `spaced dash` or `real`" in result.fails[0].message


def test_an_x_not_y_marker_belongs_to_the_recount() -> None:
    result = check(page("# P", "", "<!-- density-exempt: X, not Y -- the brief's wording -->", "It is a map, not a list."),
                   rel=PARENT)
    assert result.markers == [] and result.fails == []


@pytest.mark.parametrize(("marker", "problem"), [
    ("<!-- density-exempt: spaced dash -- -->", "no reason"),
    ("<!-- density-exempt: spaced dash --- the brief's wording -->", "not parted by ' -- '"),
    ("<!-- density-exempt: spaced dash -- the spec's section 12 -->", "cites its source by number"),
    ("<!-- density-exempt: real -- step 2 of the brief -->", "cites its source by number"),
    ("<!-- density-exempt: spaced dash -- the brief's step 4, which this list lacks -->",
     "cites its source by number (\"brief's step 4\"); name the source instead"),
    ("<!-- density-exempt: spaced dash -- step 4 keeps its fixed wording -->",
     "a number names only an item of the numbered list the marker covers"),
])
def test_a_marker_with_no_reason_or_a_numbered_source_is_refused(marker: str, problem: str) -> None:
    result = check(page("# P", "", marker, "1. One -- two.", "2. Three."), rel=PARENT)
    assert fail_kinds(result) == ["marker"]
    assert problem in result.fails[0].message
    assert all(d.exempt_by is None for d in result.devices)


def test_a_marker_may_name_a_step_of_the_list_it_covers() -> None:
    result = check(page("# P", "", "<!-- density-exempt: spaced dash -- step 2 keeps its fixed wording -->",
                        "1. One.", "2. Three -- four."), rel=PARENT)
    assert result.fails == []
    assert [d.exempt_by for d in dashes(result)] == [3]


@pytest.mark.parametrize(("lines", "problem"), [
    (["One -- two. <!-- density-exempt: spaced dash -- the brief's wording -->"], "text shares its lines"),
    (["<!-- density-exempt: spaced dash -- the brief's wording --> <!-- a note -->", "One -- two."],
     "another comment shares its line"),
    (["- One -- two.", "", "  <!-- density-exempt: spaced dash -- the brief's wording -->", "  Three -- four."],
     "inside a block quote or a list item"),
    (["One -- two.", "", "<!-- density-exempt: spaced dash -- the brief's wording -->"], "covers nothing"),
])
def test_a_misplaced_marker_is_refused(lines: list[str], problem: str) -> None:
    result = check(page("# P", "", *lines), rel=PARENT)
    assert "marker" in fail_kinds(result)
    assert problem in " ".join(n.message for n in result.fails)
    assert all(d.exempt_by is None for d in result.devices)


TITLE_FIX = "put the marker above the paragraph, list, block quote or `##` section it is for"


def test_a_marker_above_the_page_title_is_refused() -> None:
    # Above the title a marker would cover the whole page: a per-file waiver.
    result = check(page("<!-- markdownlint-disable MD013 -->",
                        "<!-- density-exempt: spaced dash -- the brief's wording for this page -->", "", "# S", "",
                        "One -- two.", "", "## Goal", "", "Three -- four.", "", "## Steps", "", "Five -- six.", "",
                        "Seven -- eight."))
    assert result.markers[0].problem == td.xny.TITLE_MARKER_PROBLEM
    assert TITLE_FIX in result.markers[0].problem
    assert all(d.exempt_by is None for d in result.devices)
    assert sorted(set(fail_kinds(result))) == ["marker", "spaced dash file cap", "spaced dash section cap"]


def test_a_marker_above_a_section_under_the_title_is_accepted() -> None:
    marker = "<!-- density-exempt: spaced dash -- the brief's wording for these steps -->"
    result = check(page("# S", "", *filler(10), marker, "## Steps", "", "Five -- six.", "", "Seven -- eight."))
    assert result.fails == []
    assert result.markers[0].scope_desc == "section 'Steps' (lines 24-29)"
    assert [d.exempt_by for d in dashes(result)] == [23, 23]


def test_a_refused_marker_is_named_and_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, PARENT, page("# P", "", "<!-- density-exempt: spaced dash -- -->", "One -- two."))
    code, out = run(root, capsys=capsys)
    assert code == 1
    assert "marker line 3 [spaced dash] REFUSED (no reason after ' -- ')" in out


def test_every_marker_in_use_is_printed_with_its_scope_and_hits(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, PARENT, page("# P", "", "<!-- density-exempt: spaced dash -- the batch 1 brief's wording -->",
                             "One -- two.", "", *filler(3)))
    code, out = run(root, capsys=capsys)
    assert code == 0
    assert "marker line 3 [spaced dash] next block (lines 4-4); exempts lines [4]" in out
    assert "reason: the batch 1 brief's wording" in out


def test_a_marker_waives_a_count_and_never_a_test_or_a_ban(tmp_path: Path, capsys: Any) -> None:
    text = page("# S", "", "<!-- density-exempt: spaced dash -- the brief's wording -->",
                "Pick one -- you can change it later.", "",
                "<!-- density-exempt: real -- the brief's wording -->", "Hope is real, so studies show it.")
    result = check(text)
    assert result.counts["spaced dash"] == 0 and result.counts["spaced dash exempted"] == 1
    assert dashes(result)[0].test3 == "t3-finite"
    assert fail_kinds(result) == ["T100"]
    root = repository(tmp_path)
    write(root, PARENT, page("# P", "", "<!-- density-exempt: spaced dash -- the brief's wording -->",
                             "Pick one -- you can change it later."))
    _, out = run(root, capsys=capsys)
    assert "test 3 line 4 (t3-finite, exempted by the marker on line 3)" in out


def test_there_is_no_per_file_waiver() -> None:
    text = page("<!-- trope-cap: dash=18 -- every entry is a label -->", "# S", "", "One -- two.", "",
                "Three -- four.")
    assert fail_kinds(check(text)) == ["spaced dash file cap"]


# ---------------------------------------------------------------------------
# What is printed and never fails
# ---------------------------------------------------------------------------


def test_the_test_three_classes_are_printed_and_never_fail(tmp_path: Path, capsys: Any) -> None:
    assert td.test3_class(" you can change it later.") == "t3-finite"
    assert td.test3_class(" check the map.") == "t3-imperative"
    assert td.test3_class(" the big one.") == "t4-verbless"
    assert td.test3_class(" like this ", paired=True) == "t4-paired-aside"
    root = repository(tmp_path)
    write(root, PARENT, page("# P", "", "Pick one -- you can change it later.", "", *filler(4)))
    code, out = run(root, capsys=capsys)
    assert code == 0
    assert "test 3 line 3 (t3-finite)" in out


def test_contractions_and_banned_words_are_printed_and_never_fail(tmp_path: Path, capsys: Any) -> None:
    text = page("# S", "", "You are here and you do not stop.", "", "Earn a badge and go on a quest.")
    result = check(text)
    assert result.fails == []
    assert result.contractions == (2, 0)
    assert advice_kinds(result) == ["banned word", "banned word"]
    root = repository(tmp_path)
    write(root, "framework/sessions/phase_00_setup/97_words.md", text)
    code, out = run(root, capsys=capsys)
    assert code == 0
    assert "contractions 2 full : 0 contracted" in out
    assert "banned-word mention (gamification: 'badge')" in out


def test_a_spaced_dash_needs_space_the_page_wrote() -> None:
    assert len(dashes(check(page("# P", "", "Run " + TICK + "a" + TICK + " -- then stop."), rel=PARENT))) == 1
    assert dashes(check(page("# P", "", "Run " + TICK + "a" + TICK + "-- then stop."), rel=PARENT)) == []
    assert dashes(check(page("# P", "", "Run " + TICK + "a -- b" + TICK + " now."), rel=PARENT)) == []
    assert dashes(check(page("# P", "", "One --- two."), rel=PARENT)) == []
    assert dashes(check(page("# P", "", "One <!-- -- --> two."), rel=PARENT)) == []


def test_the_json_report_carries_every_page(tmp_path: Path, capsys: Any) -> None:
    root = repository(tmp_path)
    write(root, "docs/build/brief.md", page("# Brief", "", "One -- two."))
    code, out = run(root, "--format", "json", capsys=capsys)
    data = json.loads(out)
    assert code == 0
    assert data["totals"]["gated_pages"] == 1 and data["totals"]["records"] == 1
    assert data["pages"][0]["path"] == CHILD and data["records"][0]["path"] == "docs/build/brief.md"


# ---------------------------------------------------------------------------
# Grade report
# ---------------------------------------------------------------------------


def test_grade_changes_marks_only_a_rise() -> None:
    grades = {"easy": 3.0, "hard": 6.0}
    rows = td.grade_changes([("a.md", "easy", "hard"), ("b.md", "hard", "easy"), ("c.md", None, "hard")],
                            lambda text, rel: grades[text])
    assert [(r["path"], r["rose"], r["new_page"]) for r in rows] == [
        ("a.md", True, False), ("b.md", False, False), ("c.md", False, True)]


def git(root: Path, *args: str) -> str:
    """Run git in a test repository."""
    return subprocess.run(["git", "-C", str(root), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                           "-c", "commit.gpgsign=false", *args], check=True, capture_output=True, text=True).stdout


def test_the_grade_report_prints_a_rise_and_never_fails(tmp_path: Path, capsys: Any) -> None:
    rel = "framework/sessions/phase_00_setup/96_grades.md"
    easy = " ".join(["You pick a map. It is fun. You go on."] * 8)
    hard = " ".join([("Considering the comparative accessibility of interconnected transportation alternatives,"
                      " travelers frequently reconsider itineraries.")] * 8)
    write(tmp_path, rel, page("# Session", "", easy))
    write(tmp_path, PARENT, page("# Parent", "", easy))
    git(tmp_path, "init", "-q")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")
    base = git(tmp_path, "rev-parse", "HEAD").strip()
    write(tmp_path, rel, page("# Session", "", hard))
    write(tmp_path, PARENT, page("# Parent", "", hard))
    git(tmp_path, "commit", "-q", "-am", "harder")
    code, out = run(tmp_path, "--grade-report", base, capsys=capsys)
    assert code == 0
    assert f"GRADE ROSE {rel}:" in out
    assert PARENT not in out
    assert "1 changed child-facing page(s) scored" in out


def test_the_grade_report_fails_when_it_cannot_run(tmp_path: Path, capsys: Any) -> None:
    write(tmp_path, CHILD, page("# Session", "", "Plain."))
    git(tmp_path, "init", "-q")
    code = td.main([str(tmp_path), "--grade-report", "no-such-base"])
    assert code == 2
    assert "error:" in capsys.readouterr().err
