"""The kit's copies of three blanks must not drift from the templates.

The build brief requires ``framework/trip_starter/family/`` to carry a copy of
the Trip-Basics card, the assumptions page and the trip goals page, so a family
can copy the whole kit out in one go. The kit's own README states the opposite
rule for everything else -- *"Do not keep two copies of the same thing in two
folders. Two copies drift apart, and then you do not know which one is right."*

Both are right, and the way to hold them together is a check rather than a
policy. Measured before this file existed: the Trip-Basics pair had already
drifted in the body at one commit's age, and the trip-goals pair drifted again
when the poll table grew to fit the roster -- the template gained two rows and
the kit copy did not, so a family of six could not record their poll on the page
the session sends them to.

Each kit copy is its template plus a preamble that belongs only to the kit: copy
it out before filling it in, and here is the blank it came from. Remove that
preamble and the two files must match line for line, character for character.
Line endings are not compared: ``.gitattributes`` stores every Markdown file
with LF endings, so they cannot differ once committed.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: template stem -> the kit copy that must mirror it
MIRRORED_BLANKS = {
    "trip_basics": "framework/trip_starter/family/trip_basics.md",
    "current_family_travel_assumptions": (
        "framework/trip_starter/family/current_family_travel_assumptions.md"
    ),
    "family_trip_goals": "framework/trip_starter/family/family_trip_goals.md",
}

#: The sentence that opens the kit-only preamble. It is matched in full rather
#: than by a prefix, so a reworded preamble fails loudly here instead of being
#: silently stripped and hiding a real difference underneath it.
PREAMBLE_FIRST = (
    "Copy this page out of the repository before you fill it in. Do not commit "
    "your filled-in work to a public repository."
)
#: The second preamble line names the blank, and its wording differs per file,
#: so it is matched by its opening rather than in full.
PREAMBLE_SECOND_PREFIX = "The blank this page was copied from is the ["


def strip_kit_preamble(lines: list[str]) -> list[str]:
    """Return ``lines`` without the kit-only preamble and its blank lines."""
    kept: list[str] = []
    index = 0
    removed = 0
    while index < len(lines):
        line = lines[index]
        if line == PREAMBLE_FIRST or line.startswith(PREAMBLE_SECOND_PREFIX):
            removed += 1
            index += 1
            # The blank line that follows the preamble line goes with it.
            if index < len(lines) and lines[index] == "":
                index += 1
            continue
        kept.append(line)
        index += 1
    assert removed == 2, f"expected two preamble lines, removed {removed}"
    return kept


@pytest.mark.parametrize("stem", sorted(MIRRORED_BLANKS))
def test_the_kit_copy_is_its_template_plus_the_kit_preamble(stem: str) -> None:
    """A change to one of these pages has to reach both of them."""
    template = REPO_ROOT / "framework" / "templates" / f"{stem}.md"
    copy = REPO_ROOT / MIRRORED_BLANKS[stem]
    assert template.is_file(), template
    assert copy.is_file(), copy

    template_lines = template.read_text(encoding="utf-8").split("\n")
    copy_lines = copy.read_text(encoding="utf-8").split("\n")
    assert strip_kit_preamble(copy_lines) == template_lines, (
        f"{copy.relative_to(REPO_ROOT).as_posix()} has drifted from "
        f"{template.relative_to(REPO_ROOT).as_posix()}. Edit both, or edit the "
        "template and copy it across. The kit README's own rule says two copies "
        "drift apart and then nobody knows which one is right."
    )


@pytest.mark.parametrize("stem", sorted(MIRRORED_BLANKS))
def test_the_kit_preamble_links_the_template_it_came_from(stem: str) -> None:
    """The mirror check strips the preamble's link, so this test checks it.

    A kit copy whose preamble linked a different blank would pass the mirror
    check and send a family to the wrong page.
    """
    copy = REPO_ROOT / MIRRORED_BLANKS[stem]
    lines = [
        line
        for line in copy.read_text(encoding="utf-8").split("\n")
        if line.startswith(PREAMBLE_SECOND_PREFIX)
    ]
    assert len(lines) == 1, f"expected one provenance line, found {len(lines)}"
    match = re.search(r"\]\(([^)\s]+)\)", lines[0])
    assert match, f"no link in {lines[0]!r}"
    linked = (copy.parent / match.group(1)).resolve()
    expected = (REPO_ROOT / "framework" / "templates" / f"{stem}.md").resolve()
    assert linked == expected, (
        f"{MIRRORED_BLANKS[stem]} says it was copied from {match.group(1)}, "
        f"but its template is framework/templates/{stem}.md."
    )


def test_every_mirrored_path_exists_so_the_list_cannot_rot() -> None:
    """A check that names a file which has gone is a check that stops checking."""
    for stem, relative in MIRRORED_BLANKS.items():
        assert (REPO_ROOT / "framework" / "templates" / f"{stem}.md").is_file(), stem
        assert (REPO_ROOT / relative).is_file(), relative
