"""Wording the build briefs or the archived spec require, which a density rewrite must keep.

The style law caps the `X, not Y` device, and a page over the cap is rewritten.
The law also says content outranks the budget: a safety statement, a required
rule, a calibration pair the spec requires, and wording a build brief fixes stay,
under a ``density-exempt`` marker where the count needs one. The first recount
under the device's full definition rewrote some of that content anyway, and a
later audit against the briefs put it back. Each entry below is one of those
sentences, with the source that requires it, so a later rewrite that drops one
fails here instead of in review.

The wording must stay where a reader sees it. So each page is read as the
recount tool reads it, through markdown-it: the text of its paragraphs,
headings and table cells, without comments, fenced blocks, code spans, link
destinations or emphasis markers. Wording kept only in a comment, a fence or a
marker's reason does not count. Each required passage must stand within one
block, as a reader meets it: wording split across two paragraphs, two list
items or a heading and a paragraph does not count. And it must stand as whole
words: past any punctuation beside it, each side is white space or the edge of
the block, so wording kept only inside a longer word (``XAI can make up
facts``, ``sound right.ly``) does not count. The tool needs Node.js and the
repository's ``node_modules``.

A page is read only after the check the recount tool and the hooks make before
they read: a link, even one back inside the tree, anything but a regular file,
and a path that resolves outside the repository are refused by name. The
Markdown workflow runs this test before the self-containment scan, which
refuses a tracked link, so this test cannot wait for that scan.

A sentence may change only with the authority of the source named beside it.

The suite also holds a lead-in's count to its list, because a child counts
along with the page. A paragraph whose last sentence ends with a colon and
states a count as a number word, two to twelve, must be directly followed by a
list of that many items, so ``Keep these three habits:`` above four items
fails. A comment between them, such as a ``density-exempt`` marker, prints
nothing, so the list below it is the one checked. Digits are not read: above a list they are a session number, a range or
the end of a scale more often than a count. Nor is a number word joined to the
next word by a hyphen, as in ``your big two-slice total:``. Every tracked page
under ``framework/`` and ``destinations/`` is read, and the root ``README.md``
and ``GETTING_STARTED.md``.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "check-x-not-y.py"
SPEC = importlib.util.spec_from_file_location("check_x_not_y", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load the recount script from {SCRIPT_PATH}")
_module = sys.modules.get(SPEC.name) or importlib.util.module_from_spec(SPEC)
if SPEC.name not in sys.modules:
    sys.modules[SPEC.name] = _module
    SPEC.loader.exec_module(_module)
cx = cast(Any, _module)

S05 = "framework/sessions/phase_01_research_skills/05_good_sources_bad_sources.md"
S02 = "framework/sessions/phase_00_setup/02_family_traveler_profiles.md"
S03 = "framework/sessions/phase_00_setup/03_what_makes_a_good_trip.md"
S11 = "framework/sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md"
TIME = "framework/parent_guide/time_and_effort.md"
GLOSSARY = "framework/docs/glossary.md"

REQUIRED = [
    # (page, required wording as a reader sees it, source)
    (S05, "AI can make up facts that sound right.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI is never your only source.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI never decides legal, safety, entry, medical, money, or booking questions. Those are for the adults.",
     "batch 1 brief: Session 05 preserves the three AI lines; ai_use_rules.md names them"),
    ("framework/docs/ai_use_rules.md", "AI may help brainstorm or organize, but it cannot be the only source.",
     "batch 1 brief: the verification rules, quoted"),
    ("framework/parent_guide/booking_guidance.md",
     "Never silently. An owned pick is reshaped only with a stated reason.",
     "batch 2 brief, booking item 7; the spec's transparency obligation"),
    ("framework/parent_guide/coaching_and_support.md", "keep any comparison cooperative, never scored.",
     "spec: the sibling note"),
    ("framework/parent_guide/differentiation.md",
     "The checkpoint reflections are optional and for noticing, not grading.",
     "spec: reflection pressure, noticing, not grading"),
    ("framework/parent_guide/flights_from_origin_guidance.md", "It is not where you reveal it for the first time.",
     "batch 2 brief B3: Checkpoint 4 is not where the shape is first revealed"),
    ("framework/parent_guide/session_support_notes.md", "A filter reduces exposure but does not remove it.",
     "spec: the kid-safe filter caveat, a standalone safety rule"),
    ("framework/parent_guide/adult_only_logistics.md", "They don't research the fix.",
     "batch 2 brief B2, bold; the spec's child-flags-not-fixes boundary"),
    (TIME, "If you want a rough signal over time rather than a feeling,", "batch 1 brief H6: the appended line"),
    (TIME, "not heavier across the board.", "spec: pilot signal (c), which the page must contain"),
    (S02, "A grown-up owns that page, so you read it, but you do not change it.",
     "batch 1 brief: Session 02's First Steps, exact wording"),
    (S02, "Do not wait on anyone's schedule.", "batch 1 brief: the relay fallback in Session 03's words"),
    (S03, "Do not wait on anyone's schedule.", "batch 1 brief: the relay fallback in Session 03's words"),
    (S11, "You do not need to memorize this. Your job is to understand enough geography to make better travel "
          "decisions.", "batch 1 brief: the canonical reassurance, as a block quote"),
    ("destinations/japan/session_inserts/README.md", "Re-checking is optional upkeep, not a maintenance promise.",
     "batch 1 brief: the Last reviewed rule, in exactly this form"),
    ("framework/templates/student_session_template.md", "and never by citing a spec section number.",
     "batch 1 brief: the conditional-core line's built form"),
    ("framework/templates/reservation_watchlist.md", "not to force the dates",
     "batch 2 brief: the fix is awareness, not forcing dates"),
    ("framework/templates/budget_estimate.md", "It's not the final total.",
     "spec: one warm kid-facing line on the budget worksheet"),
    ("framework/templates/budget_estimate.md",
     "It's not part of your worksheet or your band check, so there's nothing to fill in here.",
     "batch 2 brief: the page says in as many words that there is nothing to fill in"),
    ("framework/student_guide/planner_mindset.md", "not to research forever.",
     "spec: good enough is good enough"),
    ("framework/templates/hotel_comparison_card.md", "Four or five cards for the whole trip is plenty",
     "batch 2 brief A3: cap the whole trip at about four or five"),
    ("framework/templates/language_etiquette_quick_sheet.md", "not just a binder page.",
     "batch 2 brief A10: a tool for the trip, not only a binder page"),
    (GLOSSARY, "the part of a session where the child's own taste decides, rather than the research.",
     "spec: the Make It Yours zone is kept separate from the research"),
    (GLOSSARY, 'so "done" is a fact rather than a feeling.', "the Stop Point field's definition"),
    ("framework/templates/parent_review_form.md", "You don't have to be the expert. Your job is to model the process",
     "spec and batch 2 brief: the reviewing parent's mandatory note"),
]


def visible_blocks(text: str) -> list[str]:
    """Return the words a reader sees on a page, one entry per block: each paragraph, heading and table cell.

    Blocks are kept apart, so a passage counts only when one block holds all of it.
    """
    page = cx.parse_text(text)
    blocks = [cx.plain(cx.paragraph_text(para)) for para in cx.paragraphs(page.prose)]
    blocks += [cx.plain(label.text) for label in page.labels]
    return [cx.normalize_space(block) for block in blocks]


def is_visible(wording: str, text: str) -> bool:
    """True when one block of the page shows all of `wording`, as whole words.

    Past any punctuation beside the passage, each side must be white space or
    the edge of the block.
    """
    wanted = re.compile(r"(?:^|(?<=\s))[^\w\s]*" + re.escape(cx.normalize_space(wording)) + r"[^\w\s]*(?:\s|$)")
    return any(wanted.search(block) for block in visible_blocks(text))


def read_page(page: str, root: Path | None = None) -> str:
    """Read a page of the repository, or raise ReadError naming it when the tool's check refuses it."""
    base = REPO_ROOT if root is None else root
    why = cx.refusal(base / page, base)
    if why is not None:
        raise cx.ReadError(f"{page} {why}; refusing to read it")
    return (base / page).read_text(encoding="utf-8")


@pytest.mark.parametrize(("page", "wording", "source"), REQUIRED, ids=[f"{p}: {w[:40]}" for p, w, _ in REQUIRED])
def test_required_wording_is_visible_on_its_page(page: str, wording: str, source: str) -> None:
    text = read_page(page)
    assert is_visible(wording, text), (
        f"{page} no longer shows required wording ({source}): {wording}")


@pytest.mark.parametrize("hidden", [
    "<!-- AI never decides legal questions. -->",
    "<!-- density-exempt: X, not Y -- AI never decides legal questions. -->",
    "```text\nAI never decides legal questions.\n```",
    "Say `AI never decides legal questions.` aloud.",
])
def test_wording_the_page_does_not_show_is_not_visible(hidden: str) -> None:
    assert not is_visible("AI never decides legal questions.", "Intro.\n\n" + hidden + "\n\nOutro.\n")


def test_wording_in_prose_is_visible_through_markup() -> None:
    text = "- **AI never decides** legal [questions](a.md).\n"
    assert is_visible("AI never decides legal questions.", text)


@pytest.mark.parametrize("text", [
    "AI never decides legal\n\nquestions.\n",
    "- AI never decides legal\n- questions.\n",
    "- AI never decides legal\n\n  questions.\n",
    "## AI never decides legal\n\nquestions.\n",
    "> AI never decides legal\n\nquestions.\n",
])
def test_wording_split_across_two_blocks_is_not_visible(text: str) -> None:
    assert not is_visible("AI never decides legal questions.", text)


@pytest.mark.parametrize("text", [
    "AI never decides\nlegal questions.\n",
    "- AI never decides legal questions.\n",
    "## AI never decides legal questions.\n",
    "| AI never decides legal questions. | x |\n| --- | --- |\n",
])
def test_wording_within_one_block_is_visible(text: str) -> None:
    assert is_visible("AI never decides legal questions.", text)


AI = "AI can make up facts that sound right."


@pytest.mark.parametrize("text", [
    "XAI can make up facts that sound right.\n",
    "AI can make up facts that sound right.ly\n",
    "Non-AI can make up facts that sound right.\n",
    "Human/AI can make up facts that sound right.\n",
    "AI can make up facts that sound right.2\n",
])
def test_wording_kept_only_inside_a_longer_word_is_not_visible(text: str) -> None:
    assert not is_visible(AI, text)


@pytest.mark.parametrize(("wording", "text"), [
    (AI, "AI can make up facts that sound right.\n"),
    (AI, "Careful. AI can make up facts that sound right. Check it.\n"),
    (AI, '"AI can make up facts that sound right."\n'),
    (AI, "(AI can make up facts that sound right.)\n"),
    (AI, "**AI** can make up facts that sound right.\n"),
    ("not to force the dates", "The fix is awareness, not to force the dates, and it helps.\n"),
    ("not to force the dates", "The fix is awareness, not to force the dates.\n"),
])
def test_wording_that_stands_as_whole_words_is_visible(wording: str, text: str) -> None:
    assert is_visible(wording, text)


def make_link(link: Path, target: Path) -> None:
    """Create a symbolic link, or skip the test where the platform cannot."""
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(target, target_is_directory=target.is_dir())
    except (OSError, NotImplementedError):
        pytest.skip("this platform cannot create a symlink here")


def write_page(path: Path, text: str) -> None:
    """Write one page, making its directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


@pytest.mark.parametrize(("kind", "why"), [
    ("a link back inside the tree", "is a symbolic link or a junction"),
    ("a link out of the tree", "is a symbolic link or a junction"),
    ("a page under a linked directory", "resolves outside the repository"),
])
def test_a_required_page_that_is_a_link_is_refused_before_it_is_read(tmp_path: Path, kind: str, why: str) -> None:
    root, outside = tmp_path / "repo", tmp_path / "outside"
    write_page(root / "real.md", AI + "\n")
    write_page(outside / "a.md", AI + "\n")
    if kind == "a link back inside the tree":
        make_link(root / "framework/a.md", root / "real.md")
    elif kind == "a link out of the tree":
        make_link(root / "framework/a.md", outside / "a.md")
    else:
        make_link(root / "framework", outside)
    with pytest.raises(cx.ReadError, match=why):
        read_page("framework/a.md", root)


def test_a_required_page_that_is_a_directory_is_refused(tmp_path: Path) -> None:
    (tmp_path / "framework/a.md").mkdir(parents=True)
    with pytest.raises(cx.ReadError, match="is not a regular file"):
        read_page("framework/a.md", tmp_path)


def test_a_required_page_that_is_a_regular_file_is_read(tmp_path: Path) -> None:
    write_page(tmp_path / "framework/a.md", AI + "\n")
    assert read_page("framework/a.md", tmp_path) == AI + "\n"


def test_the_required_wording_test_reads_through_the_check(tmp_path: Path, monkeypatch: Any) -> None:
    page, wording, source = REQUIRED[0]
    write_page(tmp_path / "outside.md", wording + "\n")
    make_link(tmp_path / page, tmp_path / "outside.md")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)
    with pytest.raises(cx.ReadError, match="refusing to read it"):
        test_required_wording_is_visible_on_its_page(page, wording, source)


# A pack's freshness stamp. Each reference file and each session insert of a
# destination pack carries one `Last reviewed` label as the first block below
# its title, so a parent can judge whether a fact may be stale. The contents
# pages, each folder's README.md, hold no facts and carry none.
STAMP_GLOBS = ("destinations/*/reference/*.md", "destinations/*/session_inserts/*.md")
#: A label is a paragraph whose printed text starts with this, in any case.
STAMP_RE = re.compile(r"last reviewed:", re.IGNORECASE)


def stamped_pages(root: Path | None = None) -> list[str]:
    """Return every pack page that must carry a stamp, each folder's README.md aside."""
    base = REPO_ROOT if root is None else root
    return sorted({path.relative_to(base).as_posix() for pattern in STAMP_GLOBS for path in base.glob(pattern)
                   if path.name != "README.md"})


def stamp_problem(text: str) -> str | None:
    """Return what is wrong with a page's `Last reviewed` label, or None when it has one, in its place.

    The page is read as the recount reads it, through markdown-it. A label is a
    paragraph whose printed text starts with `Last reviewed:`, in any case and
    with any emphasis. So a label in a comment or a fence, which prints nothing,
    does not count, and neither does one that follows other text in its
    paragraph. A page needs exactly one, as the first block below its title,
    the first level-1 heading.
    """
    blocks = cx.read_blocks(text)
    labels = [i for i, block in enumerate(blocks)
              if block["type"] == "paragraph" and STAMP_RE.match(cx.normalize_space(cx.plain(block["text"])))]
    lines = ", ".join(str(blocks[i]["start"]) for i in labels) or "none"
    if len(labels) != 1:
        return f"{len(labels)} `Last reviewed` labels (lines: {lines}); it needs exactly one, below its title"
    title = next((i for i, block in enumerate(blocks) if block["type"] == "heading" and block["level"] == 1), None)
    if title is None:
        return f"1 `Last reviewed` label (line {lines}), but no title for it to stand below"
    if labels[0] != title + 1:
        return (f"1 `Last reviewed` label (line {lines}), but it is not the first block below the title"
                f" at line {blocks[title]['start']}")
    return None


def test_each_pack_page_carries_one_last_reviewed_label_below_its_title() -> None:
    """Each pack reference file and session insert shows one `Last reviewed` label, first below its title.

    The globs take a new pack's files with no edit here. Globs that match no
    file fail, so a moved folder cannot pass by matching nothing.
    """
    pages = stamped_pages()
    assert pages, f"{' and '.join(STAMP_GLOBS)} matched no file, so no pack page was checked"
    problems = [f"{page}: {why}" for page in pages if (why := stamp_problem(read_page(page))) is not None]
    assert not problems, "pack pages without one `Last reviewed` label below the title:\n" + "\n".join(problems)


PAGE_TOP = "<!-- markdownlint-disable MD013 -->\n<!-- audience: child -->\n\n# A Pack Page\n\n"
STAMP = "**Last reviewed:** September 2026\n"


@pytest.mark.parametrize("text", [
    PAGE_TOP + STAMP + "\nA fact to check.\n",
    PAGE_TOP + "Last reviewed: September 2026\n\nA fact to check.\n",
    PAGE_TOP + "*LAST REVIEWED:* September 2026\n\nA fact to check.\n",
    PAGE_TOP + "**Last reviewed**: September 2026\n\nA fact to check.\n",
])
def test_one_label_first_below_the_title_passes(text: str) -> None:
    assert stamp_problem(text) is None


@pytest.mark.parametrize(("text", "why"), [
    (PAGE_TOP + "A fact to check.\n", "0 `Last reviewed` labels (lines: none)"),
    (PAGE_TOP + STAMP + "\nA fact to check.\n\n" + STAMP, "2 `Last reviewed` labels (lines: 6, 10)"),
    (PAGE_TOP + "<!-- " + STAMP.strip() + " -->\n\nA fact to check.\n", "0 `Last reviewed` labels"),
    (PAGE_TOP + "```text\n" + STAMP + "```\n\nA fact to check.\n", "0 `Last reviewed` labels"),
    (PAGE_TOP + "A fact to check. " + STAMP, "0 `Last reviewed` labels"),
    (PAGE_TOP + "A fact to check.\n\n" + STAMP,
     "1 `Last reviewed` label (line 8), but it is not the first block below the title at line 4"),
], ids=["no label", "two labels", "a label in a comment", "a label in a fence", "a label after other text on its line",
        "a label below other text"])
def test_a_missing_doubled_hidden_or_misplaced_label_fails(text: str, why: str) -> None:
    problem = stamp_problem(text)
    assert problem is not None and problem.startswith(why), problem


def test_the_stamp_test_fails_when_its_globs_match_no_file(tmp_path: Path, monkeypatch: Any) -> None:
    write_page(tmp_path / "destinations/somewhere/README.md", "# Contents\n")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)
    with pytest.raises(AssertionError, match="matched no file"):
        test_each_pack_page_carries_one_last_reviewed_label_below_its_title()


def test_the_stamp_test_names_an_unstamped_page_and_leaves_out_each_readme(tmp_path: Path, monkeypatch: Any) -> None:
    pack = tmp_path / "destinations/somewhere"
    write_page(pack / "reference/README.md", "# Contents\n\nNo facts here.\n")
    write_page(pack / "session_inserts/README.md", "# Routing\n\nNo facts here.\n")
    write_page(pack / "reference/stamped.md", PAGE_TOP + STAMP)
    write_page(pack / "session_inserts/unstamped.md", PAGE_TOP + "A fact to check.\n")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)
    assert stamped_pages() == ["destinations/somewhere/reference/stamped.md",
                               "destinations/somewhere/session_inserts/unstamped.md"]
    with pytest.raises(AssertionError) as failure:
        test_each_pack_page_carries_one_last_reviewed_label_below_its_title()
    assert ("destinations/somewhere/session_inserts/unstamped.md: 0 `Last reviewed` labels (lines: none)"
            in str(failure.value))
    assert "reference/stamped.md" not in str(failure.value)


# A lead-in's count. The roots are Git pathspecs: the two folders, and the two
# root pages by name.
LEAD_IN_ROOTS = ("framework", "destinations", "README.md", "GETTING_STARTED.md")
COUNT_WORDS = ("two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
#: A stated count: a number word, not joined to the next word by a hyphen. Digits are never read.
COUNT_RE = re.compile(r"\b(" + "|".join(COUNT_WORDS) + r")\b(?!-\w)", re.IGNORECASE)


def lead_in_pages() -> list[str]:
    """Return every tracked page under framework/ and destinations/, and the two root pages, as Git lists them."""
    listed = subprocess.run(["git", "ls-files", "-z", "--", *LEAD_IN_ROOTS], cwd=REPO_ROOT, capture_output=True,
                            text=True, encoding="utf-8", check=True)
    return sorted(page for page in listed.stdout.split("\0") if page.endswith(".md"))


def count_mismatches(text: str) -> list[str]:
    """Return each lead-in on a page whose stated count differs from the list directly below it.

    A lead-in is a paragraph directly followed by a list, whose last sentence
    ends with a colon. A block that shows nothing, such as a comment holding a
    ``density-exempt`` marker, is read past, as the recount reads past it to
    find a marker's block. The count is the first number word in that
    sentence. A lead-in with no number word states no count. Each entry names
    the line the number word is on, the claim and the list's item count.
    """
    blocks = cx.read_blocks(text)
    out: list[str] = []
    for index, para in enumerate(blocks):
        if para["type"] != "paragraph":
            continue
        below = next((block for block in blocks[index + 1:] if not cx.shows_nothing(block)), None)
        if below is None or below["type"] not in ("bullet_list", "ordered_list"):
            continue
        # One printed line per source line, as the recount splits a paragraph into sentences.
        printed = "\n".join(cx.plain(line) for line in para["text"].split("\n"))
        spans = cx.sentence_spans(printed)
        if not spans or not printed[spans[-1][0]:spans[-1][1]].endswith(":"):
            continue
        start, end = spans[-1]
        found = COUNT_RE.search(printed, start, end)
        if found is None:
            continue
        claim = COUNT_WORDS.index(found.group(1).lower()) + 2
        if claim != below["items"]:
            line = para["start"] + printed.count("\n", 0, found.start())
            out.append(f"line {line}: {cx.normalize_space(printed[start:end])!r} states {claim}, and the list"
                       f" below it has {below['items']}")
    return out


def test_each_lead_in_count_matches_the_list_below_it() -> None:
    pages = lead_in_pages()
    assert pages, f"git listed no page under {', '.join(LEAD_IN_ROOTS)}, so no lead-in was checked"
    problems = [f"{page}: {problem}" for page in pages for problem in count_mismatches(read_page(page))]
    assert not problems, "lead-ins whose count differs from the list below them:\n" + "\n".join(problems)


HABITS = "- Read it.\n- Check it.\n- Ask about it.\n"


@pytest.mark.parametrize("text", [
    "Keep these three habits:\n\n" + HABITS,
    "Four steps, in order:\n\n1. Look.\n2. Read.\n3. Check.\n4. Write.\n",
    "Add up your big two-slice total:\n\n- a\n- b\n- c\n- d\n- e\n",
    "Keep these three habits.\n\n- Read it.\n",
    "- Pack two things:\n  - a hat\n  - a map\n",
    "Keep these three habits:\n\n<!-- a note for the builder -->\n\n<!-- a second note -->\n\n" + HABITS,
    "Keep these three habits:\n\nThen read on.\n\n- Read it.\n",
], ids=["three over three", "four over four", "two-slice total over five", "no colon", "a nested list",
        "three over three past two comments", "a paragraph between"])
def test_a_count_that_matches_or_states_nothing_passes(text: str) -> None:
    assert count_mismatches(text) == []


@pytest.mark.parametrize("text", [
    "At 2-4 sessions a week:\n\n" + HABITS,
    "Before you start Session 53:\n\n" + HABITS,
    "Score each city from 1 (low) to 5 (high) on three things:\n\n" + HABITS,
], ids=["a range", "a session number", "a scale's ends beside a number word"])
def test_a_digit_count_is_ignored(text: str) -> None:
    assert count_mismatches(text) == []


@pytest.mark.parametrize(("text", "why"), [
    ("Keep these three habits:\n\n" + HABITS + "- Write it down.\n",
     "line 1: 'Keep these three habits:' states 3, and the list below it has 4"),
    ("# Steps\n\nFive steps, in order:\n\n1. Look.\n2. Read.\n3. Check.\n",
     "line 3: 'Five steps, in order:' states 5, and the list below it has 3"),
    ("- Pack two things:\n  - a hat\n  - a map\n  - a snack\n",
     "line 1: 'Pack two things:' states 2, and the list below it has 3"),
    ("Read the page first. Then keep\nthese four habits:\n\n" + HABITS,
     "line 2: 'Then keep these four habits:' states 4, and the list below it has 3"),
    ("Keep these three habits:\n\n<!-- density-exempt: X, not Y -- a reason -->\n\n" + HABITS + "- Write it down.\n",
     "line 1: 'Keep these three habits:' states 3, and the list below it has 4"),
], ids=["three over four", "five over three", "a nested list", "a count on the paragraph's second line",
        "three over four behind a comment"])
def test_a_wrong_count_fails_with_its_line_claim_and_count(text: str, why: str) -> None:
    assert count_mismatches(text) == [why]
