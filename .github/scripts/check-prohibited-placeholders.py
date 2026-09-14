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

#: CommonMark HTML block start condition 7: a complete open or closing tag,
#: alone on its line. It is the one condition that may not interrupt a
#: paragraph, which is why the classifier below is given the paragraph state.
#: Conditions 1 to 6 are tried first, so an opening ``<script>`` never reaches
#: this pattern. Kept identical to the constants in the sibling hook.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_TAG_NAME = r"[A-Za-z][A-Za-z0-9-]*"
HTML_BLOCK_ATTRIBUTE = (
    r"[ \t]+[_:A-Za-z][A-Za-z0-9_.:-]*"
    r"""(?:[ \t]*=[ \t]*(?:[^\s"'=<>`]+|'[^']*'|"[^"]*"))?"""
)
HTML_BLOCK_TYPE_SEVEN_PATTERN = re.compile(
    rf"^ {{0,3}}(?:<{HTML_BLOCK_TAG_NAME}(?:{HTML_BLOCK_ATTRIBUTE})*[ \t]*/?>"
    rf"|</{HTML_BLOCK_TAG_NAME}[ \t]*>)[ \t]*$"
)

#: The two block shapes that close a paragraph and are not themselves one.
#: They are all the paragraph tracker needs: everything else nonblank that
#: reaches it is either paragraph text or a line already known to be inside a
#: fence or an HTML block.
ATX_HEADING_LINE_PATTERN = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)")
THEMATIC_BREAK_LINE_PATTERN = re.compile(
    r"^ {0,3}(?:(?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})$"
)
#: A Setext heading underline. A run of ``=`` or ``-`` under a paragraph
#: turns that whole paragraph into a heading, so the paragraph is closed and
#: nothing below the underline continues it. A ``-`` run is a Setext
#: underline only while a paragraph is open; with nothing open it is the
#: thematic break ``THEMATIC_BREAK_LINE_PATTERN`` already names, which is why
#: the two tests are ordered. Kept identical to the constant in
#: ``.github/scripts/check-session-structure.py``.
#: <https://spec.commonmark.org/0.31.2/#setext-headings>
SETEXT_UNDERLINE_PATTERN = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
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
class HtmlBlockCondition:
    """One CommonMark HTML block condition: how it starts and how it ends.

    ``end`` is the pattern that closes the block on the line carrying it, or
    ``None`` for the conditions a blank line closes; the blank line itself is
    outside the block, which is why it is tested before the start conditions
    are. ``interrupts_paragraph`` is false for condition 7 alone, which is what
    the spec says of it. Kept identical to the record in the sibling hook.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """

    name: str
    start: re.Pattern[str]
    end: re.Pattern[str] | None
    interrupts_paragraph: bool = True


@dataclass(frozen=True)
class ActiveHtmlBlock:
    """The open HTML block's condition and the container holding it.

    The containment path is here for the reason ``ActiveFence`` carries one:
    CommonMark ends a leaf block with its containing block, so an unclosed
    ``<script>`` opened inside a blockquote ends where the blockquote does
    rather than running to the end of the document. Kept identical to the
    record in the sibling hook.
    """

    condition: HtmlBlockCondition
    containment_path: tuple[Container, ...] = ()


#: The name condition 2 answers to. The comment is a condition of this machine
#: rather than a state beside it, which is what keeps a ``<script>`` line
#: *inside* a comment from opening a second block that outlives the comment.
HTML_BLOCK_COMMENT = "comment"

HTML_BLOCK_CONDITIONS: tuple[HtmlBlockCondition, ...] = (
    HtmlBlockCondition(
        "script",
        re.compile(r"^ {0,3}<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.IGNORECASE),
        re.compile(r"</(?:script|pre|style|textarea)>", re.IGNORECASE),
    ),
    HtmlBlockCondition(HTML_BLOCK_COMMENT, HTML_BLOCK_COMMENT_START_PATTERN, re.compile(r"-->")),
    HtmlBlockCondition("instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    HtmlBlockCondition("declaration", re.compile(r"^ {0,3}<![A-Za-z]"), re.compile(r">")),
    HtmlBlockCondition("cdata", re.compile(r"^ {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    HtmlBlockCondition(
        "element",
        re.compile(
            rf"^ {{0,3}}</?(?:{HTML_BLOCK_ELEMENT_NAMES})(?:[ \t>]|/>|$)",
            re.IGNORECASE,
        ),
        None,
    ),
    HtmlBlockCondition("tag", HTML_BLOCK_TYPE_SEVEN_PATTERN, None, interrupts_paragraph=False),
)


@dataclass(frozen=True)
class ListContext:
    """An active Markdown list, identified by its full containment path from the document root."""

    containment_path: tuple[Container, ...]


class FileReadError(RuntimeError):
    """Raised when a candidate Markdown file cannot be read."""

    def __init__(self, display_path: str, error: Exception) -> None:
        # Only OSError carries ``strerror``. A UnicodeDecodeError does not, and
        # reading it unconditionally turned a readable failure into an
        # AttributeError traceback, which is the opposite of what this class is
        # for.
        detail = getattr(error, "strerror", None) or str(error) or "I/O error"
        error_summary = f"{type(error).__name__}: {detail}"
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

    # Containers alternate freely on one line: ``> - item``, ``- > quoted``,
    # and ``- - item`` are all valid CommonMark. Peeling every blockquote and
    # then at most one list item handles only the first of those; the rest
    # leave a container prefix in front of the fence, so the fence is missed
    # and the fence state stays wrong for the rest of the file.
    # https://spec.commonmark.org/0.31.2/#container-blocks
    extras: list[Container] = []
    while True:
        quote_match = BLOCK_QUOTE_PREFIX_PATTERN.match(relative_line)
        if quote_match is not None:
            extras.append(Container(kind=CONTAINER_KIND_BLOCK_QUOTE))
            relative_line = relative_line[quote_match.end() :]
            continue

        list_match = LIST_ITEM_PATTERN.match(relative_line)
        if list_match is None:
            break

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


def container_line(line: str, list_contexts: list[ListContext]) -> FenceLine:
    """Return what CommonMark reads on a line, and the containers holding it.

    A line's block type -- an HTML block among them -- is decided from what is
    left once the blockquote and list-item prefixes are consumed, so
    ``> <!-- a comment -->`` opens an HTML block exactly as the unindented form
    does. The path comes back with the content because a block opened on this
    line ends when that path ends. The list contexts are copied because this
    asks a question about one line rather than advancing the document: the
    contexts that govern the rest of the file are the ones the fence
    normalization takes below, from the span-stripped line. Kept identical to
    the helper in the sibling hook.
    """
    return normalize_for_fence_opening(line, list(list_contexts))


def container_content(line: str, list_contexts: list[ListContext]) -> str:
    """Return what CommonMark reads on a line, container prefixes peeled off."""
    return container_line(line, list_contexts).content


def opens_a_paragraph(content: str, paragraph_open: bool) -> bool:
    """Return whether a line of document text leaves a paragraph open below it.

    HTML block condition 7 is the one condition that may not interrupt a
    paragraph, so classifying it needs to know whether one is open. The test is
    deliberately liberal: anything nonblank that is not a heading, a thematic
    break or a Setext underline leaves a paragraph open. Being wrong in that
    direction only ever *stops* condition 7 from opening, which is the
    behaviour this scan had before it classified condition 7 at all. Lines
    inside a fence or an HTML block never reach here; their caller closes the
    paragraph outright. Kept identical to the helper in the sibling hook.

    The underline needs the state coming in, which is the one thing the line
    alone does not say. ``=====`` under a paragraph is that paragraph's
    heading underline and closes it; ``=====`` with nothing open is an
    ordinary paragraph of its own, and leaves one open below it.
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    """
    if not content.strip():
        return False
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return False
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return False
    if paragraph_open and SETEXT_UNDERLINE_PATTERN.match(content) is not None:
        return False
    return True


def html_block_state(
    content: str,
    containment_path: tuple[Container, ...],
    open_block: ActiveHtmlBlock | None,
    paragraph_open: bool,
) -> tuple[ActiveHtmlBlock | None, ActiveHtmlBlock | None]:
    """Return the state after one line, and the block the line itself is in.

    Two values because they are two questions. The state after the line is what
    the next line inherits; the block the line is *in* is what says whether this
    line is raw HTML, and a block that ends on its own last line is still the
    block that line belonged to.

    ``content`` is the line with its container prefixes already peeled, for the
    reason ``container_line`` exists: CommonMark decides a line's block type
    from what is left once the prefixes are consumed. The caller is responsible
    for ending a block whose container has ended, which it does before calling
    this. Kept identical to the helper in the sibling hook.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """
    if open_block is not None and open_block.condition.end is None and not content.strip():
        # A blank line closes the conditions that have no end tag, and the
        # blank line is not itself part of the block.
        open_block = None

    if open_block is None:
        # No start condition is tried while a block is open, which is what the
        # spec says and is also what keeps a ``<script>`` line inside an open
        # comment from opening a block that survives the ``-->``.
        for condition in HTML_BLOCK_CONDITIONS:
            if paragraph_open and not condition.interrupts_paragraph:
                continue
            if condition.start.match(content) is not None:
                open_block = ActiveHtmlBlock(
                    condition=condition, containment_path=containment_path
                )
                break

    line_block = open_block
    if open_block is not None and open_block.condition.end is not None:
        if open_block.condition.end.search(content) is not None:
            open_block = None

    return open_block, line_block


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


def container_path_ended(line: str, containment_path: tuple[Container, ...]) -> bool:
    """Return whether ``line`` has left the container holding an open block.

    CommonMark ends a leaf block at the end of its containing block, so a block
    opened inside a list item or a blockquote does not run to the end of the
    document once the document outdents past that container. A nonblank line
    that does not peel to the block's container has left it. A blank line has
    left a blockquote, which a blank line ends, but not a list item, where a
    blank line is ordinary content. Kept identical to the helper in the sibling
    hooks. https://spec.commonmark.org/0.31.2/#container-blocks
    """
    _, peeled_count = peel_containers(line, containment_path)
    if peeled_count == len(containment_path):
        return False
    if line.strip():
        return True
    return containment_path[peeled_count].kind == CONTAINER_KIND_BLOCK_QUOTE


def fence_container_ended(line: str, active_fence: ActiveFence) -> bool:
    """Return whether ``line`` has left the container holding the open fence.

    A fenced block is one of the leaf blocks ``container_path_ended`` speaks
    for; the rule is the container's rather than the fence's.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    return container_path_ended(line, active_fence.containment_path)


def parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the opening fence marker character and length, if present.

    The info string of a *backtick* fence may not itself contain a
    backtick, so a line whose marker is followed by a code span opens no
    fence: it is an ordinary paragraph. Without this check the checker
    drops every following line until another matching fence or the end of
    the file. A tilde fence carries no such restriction.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    match = FENCE_OPEN_PATTERN.match(line)
    if match is None:
        return None

    marker = match.group("marker")
    if marker[0] == "`" and "`" in line[match.end() :]:
        return None
    return marker[0], len(marker)


def is_closing_fence(line: str, fence_character: str, minimum_length: int) -> bool:
    """Return whether a line closes the active fenced code block.

    CommonMark closes a fenced block only on a fence of the same character that
    is at least as long as the opening fence and that carries nothing but
    spaces or tabs after it. An info string does not close a block, and
    trailing prose does not close one either.

    Spaces and tabs, and not a whitespace class. Python reads ``\\s`` as Unicode
    whitespace, so a nonbreaking space or a form feed after the backticks would
    close the block here while the renderer kept every line below it inside the
    code -- and a fake scaffold heading under such a fence would count as
    structure. Measured against markdown-it 14.3.0: a fence followed by U+00A0
    does not close. Kept in step with the sibling hooks.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    closing_pattern = re.compile(
        rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}[ \t]*$"
    )
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
    html_block: ActiveHtmlBlock | None = None
    paragraph_open = False

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
            paragraph_open = False
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
        block_line = container_line(raw_line, list_contexts)
        block_content = block_line.content
        if html_block is not None and container_path_ended(raw_line, html_block.containment_path):
            # The list item or blockquote holding the block has ended, so the
            # block ended with it, exactly as an unclosed fence does.
            html_block = None
        html_block, line_html_block = html_block_state(
            block_content, block_line.containment_path, html_block, paragraph_open
        )
        # The comment is one of the conditions the machine tracks; an inline
        # comment opened part way along a line is not a block, so its
        # cross-line state is still consulted here.
        in_html_block = was_in_html_comment or line_html_block is not None

        opening_fence_line = normalize_for_fence_opening(commentless_line, list_contexts)
        opening_fence = (
            None if in_html_block else parse_opening_fence(opening_fence_line.content)
        )
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, opening_fence_line)
            # A fence line opens a code block, not a paragraph. Leaving the
            # state set meant that a fence whose container ended on the very
            # next line handed a stale open paragraph to the line below it,
            # which then refused to open the HTML block CommonMark opens
            # there -- and a placeholder inside that block went unreported.
            paragraph_open = False
            continue

        # Written here rather than above, so the fence branch reads the state
        # the line above left and not the one this line would leave. The
        # sibling hook writes it in the same place.
        paragraph_open = (
            False if in_html_block else opens_a_paragraph(block_content, paragraph_open)
        )

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
        except (OSError, UnicodeDecodeError) as error:
            # UnicodeDecodeError is a ValueError, so ``except OSError`` never
            # caught it: a file that is not valid UTF-8 crashed the run with a
            # traceback instead of reporting one unreadable file.
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
