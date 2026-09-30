"""The cross-reference map's routing mirror matches each pack's routing contract.

Every destination pack carries the routing contract, at
``destinations/<pack>/session_inserts/README.md``. Two of its tables say which
pack file each session reads and which pack file each parent-facing page points
to, and the contract is the canonical copy of both. Part 2 of the framework's
``cross_reference_map.md`` copies the two tables, so a reader on the framework
side sees the routing without opening a pack. Two copies kept by hand drift
apart, and no other check compares them. So this suite compares them row for
row, header rows included, for every pack.

Both pages are read through markdown-it, as ADR-0002 says a new tool reads
Markdown, by ``tests/markdown_tables.mjs``. It gives each heading and each
table as the page prints them, so a heading or a table inside a fenced block
or an HTML comment is not read. The copies are compared as the reader prints
them, so they may differ in markup that prints the same text, links above all.
The contract links each pack file it names, and a pack still being built writes a
file it has not written yet in inline code. The mirror writes every pack file
in inline code, unlinked, so no framework page links into a pack, and it links
each parent-facing page that the contract names in plain text. The reader
prints a link as its label and a code span as its code between backticks, so
a linked filename matches the same name in inline code, and two filenames
never match each other. Markup that prints nothing, such as emphasis marks, an
image, a comment or an HTML tag, is not compared, and none of it changes which
file a row routes to. Everything else the copies print must match exactly, in
the same order.

Every folder under ``destinations/`` is one pack, as the leak check reads them,
and each must carry the contract. A table is the first one under its heading,
before the next heading of any level. A missing heading, a heading with no
table under it, a table with no rows below its header and a pack without its
contract each fail by name, so the suite cannot pass on tables it never found.
Without Node.js or markdown-it the suite fails and names ``npm ci``; the
Markdown workflow installs both before it runs the suite. The rules for a
check are in ``docs/writing_checkers.md``.
"""

from __future__ import annotations

import difflib
import functools
import json
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The Node program that reads a page's headings and tables through markdown-it.
READER = REPO_ROOT / "tests" / "markdown_tables.mjs"
#: The framework page that holds the mirror.
MIRROR = "framework/cross_reference_map.md"
#: The folder of the destination packs. Each folder under it is one pack.
PACKS_FOLDER = "destinations"
#: The contract's path inside each pack's folder.
CONTRACT = "session_inserts/README.md"

Heading = tuple[int, str]
Row = tuple[str, ...]

#: Each table the mirror copies: its name, the heading path to it in the
#: contract, and the heading path to it in the mirror. A heading is its level
#: and the text it prints.
TABLES: tuple[tuple[str, tuple[Heading, ...], tuple[Heading, ...]], ...] = (
    (
        "sessions",
        ((2, "The insert and reference contract"),),
        ((2, "Part 2: The destination routing mirror"), (3, "Sessions")),
    ),
    (
        "parent-facing pages",
        ((2, "The insert and reference contract"), (3, "Parent-facing pages")),
        ((2, "Part 2: The destination routing mirror"), (3, "Parent-facing pages")),
    ),
)


def markdown_it_blocks(
    texts: Sequence[str], node_command: str = "node", reader: Path = READER
) -> list[list[dict[str, Any]]]:
    """Return each text's headings and tables, read by markdown-it in one Node process.

    **Without Node.js, or without markdown-it, the suite fails and says so.**
    Skipping would report a match for tables nobody compared.
    """
    node = shutil.which(node_command)
    if node is None:
        raise AssertionError(
            f"{node_command!r} was not found. This suite reads each page through "
            f"{reader.name}, which needs Node.js: install Node.js and run `npm ci` "
            "in the repository root."
        )
    request = "".join(json.dumps({"text": text}) + "\n" for text in texts)
    completed = subprocess.run(
        [node, str(reader)],
        input=request,
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=REPO_ROOT,
        check=False,
    )
    answers = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    if completed.returncode != 0 or len(answers) != len(texts):
        raise AssertionError(
            f"{reader.name} answered {len(answers)} of {len(texts)} page(s) and exited "
            f"{completed.returncode}. Run `npm ci` in the repository root so that "
            "markdown-it is installed. It said: " + completed.stderr.strip()[-600:]
        )
    errors = [answer["error"] for answer in answers if "error" in answer]
    if errors:
        raise AssertionError(f"{reader.name} could not read a page: {errors}")
    return [answer["blocks"] for answer in answers]


@functools.lru_cache(maxsize=None)
def page_blocks(text: str) -> tuple[dict[str, Any], ...]:
    """Return one page's headings and tables, reading each text once."""
    return tuple(markdown_it_blocks([text])[0])


def heading_name(heading: Heading) -> str:
    """Write a heading as its Markdown source line."""
    level, text = heading
    return f"{'#' * level} {text}"


def read_table(text: str, path: Sequence[Heading], where: str) -> list[Row]:
    """Return the header row and body rows of the first table under a heading path.

    Each heading in ``path`` is looked for inside the section of the one before
    it, which runs to the next heading of the same level or a higher one. The
    table is the first one after the last heading, before the next heading of
    any level.
    """
    blocks = page_blocks(text)
    start, end = 0, len(blocks)
    for heading in path:
        level = heading[0]
        found = next(
            (
                index
                for index in range(start, end)
                if blocks[index]["type"] == "heading" and (blocks[index]["level"], blocks[index]["text"]) == heading
            ),
            None,
        )
        if found is None:
            route = " > ".join(heading_name(step) for step in path)
            raise LookupError(f"{where}: no heading {heading_name(heading)!r} where the path {route!r} leads")
        start = found + 1
        end = next(
            (index for index in range(start, end) if blocks[index]["type"] == "heading" and blocks[index]["level"] <= level),
            end,
        )
    table = None
    for block in blocks[start:end]:
        if block["type"] == "heading":
            break
        if block["type"] == "table":
            table = block
            break
    if table is None:
        raise LookupError(f"{where}: no table under {heading_name(path[-1])!r}")
    rows = [tuple(row) for row in table["rows"]]
    if len(rows) < 2:
        raise LookupError(f"{where}: the table under {heading_name(path[-1])!r} has no rows below its header")
    return rows


def differences(contract: list[Row], mirror: list[Row]) -> list[str]:
    """Return a unified diff of two tables' rows, empty when the rows match."""
    return list(
        difflib.unified_diff(
            [" | ".join(row) for row in contract],
            [" | ".join(row) for row in mirror],
            "contract",
            "mirror",
            lineterm="",
            n=0,
        )
    )


def pack_folders(root: Path = REPO_ROOT) -> list[Path]:
    """Return every pack's folder, in name order."""
    return sorted(path for path in (root / PACKS_FOLDER).iterdir() if path.is_dir())


def check_packs(root: Path = REPO_ROOT) -> None:
    """Fail unless at least one pack exists and each one holds the contract."""
    packs = pack_folders(root)
    assert packs, f"no pack folder under {PACKS_FOLDER}/"
    missing = [f"{PACKS_FOLDER}/{pack.name}/{CONTRACT}" for pack in packs if not (pack / CONTRACT).is_file()]
    assert not missing, f"a pack must carry the routing contract; missing: {missing}"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_every_pack_carries_the_contract() -> None:
    """At least one pack exists, and each one holds the contract the mirror copies."""
    check_packs()


def test_a_folder_without_the_contract_fails_by_name(tmp_path: Path) -> None:
    """Every folder is a pack: no folder fails, and a folder without the contract is named."""
    (tmp_path / PACKS_FOLDER).mkdir()
    with pytest.raises(AssertionError, match="no pack folder"):
        check_packs(tmp_path)
    (tmp_path / PACKS_FOLDER / "built" / "session_inserts").mkdir(parents=True)
    (tmp_path / PACKS_FOLDER / "built" / CONTRACT).touch()
    check_packs(tmp_path)
    (tmp_path / PACKS_FOLDER / "unbuilt").mkdir()
    with pytest.raises(AssertionError) as refused:
        check_packs(tmp_path)
    assert f"missing: ['{PACKS_FOLDER}/unbuilt/{CONTRACT}']" in str(refused.value)


@pytest.mark.parametrize("pack", [pack.name for pack in pack_folders()])
@pytest.mark.parametrize(("table", "contract_path", "mirror_path"), TABLES, ids=[t[0] for t in TABLES])
def test_the_mirror_matches_the_contract(
    pack: str, table: str, contract_path: tuple[Heading, ...], mirror_path: tuple[Heading, ...]
) -> None:
    """The mirror's copy of each table matches the pack's contract row for row."""
    contract_file = f"{PACKS_FOLDER}/{pack}/{CONTRACT}"
    contract = read_table(read(REPO_ROOT / contract_file), contract_path, contract_file)
    mirror = read_table(read(REPO_ROOT / MIRROR), mirror_path, MIRROR)
    diff = differences(contract, mirror)
    assert not diff, (
        f"the {table} table in {MIRROR} differs from the one in {contract_file}. "
        "The contract is the canonical copy: make the mirror match it, or change both in one commit.\n"
        + "\n".join(diff)
    )


CONTRACT_PAGE = """\
# A pack's contract

## The insert and reference contract

Sessions first.

| Session | Insert | Reference |
| --- | --- | --- |
| 05 First | none | [`a.md`](../reference/a.md) |
| 10 Second | [`10_b.md`](10_b.md) | [`c.md`](../reference/c.md) (its note) |

### Parent-facing pages

| Parent-facing page | Insert | Reference |
| --- | --- | --- |
| Money guidance | none | [`d.md`](../reference/d.md) |

## What each slot supplies
"""

MIRROR_PAGE = """\
# The map

## Part 2: The destination routing mirror

### Sessions

| Session | Insert | Reference |
| --- | --- | --- |
| 05 First | none | `a.md` |
| 10 Second | `10_b.md` | `c.md` (its note) |

### Parent-facing pages

| Parent-facing page | Insert | Reference |
| --- | --- | --- |
| [Money guidance][p-money] | none | `d.md` |

[p-money]: parent_guide/money.md
"""

SESSIONS_PATH = TABLES[0][2]


def compare(contract_page: str, mirror_page: str) -> list[str]:
    """Compare both sample tables, and return every difference found."""
    found: list[str] = []
    for _, contract_path, mirror_path in TABLES:
        found += differences(
            read_table(contract_page, contract_path, "contract"),
            read_table(mirror_page, mirror_path, "mirror"),
        )
    return found


def test_matching_samples_pass() -> None:
    """A linked filename matches the same name in inline code, and a linked page name its plain text."""
    assert compare(CONTRACT_PAGE, MIRROR_PAGE) == []


def test_each_cell_reads_as_the_page_prints_it() -> None:
    """Every link form prints its label, and code keeps its backticks; a bracket with no definition stays."""
    page = (
        "### Sessions\n\n| A | B |\n| --- | --- |\n"
        "| [`a.md`](../reference/a_(b).md) | [Money guidance][p-money] |\n"
        "| [Money guidance][] | [Money guidance] |\n"
        "| **`c.md`**, `d.md` | [no definition] &amp; a\\|b |\n\n"
        "[money guidance]: parent_guide/money.md\n[p-money]: parent_guide/money.md\n"
    )
    assert read_table(page, [(3, "Sessions")], "sample") == [
        ("A", "B"),
        ("`a.md`", "Money guidance"),
        ("Money guidance", "Money guidance"),
        ("`c.md`, `d.md`", "[no definition] & a|b"),
    ]


@pytest.mark.parametrize(
    "heading",
    ["Part 2: The destination\nrouting mirror\n---\n", "Part 2: The destination\\\nrouting mirror\n---\n"],
    ids=["soft-break", "hard-break"],
)
def test_white_space_reads_as_one_space(heading: str) -> None:
    """A soft or a hard line break and each run of white space print one space, and a cell's ends are trimmed."""
    page = heading + "\n### Sessions\n\n| A | B |\n| --- | --- |\n| `a.md`,  \t`b.md` <!-- note --> | x |\n"
    assert read_table(page, SESSIONS_PATH, "sample") == [("A", "B"), ("`a.md`, `b.md`", "x")]


@pytest.mark.parametrize(
    ("before", "after", "reported"),
    [
        ("| 10 Second | `10_b.md` | `c.md` (its note) |", "| 10 Second | `10_b.md` | `e.md` (its note) |", "`e.md`"),
        ("| 10 Second | `10_b.md` | `c.md` (its note) |\n", "", "-10 Second"),
        ("| 05 First | none | `a.md` |\n| 10 Second | `10_b.md` | `c.md` (its note) |",
         "| 10 Second | `10_b.md` | `c.md` (its note) |\n| 05 First | none | `a.md` |", "+10 Second"),
        ("| Session | Insert | Reference |", "| Session | Slot | Reference |", "Slot"),
        ("| [Money guidance][p-money] | none | `d.md` |", "| Money guide | none | `d.md` |", "Money guide"),
    ],
    ids=["changed-cell", "missing-row", "moved-row", "changed-header", "changed-page-name"],
)
def test_a_drifted_mirror_is_reported(before: str, after: str, reported: str) -> None:
    """A changed cell, a missing row, a moved row, a changed header and a changed page name each fail."""
    assert before in MIRROR_PAGE
    found = compare(CONTRACT_PAGE, MIRROR_PAGE.replace(before, after, 1))
    assert found and any(reported in line for line in found), found


def test_a_missing_heading_is_refused_by_name() -> None:
    """The refusal names the heading that is missing, whichever step of the path it is."""
    page = MIRROR_PAGE.replace("### Sessions", "### Session rows")
    with pytest.raises(LookupError, match="no heading '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")
    page = MIRROR_PAGE.replace("## Part 2:", "## Part Two:")
    with pytest.raises(LookupError, match="no heading '## Part 2: The destination routing mirror'"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_a_heading_without_a_table_is_refused() -> None:
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\nNo table.\n\n### Parent-facing pages\n"
    with pytest.raises(LookupError, match="no table under '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_a_table_without_rows_is_refused() -> None:
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\n| Session | Insert |\n| --- | --- |\n"
    with pytest.raises(LookupError, match="no rows below its header"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_a_fenced_heading_and_table_are_not_read() -> None:
    """A sample inside a fenced block is neither the heading nor the table."""
    fenced = "```text\n### Sessions\n\n| Session | Insert |\n| --- | --- |\n| 05 First | none |\n```\n"
    page = "## Part 2: The destination routing mirror\n\n" + fenced
    with pytest.raises(LookupError, match="no heading '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\n" + fenced.replace("### Sessions\n\n", "")
    with pytest.raises(LookupError, match="no table under '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_a_table_inside_a_comment_is_not_read() -> None:
    """A table a comment hides prints nothing, so it is not the mirror's table."""
    hidden = "<!--\n| Session | Insert |\n| --- | --- |\n| 05 First | none |\n-->\n"
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\n" + hidden
    with pytest.raises(LookupError, match="no table under '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_the_table_is_the_one_under_its_own_heading() -> None:
    """The contract's session table is read from above the parent-facing heading, not below it."""
    rows = read_table(CONTRACT_PAGE, TABLES[0][1], "contract")
    assert [row[0] for row in rows] == ["Session", "05 First", "10 Second"]
    rows = read_table(CONTRACT_PAGE, TABLES[1][1], "contract")
    assert [row[0] for row in rows] == ["Parent-facing page", "Money guidance"]


SESSION_ROWS = (
    "| Session | Insert | Reference |\n| --- | --- | --- |\n"
    "| 05 First | none | [`a.md`](../reference/a.md) |\n"
    "| 10 Second | [`10_b.md`](10_b.md) | [`c.md`](../reference/c.md) (its note) |\n"
)


def test_a_section_without_its_own_table_is_refused() -> None:
    """The search for a table stops at the next heading, so the table under a deeper heading is not taken.

    The contract's session path is its ``##`` heading alone, and its
    parent-facing table sits under a ``###`` heading inside that section.
    Without its own table, the session path fails by name.
    """
    assert SESSION_ROWS in CONTRACT_PAGE
    page = CONTRACT_PAGE.replace(SESSION_ROWS, "")
    with pytest.raises(LookupError, match="no table under '## The insert and reference contract'"):
        read_table(page, TABLES[0][1], "contract")


def test_the_first_of_two_tables_is_read() -> None:
    page = "### Sessions\n\n| A |\n| - |\n| first |\n\n| B |\n| - |\n| second |\n"
    assert read_table(page, [(3, "Sessions")], "sample") == [("A",), ("first",)]


def test_a_heading_is_looked_for_only_inside_the_section_before_it() -> None:
    """A section ends at the next heading of its level, so a ``### Sessions`` under another part is not the mirror's."""
    page = MIRROR_PAGE.replace("### Sessions", "### Session rows")
    page += "\n## Part 3: Other\n\n### Sessions\n\n| A |\n| - |\n| x |\n"
    with pytest.raises(LookupError, match="no heading '### Sessions'"):
        read_table(page, SESSIONS_PATH, "mirror")


def test_the_reader_names_npm_ci_when_node_is_missing() -> None:
    """A missing Node.js fails the suite, and the message says how to fix it."""
    with pytest.raises(AssertionError, match="npm ci"):
        markdown_it_blocks(["# A\n"], node_command="node-absent-for-this-test")


def test_the_reader_names_npm_ci_when_markdown_it_is_missing(tmp_path: Path) -> None:
    """A reader that cannot load its module fails the suite the same way."""
    reader = tmp_path / "reader.mjs"
    reader.write_text("import 'markdown-it-absent-for-this-test';\n", encoding="utf-8")
    with pytest.raises(AssertionError, match="npm ci"):
        markdown_it_blocks(["# A\n"], reader=reader)
