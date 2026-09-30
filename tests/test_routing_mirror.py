"""The cross-reference map's routing mirror matches each pack's routing contract.

Every destination pack carries the routing contract, at
``destinations/<pack>/session_inserts/README.md``. Two of its tables say which
pack file each session reads and which pack file each parent-facing page points
to, and the contract is the canonical copy of both. Part 2 of the framework's
``cross_reference_map.md`` copies the two tables, so a reader on the framework
side sees the routing without opening a pack. Two copies kept by hand drift
apart, and no other check compares them. So this suite compares them row for
row, header rows included, for every pack.

The copies may differ in their links only. The contract links each pack file it
names, and a pack still being built writes a file it has not written yet in
inline code. The mirror writes every pack file in inline code, unlinked, so no
framework page links into a pack, and it links each parent-facing page that the
contract names in plain text. So each link is read as its text: an inline link
``[text](destination)``, a full reference link ``[text][label]`` and a
collapsed one ``[text][]``. A run of white space counts as one space.
Everything else must match exactly, in the same order.

Every folder under ``destinations/`` is one pack, as the leak check reads them,
and each must carry the contract. A table is the first one under its heading,
before the next heading of any level, and a heading or a table inside a fenced
block is not read. A missing heading, a heading with no table under it, a table
with no rows below its header and a pack without its contract each fail by
name, so the suite cannot pass on tables it never found.
"""

from __future__ import annotations

import difflib
import re
from pathlib import Path

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The framework page that holds the mirror.
MIRROR = "framework/cross_reference_map.md"
#: The folder of the destination packs. Each folder under it is one pack.
PACKS_FOLDER = "destinations"
#: The contract's path inside each pack's folder.
CONTRACT = "session_inserts/README.md"

#: Each table the mirror copies: its name, the heading path to it in the
#: contract, and the heading path to it in the mirror.
TABLES = (
    (
        "sessions",
        ("## The insert and reference contract",),
        ("## Part 2: The destination routing mirror", "### Sessions"),
    ),
    (
        "parent-facing pages",
        ("## The insert and reference contract", "### Parent-facing pages"),
        ("## Part 2: The destination routing mirror", "### Parent-facing pages"),
    ),
)

HEADING = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]|$)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
TABLE_LINE = re.compile(r"^ {0,3}\|")
DELIMITER_CELL = re.compile(r"^:?-+:?$")
INLINE_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
REFERENCE_LINK = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
CELL_BORDER = re.compile(r"(?<!\\)\|")

Row = tuple[str, ...]


def visible_lines(text: str) -> list[str]:
    """Return the page's lines, with each line of a fenced block left blank."""
    lines: list[str] = []
    fence = ""
    for line in text.splitlines():
        if not fence:
            opening = FENCE.match(line)
            if opening:
                fence = opening.group(1)
                lines.append("")
            else:
                lines.append(line)
            continue
        closing = line.strip()
        if closing and set(closing) == {fence[0]} and len(closing) >= len(fence):
            fence = ""
        lines.append("")
    return lines


def heading_level(line: str) -> int:
    """Return the level of an ATX heading line, or 0 for any other line."""
    match = HEADING.match(line)
    return len(match.group(1)) if match else 0


def normalize(cell: str) -> str:
    """Read each link in a cell as its text, and each run of white space as one space."""
    text = INLINE_LINK.sub(r"\1", cell)
    text = REFERENCE_LINK.sub(r"\1", text)
    return " ".join(text.split())


def split_row(line: str) -> Row:
    """Split one table line into its normalized cells."""
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return tuple(normalize(cell) for cell in CELL_BORDER.split(body))


def read_table(text: str, path: tuple[str, ...], where: str) -> list[Row]:
    """Return the header row and body rows of the first table under a heading path.

    Each heading in ``path`` is looked for inside the section of the one before
    it. The table is the first one after the last heading, before the next
    heading of any level. Its delimiter row is dropped.
    """
    lines = visible_lines(text)
    start, end = 0, len(lines)
    for heading in path:
        level = heading_level(heading)
        found = next((i for i in range(start, end) if lines[i].strip() == heading), None)
        if found is None:
            raise LookupError(f"{where}: no heading {heading!r} where the path {path!r} leads")
        start = found + 1
        end = next((j for j in range(start, end) if 0 < heading_level(lines[j]) <= level), end)
    table: list[str] = []
    for line in lines[start:end]:
        if heading_level(line):
            break
        if TABLE_LINE.match(line):
            table.append(line)
        elif table:
            break
    if len(table) < 2 or not all(DELIMITER_CELL.match(cell) for cell in split_row(table[1])):
        raise LookupError(f"{where}: no table under {path[-1]!r}")
    if len(table) < 3:
        raise LookupError(f"{where}: the table under {path[-1]!r} has no rows below its header")
    return [split_row(table[0])] + [split_row(line) for line in table[2:]]


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


def pack_folders() -> list[Path]:
    """Return every pack's folder, in name order."""
    return sorted(path for path in (REPO_ROOT / PACKS_FOLDER).iterdir() if path.is_dir())


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_every_pack_carries_the_contract() -> None:
    """At least one pack exists, and each one holds the contract the mirror copies."""
    packs = pack_folders()
    assert packs, f"no pack folder under {PACKS_FOLDER}/"
    missing = [f"{PACKS_FOLDER}/{pack.name}/{CONTRACT}" for pack in packs if not (pack / CONTRACT).is_file()]
    assert not missing, f"a pack must carry the routing contract; missing: {missing}"


@pytest.mark.parametrize("pack", [pack.name for pack in pack_folders()])
@pytest.mark.parametrize(("table", "contract_path", "mirror_path"), TABLES, ids=[t[0] for t in TABLES])
def test_the_mirror_matches_the_contract(
    pack: str, table: str, contract_path: tuple[str, ...], mirror_path: tuple[str, ...]
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


def test_every_link_form_reads_as_its_text() -> None:
    assert normalize("[`a.md`](../reference/a.md) (note)") == "`a.md` (note)"
    assert normalize("[Money guidance][p-money]") == "Money guidance"
    assert normalize("[Money guidance][]") == "Money guidance"
    assert normalize("  `a.md`,\t `b.md`  ") == "`a.md`, `b.md`"


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
    page = MIRROR_PAGE.replace("### Sessions", "### Session rows")
    with pytest.raises(LookupError, match="'### Sessions'"):
        read_table(page, TABLES[0][2], "mirror")


def test_a_heading_without_a_table_is_refused() -> None:
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\nNo table.\n\n### Parent-facing pages\n"
    with pytest.raises(LookupError, match="no table under '### Sessions'"):
        read_table(page, TABLES[0][2], "mirror")


def test_a_table_without_rows_is_refused() -> None:
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\n| Session | Insert |\n| --- | --- |\n"
    with pytest.raises(LookupError, match="no rows below its header"):
        read_table(page, TABLES[0][2], "mirror")


def test_a_fenced_heading_and_table_are_not_read() -> None:
    """A sample inside a fenced block is neither the heading nor the table."""
    fenced = "```text\n### Sessions\n\n| Session | Insert |\n| --- | --- |\n| 05 First | none |\n```\n"
    page = "## Part 2: The destination routing mirror\n\n" + fenced
    with pytest.raises(LookupError, match="'### Sessions'"):
        read_table(page, TABLES[0][2], "mirror")
    page = "## Part 2: The destination routing mirror\n\n### Sessions\n\n" + fenced.replace("### Sessions\n\n", "")
    with pytest.raises(LookupError, match="no table under '### Sessions'"):
        read_table(page, TABLES[0][2], "mirror")


def test_the_table_is_the_one_under_its_own_heading() -> None:
    """The contract's session table is read from above the parent-facing heading, not below it."""
    rows = read_table(CONTRACT_PAGE, TABLES[0][1], "contract")
    assert [row[0] for row in rows] == ["Session", "05 First", "10 Second"]
    rows = read_table(CONTRACT_PAGE, TABLES[1][1], "contract")
    assert [row[0] for row in rows] == ["Parent-facing page", "Money guidance"]
