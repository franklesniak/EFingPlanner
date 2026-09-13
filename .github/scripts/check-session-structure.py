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
2. The navigation line is present, outside every fenced block.
3. The parent metadata strip is present, outside every fenced block, and it
   carries a bullet for Status, for Estimated time, and for Parent
   involvement.
4. The six always-mandatory sections exist: Goal, Start Here, Steps, Workspace,
   Artifact Created, Stop Point.
5. Source Check exists, unless the session is exempt (see below).
6. The scaffold sections appear in the canonical relative order, Source Check
   included. The style guide numbers it seventh, and seventh is a position, not
   a label. Other sections may be interleaved freely -- Session 00 carries
   several -- but the scaffold ones may not be reordered, because the order
   *is* the scaffold.
7. No mandatory section is empty. A body that holds only whitespace, only HTML
   comments, or only a bare list marker prints as a bare heading, so it counts
   as empty.
8. No fenced code block is used as a worksheet fill-in. Worksheet forms are
   Markdown tables; a fenced block of blanks does not print as a box, does not
   become an editable cell when the page is copied into Google Docs, and does
   not reflow on a phone. A blank is a run of four or more underscores that
   starts or ends a token, which is what a child writes on; a run with word
   characters on both sides, such as ``A____B``, is part of an identifier in a
   code example and is left alone. A fence nested in a list item or a
   blockquote is still a fence; a fence line carrying anything but whitespace
   after the backticks does not close one; a fence ends with the list item or
   blockquote that holds it, as CommonMark says it does; and a fence that is
   never closed still holds what it holds.

Source Check exemptions
-----------------------
Source Check is required only when a session has a research step. Two exemptions
are recognised, both explicit and both visible in the file:

* an adult-audience marker (``<!-- audience: adult -->``), since an adult-only
  setup session is not doing child research; or
* ``<!-- no-source-check: <reason> -->``, which states why in the file itself.

Both markers must be real markers. One document scan removes every fenced block
before any structural search runs, so a marker printed inside a fenced example
is an example of a marker, not a marker. The same scan is what the navigation
search, the parent-strip search, and the heading scan read.

That scan also removes every HTML comment span, because a comment prints as
nothing: a ``## Goal`` inside ``<!-- ... -->`` is a heading the child never
sees, and a gate that counts it reports a section that is not on the page. The
two exemption markers are themselves comments, so they are searched against a
second view of the same scan, one that keeps the comments in.

Silence is never an exemption. If a session genuinely has no research step, it
says so.

Which files are read
--------------------
With no arguments the script walks ``framework/sessions``. It walks rather
than globs, and that is the load-bearing choice. A glob reports what it
matched and is silent about what it passed over, so everything it passes over
is invisible to the gate: ``Path.glob`` does not descend into a symbolic link
to a directory, does not match ``.MD`` on a case-sensitive filesystem, and
swallows the ``PermissionError`` from a directory it cannot read. Each of
those is a subtree the gate never opens while it prints ``all well-formed``.

So the walk enumerates directory entries and gives every entry it sees exactly
one disposition: checked, refused, descended into, or skipped for a stated
reason. The four are counted, and a run whose dispositions do not add up to
the number of entries seen fails rather than reports. An entry cannot go
missing without the arithmetic saying so.

Every path the walk accepts goes through one guard, as does every explicit
file argument. The guard refuses a symbolic link, refuses a Windows junction,
and refuses anything that resolves outside the repository root; all three
tests are needed, because a link is not always what ``resolve()`` catches, a
junction is not what ``is_symlink()`` catches, and a link that points back
inside the tree is caught by neither.

A refused path is a violation, not a silent skip. A gate that prints ``all
well-formed`` over a session file it declined to open is telling the reader
something it does not know, so a refusal fails the run.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The directory the default scan reads. It is a directory, not a glob,
#: because the walk below enumerates what is there and gives every entry a
#: disposition. A pattern can only report what it matched; it can never
#: report what it passed over, and what it passes over is invisible.
DEFAULT_SCAN_ROOT = "framework/sessions"

#: The extension a session file carries, compared case-insensitively. The
#: CI runner's filesystem is case-sensitive and the developer's is not, so a
#: lowercase pattern reads a different corpus in the two places. A gate that
#: checks a different set of files on CI than on the desk is not a gate.
MARKDOWN_SUFFIX = ".md"

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

#: The strip's load-bearing fields. Each pattern requires a *value* after
#: the colon, on the field's own line. A bullet reading ``- Status:`` with
#: nothing after it prints a label and no fact, so a strip made of three of
#: them tells a parent exactly as much as no strip at all.
#:
#: The character classes are exact. ``[^\S\r\n]`` is horizontal
#: whitespace only: a plain ``\s*`` would cross the line break and find
#: the *next* bullet's text, so an empty field would pass anyway. And the
#: value must hold a character that is neither whitespace nor ``*``,
#: because in ``- **Status:**`` the only thing after the colon is the
#: label's own closing emphasis, which is not a value either.
#:
#: Every one of the 15 sessions carries all
#: three, and the spec names them. They are the three facts a parent needs
#: before the child starts: is this session required, how long is it, and
#: does an adult have to be there. ``Planner skill`` and ``Materials`` are
#: not required here: Session 00 carries no ``Planner skill`` line, and a
#: session can need no materials.
PARENT_STRIP_FIELDS: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (
        field,
        re.compile(
            rf"^\s*(?:[-*+]|\d{{1,9}}[.)])\s+\*{{0,2}}{field}\*{{0,2}}"
            rf"[^\S\r\n]*:[^\r\n]*[^\s*\r\n]",
            re.IGNORECASE | re.MULTILINE,
        ),
    )
    for field in ("Status", "Estimated time", "Parent involvement")
)
HEADING_PATTERN = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")

#: A worksheet fill-in blank: a run of four or more underscores that starts
#: or ends a token. ``Total days ____``, ``Name:____`` and ``$____ per night``
#: are all blanks a child writes on. A run with word characters on both sides
#: is not one: ``A____B`` in a code example renders as code, and the rule this
#: script enforces prohibits underscore *forms*, not underscores.
WORKSHEET_BLANK_PATTERN = re.compile(r"(?<!\w)_{4,}|_{4,}(?!\w)")

#: CommonMark starts an HTML block on a line whose content begins with
#: ``<!--`` and ends it on the line that carries ``-->``. Every line of that
#: block is raw HTML, so nothing on it is a heading -- not even text after
#: the ``-->``, which prints as the literal characters the author typed.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_COMMENT_START_PATTERN = re.compile(r"^ {0,3}<!--")

#: A list marker with nothing after it. It prints as a bullet and no words.
BARE_LIST_MARKER_PATTERN = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s*$")

#: These three patterns, and the fence helpers below, are kept identical to
#: ``.github/scripts/check-prohibited-placeholders.py``. A search for
#: ``normalize_for_fence_opening`` finds every copy of the same CommonMark rule
#: in this repository, so the copies cannot drift unnoticed.
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}> ?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing> +)")

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


CONTAINER_KIND_LIST = "list"
CONTAINER_KIND_BLOCK_QUOTE = "blockquote"


@dataclass(frozen=True)
class Container:
    """A peelable Markdown container prefix on a line."""

    kind: str
    indent: int = 0


@dataclass(frozen=True)
class FenceLine:
    """A Markdown line normalized for fenced code block detection."""

    content: str
    containment_path: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ActiveFence:
    """The active fenced code block marker and containing Markdown context."""

    character: str
    minimum_length: int
    containment_path: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ListContext:
    """An active Markdown list, identified by its containment path from the root."""

    containment_path: tuple[Container, ...]


@dataclass(frozen=True)
class DocumentScan:
    """One container-aware pass over a session document.

    ``content_lines`` holds every line a reader sees as document text. Each
    line inside a fenced block, each fence marker, and each HTML comment span
    becomes an empty string, so line numbers stay the numbers in the file. The
    heading scan, the navigation search and the parent-strip search all read
    these lines. That is what makes one fence parser and one comment parser
    govern the whole check, rather than the heading scan alone.

    ``marker_lines`` holds only the lines CommonMark reads as an HTML
    comment block, because the two Source Check exemption markers *are*
    comments and nothing else is one. A marker in a fenced block, in a code
    span, behind a backslash escape, inside an HTML attribute or indented
    four spaces prints as characters on the page; it is prose *about* a
    marker, and it exempts nothing.
    """

    content_lines: tuple[str, ...]
    marker_lines: tuple[str, ...]
    worksheet_fences: tuple[int, ...]

    @property
    def text(self) -> str:
        """Return the document text a reader sees: no fences, no comments."""
        return "\n".join(self.content_lines)

    @property
    def marker_text(self) -> str:
        """Return the document text outside every fence, comments included."""
        return "\n".join(self.marker_lines)


def strip_html_comments(line: str, is_in_html_comment: bool) -> tuple[str, bool]:
    """Remove HTML comment spans from a Markdown line.

    An HTML comment prints as nothing, and it spans lines: CommonMark ends an
    HTML block opened by ``<!--`` only on the line that carries ``-->``. The
    caller threads ``is_in_html_comment`` from one line to the next, which is
    why this takes it and returns it. Kept identical to the parser in
    ``.github/scripts/check-prohibited-placeholders.py``.
    """
    uncommented_parts: list[str] = []
    index = 0

    while index < len(line):
        if is_in_html_comment:
            comment_end = line.find("-->", index)
            if comment_end == -1:
                return "".join(uncommented_parts), True
            index = comment_end + len("-->")
            is_in_html_comment = False
            continue

        comment_start = line.find("<!--", index)
        if comment_start == -1:
            uncommented_parts.append(line[index:])
            break

        uncommented_parts.append(line[index:comment_start])
        comment_end = line.find("-->", comment_start + len("<!--"))
        if comment_end == -1:
            is_in_html_comment = True
            break
        index = comment_end + len("-->")

    return "".join(uncommented_parts), is_in_html_comment


def count_leading_spaces(line: str) -> int:
    """Return the number of leading space characters in a line."""
    return len(line) - len(line.lstrip(" "))


def peel_containers(line: str, path: tuple[Container, ...]) -> tuple[str, int]:
    """Peel container prefixes from ``line`` in order; return ``(remaining, peeled)``."""
    for index, container in enumerate(path):
        if container.kind == CONTAINER_KIND_LIST:
            if count_leading_spaces(line) < container.indent:
                return line, index
            line = line[container.indent :]
        else:
            match = BLOCK_QUOTE_PREFIX_PATTERN.match(line)
            if match is None:
                return line, index
            line = line[match.end() :]
    return line, len(path)


def prune_inactive_list_contexts(line: str, list_contexts: list[ListContext]) -> None:
    """Drop active list contexts that a nonblank Markdown line has outdented past."""
    if not line.strip():
        return

    while list_contexts:
        top = list_contexts[-1]
        remaining, peeled_count = peel_containers(line, top.containment_path)
        if peeled_count == len(top.containment_path):
            return
        if not remaining.strip():
            return
        failed_container = top.containment_path[peeled_count]
        if (
            failed_container.kind == CONTAINER_KIND_LIST
            and BLOCK_QUOTE_PREFIX_PATTERN.match(remaining) is not None
        ):
            return
        list_contexts.pop()


def list_content_indent(match: re.Match[str]) -> int:
    """Return the list-item content indent relative to the marker's parent interior."""
    marker_end_column = match.end("marker")
    spacing_width = len(match.group("spacing"))
    content_padding = spacing_width if spacing_width <= 4 else 1
    return marker_end_column + content_padding


def normalize_for_fence_opening(line: str, list_contexts: list[ListContext]) -> FenceLine:
    """Return a line normalized to its current Markdown container content column."""
    prune_inactive_list_contexts(line, list_contexts)

    active_path = list_contexts[-1].containment_path if list_contexts else ()
    relative_line, peeled_count = peel_containers(line, active_path)
    effective_path = active_path[:peeled_count]

    extras: list[Container] = []
    while True:
        match = BLOCK_QUOTE_PREFIX_PATTERN.match(relative_line)
        if match is None:
            break
        extras.append(Container(kind=CONTAINER_KIND_BLOCK_QUOTE))
        relative_line = relative_line[match.end() :]

    list_match = LIST_ITEM_PATTERN.match(relative_line)
    if list_match is not None:
        content_indent_rel = list_content_indent(list_match)
        extras.append(Container(kind=CONTAINER_KIND_LIST, indent=content_indent_rel))
        relative_line = (
            relative_line[content_indent_rel:] if len(relative_line) >= content_indent_rel else ""
        )
        list_contexts.append(ListContext(containment_path=effective_path + tuple(extras)))

    return FenceLine(content=relative_line, containment_path=effective_path + tuple(extras))


def normalize_for_fence_closing(line: str, active_fence: ActiveFence) -> str:
    """Return a fenced-block line normalized to the opening fence's container."""
    peeled, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count < len(active_fence.containment_path):
        return line
    return peeled


def fence_container_ended(line: str, active_fence: ActiveFence) -> bool:
    """Return whether ``line`` has left the container holding the open fence.

    CommonMark ends a fenced block at the end of its containing block when no
    closing fence is found, so a fence opened inside a list item or a
    blockquote does not run to the end of the document once the document
    outdents past that container. A nonblank line that does not peel to the
    fence's container has left it. A blank line has left a blockquote, which a
    blank line ends, but not a list item, where a blank line is ordinary
    content. Kept identical to the helper in
    ``.github/scripts/check-prohibited-placeholders.py``.
    """
    _, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count == len(active_fence.containment_path):
        return False
    if line.strip():
        return True
    return active_fence.containment_path[peeled_count].kind == CONTAINER_KIND_BLOCK_QUOTE


def parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the opening fence marker character and length, if present."""
    match = FENCE_OPEN_PATTERN.match(line)
    if match is None:
        return None

    marker = match.group("marker")
    return marker[0], len(marker)


def is_closing_fence(line: str, fence_character: str, minimum_length: int) -> bool:
    """Return whether a line closes the active fenced code block.

    CommonMark closes a fenced block only on a fence of the same character that
    is at least as long as the opening fence and that carries nothing but
    whitespace after it. An info string does not close a block, and trailing
    prose does not close one either.
    """
    closing_pattern = re.compile(rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}\s*$")
    return closing_pattern.match(line) is not None


def fence_holds_worksheet(fence_lines: Sequence[str]) -> bool:
    """Return whether the body of one fenced block reads as a worksheet fill-in."""
    return any(WORKSHEET_BLANK_PATTERN.search(line) for line in fence_lines)


def scan_document(text: str) -> DocumentScan:
    """Return the text outside every fence, and the worksheet fences in the document.

    One pass, one fence parser. A fenced block is found where Markdown finds
    one, which includes a block nested in a list item or a blockquote. The
    container machinery above is the machinery
    ``check-prohibited-placeholders.py`` uses, under the same names.
    """
    content_lines: list[str] = []
    marker_lines: list[str] = []
    worksheet_fences: list[int] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    is_in_html_comment = False
    fence_start = 0
    buffer: list[str] = []

    for number, raw_line in enumerate(text.split("\n"), start=1):
        if active_fence is not None and fence_container_ended(raw_line, active_fence):
            # The list item or blockquote holding the fence has ended, so the
            # fence ended with it and this line is document text again.
            if fence_holds_worksheet(buffer):
                worksheet_fences.append(fence_start)
            active_fence = None
            buffer = []

        if active_fence is not None:
            closing_line = normalize_for_fence_closing(raw_line, active_fence)
            if is_closing_fence(
                closing_line, active_fence.character, active_fence.minimum_length
            ):
                if fence_holds_worksheet(buffer):
                    worksheet_fences.append(fence_start)
                active_fence = None
                buffer = []
            else:
                buffer.append(closing_line)
            content_lines.append("")
            marker_lines.append("")
            continue

        was_in_html_comment = is_in_html_comment
        visible_line, is_in_html_comment = strip_html_comments(raw_line, was_in_html_comment)
        # Fence detection reads the span-stripped line, because the sibling
        # hook reads it that way and the two must not disagree about which
        # fences exist. The structural searches read less: a whole HTML block
        # line carries no heading, even after its ``-->``.
        in_html_block = was_in_html_comment or (
            HTML_BLOCK_COMMENT_START_PATTERN.match(raw_line) is not None
        )

        opening_fence_line = normalize_for_fence_opening(visible_line, list_contexts)
        opening_fence = parse_opening_fence(opening_fence_line.content)
        if opening_fence is not None:
            character, minimum_length = opening_fence
            active_fence = ActiveFence(
                character=character,
                minimum_length=minimum_length,
                containment_path=opening_fence_line.containment_path,
            )
            fence_start = number
            buffer = []
            content_lines.append("")
            marker_lines.append("")
            continue

        content_lines.append("" if in_html_block else visible_line)
        # A marker is a marker only where CommonMark reads it as a comment.
        # Keeping only HTML-block lines states that positively, so this does
        # not have to subtract code spans, backslash escapes, HTML
        # attributes and indented code one context at a time.
        marker_lines.append(raw_line if in_html_block else "")

    if active_fence is not None and fence_holds_worksheet(buffer):
        worksheet_fences.append(fence_start)

    return DocumentScan(tuple(content_lines), tuple(marker_lines), tuple(worksheet_fences))


def find_headings(scan: DocumentScan) -> list[Heading]:
    """Return every heading, at every level, from outside every fenced block.

    Every heading the checker looks at comes from here, the session title
    included. One fence parser means one behaviour: a heading inside a fenced
    example is an example, whether it is a ``# Session NN`` title or a
    ``## Stop Point`` section.
    """
    headings: list[Heading] = []

    for number, line in enumerate(scan.content_lines, start=1):
        heading_match = HEADING_PATTERN.match(line)
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


def parent_strip_body(
    content_lines: tuple[str, ...], headings: list[Heading], label_line: int
) -> str:
    """Return the parent strip: the label line, to the next heading.

    The strip sits between the label and the first section, so the first
    heading after the label is where it stops. A document with no heading after
    the label gives the rest of the document, which is the safe direction: the
    checker then looks at more text, not less.
    """
    end = len(content_lines)
    for heading in headings:
        if heading.line_number > label_line:
            end = heading.line_number - 1
            break
    return "\n".join(content_lines[label_line - 1 : end])


def renders_as_content(body: str) -> bool:
    """Return whether a section body puts anything on the page.

    Whitespace, an HTML comment such as ``<!-- markdownlint-disable -->``, and
    a list marker with no words after it all print as nothing. A section that
    holds only those is empty to the child, whatever the file holds.
    """
    is_in_html_comment = False
    for line in body.split("\n"):
        visible, is_in_html_comment = strip_html_comments(line, is_in_html_comment)
        if not visible.strip():
            continue
        if BARE_LIST_MARKER_PATTERN.match(visible):
            continue
        return True
    return False


def check_text(text: str, display_path: str, file_name: str) -> list[Violation]:
    """Return every structural violation in one session document."""
    violations: list[Violation] = []

    scan = scan_document(text)
    content = scan.text

    headings = find_headings(scan)
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
        if name_match is None:
            violations.append(
                Violation(
                    display_path,
                    first_heading.line_number,
                    "the filename does not start with a two-digit session number, so the "
                    "title cannot be checked against it. Name the file NN_short_title.md, "
                    "matching every other session.",
                )
            )
        elif name_match.group("number") != title_match.group("number"):
            violations.append(
                Violation(
                    display_path,
                    first_heading.line_number,
                    f"title says Session {title_match.group('number')} but the filename says "
                    f"Session {name_match.group('number')}. They must agree.",
                )
            )

    if NAV_PATTERN.search(content) is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no navigation line. Every session starts with "You are here: ..." so a child '
                "can see where they are in the sequence.",
            )
        )

    strip_match = PARENT_STRIP_PATTERN.search(content)
    if strip_match is None:
        violations.append(
            Violation(
                display_path,
                1,
                'no parent metadata strip. Every session carries a "**For parents:**" strip '
                "near the top with status, time, and involvement.",
            )
        )
    else:
        label_line = content.count("\n", 0, strip_match.start()) + 1
        strip = parent_strip_body(scan.content_lines, headings, label_line)
        missing = [name for name, pattern in PARENT_STRIP_FIELDS if pattern.search(strip) is None]
        if missing:
            violations.append(
                Violation(
                    display_path,
                    label_line,
                    'the "**For parents:**" strip has no bullet for these fields: '
                    + ", ".join(missing)
                    + ". A label with no fields under it tells a parent nothing. Give "
                    "one bullet for each of Status, Estimated time, and Parent "
                    "involvement.",
                )
            )

    section_headings = [heading for heading in headings if heading.level == 2]
    titles = [heading.title for heading in section_headings]

    for section in MANDATORY_SECTIONS:
        if section not in titles:
            violations.append(
                Violation(display_path, 1, f'missing mandatory section "## {section}".')
            )

    exempt = bool(AUDIENCE_ADULT_PATTERN.search(scan.marker_text)) or bool(
        NO_SOURCE_CHECK_PATTERN.search(scan.marker_text)
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
        if not renders_as_content(section_body(text, section_headings, index)):
            violations.append(
                Violation(
                    display_path,
                    heading.line_number,
                    f'section "## {heading.title}" is empty.',
                )
            )

    for number in scan.worksheet_fences:
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
class SkippedEntry:
    """One directory entry the walk saw, did not check, and will not fail on.

    A skip is a decision, not an omission. It is recorded so that the walk can
    prove every entry it saw received exactly one disposition; a file that is
    simply not Markdown is the only thing that lands here.
    """

    display_path: str
    reason: str


@dataclass
class WalkTally:
    """How many directory entries the walk saw, and what became of each.

    The four dispositions are exhaustive and mutually exclusive by
    construction. ``balances`` is the reconciliation: if it is ever false, an
    entry was seen and then lost, which is the shape of every silent gate hole
    this checker has had.
    """

    seen: int = 0
    checked: int = 0
    refused: int = 0
    descended: int = 0
    skipped: int = 0

    def balances(self) -> bool:
        """Return whether every entry seen received exactly one disposition."""
        return self.seen == self.checked + self.refused + self.descended + self.skipped


@dataclass(frozen=True)
class ScanTargets:
    """The session files to read, the refusals that must fail the run, and the
    entries deliberately passed over."""

    paths: tuple[Path, ...]
    refusals: tuple[Violation, ...]
    skipped: tuple[SkippedEntry, ...] = ()


def display_name(path: Path, root: Path, fallback: str) -> str:
    """Return the repo-relative name of a path, or ``fallback`` when it is outside."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return fallback


def guard_path(path: Path, root: Path, label: str) -> Violation | None:
    """Return a refusal for a path that is a link, or that resolves outside ``root``.

    ``root`` is already resolved. All three halves matter. ``Path.resolve()``
    follows symbolic links *and* Windows junctions, so the containment test is
    what enforces the boundary; the ``is_symlink()`` test refuses a link even
    when it points back inside the tree, which is what
    ``check-prohibited-placeholders.py`` already does for its own inputs; and
    ``is_junction()`` catches the Windows reparse point that ``is_symlink()``
    reports as an ordinary directory. The junction test is not decoration: the
    walk descends into directories, and a junction pointing at one of its own
    ancestors would otherwise make it descend forever.
    """
    if path.is_symlink() or path.is_junction():
        return Violation(
            label,
            1,
            "symbolic link or junction, not a real file. A session file must be a real "
            "file in the repository, because a link can point at content outside the "
            "allowlisted tree, and a linked directory is a subtree this run would "
            "otherwise never open. Refusing to read it.",
        )
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return Violation(
            label, 1, "resolves outside the repository root. Refusing to read it."
        )
    return None


def walk_session_directory(
    directory: Path,
    root: Path,
    paths: list[Path],
    refusals: list[Violation],
    skipped: list[SkippedEntry],
    tally: WalkTally,
) -> None:
    """Enumerate one directory tree, dispositioning every entry it holds.

    This exists instead of ``Path.glob`` / ``Path.rglob`` because a pattern
    answers only "what matched". Three things a pattern passes over in silence
    have each been a hole in this gate:

    * a **symbolic link to a directory**, which ``**`` does not descend into,
      so the whole linked subtree is never read;
    * an **uppercase ``.MD``**, which a lowercase pattern does not match on the
      case-sensitive filesystem CI runs on, though it matches on the
      developer's case-insensitive one; and
    * a **directory the process cannot read**, whose ``PermissionError``
      ``glob`` swallows, so an unreadable subtree reads as an empty one.

    None of the three can hide from an enumeration that must account for every
    entry it saw. Directories are descended into, Markdown files are checked,
    links and escapes are refused, and anything else is skipped for a reason
    that is written down. ``tally`` counts the four so the caller can prove
    they add up.
    """
    try:
        entries = sorted(directory.iterdir(), key=lambda entry: entry.name)
    except FileNotFoundError:
        # Not there at all. The zero-target guard in collect_targets reports
        # that this run checked nothing, which is the accurate thing to say
        # and the message that names the setting to fix.
        return
    except OSError as error:
        # A directory that cannot be listed is not an empty directory, and
        # this is exactly where glob() would have returned nothing instead.
        refusals.append(
            Violation(
                display_name(directory, root, directory.as_posix()),
                1,
                f"could not be read ({error.strerror}), so this run does not know what "
                "is inside it. An unreadable directory is not an empty one; refusing "
                "to report a clean corpus for a subtree that was never listed.",
            )
        )
        return

    for entry in entries:
        tally.seen += 1
        label = display_name(entry, root, entry.as_posix())

        refusal = guard_path(entry, root, label)
        if refusal is not None:
            refusals.append(refusal)
            tally.refused += 1
            continue

        if entry.is_dir():
            tally.descended += 1
            walk_session_directory(entry, root, paths, refusals, skipped, tally)
            continue

        if entry.is_file() and entry.suffix.lower() == MARKDOWN_SUFFIX:
            paths.append(entry)
            tally.checked += 1
            continue

        skipped.append(SkippedEntry(label, "not a Markdown file"))
        tally.skipped += 1


def collect_targets(path_arguments: Sequence[str], root: Path) -> ScanTargets:
    """Turn command-line arguments into session Markdown paths, refusing escapes.

    Every path the checker reads passes through here: the default walk, the
    walk of a directory argument, and an explicit file argument alike.
    Validating only the explicit arguments would leave the one path CI
    actually uses -- the default walk -- unguarded.
    """
    root = root.resolve()
    paths: list[Path] = []
    refusals: list[Violation] = []
    skipped: list[SkippedEntry] = []
    tally = WalkTally()

    if not path_arguments:
        walk_session_directory(
            root / DEFAULT_SCAN_ROOT, root, paths, refusals, skipped, tally
        )
    else:
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
                walk_session_directory(candidate, root, paths, refusals, skipped, tally)
            elif candidate.is_file() and candidate.suffix.lower() == MARKDOWN_SUFFIX:
                paths.append(candidate)
            else:
                # The argument survived the guard but names nothing this checker
                # can read: a path that does not exist, or a file that is not
                # Markdown.
                refusals.append(
                    Violation(
                        display_name(candidate, root, argument),
                        1,
                        "not a Markdown file or a directory, so there is nothing to "
                        "check. Check the path: a typo here would otherwise pass "
                        "silently, because a run that checks nothing reports no "
                        "problems.",
                    )
                )

    if not tally.balances():
        # The reconciliation. Every entry the walk saw is checked, refused,
        # descended into, or skipped for a reason; the four are exhaustive by
        # construction, so they can only fail to add up if a future edit
        # introduces a fifth, silent outcome. That is the shape of every hole
        # this gate has had, so it fails the run rather than reporting one.
        refusals.append(
            Violation(
                DEFAULT_SCAN_ROOT if not path_arguments else " ".join(path_arguments),
                1,
                f"the walk saw {tally.seen} directory entr(ies) but accounted for "
                f"{tally.checked + tally.refused + tally.descended + tally.skipped} "
                "of them. An entry that is neither checked, refused, descended into, "
                "nor skipped for a stated reason has gone missing, and this run "
                "cannot say what is in the corpus.",
            )
        )

    if not paths and not refusals:
        # One guard for every shape of the same mistake: the run was asked for
        # something and opened nothing. An empty directory, a directory holding
        # no Markdown, and a scan root that has moved all land here, so none of
        # them can report a clean corpus that was never read.
        requested = " ".join(path_arguments) if path_arguments else DEFAULT_SCAN_ROOT
        refusals.append(
            Violation(
                requested,
                1,
                "matched no session file, so this run checked nothing. A run that "
                "opens no file has no evidence that anything is well-formed. Check "
                "the path, or check DEFAULT_SCAN_ROOT if this was the default scan.",
            )
        )

    return ScanTargets(tuple(paths), tuple(refusals), tuple(skipped))


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[Path]:
    """Return the session Markdown paths the checker will read."""
    return list(collect_targets(path_arguments, root).paths)


def check_targets(targets: ScanTargets, root: Path) -> list[Violation]:
    """Check every collected session file and return all violations."""
    violations: list[Violation] = list(targets.refusals)
    resolved_root = root.resolve()
    for path in targets.paths:
        # guard_path has already proved this path resolves inside the root.
        display_path = path.resolve().relative_to(resolved_root).as_posix()
        text = path.read_text(encoding="utf-8")
        violations.extend(check_text(text, display_path, path.name))
    return violations


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[Violation]:
    """Check every named session file and return all violations."""
    return check_targets(collect_targets(path_arguments, root), root)


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
    # One traversal feeds both the verdict and the count. Counting from a
    # second walk lets the report name a number the verdict never looked at.
    targets = collect_targets(args.paths, root)
    violations = check_targets(targets, root)

    for violation in violations:
        print(violation.format_message())

    checked = len(targets.paths)
    # A skip that is recorded but never printed is still an entry the reader
    # does not know about, so the count of skips rides along with the verdict.
    passed_over = (
        f" {len(targets.skipped)} entr(ies) skipped as not Markdown."
        if targets.skipped
        else ""
    )
    if violations:
        print(
            f"\nSession structure: {checked} file(s) checked, "
            f"{len(violations)} problem(s).{passed_over}"
        )
        return 1

    print(f"Session structure: {checked} file(s) checked, all well-formed.{passed_over}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
