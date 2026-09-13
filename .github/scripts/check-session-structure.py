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
1. The title line is ``# Session NN: Title``, and ``NN`` matches the filename.
2. The navigation line is present.
3. The parent metadata strip is present.
4. The six always-mandatory sections exist: Goal, Start Here, Steps, Workspace,
   Artifact Created, Stop Point.
5. Source Check exists, unless the session is exempt (see below).
6. Those mandatory sections appear in the canonical relative order. Other
   sections may be interleaved freely -- Session 00 carries several -- but the
   mandatory ones may not be reordered, because the order *is* the scaffold.
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
import sys
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

TITLE_PATTERN = re.compile(r"^#\s+Session\s+(?P<number>\d{2}):\s+\S.*$", re.MULTILINE)
FILENAME_NUMBER_PATTERN = re.compile(r"^(?P<number>\d{2})[_-]")
NAV_PATTERN = re.compile(r"^You are here:\s*\S", re.MULTILINE)
PARENT_STRIP_PATTERN = re.compile(r"^\*\*For parents:?\*\*", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^##\s+(?P<title>.+?)\s*$", re.MULTILINE)
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


def line_of(text: str, index: int) -> int:
    """Return the 1-based line number of a character offset."""
    return text.count("\n", 0, index) + 1


def find_headings(text: str) -> list[tuple[str, int]]:
    """Return every level-2 heading as (title, line number), skipping fenced blocks."""
    headings: list[tuple[str, int]] = []
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

        heading_match = re.match(r"^##\s+(?P<title>.+?)\s*$", raw_line)
        if heading_match:
            headings.append((heading_match.group("title"), number))

    return headings


def section_body(text: str, headings: list[tuple[str, int]], index: int) -> str:
    """Return the text between one heading and the next."""
    lines = text.split("\n")
    start = headings[index][1]
    end = headings[index + 1][1] - 1 if index + 1 < len(headings) else len(lines)
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

    title_match = TITLE_PATTERN.search(text)
    if title_match is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no session title. The first heading must read "# Session NN: Title".',
            )
        )
    else:
        name_match = FILENAME_NUMBER_PATTERN.match(file_name)
        if name_match and name_match.group("number") != title_match.group("number"):
            violations.append(
                Violation(
                    display_path,
                    line_of(text, title_match.start()),
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

    headings = find_headings(text)
    titles = [title for title, _ in headings]

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

    present = [t for t in titles if t in MANDATORY_SECTIONS]
    expected = [s for s in MANDATORY_SECTIONS if s in titles]
    if present != expected:
        violations.append(
            Violation(
                display_path,
                headings[0][1] if headings else 1,
                "mandatory sections are out of order. Found "
                f"{' > '.join(present)}; expected {' > '.join(expected)}. Other sections may sit "
                "between them, but these may not be reordered.",
            )
        )

    for index, (title, number) in enumerate(headings):
        if title not in MANDATORY_SECTIONS and title != SOURCE_CHECK_SECTION:
            continue
        if not section_body(text, headings, index):
            violations.append(
                Violation(display_path, number, f'section "## {title}" is empty.')
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


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[Path]:
    """Turn command-line arguments into session Markdown paths."""
    if not path_arguments:
        return sorted(p for p in root.glob(DEFAULT_SCAN_GLOB) if p.is_file())

    resolved: list[Path] = []
    for argument in path_arguments:
        candidate = Path(argument)
        if not candidate.is_absolute():
            candidate = root / candidate
        candidate = candidate.resolve()
        try:
            candidate.relative_to(root.resolve())
        except ValueError:
            print(
                f"{argument}: outside the repository root; refusing to read it.",
                file=sys.stderr,
            )
            continue
        if candidate.is_dir():
            resolved.extend(sorted(p for p in candidate.rglob("*.md") if p.is_file()))
        elif candidate.is_file() and candidate.suffix.lower() == ".md":
            resolved.append(candidate)
    return resolved


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[Violation]:
    """Check every named session file and return all violations."""
    violations: list[Violation] = []
    for path in resolve_paths(path_arguments, root):
        try:
            display_path = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            display_path = path.as_posix()
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
