"""Check Markdown docs for prohibited placeholder markers.

The pre-commit hook calls this script with candidate Markdown paths. The
checker intentionally stays dependency-free so it can run in the repo-local
hook environment on Windows, macOS, Linux, and WSL.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDER_PATTERN = re.compile(
    r"\(default[^)]*to\s+be\s+determined[^)]*\)"
    r"|\bTODO\b\s*:"
    r"|\bTBD\b"
    r"|\bFIXME\b"
    r"|\bXXX\b"
    r"|\bto\s+be\s+determined\b",
    re.IGNORECASE,
)
ALLOW_TBD_PATTERN = re.compile(r"<!--\s*ALLOW-TBD:\s*\S.*?-->", re.IGNORECASE)
ALLOWED_LABEL_PATTERN = re.compile(
    r"^\s*(?:(?:[-*+]|\d{1,9}[.)])\s+)?\*\*(?:Open Questions?|Assumption):\*\*",
    re.IGNORECASE,
)
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")

#: CommonMark starts an HTML block on a line whose *content* begins with
#: ``<!--`` and ends it on the line carrying ``-->``. Every character on
#: those lines is raw HTML, so none of them opens a fenced code block --
#: not even backticks left behind by comment stripping. Content is what is
#: left once the blockquote and list-item prefixes are consumed, which is
#: why this is matched against ``container_content`` and not against the
#: line as the file holds it. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_COMMENT_START_PATTERN = re.compile(r"^ {0,3}<!--")

#: The element names CommonMark lists for HTML block start condition 6. A
#: comment is only one of the conditions; a ``<div>`` opens a block just as
#: surely, and every line of it is raw HTML, so a line of backticks inside
#: one opens no fence. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_ELEMENT_NAMES = (
    "address|article|aside|base|basefont|blockquote|body|caption|center|col|"
    "colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|"
    "footer|form|frame|frameset|h1|h2|h3|h4|h5|h6|head|header|hr|html|iframe|"
    "legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|p|"
    "param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|"
    "track|ul"
)
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}> ?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing> +)")

REMEDIATION_HINT = (
    "replace with a measurable value, an **Open Question:** entry, an "
    "**Assumption:** entry, or a cross-reference to another requirement. "
    "To suppress with explicit justification, add <!-- ALLOW-TBD: <reason> --> "
    'on the same line. See .github/instructions/docs.instructions.md "Prohibited Patterns".'
)


@dataclass(frozen=True)
class Violation:
    """A prohibited placeholder match in a Markdown file."""

    display_path: str
    line_number: int
    matched_text: str

    def format_message(self) -> str:
        """Return the hook failure message for this placeholder match."""
        return (
            f"{self.display_path}:{self.line_number}: prohibited placeholder "
            f"{json.dumps(self.matched_text)}; {REMEDIATION_HINT}"
        )


CONTAINER_KIND_LIST = "list"
CONTAINER_KIND_BLOCK_QUOTE = "blockquote"


@dataclass(frozen=True)
class Container:
    """A peelable Markdown container prefix on a line.

    A ``list`` container consumes ``indent`` leading spaces from its parent
    container's interior. A ``blockquote`` container consumes a single
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (``>`` optionally followed by a
    space) at the start of its parent's interior; ``indent`` is unused.
    """

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
class RawHtmlBlock:
    """One CommonMark HTML block condition: how it starts and how it ends.

    ``end`` is the pattern that closes the block on the line carrying it, or
    ``None`` for the conditions a blank line closes; the blank line itself is
    outside the block. Condition 2, the comment, is tracked by the comment
    parser above instead. Condition 7 -- any complete tag alone on a line --
    is deliberately absent, because it is the one condition that may not
    interrupt a paragraph and this scan keeps no paragraph state. Kept
    identical to the record in
    ``.github/scripts/check-session-structure.py``.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """

    name: str
    start: re.Pattern[str]
    end: re.Pattern[str] | None


RAW_HTML_BLOCKS: tuple[RawHtmlBlock, ...] = (
    RawHtmlBlock(
        "script",
        re.compile(r"^ {0,3}<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.IGNORECASE),
        re.compile(r"</(?:script|pre|style|textarea)>", re.IGNORECASE),
    ),
    RawHtmlBlock("instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    RawHtmlBlock("cdata", re.compile(r"^ {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    RawHtmlBlock("declaration", re.compile(r"^ {0,3}<![A-Za-z]"), re.compile(r">")),
    RawHtmlBlock(
        "element",
        re.compile(
            rf"^ {{0,3}}</?(?:{HTML_BLOCK_ELEMENT_NAMES})(?:[ \t>]|/>|$)",
            re.IGNORECASE,
        ),
        None,
    ),
)


@dataclass(frozen=True)
class ListContext:
    """An active Markdown list, identified by its full containment path from the document root."""

    containment_path: tuple[Container, ...]


class FileReadError(RuntimeError):
    """Raised when a candidate Markdown file cannot be read."""

    def __init__(self, display_path: str, error: OSError) -> None:
        error_summary = f"{type(error).__name__}: {error.strerror or 'I/O error'}"
        super().__init__(f"{display_path}: unable to read file ({error_summary})")


def is_changelog_file(path: Path) -> bool:
    """Return whether the file name matches the hook's changelog exemption."""
    name = path.name.lower()
    return name.startswith("changelog") and name.endswith(".md")


# Repo-relative top-level directories whose Markdown the hook guards. docs/ holds
# reference and design material (docs/spec/ is excluded by the pre-commit `exclude`
# pattern); framework/ and destinations/ hold the built curriculum.
SCAN_TARGET_ROOTS = ("docs", "framework", "destinations")


def is_scan_target(relative_path: Path) -> bool:
    """Return whether a repo-relative path is a curriculum or docs Markdown scan target."""
    return (
        len(relative_path.parts) >= 2
        and relative_path.parts[0] in SCAN_TARGET_ROOTS
        and relative_path.suffix.lower() == ".md"
        and not is_changelog_file(relative_path)
    )


def resolve_candidate_path(path_argument: str | Path, root: Path) -> tuple[Path, str] | None:
    """Resolve a pre-commit path argument to a contained scan target."""
    root = root.resolve()
    path = Path(path_argument)
    candidate = path if path.is_absolute() else root / path

    if candidate.is_symlink() or not candidate.is_file():
        return None

    resolved_candidate = candidate.resolve()
    try:
        relative_path = resolved_candidate.relative_to(root)
    except ValueError:
        return None

    if not is_scan_target(relative_path):
        return None

    return resolved_candidate, relative_path.as_posix()


def strip_html_comments(line: str, is_in_html_comment: bool) -> tuple[str, bool]:
    """Remove HTML comment spans from a Markdown line."""
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
    """Peel container prefixes from ``line`` in order; return ``(remaining, peeled_count)``.

    A list container consumes ``container.indent`` leading spaces (or fails if
    the line has fewer). A blockquote container consumes one
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (or fails if the line does not start
    with one in its current coordinate system). Peeling stops at the first
    container that cannot be consumed; the caller can compare ``peeled_count``
    to ``len(path)`` to detect partial peels.
    """
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
        # The line did not peel cleanly to this list's interior. Decide
        # whether the partial peel still keeps the list active.
        if not remaining.strip():
            # A blank line inside a partly-peeled container is a continuation.
            return
        failed_container = top.containment_path[peeled_count]
        if (
            failed_container.kind == CONTAINER_KIND_LIST
            and BLOCK_QUOTE_PREFIX_PATTERN.match(remaining) is not None
        ):
            # A deeper blockquote nested inside the list keeps the list active;
            # the list's content indent is not meaningful in that deeper
            # coordinate system.
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

    return FenceLine(
        content=relative_line,
        containment_path=effective_path + tuple(extras),
    )


def container_content(line: str, list_contexts: list[ListContext]) -> str:
    """Return what CommonMark reads on a line, container prefixes peeled off.

    A line's block type -- an HTML block among them -- is decided from what is
    left once the blockquote and list-item prefixes are consumed, so
    ``> <!-- a comment -->`` opens an HTML block exactly as the unindented form
    does. The list contexts are copied because this asks a question about one
    line rather than advancing the document: the contexts that govern the rest
    of the file are the ones the fence normalization takes below, from the
    span-stripped line. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
    """
    return normalize_for_fence_opening(line, list(list_contexts)).content


def raw_html_block_state(
    content: str, open_block: RawHtmlBlock | None
) -> tuple[RawHtmlBlock | None, bool]:
    """Return the HTML-block state after one line, and whether the line is in one.

    ``content`` is the line with its container prefixes already peeled, for
    the reason ``container_content`` exists: CommonMark decides a line's block
    type from what is left once the prefixes are consumed. Kept identical to
    the helper in ``.github/scripts/check-session-structure.py``.
    """
    if open_block is not None and open_block.end is None and not content.strip():
        # A blank line closes the conditions that have no end tag, and the
        # blank line is not itself part of the block.
        open_block = None

    if open_block is None:
        for candidate in RAW_HTML_BLOCKS:
            if candidate.start.match(content) is not None:
                open_block = candidate
                break

    in_block = open_block is not None
    if open_block is not None and open_block.end is not None:
        if open_block.end.search(content) is not None:
            open_block = None

    return open_block, in_block


def normalize_for_fence_closing(line: str, active_fence: ActiveFence) -> str:
    """Return a fenced-block line normalized to the opening fence's container."""
    peeled, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count < len(active_fence.containment_path):
        return line
    return peeled


def build_active_fence(
    opening_fence: tuple[str, int],
    fence_line: FenceLine,
) -> ActiveFence:
    """Return active fenced code block state for a detected opening fence."""
    fence_character, minimum_length = opening_fence
    return ActiveFence(
        character=fence_character,
        minimum_length=minimum_length,
        containment_path=fence_line.containment_path,
    )


def fence_container_ended(line: str, active_fence: ActiveFence) -> bool:
    """Return whether ``line`` has left the container holding the open fence.

    CommonMark ends a fenced block at the end of its containing block when no
    closing fence is found, so a fence opened inside a list item or a
    blockquote does not run to the end of the document once the document
    outdents past that container. A nonblank line that does not peel to the
    fence's container has left it. A blank line has left a blockquote, which a
    blank line ends, but not a list item, where a blank line is ordinary
    content. Kept identical to the helper in
    ``.github/scripts/check-session-structure.py``.
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
    """Return whether a line closes the active fenced code block."""
    closing_pattern = re.compile(rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}\s*$")
    return closing_pattern.match(line) is not None


def is_allowed_label_line(line: str) -> bool:
    """Return whether the line is an explicit Open Question or Assumption entry."""
    return ALLOWED_LABEL_PATTERN.match(line) is not None


def find_violations_in_text(text: str, display_path: str) -> list[Violation]:
    """Find prohibited placeholder markers in Markdown text."""
    violations: list[Violation] = []
    is_in_html_comment = False
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    raw_html_block: RawHtmlBlock | None = None

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if active_fence is not None and fence_container_ended(raw_line, active_fence):
            # The container holding the fence has ended, so the fence ended
            # with it and this line is document text again.
            active_fence = None

        if active_fence is not None:
            closing_line = normalize_for_fence_closing(raw_line, active_fence)
            if is_closing_fence(
                closing_line,
                active_fence.character,
                active_fence.minimum_length,
            ):
                active_fence = None
            continue

        was_in_html_comment = is_in_html_comment
        commentless_line, is_in_html_comment = strip_html_comments(raw_line, is_in_html_comment)
        # A line CommonMark reads as raw HTML opens no fenced block. Without
        # this the backticks left behind by comment stripping open one, and
        # every placeholder to the end of the file is hidden inside it. The
        # test reads the line with its container prefixes peeled, because a
        # comment nested in a blockquote or a list item opens an HTML block
        # just as the unindented one does -- and hides just as much. A comment
        # is one condition out of several: a ``<div>`` opens a block too, and
        # a line of backticks inside one is raw HTML rather than a fence.
        block_content = container_content(raw_line, list_contexts)
        raw_html_block, in_raw_html_block = raw_html_block_state(block_content, raw_html_block)
        in_html_block = (
            was_in_html_comment
            or HTML_BLOCK_COMMENT_START_PATTERN.match(block_content) is not None
            or in_raw_html_block
        )

        opening_fence_line = normalize_for_fence_opening(commentless_line, list_contexts)
        opening_fence = (
            None if in_html_block else parse_opening_fence(opening_fence_line.content)
        )
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, opening_fence_line)
            continue

        if ALLOW_TBD_PATTERN.search(raw_line):
            continue

        if is_allowed_label_line(commentless_line):
            continue

        for match in PLACEHOLDER_PATTERN.finditer(commentless_line):
            violations.append(
                Violation(
                    display_path=display_path,
                    line_number=line_number,
                    matched_text=match.group(0),
                )
            )

    return violations


def scan_files(path_arguments: Iterable[str | Path], root: Path = REPO_ROOT) -> list[Violation]:
    """Find prohibited placeholder markers in candidate Markdown docs."""
    violations: list[Violation] = []
    for path_argument in path_arguments:
        candidate = resolve_candidate_path(path_argument, root)
        if candidate is None:
            continue

        path, display_path = candidate
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise FileReadError(display_path, error) from error

        violations.extend(find_violations_in_text(text, display_path))

    return violations


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check docs Markdown for prohibited placeholder markers."
    )
    parser.add_argument("paths", nargs="*", help="Markdown files passed by pre-commit.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the placeholder check."""
    args = parse_args(argv)

    try:
        violations = scan_files(args.paths, root=root)
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1

    for violation in violations:
        print(violation.format_message())

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
