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


@pytest.mark.parametrize(
    "sentence",
    [
        "It's not a toy; it's a tool.",
        "It's not a toy, it's a tool.",
        "It isn't a test: it's practice.",
        "It isn't a test -- it's practice.",
        "It isn't a test — it's practice.",
        "This does not replace the notes; it is the map.",
        "If you're stuck, it's not a failure; it's a signal.",
    ],
)
def test_the_banned_shape_joined_into_one_sentence_is_a_candidate(sentence: str) -> None:
    assert ("banned", sentence) in kinds(sentence)


def test_a_condition_joined_to_a_claim_is_not_the_banned_shape() -> None:
    assert [k for k, _ in kinds("If some travelers are not reachable yet, that is fine.")] == []


def test_a_curly_apostrophe_negation_is_a_split_candidate() -> None:
    found = kinds("You move a block. You don’t start over.")
    assert ("split", "You move a block. → You don’t start over.") in found


def test_cannot_is_a_negation() -> None:
    found = kinds("Look it up. You cannot guess it.")
    assert ("split", "Look it up. → You cannot guess it.") in found


def test_opening_words_read_both_apostrophes_alike() -> None:
    assert cx.opening_words("It’s a tool.") == cx.opening_words("It's a tool.") == ["it's", "a"]


def test_a_pair_whose_two_sentences_both_negate_is_one_candidate() -> None:
    found = kinds("You do not need a plan. You do not need a map.")
    assert [k for k, _ in found].count("split") == 1


def test_a_sentence_wrapped_over_two_lines_is_read_whole() -> None:
    found = candidates("One line.\nChoose the map rather\nthan the list.")
    assert [(c.kind, c.text, c.lineno) for c in found] == [
        ("device", "Choose the map rather than the list.", 2),
    ]


@pytest.mark.parametrize(("text", "first"), [
    ("Use them as **starting points, not answers.** Read them first.", "Use them as **starting points, not answers.**"),
    ('He said "stop here." Then we went on.', 'He said "stop here."'),
    ("It is _a map, not a list._ Read it.", "It is _a map, not a list._"),
    ("(It is a map, not a list.) Read it.", "(It is a map, not a list.)"),
])
def test_a_sentence_keeps_its_closing_marks(text: str, first: str) -> None:
    assert cx.split_sentences(text)[0] == first


def test_a_key_is_the_sentence_as_the_page_prints_it() -> None:
    (found,) = candidates("It is **a map, not a list.** Read it.")
    assert found.key == "device|It is a map, not a list.|1"


def test_markup_that_prints_the_same_words_keeps_the_key() -> None:
    spellings = [
        "It is a map, not a list.",
        "It is **a map**, not a list.",
        "It is [a map](map.md), not a list.",
        "It is [a map][m], not a list.\n\n[m]: map.md",
        "It is a map, not a&nbsp;list.",
    ]
    assert {c.key for text in spellings for c in candidates(text)} == {"device|It is a map, not a list.|1"}


@pytest.mark.parametrize("sentence", [
    "It is a draft, _not a decision_.",
    "It is a draft, __not a decision__.",
    "It is a draft, _not_ a decision.",
])
def test_underscore_emphasis_does_not_hide_a_contrast(sentence: str) -> None:
    assert kinds(sentence) == [("device", "It is a draft, not a decision.")]


def test_underscore_emphasis_does_not_hide_a_negation() -> None:
    found = kinds("You move a block. You _don't_ start over.")
    assert ("split", "You move a block. → You don't start over.") in found


def test_an_underscore_inside_a_word_is_not_emphasis() -> None:
    assert cx.plain("a snake_case word, _stressed_") == "a snake_case word, stressed"


def test_a_code_span_that_crosses_a_line_break_is_skipped() -> None:
    assert kinds("Use `choose the map,\nnot the list` as literal syntax.") == []


def test_code_spans_pair_across_a_line_break() -> None:
    found = kinds("Use `x` then `y and\nz` here, not there `w`.")
    assert [k for k, _ in found] == ["device"]
    assert "here, not there" in found[0][1]


def test_a_comment_that_crosses_a_line_break_is_skipped() -> None:
    assert kinds("It is a map <!-- a note,\nnot a list --> for you.") == []


def test_a_comment_line_does_not_part_two_paragraphs() -> None:
    text = "You will change the plan. That is normal.\n\n<!-- a note -->\n**Never silently.** Tell them why."
    assert [k for k, _ in kinds(text)] == ["device"]


def test_a_comment_over_several_lines_does_not_part_two_paragraphs() -> None:
    text = "It's not a toy.\n\n<!-- a note that\nruns on -->\n\nIt's a tool."
    assert ("banned", "It's not a toy. → It's a tool.") in kinds(text)


@pytest.mark.parametrize(("sentence", "printed"), [
    ("Say \\`a map, not a list\\` aloud.", "Say `a map, not a list` aloud."),
    ("Say `a map, not a list`` aloud.", "Say `a map, not a list`` aloud."),
    ("Say ``a map, not a list` aloud.", "Say ``a map, not a list` aloud."),
])
def test_backticks_that_open_no_code_span_leave_the_prose(sentence: str, printed: str) -> None:
    assert kinds(sentence) == [("device", printed)]


def test_a_code_span_closes_only_on_a_run_of_its_own_length() -> None:
    assert kinds("Say ``a map, not `a` list`` aloud.") == []


@pytest.mark.parametrize(("page", "printed"), [
    ("It is a map, [not](other.md) a list.", "It is a map, not a list."),
    ("Choose the map rather [than](other.md) the list.", "Choose the map rather than the list."),
    ("It is a map, [not][ref] a list.\n\n[ref]: other.md", "It is a map, not a list."),
    ("It is a map, [not][] a list.\n\n[not]: other.md", "It is a map, not a list."),
])
def test_a_link_label_is_read_as_prose(page: str, printed: str) -> None:
    assert kinds(page) == [("device", printed)]


@pytest.mark.parametrize(("page", "printed"), [
    ("It is a map, [not] a list.\n\n[not]: other.md", "It is a map, not a list."),
    ("It is a map, [Not] a list.\n\n[not]: other.md", "It is a map, Not a list."),
])
def test_a_shortcut_reference_link_is_read_as_its_label(page: str, printed: str) -> None:
    # CommonMark matches a reference label without regard to case.
    assert kinds(page) == [("device", printed)]


@pytest.mark.parametrize("sentence", [
    'Read the [guide](a.md "Pick this, not that") first.',
    "Read the [guide](notes/a,not-b.md) first.",
    "See ![a map, not a list](m.png) here.",
])
def test_a_link_destination_title_or_image_is_not_prose(sentence: str) -> None:
    assert kinds(sentence) == []


@pytest.mark.parametrize("sentence", [
    "It can't be final; it's a draft.",
    "It won't be final; it's a draft.",
    "It couldn't be final; it's a draft.",
    "This could not be final; it is a draft.",
    "It shan't be final; it's a draft.",
    "You can't start over; you move a block.",
    "You won't start over; you move a block.",
])
def test_every_negated_auxiliary_opens_the_banned_shape(sentence: str) -> None:
    assert ("banned", sentence) in kinds(sentence)


def test_every_negated_auxiliary_is_read_by_the_inline_patterns() -> None:
    assert [k for k, _ in kinds("Pick the map, but you couldn't pick the list.")] == ["device"]


def test_a_release_is_keyed_with_the_sentence_that_follows() -> None:
    first = candidates("Write today's date. You do not have to fill every line. A few notes are enough.")
    second = candidates("Write today's date. You do not have to fill every line. Tomorrow is Tuesday.")
    assert [c.text for c in first if c.kind == "split"] == [
        "Write today's date. → You do not have to fill every line. → A few notes are enough."]
    assert {c.key for c in first}.isdisjoint({c.key for c in second})


def test_a_negation_that_is_not_a_release_keeps_its_pair() -> None:
    found = kinds("You move a block. You don't start over. It stays.")
    assert ("split", "You move a block. → You don't start over.") in found


def test_a_contrast_in_parentheses_is_a_candidate() -> None:
    assert kinds("Choose the map (not the list).") == [("device", "Choose the map (not the list).")]


def test_a_link_reference_definition_is_not_prose() -> None:
    assert kinds('[guide]: /guide "Choose the map, not the list."\n\nSee the [guide].') == []


def test_a_fence_opened_on_a_list_item_line_is_not_prose() -> None:
    text = "- ```text\n  a map, not a list\n  ```\n\nIt is a map, not a list."
    assert kinds(text) == [("device", "It is a map, not a list.")]


def test_an_indented_code_block_is_not_prose() -> None:
    assert kinds("Intro.\n\n    code, not prose\n") == []


def test_a_marker_skips_a_comment_over_several_lines() -> None:
    text = "<!-- density-exempt: X, not Y -- required -->\n<!-- note\ncontinues -->\n\nIt is a map, not a list."
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end) == (5, 5)


def test_an_unclosed_inline_comment_leaves_the_next_paragraph_visible() -> None:
    # CommonMark prints `Visible <!-- note` as text and the next paragraph as prose.
    text = "Visible <!-- note\n\nChoose the map, not the list.\n\n--> tail."
    assert ("device", "Choose the map, not the list.") in kinds(text)


def test_an_abbreviation_that_ends_a_sentence_ends_it() -> None:
    found = kinds("It isn't at 5 p.m. It's at 6 p.m.")
    assert ("banned", "It isn't at 5 p.m. → It's at 6 p.m.") in found


def test_an_abbreviation_that_leads_on_stays_in_its_sentence() -> None:
    assert cx.split_sentences("Pick a city, e.g. Kyoto, not a region.") == ["Pick a city, e.g. Kyoto, not a region."]


@pytest.mark.parametrize(("sentence", "printed"), [
    ("Choose the map rather&nbsp;than the list.", "Choose the map rather than the list."),
    ("Choose the map&#44; not the list.", "Choose the map, not the list."),
    ("Choose the map&comma; not the list.", "Choose the map, not the list."),
])
def test_a_character_reference_is_read_as_its_character(sentence: str, printed: str) -> None:
    assert kinds(sentence) == [("device", printed)]


@pytest.mark.parametrize("page", [
    "Choose the map rather\\\nthan the list.",
    "Choose the map rather  \nthan the list.",
])
def test_a_hard_line_break_is_read_as_a_line_break(page: str) -> None:
    found = candidates(page)
    assert [(c.kind, c.text, c.lineno) for c in found] == [("device", "Choose the map rather than the list.", 1)]


@pytest.mark.parametrize(("page", "printed"), [
    ("It is a map, \\*not\\* a list.", "It is a map, *not* a list."),
    ("It is a map\\, not a list.", "It is a map, not a list."),
    ("It is a map, <span>not</span> a list.", "It is a map, not a list."),
    ("It is a map, <!-- note --> not a list.", "It is a map, not a list."),
])
def test_an_escape_or_a_tag_is_read_as_the_page_prints_it(page: str, printed: str) -> None:
    assert kinds(page) == [("device", printed)]


def test_a_sentence_keeps_its_line_after_markup_over_a_line_break() -> None:
    page = "\n".join([
        "Type `a",
        "b` now. See [the guide](guide.md",
        '"Guide") here. Look at ![a map](map.png',
        '"Map") there.',
        "It is a map, not a list.",
    ])
    assert [(c.text, c.lineno) for c in candidates(page)] == [("It is a map, not a list.", 5)]


def test_the_run_stops_when_the_markdown_reader_cannot_start(tmp_path: Path, capsys: Any,
                                                             monkeypatch: Any) -> None:
    write(tmp_path, "framework/templates/a.md", "## A\n\nIt is a map, not a list.\n")
    monkeypatch.setattr(cx, "NODE", str(tmp_path / "no-such-node"))
    monkeypatch.setattr(cx, "read_blocks", cx.BlockReader())
    assert cx.main([str(tmp_path)]) == 3
    assert "Node.js" in capsys.readouterr().err


@pytest.mark.parametrize(("answer", "message"), [
    ('{"blocks": "no"}', "unexpected answer"),
    # The helper's own error is the message, so the report says what went wrong.
    ('{"error": "printed text has 1 lines for 2 source lines"}', r"^x-not-y-blocks\.js: printed text has 1 lines"),
])
def test_the_reader_refuses_an_answer_it_cannot_use(answer: str, message: str) -> None:
    class Pipe:
        def write(self, text: str) -> None:
            pass

        def flush(self) -> None:
            pass

        def readline(self) -> str:
            return answer + "\n"

    class Process:
        stdin = Pipe()
        stdout = Pipe()

        def poll(self) -> None:
            return None

    reader = cx.BlockReader()
    reader.process = cast(Any, Process())
    with pytest.raises(cx.ReadError, match=message):
        reader("Text.")


def test_a_page_the_reader_cannot_read_stops_the_run_and_is_named(tmp_path: Path, capsys: Any,
                                                                  monkeypatch: Any) -> None:
    class Refuse:
        def __call__(self, text: str) -> list:
            raise cx.ReadError("x-not-y-blocks.js: printed text has 1 lines for 2 source lines")

        def close(self) -> None:
            pass

    write(tmp_path, "framework/templates/a.md", "## A\n\nIt is a map, not a list.\n")
    monkeypatch.setattr(cx, "read_blocks", Refuse())
    assert cx.main([str(tmp_path)]) == 3
    err = capsys.readouterr().err
    assert "framework/templates/a.md: x-not-y-blocks.js: printed text has 1 lines" in err
    assert "npm ci" not in err


def test_a_marker_over_two_lines_is_read() -> None:
    (mk,) = scoped("<!-- density-exempt: X, not Y --\n  a reason on the next line -->\nIt is a map, not a list.")
    assert (mk.applies, mk.scope_start, mk.scope_end) == (True, 3, 3)


def test_a_block_quote_under_a_lead_in_line_is_its_own_block() -> None:
    assert kinds("**Plan A is off.**\n> Don't worry about it.") == []


def test_a_pair_does_not_reach_across_the_edge_of_a_block_quote() -> None:
    assert kinds("> Your job is to map it.\n\nMapping is not choosing.") == []


@pytest.mark.parametrize(("text", "suffix"), [
    ("Choose the map, not the list.", ""),
    ("> Choose the map, not the list.", "|block quote"),
    ('> "Choose the map, not the list."', "|quotation block quote"),
    ('> "Look first. Choose the map, not the list."', "|quotation block quote"),
    ("> Choose the map, not the list.\n>\n> — A parent", "|quotation block quote"),
    ("> 'Choose the map, not the list.'", "|quotation block quote"),
    ("> ‘Choose the map, not the list.’", "|quotation block quote"),
    ("> **‘Choose the map, not the list.’**", "|quotation block quote"),
    ("> Choose the map, not the list, for the kids'", "|block quote"),
])
def test_a_key_carries_the_quotation_context(text: str, suffix: str) -> None:
    (found,) = candidates(text)
    assert found.key.endswith("|1" + suffix)


@pytest.mark.parametrize("after", [
    "> Look first. Choose the map, not the list. Then go.",
    "Look first. Choose the map, not the list. Then go.",
])
def test_a_judgment_does_not_follow_a_sentence_out_of_a_quotation(tmp_path: Path, after: str) -> None:
    # The middle sentence reads the same with or without the quotation marks.
    write(tmp_path, "framework/templates/a.md", '## A\n\n> "Look first. Choose the map, not the list. Then go."\n')
    judged = judge_all(tmp_path, "no")
    write(tmp_path, "framework/templates/a.md", "## A\n\n" + after + "\n")
    (rep,) = cx.scan(tmp_path, judged, {})
    assert [c.judgment for c in rep.candidates] == [None]


# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------


def scoped(text: str) -> list[Any]:
    """Return the page's markers; parsing sets their scopes."""
    return cast(list, cx.parse_text(text).markers)


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


def test_a_marker_covers_a_whole_loose_list() -> None:
    text = "\n".join([
        "<!-- density-exempt: X, not Y -- required -->",
        "- first item",
        "",
        "- second item",
        "",
        "  more of the second item",
        "",
        "After the list.",
    ])
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end) == (2, 6)


def test_a_marker_over_a_list_stops_where_another_list_starts() -> None:
    text = "<!-- density-exempt: X, not Y -- required -->\n- first item\n\n1. a new list"
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end) == (2, 2)


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


@pytest.mark.parametrize("marker", [
    "<!-- density-exempt: X, not Y --  -->",
    "<!-- density-exempt: X, not Y -->",
])
def test_a_marker_without_a_reason_exempts_nothing(marker: str) -> None:
    (mk,) = scoped(marker + "\nIt is a map, not a list.")
    assert mk.applies is False
    assert mk.problem


def test_a_marker_without_a_reason_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\n<!-- density-exempt: X, not Y --  -->\nIt is a map, not a list.\n")
    assert run(root, judge_all(root), capsys) == 1


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


def test_two_sections_with_one_title_are_capped_apart(tmp_path: Path) -> None:
    text = "## Same\n\nIt is a map, not a list.\n\n## Same\n\nDraw it rather than fill it in.\n"
    write(tmp_path, "framework/parent_guide/a.md", text)
    row = summary_for(tmp_path, "framework/parent_guide/a.md", judge_all(tmp_path))
    assert [(r["section"], r["counted"], r["status"]) for r in row["sections"] if r["section"] == "Same"] == [
        ("Same", 1, "PASS"),
        ("Same", 1, "PASS"),
    ]


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
            for context in ("|block quote", "|quotation block quote"):
                rest = rest.removesuffix(context)
            assert rest.rsplit("|", 1)[1].isdigit()
            assert entry["judgment"] in cx.VALID_JUDGMENTS
            assert entry["reason"]


@pytest.mark.parametrize("path", [cx.DEFAULT_JUDGMENTS, cx.DEFAULT_REGISTERS])
def test_a_data_file_uses_two_space_indentation_and_no_comment_keys(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert raw == json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    assert not [k for k in data if k.startswith("_")]
    assert list(data) == sorted(data)


def test_the_registers_file_is_well_formed() -> None:
    data = cx.load_json(cx.DEFAULT_REGISTERS)
    for rel, entry in data.items():
        assert rel.endswith(".md")
        assert entry["register"] in cx.FILE_CAP
        assert entry["basis"]
