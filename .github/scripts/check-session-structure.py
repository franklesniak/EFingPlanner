"""Check that every curriculum session carries its mandatory structure.

A session is the unit a child actually sits down with, and its shape is load
bearing rather than cosmetic. The seven mandatory fields are what make a session
startable and, more importantly, *stoppable*: a child with executive-function
difficulty needs to know where to begin, what they are making, and when they are
allowed to be finished. A session missing its Stop Point is not a stylistic
lapse; it is a session that never ends.

The style guide states the rule. This script enforces it, because the curriculum
grows to dozens of sessions and a human will not reliably notice the one that
lost its Workspace heading in an edit.

What is checked
---------------
1. The first heading in the document -- outside every fenced block -- is
   ``# Session NN: Title``, and ``NN`` matches the filename.
2. The navigation line is present.
3. The parent metadata strip is present.
4. The six always-mandatory sections exist: Goal, Start Here, Steps, Workspace,
   Artifact Created, Stop Point.
5. Source Check exists, unless the session is exempt (see below).
6. The scaffold sections appear in the canonical relative order, Source Check
   included. The style guide numbers it seventh, and seventh is a position, not
   a label. Other sections may be interleaved freely -- Session 00 carries
   several -- but the scaffold ones may not be reordered, because the order
   *is* the scaffold.
7. No mandatory section is empty.
8. No fenced code block is used as a worksheet fill-in. Worksheet forms are
   Markdown tables; a fenced block of underscores does not print as a box, does
   not become an editable cell when the page is copied into Google Docs, and
   does not reflow on a phone.

Source Check exemptions
-----------------------
Source Check is required only when a session has a research step. Two exemptions
are recognised, both explicit and both visible in the file:

* an adult-audience marker (``<!-- audience: adult -->``), since an adult-only
  setup session is not doing child research; or
* ``<!-- no-source-check: <reason> -->``, which states why in the file itself.

Silence is never an exemption. If a session genuinely has no research step, it
says so.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DEFAULT_SCAN_GLOB = "framework/sessions/**/*.md"

#: The six sections every session carries, in the order they must appear.
MANDATORY_SECTIONS = (
    "Goal",
    "Start Here",
    "Steps",
    "Workspace",
    "Artifact Created",
    "Stop Point",
)

#: The seventh, required only when the session has a research step.
SOURCE_CHECK_SECTION = "Source Check"

#: Every scaffold section, in the order it must appear. Source Check is
#: conditional in *presence* -- a session with no research step does not carry
#: it -- but not in *position*. A session that carries it puts it seventh.
ORDERED_SECTIONS = MANDATORY_SECTIONS + (SOURCE_CHECK_SECTION,)

#: Matches the *title text* of a heading, not the heading line. The leading
#: hashes are consumed by HEADING_PATTERN, so there is one heading parser.
TITLE_PATTERN = re.compile(r"^Session\s+(?P<number>\d{2}):\s+\S")
FILENAME_NUMBER_PATTERN = re.compile(r"^(?P<number>\d{2})[_-]")
NAV_PATTERN = re.compile(r"^You are here:\s*\S", re.MULTILINE)
PARENT_STRIP_PATTERN = re.compile(r"^\*\*For parents:?\*\*", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")
FENCE_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})", re.MULTILINE)
UNDERSCORE_RUN_PATTERN = re.compile(r"_{4,}")

AUDIENCE_ADULT_PATTERN = re.compile(
    r"<!--\s*audience:\s*(?:adult|parent|builder)\b.*?-->", re.IGNORECASE
)
NO_SOURCE_CHECK_PATTERN = re.compile(r"<!--\s*no-source-check:\s*\S.*?-->", re.IGNORECASE)


@dataclass(frozen=True)
class Violation:
    """One structural problem in one session file."""

    display_path: str
    line_number: int
    message: str

    def format_message(self) -> str:
        """Return the failure line for this violation."""
        return f"{self.display_path}:{self.line_number}: {self.message}"


@dataclass(frozen=True)
class Heading:
    """One ATX heading, found outside every fenced block."""

    level: int
    title: str
    line_number: int


def find_headings(text: str) -> list[Heading]:
    """Return every heading, at every level, skipping fenced blocks.

    Every heading the checker looks at comes from here, the session title
    included. One fence parser means one behaviour: a heading inside a fenced
    example is an example, whether it is a ``# Session NN`` title or a
    ``## Stop Point`` section.
    """
    headings: list[Heading] = []
    active_fence: str | None = None

    for number, raw_line in enumerate(text.split("\n"), start=1):
        fence_match = FENCE_PATTERN.match(raw_line)
        if fence_match:
            marker = fence_match.group("marker")
            if active_fence is None:
                active_fence = marker
            elif marker[0] == active_fence[0] and len(marker) >= len(active_fence):
                active_fence = None
            continue
        if active_fence is not None:
            continue

        heading_match = HEADING_PATTERN.match(raw_line)
        if heading_match:
            headings.append(
                Heading(
                    level=len(heading_match.group("hashes")),
                    title=heading_match.group("title"),
                    line_number=number,
                )
            )

    return headings


def section_body(text: str, headings: list[Heading], index: int) -> str:
    """Return the text between one section heading and the next."""
    lines = text.split("\n")
    start = headings[index].line_number
    end = (
        headings[index + 1].line_number - 1 if index + 1 < len(headings) else len(lines)
    )
    return "\n".join(lines[start:end]).strip()


def find_worksheet_fences(text: str) -> list[int]:
    """Return the line numbers of fenced blocks used as underscore fill-ins."""
    offenders: list[int] = []
    active_fence: str | None = None
    fence_start = 0
    buffer: list[str] = []

    for number, raw_line in enumerate(text.split("\n"), start=1):
        fence_match = FENCE_PATTERN.match(raw_line)
        if fence_match:
            marker = fence_match.group("marker")
            if active_fence is None:
                active_fence = marker
                fence_start = number
                buffer = []
            elif marker[0] == active_fence[0] and len(marker) >= len(active_fence):
                if any(UNDERSCORE_RUN_PATTERN.search(line) for line in buffer):
                    offenders.append(fence_start)
                active_fence = None
            continue
        if active_fence is not None:
            buffer.append(raw_line)

    return offenders


def check_text(text: str, display_path: str, file_name: str) -> list[Violation]:
    """Return every structural violation in one session document."""
    violations: list[Violation] = []

    headings = find_headings(text)
    first_heading = headings[0] if headings else None
    title_match = (
        TITLE_PATTERN.match(first_heading.title)
        if first_heading is not None and first_heading.level == 1
        else None
    )

    if title_match is None:
        violations.append(
            Violation(
                display_path,
                first_heading.line_number if first_heading is not None else 1,
                "no session title. The first heading in the document must read "
                '"# Session NN: Title". A title inside a fenced example is an example, '
                "not the name of the session.",
            )
        )
    else:
        name_match = FILENAME_NUMBER_PATTERN.match(file_name)
        if name_match and name_match.group("number") != title_match.group("number"):
            violations.append(
                Violation(
                    display_path,
                    first_heading.line_number,
                    f"title says Session {title_match.group('number')} but the filename says "
                    f"Session {name_match.group('number')}. They must agree.",
                )
            )

    if NAV_PATTERN.search(text) is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no navigation line. Every session starts with "You are here: ..." so a child '
                "can see where they are in the sequence.",
            )
        )

    if PARENT_STRIP_PATTERN.search(text) is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no parent metadata strip. Every session carries a "**For parents:**" strip '
                "near the top with status, time, and involvement.",
            )
        )

    section_headings = [heading for heading in headings if heading.level == 2]
    titles = [heading.title for heading in section_headings]

    for section in MANDATORY_SECTIONS:
        if section not in titles:
            violations.append(
                Violation(display_path, 1, f'missing mandatory section "## {section}".')
            )

    exempt = bool(AUDIENCE_ADULT_PATTERN.search(text)) or bool(
        NO_SOURCE_CHECK_PATTERN.search(text)
    )
    if SOURCE_CHECK_SECTION not in titles and not exempt:
        violations.append(
            Violation(
                display_path,
                1,
                'missing "## Source Check". A session with a research step must carry it. If '
                "this session has no research step, say so in the file with "
                "<!-- no-source-check: reason --> rather than leaving it silent.",
            )
        )

    present = [t for t in titles if t in ORDERED_SECTIONS]
    expected = [s for s in ORDERED_SECTIONS if s in titles]
    if present != expected:
        violations.append(
            Violation(
                display_path,
                section_headings[0].line_number if section_headings else 1,
                "scaffold sections are out of order. Found "
                f"{' > '.join(present)}; expected {' > '.join(expected)}. Other sections may sit "
                "between them, but these may not be reordered.",
            )
        )

    for index, heading in enumerate(section_headings):
        if heading.title not in ORDERED_SECTIONS:
            continue
        if not section_body(text, section_headings, index):
            violations.append(
                Violation(
                    display_path,
                    heading.line_number,
                    f'section "## {heading.title}" is empty.',
                )
            )

    for number in find_worksheet_fences(text):
        violations.append(
            Violation(
                display_path,
                number,
                "fenced block used as a worksheet fill-in. Worksheet forms are Markdown tables "
                "(a two-column Prompt | Your answer form, or a narrow criteria-by-option grid). "
                "An empty table cell prints as a box, becomes an editable cell in Google Docs, "
                "and reflows on a phone; a fenced underscore block does none of those.",
            )
        )

    return violations


@dataclass(frozen=True)
class ScanTargets:
    """The session files to read, and the refusals that must fail the run."""

    paths: tuple[Path, ...]
    refusals: tuple[Violation, ...]


def display_name(path: Path, root: Path, fallback: str) -> str:
    """Return the repo-relative name of a path, or ``fallback`` when it is outside."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return fallback


def guard_path(path: Path, root: Path, label: str) -> Violation | None:
    """Return a refusal for a path that is a link, or that resolves outside ``root``.

    ``root`` is already resolved. Both halves matter. ``Path.resolve()`` follows
    symbolic links *and* Windows junctions, so the containment test is what
    enforces the boundary; the ``is_symlink()`` test refuses a link even when it
    points back inside the tree, which is what
    ``check-prohibited-placeholders.py`` already does for its own inputs.
    """
    if path.is_symlink():
        return Violation(
            label,
            1,
            "symbolic link, not a real file. A session file must be a real file in the "
            "repository, because a link can point at content outside the allowlisted "
            "tree. Refusing to read it.",
        )
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return Violation(
            label, 1, "resolves outside the repository root. Refusing to read it."
        )
    return None


def collect_targets(path_arguments: Sequence[str], root: Path) -> ScanTargets:
    """Turn command-line arguments into session Markdown paths, refusing escapes.

    Every path the checker reads passes through here: the default glob, the walk
    of a directory argument, and an explicit file argument alike. Validating only
    the explicit arguments would leave the one path CI actually uses -- the
    default glob -- unguarded.
    """
    root = root.resolve()
    paths: list[Path] = []
    refusals: list[Violation] = []

    def take(path: Path) -> None:
        """Accept one discovered path, or record why it was refused."""
        refusal = guard_path(path, root, display_name(path, root, path.as_posix()))
        if refusal is not None:
            refusals.append(refusal)
        elif path.is_file():
            paths.append(path)

    if not path_arguments:
        for path in sorted(root.glob(DEFAULT_SCAN_GLOB)):
            take(path)
        return ScanTargets(tuple(paths), tuple(refusals))

    for argument in path_arguments:
        candidate = Path(argument)
        if not candidate.is_absolute():
            candidate = root / candidate
        refusal = guard_path(candidate, root, display_name(candidate, root, argument))
        if refusal is not None:
            refusals.append(refusal)
            continue
        candidate = candidate.resolve()
        if candidate.is_dir():
            for path in sorted(candidate.rglob("*.md")):
                take(path)
        elif candidate.is_file() and candidate.suffix.lower() == ".md":
            paths.append(candidate)

    return ScanTargets(tuple(paths), tuple(refusals))


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[Path]:
    """Return the session Markdown paths the checker will read."""
    return list(collect_targets(path_arguments, root).paths)


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[Violation]:
    """Check every named session file and return all violations."""
    targets = collect_targets(path_arguments, root)
    violations: list[Violation] = list(targets.refusals)
    resolved_root = root.resolve()
    for path in targets.paths:
        # guard_path has already proved this path resolves inside the root.
        display_path = path.resolve().relative_to(resolved_root).as_posix()
        text = path.read_text(encoding="utf-8")
        violations.extend(check_text(text, display_path, path.name))
    return violations


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Check curriculum sessions for their mandatory structure. "
            "With no paths, checks every session."
        )
    )
    parser.add_argument("paths", nargs="*", help="Session files or directories to check.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the session-structure check."""
    args = parse_args(argv)
    violations = scan_files(args.paths, root=root)

    for violation in violations:
        print(violation.format_message())

    checked = len(resolve_paths(args.paths, root))
    if violations:
        print(f"\nSession structure: {checked} file(s) checked, {len(violations)} problem(s).")
        return 1

    print(f"Session structure: {checked} file(s) checked, all well-formed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
