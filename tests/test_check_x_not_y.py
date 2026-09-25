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


def every_candidate(text: str) -> list[Any]:
    """Return every candidate the script finds in one page, each sentence's own included."""
    page = cx.parse_text(text)
    return cx.find_candidates("page.md", page.prose, text.split("\n"))


def candidates(text: str) -> list[Any]:
    """Return the candidates a negation word or a pattern gives in one page.

    Every other sentence also gets a candidate of its own (see the tests under
    "Every sentence is judged"). Most tests here are about the words and the
    patterns, so they leave those out.
    """
    return [c for c in every_candidate(text) if c.patterns[0] not in cx.SENTENCE_PATTERNS]


def kinds(text: str) -> list[tuple[str, str]]:
    """Return (kind, text) for every candidate in one page."""
    return [(c.kind, c.text) for c in candidates(text)]


def write(root: Path, rel: str, text: str) -> None:
    """Write one page under a test repository root."""
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def judge_all(root: Path, judgment: str = "device") -> dict:
    """Return judgments that record every candidate under `root` as `judgment`.

    A sentence's own candidate (one that holds no negation word and matches no
    pattern) is recorded as `no`, so a test page counts its words and patterns.
    """
    out: dict = {}
    for rep in cx.scan(root, {}, {}):
        out[rep.path] = {c.key: {"line": c.lineno, "reason": "test",
                                 "judgment": "no" if c.patterns[0] in cx.SENTENCE_PATTERNS else judgment}
                         for c in rep.candidates}
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
    # The break parts the two paragraphs, so the negation stands alone.
    assert kinds("One line.\n\n---\n\nDo not copy it.") == [("device", "Do not copy it.")]


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
    (alone,) = candidates("Not every station has an elevator.")
    assert "fragment" not in alone.patterns


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
    assert "banned" not in [k for k, _ in kinds("If some travelers are not reachable yet, that is fine.")]


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
    assert kinds("**Plan A is off.**\n> Don't worry about it.") == [("device", "Don't worry about it.")]


def test_a_pair_does_not_reach_across_the_edge_of_a_block_quote() -> None:
    assert kinds("> Your job is to map it.\n\nMapping is not choosing.") == [("device", "Mapping is not choosing.")]


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


@pytest.mark.parametrize("last", [
    "> — A parent",
    "> -- Session 05's script",
    "> ― A parent, after Session 05",
    "> — *A parent*",
    "> — 3 families in the pilot",
])
@pytest.mark.parametrize("layout", ["paragraph", "line"])
def test_a_named_attribution_closing_the_quote_makes_it_a_quotation(last: str, layout: str) -> None:
    joiner = "\n>\n" if layout == "paragraph" else "\n"
    (found,) = candidates("> Choose the map, not the list." + joiner + last)
    assert found.key.endswith("|quotation block quote")


@pytest.mark.parametrize("last", [
    "> -- and then check the route.",
    "> -- and then check the route",
    "> — because this matters.",
    "> — Then check the route.",
    "> — A parent!",
    "> — A parent who ran the first three sessions with us last spring",
    "> —",
])
@pytest.mark.parametrize("layout", ["paragraph", "line"])
def test_a_dash_led_line_of_prose_is_no_attribution(last: str, layout: str) -> None:
    # The style law exempts only text the page shows is borrowed, through
    # quotation marks or a named attribution; a dash-led sentence is prose.
    joiner = "\n>\n" if layout == "paragraph" else "\n"
    keys = [c.key for c in every_candidate("> Choose the map, not the list." + joiner + last)]
    assert keys
    assert all(k.endswith("|block quote") and not k.endswith("|quotation block quote") for k in keys)


def test_an_attribution_that_does_not_close_the_quote_is_no_attribution() -> None:
    keys = [c.key for c in every_candidate("> — A parent\n>\n> Choose the map, not the list.")]
    assert "device|Choose the map, not the list.|1|block quote" in keys
    assert not any(k.endswith("|quotation block quote") for k in keys)


def test_a_continuation_in_place_of_an_attribution_reopens_the_judgment(tmp_path: Path) -> None:
    write(tmp_path, "framework/templates/a.md", "## A\n\n> Choose the map, not the list.\n>\n> — A parent\n")
    judged = judge_all(tmp_path, "no")
    write(tmp_path, "framework/templates/a.md", "## A\n\n> Choose the map, not the list.\n>\n> -- and then check the route.\n")
    (rep,) = cx.scan(tmp_path, judged, {})
    assert [c.judgment for c in rep.candidates if c.text == "Choose the map, not the list."] == [None]


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
    # Every sentence's judgment reopens: the first sentence of the quotation
    # read `"Look first.`, and each other key carries the context.
    assert [c.judgment for c in rep.candidates] == [None, None, None]


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


@pytest.mark.parametrize("reason", [
    "the field spec 21.5 requires in every entry",
    "the AI safety rule (spec, Section 20)",
    "a standalone safety rule (specification line 4245)",
    "privacy rules (specification lines 4235-4237)",
    "the privacy rules (spec 24)",
    "the privacy rules (§ 24)",
    "the reachability fallback (21.8)",
    "the OQ-7 navigation rendering rules",
    "the reference rule AC-6-2 states",
    "supervision safety rule (batch 1 brief F6)",
    "the spending-money rule (B4, item 7)",
    "the floor warning the brief requires (item 2)",
])
def test_a_marker_that_cites_its_source_by_number_exempts_nothing(reason: str) -> None:
    # The style law's name-first rule: a built file names its source.
    (mk,) = scoped(f"<!-- density-exempt: X, not Y -- {reason} -->\nIt is a map, not a list.")
    assert mk.applies is False
    assert "by number" in mk.problem


@pytest.mark.parametrize("reason", [
    "the field the spec's Session Support Notes require in every entry",
    "the batch 1 brief's entry for this page",
    "the privacy rule for Session 02's profile fields",
    "the Checkpoint 4 booked-dates beat",
    "step 3's kid-sized Budget Band, on the Phases 0-2 path",
    "the sections of the spec that hold its privacy rules",
])
def test_a_marker_that_names_its_source_applies(reason: str) -> None:
    (mk,) = scoped(f"<!-- density-exempt: X, not Y -- {reason} -->\nIt is a map, not a list.")
    assert (mk.applies, mk.problem) == (True, "")


def test_another_devices_marker_is_not_read_for_its_source() -> None:
    (mk,) = scoped("<!-- density-exempt: spaced dash -- spec 21.5 -->\nText.")
    assert (mk.applies, mk.problem) == (False, "")


@pytest.mark.parametrize("reason", [
    "required content (Batch 1 brief lines 3330-3335)",
    "the batch 2 brief's line 412",
    "the rule on line 7 of the spec's entry",
    "the privacy page's lines 4-6",
])
def test_a_marker_that_cites_a_line_of_any_source_exempts_nothing(reason: str) -> None:
    (mk,) = scoped(f"<!-- density-exempt: X, not Y -- {reason} -->\nIt is a map, not a list.")
    assert mk.applies is False
    assert "by number" in mk.problem


@pytest.mark.parametrize("reason", [
    "the relay fallback in step 3 is required",
    "the contrasts are in rule 5 of the list below",
    "this list is where a child reads what counts toward the 13",
    "a timeline and its guidelines, from the batch 1 brief's entry for this page",
])
def test_a_step_a_rule_or_a_word_holding_line_is_not_a_numbered_source(reason: str) -> None:
    (mk,) = scoped(f"<!-- density-exempt: X, not Y -- {reason} -->\nIt is a map, not a list.")
    assert (mk.applies, mk.problem) == (True, "")


@pytest.mark.parametrize("text", [
    "> Intro.\n>\n> <!-- density-exempt: X, not Y -- required -->\n\nChoose the map, not the list.",
    "> <!-- density-exempt: X, not Y -- required -->\n\n## Rule\n\nChoose the map, not the list.",
    "- One.\n  <!-- density-exempt: X, not Y -- required -->\n- Pick the map, not the list.",
    "- One.\n  <!-- density-exempt: X, not Y -- required -->\n\nChoose the map, not the list.",
    "Intro.\n\n<!-- density-exempt: X, not Y -- required -->",
])
def test_a_marker_never_covers_a_block_beyond_its_container(text: str) -> None:
    (mk,) = scoped(text)
    assert (mk.scope_start, mk.scope_end, mk.applies) == (0, 0, False)
    assert mk.problem.startswith("covers nothing")


@pytest.mark.parametrize(("text", "scope"), [
    ("<!-- density-exempt: X, not Y -- required -->\n> Choose the map.\n> Not the list.", (2, 3)),
    ("> <!-- density-exempt: X, not Y -- required -->\n> Choose the map, not the list.", (2, 2)),
    ("- One.\n\n  <!-- density-exempt: X, not Y -- required -->\n\n  Choose the map, not the list.", (5, 5)),
    ("- One.\n\n  <!-- density-exempt: X, not Y -- required -->\n\n  - Pick the map, not the list.", (5, 5)),
])
def test_a_marker_covers_the_next_block_inside_its_container(text: str, scope: tuple[int, int]) -> None:
    (mk,) = scoped(text)
    assert ((mk.scope_start, mk.scope_end), mk.applies, mk.problem) == (scope, True, "")


def test_another_devices_marker_that_covers_nothing_is_not_a_problem() -> None:
    (mk,) = scoped("> <!-- density-exempt: spaced dash -- required -->\n\nText -- more text.")
    assert (mk.applies, mk.problem) == (False, "")


def test_a_marker_that_covers_nothing_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\n> <!-- density-exempt: X, not Y -- required -->\n\nIt is a map, not a list.\n")
    assert run(root, judge_all(root), capsys) == 1


def test_a_marker_that_cites_its_source_by_number_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\n<!-- density-exempt: X, not Y -- the spec's rule (spec 21.5) -->\n"
                               "It is a map, not a list.\n")
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


def test_the_data_files_pass_the_checks_the_script_runs_on_them() -> None:
    assert cx.load_judgments(cx.DEFAULT_JUDGMENTS)
    assert cx.load_registers(cx.DEFAULT_REGISTERS)


# ---------------------------------------------------------------------------
# The data files' schemas and the script's own checks agree
# ---------------------------------------------------------------------------

SCHEMAS = SCRIPT_PATH.parents[2] / "schemas"
LOADERS = {"x-not-y-judgments": "load_judgments", "x-not-y-registers": "load_registers"}
SCHEMA_EXAMPLES = sorted((name, side, path) for name in LOADERS for side in ("valid", "invalid")
                         for path in (SCHEMAS / "examples" / name / side).glob("*.json"))


def test_each_data_file_has_a_schema_with_valid_and_invalid_examples() -> None:
    for name in LOADERS:
        assert (SCHEMAS / f"{name}.schema.json").is_file()
        assert {side for n, side, _ in SCHEMA_EXAMPLES if n == name} == {"valid", "invalid"}


@pytest.mark.parametrize(("name", "side", "path"), SCHEMA_EXAMPLES,
                         ids=[f"{n}/{s}/{p.name}" for n, s, p in SCHEMA_EXAMPLES])
def test_the_script_reads_each_schema_example_as_the_schema_does(name: str, side: str, path: Path) -> None:
    # tests/test_schema_examples.py holds each example to the schema; this holds
    # it to the script's loader, so the two cannot drift apart unseen.
    load = getattr(cx, LOADERS[name])
    if side == "valid":
        assert load(path)
    else:
        with pytest.raises(cx.DataError):
            load(path)


def test_the_schemas_name_the_values_the_script_accepts() -> None:
    judgments = json.loads((SCHEMAS / "x-not-y-judgments.schema.json").read_text(encoding="utf-8"))
    registers = json.loads((SCHEMAS / "x-not-y-registers.schema.json").read_text(encoding="utf-8"))
    entry = judgments["$defs"]["judgment"]
    assert set(entry["properties"]["judgment"]["enum"]) == cx.VALID_JUDGMENTS
    assert set(entry["required"]) == {"line", "judgment", "reason"}
    fields = registers["additionalProperties"]
    assert set(fields["properties"]["register"]["enum"]) == set(cx.FILE_CAP)
    assert set(fields["required"]) == {"register", "basis"}
    # The key pattern is the script's, with `[\s\S]` for its DOTALL `.`.
    key = judgments["additionalProperties"]["propertyNames"]["pattern"]
    assert key == cx.JUDGMENT_KEY_RE.pattern.replace(r"\|.+\|", r"\|[\s\S]+\|")
    assert judgments["$defs"]["pagePath"]["pattern"] == registers["propertyNames"]["pattern"]


def data_run(tmp_path: Path, capsys: Any, judgments: str | None = None, registers: str | None = None) -> tuple[int, str]:
    """Run main() on one child page, with data files written as given; return the exit code and stderr."""
    write(tmp_path, "framework/templates/a.md", "## A\n\nIt is a map, not a list.\n")
    jpath, rpath = tmp_path / "judgments.json", tmp_path / "registers.json"
    jpath.write_text(judgments if judgments is not None else json.dumps(judge_all(tmp_path)), encoding="utf-8")
    rpath.write_text(registers if registers is not None else "{}", encoding="utf-8")
    code = cast(int, cx.main([str(tmp_path), "--judgments", str(jpath), "--registers", str(rpath)]))
    return code, capsys.readouterr().err


@pytest.mark.parametrize(("registers", "message"), [
    ('{"framework/templates/a.md": {"register": "chil", "basis": "x"}}', "register 'chil'"),
    ('{"framework/templates/a.md": {"register": "child"}}', "exactly `register` and `basis`"),
    ('{"framework/templates/a.md": {"regsiter": "parent", "basis": "x"}}', "exactly `register` and `basis`"),
    ('{"framework/templates/a.md": "child"}', "exactly `register` and `basis`"),
    ('{"framework/templates/a.md": {"register": "child", "basis": " "}}', "the basis is empty"),
    ('{"framework/templates/a": {"register": "child", "basis": "x"}}', "is not a .md page path"),
    ('["framework/templates/a.md"]', "one object of pages"),
    ('{"framework/templates/a.md": ', "registers.json"),
])
def test_a_registers_entry_the_script_cannot_use_stops_the_run(tmp_path: Path, capsys: Any, registers: str,
                                                                 message: str) -> None:
    code, err = data_run(tmp_path, capsys, registers=registers)
    assert code == 2
    assert message in err


@pytest.mark.parametrize(("entry", "message"), [
    ('{"line": 3, "judgment": "devcie", "reason": "x"}', "judgment 'devcie'"),
    ('{"line": 3, "judgment": "device", "reason": ""}', "the reason is empty"),
    ('{"line": 0, "judgment": "device", "reason": "x"}', "a whole number from 1"),
    ('{"line": "3", "judgment": "device", "reason": "x"}', "a whole number from 1"),
    ('{"line": 3, "judgment": "device"}', "exactly `line`, `judgment` and `reason`"),
    ('"device"', "exactly `line`, `judgment` and `reason`"),
])
def test_a_judgment_the_script_cannot_use_stops_the_run(tmp_path: Path, capsys: Any, entry: str,
                                                         message: str) -> None:
    judgments = '{"framework/templates/a.md": {"device|It is a map, not a list.|1": %s}}' % entry
    code, err = data_run(tmp_path, capsys, judgments=judgments)
    assert code == 2
    assert message in err


def test_a_judgment_key_of_another_form_stops_the_run(tmp_path: Path, capsys: Any) -> None:
    judgments = '{"framework/templates/a.md": {"It is a map, not a list.": {"line": 3, "judgment": "no", "reason": "x"}}}'
    code, err = data_run(tmp_path, capsys, judgments=judgments)
    assert code == 2
    assert "<kind>|<sentence text>|<occurrence>" in err


def test_data_files_the_script_can_use_pass(tmp_path: Path, capsys: Any) -> None:
    registers = '{"framework/templates/a.md": {"register": "parent", "basis": "test"}}'
    assert data_run(tmp_path, capsys, registers=registers)[0] == 0


def test_a_data_file_that_is_not_utf_8_stops_the_run(tmp_path: Path, capsys: Any) -> None:
    write(tmp_path, "framework/templates/a.md", "## A\n\nText.\n")
    (tmp_path / "registers.json").write_bytes(b'{"\xff": 1}')
    assert cx.main([str(tmp_path), "--registers", str(tmp_path / "registers.json")]) == 2
    assert "registers.json" in capsys.readouterr().err


def test_a_page_that_is_not_utf_8_stops_the_run_and_is_named(tmp_path: Path, capsys: Any) -> None:
    write(tmp_path, "framework/templates/a.md", "## A\n\nIt is a map, not a list.\n")
    (tmp_path / "framework/templates/b.md").write_bytes(b"## B\n\nA map \xff.\n")
    assert cx.main([str(tmp_path)]) == 3
    err = capsys.readouterr().err
    assert "framework/templates/b.md" in err
    assert "npm ci" not in err


# ---------------------------------------------------------------------------
# A key holds every sentence its test reads
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("before", "after"), [
    # A fragment counts only after a claim, so the claim is in its key.
    ("Write a city. Not a failure.", "A rough guess may be wrong. Not a failure."),
    # A short negation is judged with the claim before it.
    ("You move a block. You don't start over.", "You stay here. You don't start over."),
    # A bare "instead" is read against the negation before it.
    ("Do not guess. Look it up instead.", "Do not rush. Look it up instead."),
    # A release counts only when the sentence after it recasts the thing.
    ("Write the date. You do not have to fill every line. A few notes are enough.",
     "Write the date. You do not have to fill every line. Tomorrow is Tuesday."),
    # A negation that opens a paragraph is judged with the claim after it.
    ("Do not guess.\n\nLook it up.", "Do not guess.\n\nAsk a grown-up."),
    # The banned pair is judged as two sentences.
    ("It's not a toy. It's a tool.", "It's not a toy. It's a map."),
])
def test_changing_a_sentence_a_test_reads_changes_the_key(before: str, after: str) -> None:
    old = {c.key for c in candidates(before)}
    new = {c.key for c in candidates(after)}
    assert old
    assert old.isdisjoint(new)


def test_a_fragment_is_keyed_with_the_claim_before_it() -> None:
    assert kinds("Write a city. Not a failure.") == [("device", "Write a city. → Not a failure.")]


# ---------------------------------------------------------------------------
# Containers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("page", [
    "- One.\n\n  It isn't a toy.\n\nIt's a tool.",
    "1. One.\n\n   It isn't a toy.\n\nIt's a tool.",
    "- ```\n  x\n  ```\n\n  It isn't a toy.\n\nIt's a tool.",
    "> - One.\n>\n>   It isn't a toy.\n>\n> It's a tool.",
    "- One.\n\n  - Two.\n\n    It isn't a toy.\n\n  It's a tool.",
    "It isn't a toy.\n\n- It's a tool.",
    "- It isn't a toy.\n- It's a tool.",
    "- It isn't a toy.\n\n- It's a tool.",
    "- One.\n\n  It isn't a toy.\n\n- It's a tool.",
])
def test_no_pair_crosses_the_edge_of_a_list_or_an_item(page: str) -> None:
    assert [c.text for c in candidates(page) if "It's a tool." in c.text] == []


def test_two_block_quotes_stay_apart() -> None:
    assert kinds("> It isn't a toy.\n\n> It's a tool.") == [("device", "It isn't a toy.")]
    (found,) = candidates('> "Look first.\n\n> Choose the map, not the list."')
    assert found.key.endswith("|1|block quote")


def test_two_paragraphs_of_one_list_item_pair() -> None:
    found = kinds("- You move a block.\n\n  You don't start over.")
    assert ("split", "You move a block. → You don't start over.") in found


@pytest.mark.parametrize("page", [
    '> "Look first.\n>\n> > An aside.\n>\n> Choose the map, not the list."',
    '> "Look first.\n>\n> > Choose the map, not the list."',
    '> - "Look first.\n>\n> Choose the map, not the list."',
])
def test_a_block_quote_is_a_quotation_through_the_blocks_inside_it(page: str) -> None:
    (found,) = candidates(page)
    assert found.key.endswith("|quotation block quote")


# ---------------------------------------------------------------------------
# Abbreviations that can end a sentence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("text", "sentences"), [
    ("No. Use the map.", ["No.", "Use the map."]),
    ("Is it open? No. Check again.", ["Is it open?", "No.", "Check again."]),
    ("Take bus No. 5 to the park.", ["Take bus No. 5 to the park."]),
    ("Ask Dr. Kim first.", ["Ask Dr. Kim first."]),
])
def test_no_ends_a_sentence_unless_a_number_follows(text: str, sentences: list[str]) -> None:
    assert cx.split_sentences(text) == sentences


def test_a_paragraph_that_opens_with_no_is_a_split_candidate() -> None:
    assert kinds("No. Use the map.") == [("split", "No. → Use the map.")]


# ---------------------------------------------------------------------------
# Every spelling of a negation reads alike
# ---------------------------------------------------------------------------

NEGATION_SPELLINGS = [
    ["I am not", "I'm not", "I’m not"],
    ["it is not", "it isn't", "it's not", "it’s not"],
    ["we are not", "we aren't", "we're not"],
    ["we have not", "we haven't", "we've not", "we’ve not"],
    ["you will not", "you won't", "you'll not"],
    ["you would not", "you wouldn't", "you'd not"],
    ["they are never", "they're never"],
]


@pytest.mark.parametrize("template", [
    "Pick the map, {} picking the list.",
    "Pick the map; {} picking the list.",
    "Pick the map -- {} picking the list.",
    "Pick the map, but {} picking the list.",
])
@pytest.mark.parametrize("spellings", NEGATION_SPELLINGS, ids=[s[0] for s in NEGATION_SPELLINGS])
def test_every_spelling_of_a_negation_is_read_alike(template: str, spellings: list[str]) -> None:
    found = [[(c.kind, c.patterns) for c in candidates(template.format(s))] for s in spellings]
    assert found[0]
    assert all(f == found[0] for f in found)


@pytest.mark.parametrize("pair", [
    ["I am not the expert. I am the helper.", "I'm not the expert. I'm the helper.",
     "I’m not the expert. I’m the helper.", "I'm not the expert; I'm the helper."],
    ["We have never had a plan. We have a list.", "We've never had a plan. We've a list."],
    ["You will not finish it. You will start it.", "You'll not finish it. You'll start it."],
    ["You would not guess it. You would look it up.", "You'd not guess it. You'd look it up."],
    ["The kit is not a toy. It is a tool.", "The kit isn't a toy. It'll be a tool."],
], ids=["I'm", "we've", "you'll", "you'd", "it'll"])
def test_every_contraction_opens_or_closes_the_banned_shape(pair: list[str]) -> None:
    for text in pair:
        assert "banned" in [k for k, _ in kinds(text)], text


def test_a_contracted_not_reads_as_not_before_but() -> None:
    assert [k for k, _ in kinds("It isn't a map but a list.")] == ["device"]


def test_a_contracted_release_is_keyed_with_the_sentence_after_it() -> None:
    found = kinds("Write the date. It's not required to fill every line. A few notes are enough.")
    assert ("split", "Write the date. → It's not required to fill every line. → A few notes are enough.") in found


# ---------------------------------------------------------------------------
# The device's name in a marker
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["X, not Y", "X-not-Y", "x-not-y"])
def test_the_documented_names_exempt(name: str) -> None:
    (mk,) = scoped(f"<!-- density-exempt: {name} -- required -->\nIt is a map, not a list.")
    assert (mk.applies, mk.problem) == (True, "")


@pytest.mark.parametrize("name", ["xnoty", "X not Y", "X, not-y", "x, not y", "X ,not Y"])
def test_another_spelling_of_the_name_exempts_nothing_and_is_named(name: str) -> None:
    (mk,) = scoped(f"<!-- density-exempt: {name} -- required -->\nIt is a map, not a list.")
    assert mk.applies is False
    assert "not `X, not Y`" in mk.problem


def test_another_device_is_not_a_problem() -> None:
    (mk,) = scoped("<!-- density-exempt: spaced dash -- required -->\nIt is a map -- a list.")
    assert (mk.applies, mk.problem) == (False, "")


def test_a_misspelled_name_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\n<!-- density-exempt: X not Y -- required -->\nIt is a map, not a list.\n")
    assert run(root, judge_all(root), capsys) == 1


# ---------------------------------------------------------------------------
# Negation words and where they sit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("page", "text"), [
    ("Never guess. Look it up.", "Never guess. → Look it up."),
    ("Not a list. Use a map.", "Not a list. → Use a map."),
    ("No. Use the map.", "No. → Use the map."),
    ("Nothing is booked yet. Your plan is a draft.", "Nothing is booked yet. → Your plan is a draft."),
    ("None of this is final. It is a draft.", "None of this is final. → It is a draft."),
    ("Nobody books alone. A grown-up books.", "Nobody books alone. → A grown-up books."),
    ("No one books alone. A grown-up books.", "No one books alone. → A grown-up books."),
    ("Neither city is wrong. Both are fine.", "Neither city is wrong. → Both are fine."),
    ("It goes nowhere. Keep it in the binder.", "It goes nowhere. → Keep it in the binder."),
])
def test_an_opening_negation_before_its_recast_is_a_split_candidate(page: str, text: str) -> None:
    assert ("split", text) in kinds(page)


@pytest.mark.parametrize("sentence", [
    "Do not pick the list; choose the map.",
    "Never guess; check the source.",
    "Do not pick the list: choose the map.",
    "Never guess -- check the source.",
    "Never guess — check the source.",
    "Nothing here is final; it is a draft.",
])
def test_a_negation_before_a_joiner_is_a_candidate(sentence: str) -> None:
    found = candidates(sentence)
    assert [(c.kind, c.text) for c in found if "not-then-joiner" in c.patterns] == [("device", sentence)]


def test_a_comma_is_not_a_joiner_for_a_negation_before_it() -> None:
    (found,) = candidates("If you don't know, ask an adult.")
    assert "not-then-joiner" not in found.patterns


NEGATION_FORMS = ["not", "never", "no", "nor", "none", "nothing", "nobody", "no one", "nowhere", "neither",
                  "cannot", "n't", "without"]
NEGATION_SENTENCES = {
    "not": "It is not the list.", "never": "It never was the list.", "no": "It has no list.",
    "nor": "Nor is it the list.", "none": "None of it is the list.", "nothing": "Nothing here is the list.",
    "nobody": "Nobody wants the list.", "no one": "No one wants the list.", "nowhere": "The list goes nowhere.",
    "neither": "Neither one is the list.", "cannot": "It cannot be the list.", "n't": "It isn't the list.",
    "without": "It works without the list.",
}


@pytest.mark.parametrize("word", NEGATION_FORMS)
def test_every_negation_word_next_to_a_claim_is_a_candidate(word: str) -> None:
    negation = NEGATION_SENTENCES[word]
    after = [c.text for c in candidates("Choose the map. " + negation)]
    before = [c.text for c in candidates(negation + " Choose the map.")]
    assert "Choose the map. → " + negation in after
    assert negation + " → Choose the map." in before


def test_a_long_negation_sentence_next_to_a_claim_is_a_candidate() -> None:
    long = ("AI may help you brainstorm or organize your notes for a session, and it is never the source of a fact "
            "you write down in your plan.")
    assert ("split", "Use two sources. → " + long) in kinds("Use two sources. " + long)


@pytest.mark.parametrize("page", [
    "A filter reduces exposure without removing it.",
    "- A filter reduces exposure without removing it.",
    "> A filter reduces exposure without removing it.",
    "Intro.\n\n- A filter reduces exposure without removing it.\n- Keep the list.",
    "One line.\n\n---\n\nA filter reduces exposure without removing it.",
])
def test_a_negation_sentence_with_no_neighbor_is_a_candidate_keyed_alone(page: str) -> None:
    found = [(c.kind, c.text) for c in candidates(page) if "without" in c.text]
    assert found == [("device", "A filter reduces exposure without removing it.")]


@pytest.mark.parametrize("word", NEGATION_FORMS)
def test_every_negation_word_in_a_sentence_alone_is_a_candidate(word: str) -> None:
    assert kinds("- " + NEGATION_SENTENCES[word]) == [("device", NEGATION_SENTENCES[word])]


@pytest.mark.parametrize("page", ["## A filter without a guard", "| A filter without a guard |\n| --- |"])
def test_a_heading_or_a_table_cell_is_still_not_prose(page: str) -> None:
    assert every_candidate(page) == []


# ---------------------------------------------------------------------------
# Text an HTML block shows
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("page", "line"), [
    ("<!-- note --> Choose the map, not the list.", 1),
    ("<!-- note\ncontinues --> Choose the map, not the list.", 2),
    ("<!-- a --><!-- b --> Choose the map, not the list.", 1),
    ("<?x y?> Choose the map, not the list.", 1),
    ("<!X decl> Choose the map, not the list.", 1),
    ("<![CDATA[x]]> Choose the map, not the list.", 1),
    ("Intro.\n\n<!-- note --> Choose the map, not the list.", 3),
])
def test_text_after_what_an_html_block_hides_is_read(page: str, line: int) -> None:
    assert [(c.kind, c.text, c.lineno) for c in candidates(page)] == [
        ("device", "Choose the map, not the list.", line)]


def test_text_an_html_block_shows_is_read_with_its_references_decoded() -> None:
    assert kinds("<!-- note --> Choose the map&#44; not the list.") == [("device", "Choose the map, not the list.")]


def test_an_html_block_that_shows_text_next_to_a_tag_fails_the_run(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\n<div>Choose the map, not the list.</div>\n")
    assert cx.parse_text("<div>Choose the map, not the list.</div>").unread_html == [1]
    code = cx.main([str(root), "--judgments", str(tmp_path / "none.json"), "--registers", str(tmp_path / "none.json")])
    assert code == 1
    assert "UNREAD HTML line 3" in capsys.readouterr().out


def test_a_marker_that_shares_its_line_with_text_exempts_nothing_and_is_named() -> None:
    page = cx.parse_text("<!-- density-exempt: X, not Y -- required --> Choose the map, not the list.")
    assert [(m.applies, m.problem != "") for m in page.markers] == [(False, True)]


def test_a_block_of_comments_still_shows_nothing() -> None:
    assert kinds("<!-- a note -->\n<!-- another -->") == []


# ---------------------------------------------------------------------------
# A marker inside a line of text
# ---------------------------------------------------------------------------

INLINE_MARKER = "<!-- density-exempt: X, not Y -- required -->"


@pytest.mark.parametrize(("page", "line"), [
    (f"Visible text. {INLINE_MARKER}", 1),
    (f"Visible text,\nand more. {INLINE_MARKER}", 2),
    (f"- A list item. {INLINE_MARKER}", 1),
    (f"> A callout. {INLINE_MARKER}", 1),
    (f"[A link {INLINE_MARKER} label](x.md) here.", 1),
    (f"## A heading {INLINE_MARKER}\n\nChoose the map, not the list.", 1),
    (f"| A | B |\n| --- | --- |\n| a cell {INLINE_MARKER} | b |", 3),
    (f"Visible text. <!-- density-exempt: X-not-Y -- old name -->", 1),
])
def test_a_marker_inside_a_line_of_text_exempts_nothing_and_is_named(page: str, line: int) -> None:
    markers = cx.parse_text(page).markers
    assert [(m.lineno, m.applies, m.problem) for m in markers] == [
        (line, False, "text shares its lines; put the marker on a line of its own")]


@pytest.mark.parametrize("page", [
    f"Visible text `{INLINE_MARKER}` shown in a code span.",
    "Visible text. <!-- density-exempt: spaced dash -- another device's marker -->",
    "Visible text. <!-- a note -->",
])
def test_a_code_span_or_another_comment_inside_a_line_is_no_marker(page: str) -> None:
    assert cx.parse_text(page).markers == []


def test_an_audience_marker_inside_a_line_is_read() -> None:
    assert cx.parse_text("Words for grown-ups. <!-- audience: parent -->").audience == "parent"


def test_a_marker_inside_a_line_fails_the_run_and_covers_nothing(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, f"## A\n\nChoose the map, not the list. {INLINE_MARKER}\n")
    judgments = judge_all(root)
    assert summary_for(root, "framework/templates/a.md", judgments)["counted"] == 1
    jpath = tmp_path / "judgments.json"
    jpath.write_text(json.dumps(judgments), encoding="utf-8")
    assert cx.main([str(root), "--judgments", str(jpath), "--registers", str(tmp_path / "none.json")]) == 1
    assert "EXEMPTS NOTHING (text shares its lines" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# Regions under deeper headings
# ---------------------------------------------------------------------------

CONTRAST = "Choose the map, not the list."


@pytest.mark.parametrize(("page", "region"), [
    (f"## Parent Notes\n\nA note.\n\n### Coaching\n\n{CONTRAST}", "parent notes"),
    (f"## Parent Notes\n\n### Coaching\n\n#### A script\n\n{CONTRAST}", "parent notes"),
    (f"## Parent Notes\n\n### Coaching\n\n## Next\n\n{CONTRAST}", "main"),
    (f"## Parent Notes\n\n# A new page part\n\n{CONTRAST}", "main"),
    (f"## Steps\n\n### For parents\n\n{CONTRAST}", "parent notes"),
    (f"## Steps\n\n### For parents\n\nA note.\n\n### Your turn\n\n{CONTRAST}", "main"),
    (f"**For parents:**\n\n- Status: Core\n\n{CONTRAST}", "for-parents strip"),
    # The strip runs to the next heading of any level, as check-session-structure.py reads it.
    (f"**For parents:**\n\n- Status: Core\n\n### Before you start\n\n{CONTRAST}", "main"),
])
def test_a_region_lasts_while_its_heading_is_open(page: str, region: str) -> None:
    (found,) = candidates(page)
    assert found.region == region


def test_a_subheading_in_parent_notes_keeps_the_parent_register(tmp_path: Path) -> None:
    write(tmp_path, "framework/templates/a.md", f"## Parent Notes\n\nA note.\n\n### Coaching\n\n{CONTRAST}\n")
    row = summary_for(tmp_path, "framework/templates/a.md", judge_all(tmp_path))
    assert [i["register"] for i in row["instances"]] == ["parent"]


# ---------------------------------------------------------------------------
# Where a sentence starts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("text", "sentences"), [
    ("Do not guess. ✅ Look it up.", ["Do not guess.", "✅ Look it up."]),
    ("It's not a toy. Élodie calls it a tool.", ["It's not a toy.", "Élodie calls it a tool."]),
    ("It isn't a toy. Ōsaka is next.", ["It isn't a toy.", "Ōsaka is next."]),
    ("Do not guess. «Look it up.»", ["Do not guess.", "«Look it up.»"]),
    ("Do not guess. ¿Why not?", ["Do not guess.", "¿Why not?"]),
    ("Do not guess. • Look it up.", ["Do not guess.", "• Look it up."]),
    ("Pick a city, e.g. kyoto.", ["Pick a city, e.g. kyoto."]),
    ("Meet at 5 p.m. on Monday.", ["Meet at 5 p.m. on Monday."]),
    ("Done. 🙂 and then some.", ["Done. 🙂 and then some."]),
])
def test_a_sentence_starts_at_any_letter_that_is_not_lower_case(text: str, sentences: list[str]) -> None:
    assert cx.split_sentences(text) == sentences


def test_a_negation_before_an_emoji_sentence_is_a_candidate() -> None:
    assert ("split", "Do not guess. → ✅ Look it up.") in kinds("Do not guess. ✅ Look it up.")


# ---------------------------------------------------------------------------
# JSON the data files may not hold
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(("judgments", "message"), [
    ('{"framework/templates/a.md": {"device|It is a map, not a list.|1": {"line": 3, "judgment": "device", '
     '"reason": "x"}, "device|It is a map, not a list.|1": {"line": 3, "judgment": "no", "reason": "y"}}}',
     "duplicate key 'device|It is a map, not a list.|1'"),
    ('{"framework/templates/a.md": {}, "framework/templates/a.md": {}}', "duplicate key 'framework/templates/a.md'"),
    ('{"framework/templates/a.md": {"device|It is a map, not a list.|1": {"line": 3, "line": 4, '
     '"judgment": "no", "reason": "y"}}}', "duplicate key 'line'"),
    ('{"framework/templates/a.md": {"device|It is a map, not a list.|1": {"line": NaN, "judgment": "no", '
     '"reason": "y"}}}', "NaN is not JSON"),
])
def test_a_duplicate_key_or_a_constant_json_does_not_allow_stops_the_run(tmp_path: Path, capsys: Any,
                                                                            judgments: str, message: str) -> None:
    code, err = data_run(tmp_path, capsys, judgments=judgments)
    assert code == 2
    assert message in err


def test_a_duplicate_key_in_the_registers_file_stops_the_run(tmp_path: Path, capsys: Any) -> None:
    registers = '{"framework/templates/a.md": {"register": "builder", "basis": "x", "register": "child"}}'
    code, err = data_run(tmp_path, capsys, registers=registers)
    assert code == 2
    assert "duplicate key 'register'" in err


# ---------------------------------------------------------------------------
# Every sentence is judged
# ---------------------------------------------------------------------------


def judged_sentence(c: Any) -> str:
    """Return the sentence a candidate judges: the one its test flagged."""
    parts = c.text.split(cx.ARROW)
    if any(p.endswith("before-claim") for p in c.patterns):
        return parts[0]
    if "release-then-recast" in c.patterns:
        return parts[1]
    return parts[-1]


EVERY_SENTENCE_PAGES = [
    "Plan the day. Avoid the list; choose the map. Pick one.",
    "Never guess. Look it up. Then write it down.",
    "Prefer official sources for facts. A museum's own website beats a random blog.",
    "- One item.\n- Choose the map, not the list.\n\n> A callout. It is not a toy.\n\nDo not guess. Look.",
    "Write the date. You do not have to fill every line. A few notes are enough.",
    "Break a rule gently. Not a failure. Keep going.",
    "It's not a toy. It's a tool. Use it.",
]


@pytest.mark.parametrize("page", EVERY_SENTENCE_PAGES)
def test_every_sentence_is_the_sentence_judged_in_one_candidate(page: str) -> None:
    printed = cx.parse_text(page)
    sentences = [s for para in cx.paragraphs(printed.prose) for s, _ in cx.paragraph_sentences(para)]
    judged = [judged_sentence(c) for c in every_candidate(page) if c.kind != "banned"]
    assert sorted(judged) == sorted(sentences)


@pytest.mark.parametrize(("page", "expected"), [
    ("Plan the day. Avoid the list; choose the map.",
     [("device", "Plan the day.", "sentence-alone"),
      ("split", "Plan the day. → Avoid the list; choose the map.", "sentence-after-claim")]),
    ("Prefer official sources for facts. A museum's own website beats a random blog.",
     [("device", "Prefer official sources for facts.", "sentence-alone"),
      ("split", "Prefer official sources for facts. → A museum's own website beats a random blog.",
       "sentence-after-claim")]),
    # The pair is keyed from `Never guess.`, so `Look it up.` is judged alone, for what it rejects by itself.
    ("Never guess. Look it up.",
     [("split", "Never guess. → Look it up.", "negation-before-claim"),
      ("device", "Look it up.", "sentence-in-pair")]),
    ("Never guess. Do not guess.",
     [("split", "Never guess. → Do not guess.", "negation-before-claim"),
      ("device", "Do not guess.", "sentence-in-pair")]),
])
def test_a_sentence_with_no_word_or_pattern_is_keyed_so_a_split_can_be_judged(page: str, expected: list) -> None:
    assert [(c.kind, c.text, c.patterns[0]) for c in every_candidate(page)] == expected


def test_a_sentence_candidate_moves_no_key_a_word_or_a_pattern_gives() -> None:
    # The first `Do not guess.` is keyed alone as the partner of `Never guess.`. The second is a negation
    # alone, and keeps occurrence 1, as it had before every sentence was a candidate.
    found = {c.patterns[0]: c.key for c in every_candidate("Never guess. Do not guess.\n\n---\n\nDo not guess.")}
    assert found["negation-alone"] == "device|Do not guess.|1"
    assert found["sentence-in-pair"] == "device|Do not guess.|2"


@pytest.mark.parametrize("page", ["`code`", "- `a` `b`", "> `x`"])
def test_a_sentence_of_code_alone_is_no_candidate(page: str) -> None:
    assert every_candidate(page) == []


def test_a_sentence_in_a_quotation_is_keyed_with_its_context() -> None:
    (found,) = every_candidate('> "Look first."')
    assert found.key == 'device|"Look first."|1|quotation block quote'


def test_a_sentence_candidate_must_be_judged_before_the_run_passes(tmp_path: Path, capsys: Any) -> None:
    root = repo_with(tmp_path, "## A\n\nPlan the day.\n")
    assert run(tmp_path, {}, capsys) == 1
    assert run(tmp_path, judge_all(root), capsys) == 0
