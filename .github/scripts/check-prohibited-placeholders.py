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
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

#: Spaces and tabs, the only whitespace CommonMark and YAML treat as
#: horizontal. ``str.strip`` with no argument also removes U+00A0 and the
#: rest of Unicode, which is how a non-delimiter became a delimiter.
ASCII_HORIZONTAL_WHITESPACE = " \t"
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
    r"^[ \t]*(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)?\*\*(?:Open Questions?|Assumption):\*\*",
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
    r"""(?:[ \t]*=[ \t]*(?:[^ \t\r\n"'=<>`]+|'[^']*'|"[^"]*"))?"""
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
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}>[ \t]?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing>[ \t]+)")
#: A list item with nothing on its own line. ``LIST_ITEM_PATTERN`` above wants
#: whitespace after the marker, which a marker at the end of a line does not
#: have, so the container walk does not see one here -- and a table's header
#: row is where that gap becomes visible. Measured on GitHub's own renderer:
#: ``-``, ``*``, ``+``, ``1.`` and ``1)`` over a delimiter row form no table,
#: because each is an empty list item rather than a paragraph, while ``-x``
#: over the same row forms one.
#: https://spec.commonmark.org/0.31.2/#list-items
EMPTY_LIST_ITEM_PATTERN = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])[ \t]*$")
#: A GFM table's delimiter row, which is the only thing that marks a table.
#: This hook reports no table cell of its own; it carries the pattern because
#: a delimiter row ends the paragraph above it, and an HTML block condition 7
#: written under a table may not be refused on the strength of a paragraph
#: GFM has already closed. Kept identical to the pattern in the sibling hooks.
#: https://github.github.com/gfm/#tables-extension-
TABLE_DELIMITER_PATTERN = re.compile(
    r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$"
)

#: The characters a backslash may escape, which is all a backslash may do.
#: CommonMark names them as the ASCII punctuation characters and nothing else,
#: so a backslash before a space, a tab or a control character is a literal
#: backslash and the character behind it keeps its own meaning. Spelled as the
#: four ranges the specification spells, so none is missed, with the
#: regular-expression class derived from the set rather than written a second
#: time. Kept identical to the constants in the sibling hooks.
#: <https://spec.commonmark.org/0.31.2/#backslash-escapes>
ASCII_PUNCTUATION = frozenset(
    chr(code)
    for first, last in ((0x21, 0x2F), (0x3A, 0x40), (0x5B, 0x60), (0x7B, 0x7E))
    for code in range(first, last + 1)
)
_ASCII_PUNCTUATION_CLASS = "".join(
    "\\" + character for character in sorted(ASCII_PUNCTUATION)
)
#: What a bare link destination may hold, in two rules: a backslash escapes an
#: ASCII punctuation character and nothing else, and the destination ends at a
#: space, a tab or a line ending. The second is the production renderer's
#: grammar rather than CommonMark 0.31.2's, measured over 54 characters in this
#: position; the sibling hooks' copies carry the measurement in full. This hook
#: carries no inline link model and wants none; it carries the destination only
#: so that the three hooks' copies of this class cannot drift, which a
#: cross-hook test reads. Nothing in this hook's own walk asks it any more: the
#: paragraph helper used to, and a definition is now known to leave the
#: paragraph it is written into open. Kept identical to the class in the
#: sibling hooks.
#: <https://spec.commonmark.org/0.31.2/#link-destination>
_DESTINATION_CHARACTER = (
    r"(?:[^ \t\n()\\]"
    rf"|\\[{_ASCII_PUNCTUATION_CLASS}]"
    rf"|\\(?![{_ASCII_PUNCTUATION_CLASS}]))"
)
#: How deep a bare destination's parentheses may nest. CommonMark states no
#: bound at all -- a destination "includes parentheses only if [...] part of a
#: balanced pair of unescaped parentheses" -- and the two implementations that
#: decide what this page carries both state one, at the same depth. Measured
#: one level at a time on ``[x]: a(a(...(z)...))`` with a reference below it:
#: markdown-it 14.3.0 and GitHub's own renderer resolve it at 32 levels and
#: refuse it at 33. micromark 4.0.2 bounds an *inline* target at the same 32
#: and leaves a *definition's* destination unbounded, which is one call site
#: passing ``linkResourceDestinationBalanceMax`` and one passing nothing; both
#: were measured, one level at a time, before the parting was written down.
#: The page is followed here, as it is for the character class above, and the
#: number is the page's rather than a round one.
#:
#: The bound belongs to every spelling of the rule, not to the pattern alone.
#: The two hooks that also scan a target by hand say it again inside
#: ``inline_link_end``, because a pattern that refuses a destination and a
#: scan that accepts the same one make the same module answer two ways: the
#: scan masked a 33-level image as metadata, the renderers printed its
#: characters and read the marker inside it as a real comment, and an
#: adult-facing document went through the child reading gate.
#:
#: This was three, and three was a number nobody had measured. A definition
#: four levels deep was no definition to these hooks, so a reference to it was
#: literal text, a marker in that reference was honoured as a comment, and a
#: child-facing document left the reading gate in silence -- which is the one
#: direction this module must not err in.
#:
#: Written as a chain rather than as one constant per level because a level
#: names the level below it exactly once: the pattern grows by about seventy
#: characters a level rather than doubling, and is 2,189 characters and two
#: milliseconds to compile at 32. It cannot backtrack either, and that is a
#: property of ``_DESTINATION_CHARACTER`` rather than of the chain: the class
#: excludes both parentheses, so at every position exactly one branch of the
#: alternation can match. Kept identical to the constant in the sibling hooks.
#: <https://spec.commonmark.org/0.31.2/#link-destination>
DESTINATION_NESTING_LIMIT = 32


def _link_destination_pattern(limit: int) -> str:
    """Return the destination alternative that allows ``limit`` levels of nesting.

    A function rather than a module-level loop, and a control is why: at a
    limit of one the loop body does not run, so the name it bound was not
    there to delete and the module did not import at all. A limit is a number
    a maintainer may change, and one whose only safe values are the ones
    somebody happened to try is not a limit. Kept identical to the helper in
    the sibling hooks.
    """
    nested = rf"{_DESTINATION_CHARACTER}*"
    for _ in range(limit - 1):
        nested = rf"(?:{_DESTINATION_CHARACTER}|\({nested}\))*"
    return rf"(?:<[^<>\n]*>|(?!<)(?:{_DESTINATION_CHARACTER}|\({nested}\))+)"


_LINK_DESTINATION = _link_destination_pattern(DESTINATION_NESTING_LIMIT)

#: How long a link label may be. CommonMark caps it at 999 characters between
#: the brackets, and the cap decides what a definition *is*: a label one
#: character too long is no definition at all, so the line is an ordinary
#: paragraph and leaves one open below it. Kept identical to the constant in
#: the sibling hooks.
#: <https://spec.commonmark.org/0.31.2/#link-label>
#: A link label's maximum length, measured on GitHub's own renderer rather
#: than taken from CommonMark's prose, which says 999. A 1,000-character label
#: resolves there, as a definition and as a use, and a 1,001-character one
#: does not; markdown-it 14.3.0 enforces no bound at all. The renderer that
#: decides what the page carries decides this, and erring the other way is the
#: permissive direction: a bound one character too tight reads a resolved
#: reference as literal brackets and honours a marker the page hides.
#: https://spec.commonmark.org/0.31.2/#link-label
LINK_LABEL_MAXIMUM_CHARACTERS = 1000

#: Every character markdown-it 14.3.0 reads as nothing at all inside a link
#: label, measured one at a time rather than taken from a class. CommonMark's
#: prose says a label needs "at least one character that is not a space, tab, or
#: line ending", and the renderer is stricter than those words: it folds the
#: label with a Unicode trim first, so ``[\u00a0]: /url`` is a paragraph and not
#: a definition. Python's ``\s`` is a third set again -- it matches U+0085,
#: which the renderer keeps as a label, and misses U+FEFF, which the renderer
#: drops -- so the set is written out rather than spelled ``\s``. U+200B and
#: U+180E are deliberately absent: the renderer keeps a label made of either.
#: Measured one character at a time through markdown-it 14.3.0.
#: https://spec.commonmark.org/0.31.2/#link-label
_LINK_LABEL_BLANK = (
    " \t\x0b\f\r\n\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
)
#: A CommonMark link reference definition: ``[label]: destination "title"``.
#: It renders nothing at all, and it does **not** close the paragraph it is
#: written into: cmark-gfm and micromark 4.0.2 both read it into that paragraph
#: and strip it at the end, so HTML block condition 7 stays shut on the line
#: below it. Nothing in this hook reads this constant any more; it is kept so
#: the three hooks' copies cannot drift, which a cross-hook test reads. Matched
#: conservatively, the way the sibling hooks match it: the destination must be
#: one unbroken token or the angle-bracket form, a title must be properly
#: closed, and nothing else may follow. Kept identical to the constant in the
#: sibling hooks.
#: <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
LINK_REFERENCE_DEFINITION_PATTERN = re.compile(
    rf"""
    ^\ {{0,3}}                               # at most three spaces of indent
    \[ (?=[^\]]*[^{_LINK_LABEL_BLANK}\]])    # a label with one nonblank
       (?P<label> (?: [^\[\]\\] | \\. )+ ) \]
    :[ \t]*                                  # the colon, then spaces or tabs
    {_LINK_DESTINATION}                      # the destination
    (?P<title> [ \t]+                        # an optional title
        (?: " (?: [^"\\] | \\. )* "
          | ' (?: [^'\\] | \\. )* '
          | \( (?: [^()\\] | \\. )* \) )
    )?
    [ \t]*$
    """,
    re.VERBOSE,
)

#: The raw HTML runs whose content is not markup. What sits inside one is
#: characters the page shows as they stand or drops altogether, so a
#: ``<!-- ... -->`` written there is displayed text rather than a comment and
#: declares nothing.
#:
#: Two families, and each is a rule from a different place. The element names
#: are HTML's raw text and escapable raw text content models, measured against
#: Python's ``html.parser``, which reports the run as data for every name here
#: and as a comment inside ``pre`` and ``div``; ``noscript`` is left out
#: because whether its content is raw text depends on whether scripting is
#: enabled. The other three are CommonMark's own raw HTML forms -- a
#: processing instruction, a CDATA section and a declaration -- which the
#: renderer passes through untouched and an HTML parser then reads as one
#: token each.
#:
#: Each opener is anchored at the start of the line, because these are the
#: *block* forms: HTML block conditions 1, 3, 4 and 5 all begin a line. A run
#: that opens part way along a line of prose is inline raw HTML and is a
#: question for the inline scan.
#:
#: An open comment is tracked beside them, and is the one run here whose
#: content *is* markup: a marker inside a comment is the comment it looks
#: like. It is in the list because a raw HTML block may not start inside
#: another one, so a ``<script>`` line written inside a comment opens no run
#: -- which is the rule ``html_block_state`` states for the conditions it
#: tracks.
#: <https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state>
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
COMMENT_RUN = "comment"
#: The characters HTML5's tokenizer reads as whitespace inside a tag. The
#: Markdown layer's ``ASCII_HORIZONTAL_WHITESPACE`` is a different set for a
#: different question: this one carries the line ending and the form feed,
#: because a tag may hold either. Kept identical to the constant in the
#: sibling hooks.
#: https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
HTML_TAG_WHITESPACE = "\t\n\f\r "
RAW_TEXT_ELEMENT_NAMES = (
    "script",
    "style",
    "textarea",
    "title",
    "xmp",
    "iframe",
    "noembed",
    "noframes",
)
RAW_TEXT_RUNS = tuple(
    (
        name,
        re.compile(rf"^ {{0,3}}<{name}(?=[ \t/>]|$)", re.IGNORECASE),
        re.compile(rf"</{name}(?=[ \t/>]|$)", re.IGNORECASE),
    )
    for name in RAW_TEXT_ELEMENT_NAMES
) + (
    ("processing instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    ("CDATA section", re.compile(r"^ {0,3}<!\[CDATA\["), re.compile(r"\]\]>")),
    ("declaration", re.compile(r"^ {0,3}<![A-Za-z]"), re.compile(r">")),
    (COMMENT_RUN, re.compile(r"^ {0,3}<!--"), re.compile(r"-->")),
)
RAW_TEXT_CLOSERS = {key: closer for key, _, closer in RAW_TEXT_RUNS}
#: HTML5's tag-state machine, entered where a tag's name has just ended.
#: ``html_tag_close_state`` names its states as the standard names them and
#: hands the state back, because a tag may end on a line below the one it
#: started on and the machine has to be resumed where it stopped.
#: https://html.spec.whatwg.org/multipage/parsing.html#before-attribute-name-state
TAG_STATE_START = "before-attribute-name"
#: The prefix of a run state that is an unfinished *end tag* rather than a run
#: of raw text. No element name and none of the other four run keys begins with
#: it, so the one state field still holds one thing at a time. What it records
#: is the half-open tag's own tokenizer state, so that a quoted attribute value
#: carried across a line break is resumed rather than restarted.
CLOSING_TAG_RUN_PREFIX = "</"
#: One attribute of an HTML tag, with a line ending allowed wherever CommonMark
#: allows whitespace. Written once so the patterns built from it cannot drift,
#: and identical to the production the two sibling hooks carry.
#: https://spec.commonmark.org/0.31.2/#raw-html
_TAG_ATTRIBUTE = r"""
    [ \t\n]+ [_:A-Za-z][A-Za-z0-9_.:-]*             # an attribute name
    (?: [ \t\n]*=[ \t\n]*                          # an attribute value
        (?: [^ \t\r\n"\'=<>`]+ | \'[^\']*\' | "[^"]*" ) )?
"""
#: A raw-text element's own opening tag, whole. The closing delimiter of a
#: raw-text run is searched for *past* this, because an HTML parser reads the
#: start tag before it enters raw text: in ``<script title="</script>">`` the
#: end-tag spelling is an attribute value, the element never closes, and
#: everything below it to the end of the file is script data. Searching from the
#: element's name instead closed a run that had not begun, and a ``## Goal``
#: under it was reported as a heading the page never paints. Built from
#: ``_TAG_ATTRIBUTE`` so this spelling of "a tag" cannot drift from the others.
#: https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
RAW_TEXT_START_TAG_PATTERN = re.compile(
    rf"""
    < [A-Za-z][A-Za-z0-9-]*                        # the element's own name
    (?: {_TAG_ATTRIBUTE} )*
    [ \t\n]* /? >
    """,
    re.VERBOSE,
)

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

    ``ordered_start`` is an ordered list item's start number, and ``None`` for
    a bullet list item and for a blockquote. It is kept out of the comparison
    because a containment path is a path: two items of one list are the same
    container at the same depth, and a path comparison that read the start
    number would call every sibling item a different container and cut every
    list in half.
    """

    kind: str
    indent: int = 0
    ordered_start: int | None = field(default=None, compare=False)
    bullet: str | None = field(default=None, compare=False)


@dataclass(frozen=True)
class FenceLine:
    """A Markdown line normalized for fenced code block detection."""

    content: str
    containment_path: tuple[Container, ...] = ()
    #: The containers that opened on this line rather than above it. A list
    #: item among them starts a block, whatever the line goes on to hold.
    opened: tuple[Container, ...] = ()


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

#: Condition 4 asks for an *uppercase* ASCII letter after ``<!``. That is the
#: rule markdown-it 14.3.0 carries, and markdown-it is what this repository
#: measures a rendered page against. The CommonMark 0.31.2 prose says "an ASCII
#: letter" instead, and micromark-core-commonmark 2.0.3 reads it that way, so
#: the two really do part over a lowercase ``<!doctype html>``. Following the
#: renderer is also the safe way round: a lowercase declaration that opens no
#: block leaves the paragraph above it open, and a mandatory heading below it is
#: still a heading. Reading it as a block closes that paragraph, lets the next
#: line open a type-seven block, and hides every heading down to the blank line.
#: <https://spec.commonmark.org/0.31.2/#html-blocks>
HTML_BLOCK_CONDITIONS: tuple[HtmlBlockCondition, ...] = (
    HtmlBlockCondition(
        "script",
        re.compile(r"^ {0,3}<(?:script|pre|style|textarea)(?:[ \t>]|$)", re.IGNORECASE),
        re.compile(r"</(?:script|pre|style|textarea)>", re.IGNORECASE),
    ),
    HtmlBlockCondition(HTML_BLOCK_COMMENT, HTML_BLOCK_COMMENT_START_PATTERN, re.compile(r"-->")),
    HtmlBlockCondition("instruction", re.compile(r"^ {0,3}<\?"), re.compile(r"\?>")),
    HtmlBlockCondition("declaration", re.compile(r"^ {0,3}<![A-Z]"), re.compile(r">")),
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
#: What a run given no path leaves out, kept in step with the ``exclude:`` key
#: on this hook in ``.pre-commit-config.yaml``. The archived design record uses
#: the literal token for open trip parameters a family decides, and the gate
#: has never read it. A default walk that scanned it would report dozens of
#: failures the gate does not consider failures, which is the opposite mistake
#: from the silence it replaces and just as misleading.
DEFAULT_SCAN_EXCLUDES = ("docs/spec/",)


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


def strip_html_comments(
    line: str, is_in_html_comment: bool
) -> tuple[str, bool, bool]:
    """Remove HTML comment spans from a Markdown line.

    The third value says whether the comment left open below this line
    *opened on* it. The caller needs that to tell CommonMark's two comments
    apart, and the second value cannot answer it: a line that closes one
    comment and opens another comes in open and goes out open, while the
    answer changes. The sibling hook walks a line the same way and is kept
    in step with this.
    """
    uncommented_parts: list[str] = []
    index = 0
    opened_here = False

    while index < len(line):
        if is_in_html_comment:
            comment_end = line.find("-->", index)
            if comment_end == -1:
                return "".join(uncommented_parts), True, opened_here
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
            opened_here = True
            break
        index = comment_end + len("-->")

    return "".join(uncommented_parts), is_in_html_comment, opened_here


def normalize_line_endings(text: str) -> str:
    """Return ``text`` with every CommonMark line ending written as ``\\n``.

    CommonMark counts a line feed, a carriage return, and a carriage return
    followed by a line feed as one line ending each, and counts nothing else.
    The translation happens once, here, where a document enters this module --
    never in the predicates below, which would each have to spell ``\\r`` and
    would each be a place to forget it.

    ``Path.read_text`` translates both forms already, so a file this hook reads
    from disk arrives normalized whatever an editor wrote. This is what makes
    the same true for a caller that hands the document over directly, and it is
    what lets the walk below split on ``\\n`` alone, as the sibling hooks do.
    ``str.splitlines``, which this replaced, splits on a form feed, a vertical
    tab and two Unicode separators as well; measured against markdown-it
    14.3.0, a form feed before a closing fence does not close it, and the
    placeholder below that fence is an example rather than a violation.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#line-ending
    """
    if "\r" not in text:
        return text
    return text.replace("\r\n", "\n").replace("\r", "\n")


def count_leading_spaces(line: str) -> int:
    """Return the number of leading space characters in a line."""
    return len(line) - len(line.lstrip(" "))


def count_indent_columns(line: str) -> int:
    """Return how many *columns* of indentation ``line`` opens with.

    Not the number ``count_leading_spaces`` above returns, and the difference
    is the tab. CommonMark measures indentation in columns and expands a tab
    to the next multiple of four, so a line beginning with one tab starts at
    column four and is an indented code block -- while a count of *characters*
    reads zero and the line is classified as prose.

    The two counts are kept apart rather than merged, because their callers
    ask different questions of them. ``peel_containers`` counts characters
    because it then *slices* them, and a column count cannot slice a tab in
    half; this counts columns because it then *classifies* a line, which is
    what CommonMark states in columns. Merging them would have made the
    container walk cut a tab it cannot cut. Kept identical to the helper in
    the sibling hooks.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    columns = 0
    for character in line:
        if character == " ":
            columns += 1
        elif character == "\t":
            columns += 4 - columns % 4
        else:
            break
    return columns


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
    if not line.strip(ASCII_HORIZONTAL_WHITESPACE):
        return

    while list_contexts:
        top = list_contexts[-1]
        remaining, peeled_count = peel_containers(line, top.containment_path)
        if peeled_count == len(top.containment_path):
            return
        # The line did not peel cleanly to this list's interior. Decide
        # whether the partial peel still keeps the list active.
        if not remaining.strip(ASCII_HORIZONTAL_WHITESPACE):
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


def spacing_columns(match: re.Match[str]) -> int:
    """Return the column just past a list marker's spacing.

    A tab is not one column. CommonMark measures a list item's content indent
    in columns and expands a tab to the next multiple of four, so ``-`` and a
    tab put the content at column 4 exactly as ``-`` and three spaces do --
    which is why the two render identically and why a fenced block indented
    four spaces under either of them is the item's content rather than code.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    column = match.end("marker")
    for character in match.group("spacing"):
        column = column + 4 - (column % 4) if character == "\t" else column + 1
    return column


def list_content_indent(match: re.Match[str]) -> int:
    """Return the list-item content indent relative to the marker's parent interior."""
    marker_end_column = match.end("marker")
    spacing_width = spacing_columns(match) - marker_end_column
    content_padding = spacing_width if spacing_width <= 4 else 1
    return marker_end_column + content_padding


def list_content_offset(match: re.Match[str]) -> int:
    """Return where a list item's content starts on its own line, in characters.

    This is the second of the two numbers a list item's marker produces, and
    keeping them apart is the whole point. ``list_content_indent`` is a
    *column*, because that is what the lines below the marker are measured in.
    This is a *character* offset into the marker's own line, because that is
    what a slice of that line is measured in. A tab is one character and up to
    four columns, so the two numbers part company exactly where a tab appears
    -- and using either one for both jobs loses a cell: the column slices two
    characters of the item's text away, and the character count puts the
    content column at 2 where CommonMark puts it at 4.
    Kept identical to the helper in the sibling hooks.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    marker_end_column = match.end("marker")
    if spacing_columns(match) - marker_end_column <= 4:
        return match.end("spacing")
    # More than four columns of spacing is one space of content indent and the
    # rest is the item's own first line, so the content begins one character
    # past the marker.
    return marker_end_column + 1


def bullet_marker(match: re.Match[str]) -> str | None:
    """Return a bullet list item's marker character, or ``None`` if ordered.

    It travels on the container for the reason ``ordered_list_start`` gives,
    and it is read for one question: ``-`` with nothing after it is both an
    empty list item and a level 2 Setext underline, and while a paragraph is
    open CommonMark reads it as the heading. ``*`` and ``+`` underline
    nothing, so only this one marker needs telling apart. Kept identical to the
    helper in the sibling hooks.
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    """
    marker = match.group("marker")
    return marker if marker[0] in "-*+" else None


def ordered_list_start(match: re.Match[str]) -> int | None:
    """Return an ordered list item's start number, or ``None`` for a bullet.

    A list may interrupt a paragraph only when an ordered one starts at 1, so
    the number has to travel on the container the marker opens:
    ``starts_a_block`` is handed the line's interior, past the marker, and
    cannot read it back off the line. Kept identical to the helper in the
    sibling hooks.
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
    marker = match.group("marker")
    return None if marker[0] in "-*+" else int(marker[:-1])


def normalize_for_fence_opening(
    line: str,
    list_contexts: list[ListContext],
    paragraph_open: bool = False,
    previous_path: tuple[Container, ...] = (),
) -> FenceLine:
    """Return a line normalized to its current Markdown container content column.

    A container is peeled only where CommonMark opens one. A list that may
    not interrupt an open paragraph opens nothing at all, so its marker is
    that paragraph's own text and this walk leaves it on the line:
    ``Words`` over ``2. <div>`` is one paragraph of two lines on GitHub's
    own renderer, measured, and peeling the ``2.`` put a ``<div>`` at the
    start of a line CommonMark never starts there. An HTML block opened on
    it, a fence opener written behind the same marker opened a fenced
    block, and everything under either went unread.

    ``starts_a_block`` already carries the interruption rule and could not
    undo the peel, because the peel runs first and hands it an interior the
    line does not have. ``container_interrupts_paragraph`` is asked here so
    that the peel and the classification cannot disagree about one fact.

    **The paragraph has to be the one this container would open inside**,
    and that is where a container-blind reading of the rule goes wrong in
    the other direction. ``> Intro.`` over ``2. ``` `` really does open a
    list on GitHub's own renderer, measured: the paragraph is inside the
    blockquote and the list opens outside it, so there is nothing at that
    level to interrupt. ``previous_path`` is the line above's container
    path, and the rule applies only where it is exactly the path this
    marker would open in. A list item marker always begins a new item, so
    once one has been consumed on this line nothing is open inside it and
    the rule stops speaking -- which is what keeps ``- Intro.`` over
    ``- 2. x`` reading its ``2.`` as the list CommonMark opens there.

    ``paragraph_open`` and ``previous_path`` are the two facts a line alone
    does not carry. The defaults are what a caller with neither should get:
    with no paragraph open every marker peels, which is what this did
    before. Kept identical to the helper in the sibling hooks.
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
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
    # A list item marker always begins a new item, so nothing the line above
    # left open is open inside it and the paragraph rule below stops speaking.
    item_opened = False
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
        opened = Container(
            kind=CONTAINER_KIND_LIST,
            indent=content_indent_rel,
            ordered_start=ordered_list_start(list_match),
            bullet=bullet_marker(list_match),
        )
        content_offset_rel = list_content_offset(list_match)
        interior = (
            relative_line[content_offset_rel:]
            if len(relative_line) >= content_offset_rel
            else ""
        )
        if (
            paragraph_open
            and not item_opened
            and previous_path == effective_path + tuple(extras)
            and not container_interrupts_paragraph(opened, interior)
        ):
            # The list opens nothing, so the marker is the paragraph's own
            # text and the line is read whole.
            break

        extras.append(opened)
        relative_line = interior
        item_opened = True
        list_contexts.append(ListContext(containment_path=effective_path + tuple(extras)))

    return FenceLine(
        content=relative_line,
        containment_path=effective_path + tuple(extras),
        opened=tuple(extras),
    )


def container_line(
    line: str,
    list_contexts: list[ListContext],
    paragraph_open: bool = False,
    previous_path: tuple[Container, ...] = (),
) -> FenceLine:
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
    return normalize_for_fence_opening(
        line, list(list_contexts), paragraph_open, previous_path
    )


def container_content(line: str, list_contexts: list[ListContext]) -> str:
    """Return what CommonMark reads on a line, container prefixes peeled off."""
    return container_line(line, list_contexts).content




def is_link_label(label: str) -> bool:
    """Return whether ``label`` is short enough to be a link label at all.

    Kept identical to the helper in the sibling hooks.
    """
    return len(label) <= LINK_LABEL_MAXIMUM_CHARACTERS


def table_row_cells(content: str) -> tuple[tuple[int, str], ...]:
    """Return each cell of one GFM table row as ``(offset, text)``.

    The offsets are into ``content``. A leading pipe is a delimiter rather than
    an empty first cell, and a pipe an author escaped is a pipe the cell holds:
    GFM reads the table before it reads any inline, so ``\\|`` is a cell
    character even where a code span would otherwise claim it.

    The leading pipe is a delimiter only up to three columns of indentation,
    which is where GFM lets a table begin. That is the whole of this helper's
    indent rule, and claiming more than it was the defect: the sentence above
    used to end "a fourth is an indented code block and no table row at all",
    and this body parses such a line's cells like any other.

    Both halves of that sentence are wrong here, and the two errors point in
    opposite directions. A row indented four columns is not always code --
    where a paragraph is open above it the line is that paragraph's lazy
    continuation, and ``Intro.`` over a four-space ``| a |`` over ``| - |`` is
    a one-column table on GitHub's own renderer, measured, which the cap above
    refuses by reading the indentation as a cell. And where no paragraph is
    open the line is code and no row at all, which nothing here enforces: a
    pipeless four-space header over a pipeless delimiter row agrees about the
    column count and opens a table this helper never sees a reason to refuse.

    Neither is closed here, because the rule belongs to the paragraph and the
    three walks that look a delimiter row ahead carry no paragraph state --
    ``extract_prose`` carries none at all. What indentation does decide is
    settled where the state already is: ``opens_a_paragraph`` opens no
    paragraph on an indented line, and ``is_table_delimiter`` refuses an
    indented delimiter row.

    Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    """
    cells: list[tuple[int, str]] = []
    indent = len(content) - len(content.lstrip(" "))
    start = indent + 1 if indent < 4 and content[indent:].startswith("|") else 0
    index = start
    while index < len(content):
        if content[index] == "|" and (index == 0 or content[index - 1] != "\\"):
            cells.append((start, content[start:index]))
            start = index + 1
        index += 1
    if start < len(content):
        cells.append((start, content[start:]))
    return tuple(cells)


def table_column_count(content: str) -> int:
    """Return how many cells GFM reads in one table row."""
    return len(table_row_cells(content.rstrip(ASCII_HORIZONTAL_WHITESPACE)))


def table_columns(header: str, delimiter: str) -> int:
    """Return a table's column count, or ``0`` when this is not a table at all.

    A delimiter row under a line is not enough. GFM: "The header row must
    match the delimiter row in the number of cells. If not, a table will not
    be recognized." Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    """
    count = table_column_count(header)
    return count if count == table_column_count(delimiter) else 0


def is_table_delimiter(line: str) -> bool:
    """Return ``True`` when a line is a Markdown table delimiter row.

    Outer pipe characters are optional in a Markdown table, so ``--- | ---``
    is a delimiter row in the same way that ``| --- | --- |`` is -- and so,
    for a one-column table, is a row with no pipe at all.

    Two lines match the pattern and are still not delimiter rows. Both were
    found by generating rows rather than by enumerating GFM's prose, and both
    were settled against GitHub's own renderer:

    * **A pipeless row is a delimiter row only when it is not also a Setext
      underline.** ``--`` under ``| a |`` is the underline, the heading wins
      and no table forms; ``-:`` under the same header is a one-column table.
      Refusing every pipeless row -- which this helper did, on the ground that
      such a row is a thematic break -- lost the colon-bearing case and kept
      the other by accident.
    * **A row indented four columns is no delimiter row**, whatever else is
      open. ``x`` over a four-space ``-:`` is one paragraph of two lines on
      GitHub's own renderer and ``x`` over a three-space ``-:`` is a table,
      measured; a leading tab reaches column four and does the same. The
      pattern's own ``^ {0,3}`` does not say this, because the ``[ \t]*`` that
      follows the optional pipe absorbs the fourth space, and it counts no tab
      at all.
    * **A row a list item could open is a list item.** ``- |`` matches the
      delimiter pattern and renders as a bullet, because the block parser
      reaches the list before the table extension does.

    Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    if count_indent_columns(line) >= 4:
        return False
    if TABLE_DELIMITER_PATTERN.match(line) is None:
        return False
    if LIST_ITEM_PATTERN.match(line) is not None:
        return False
    return "|" in line or SETEXT_UNDERLINE_PATTERN.match(line) is None


def table_starts_here(
    header: str, delimiter: str, paragraph_above: bool = True
) -> int:
    """Return the column count of the table ``delimiter`` opens under ``header``.

    Zero where the two lines open none. This is GFM's whole precondition in
    one place -- the delimiter row's own shape, and its agreement with the
    header row about the number of cells -- so that every caller asks one
    question rather than assembling its own. The header needs no pipe of its
    own: ``x`` over ``-:`` is a one-column table on GitHub's own renderer,
    measured rather than assumed.

    What the header may not be is a list item with nothing on its line. A bare
    ``-`` is an empty list item and no paragraph at all, so nothing above the
    delimiter row can be consumed into a table -- and ``LIST_ITEM_PATTERN``
    does not see it, because that pattern wants whitespace after the marker.
    This is the one place the gap shows, so it is named here rather than
    widened there.

    Nor may the header be a line the block grammar has already classified as
    something other than a paragraph. GFM builds a table out of a *paragraph*
    whose last line is followed by a delimiter row, so an ATX heading over
    ``--- | ---`` is a heading and its backticks pair as a heading's do:
    measured on GitHub's own renderer, which paints ``# `a | <!-- x --> `b``
    over ``--- | ---`` as one heading holding one code span, so the marker
    between the backticks is printed rather than read. Splitting it into cells
    exposed the marker and let a session out of its gate on it. A thematic break
    is refused for the same reason and measured the same way.

    **This is the fifth place markdown-it 14.3.0 and the production renderer
    have been measured to part, and the proxy is on the wrong side of it**:
    markdown-it orders its table rule ahead of its heading rule, so it reads the
    same two lines as a table.

    Nor may the header be an indented code block, and that is the one shape of
    the three that a line alone cannot settle. A line indented four columns is
    code where nothing is open above it and is the paragraph's own lazy
    continuation where something is, so it is a table header in the second case
    and not in the first -- measured on GitHub's own renderer both ways.
    ``paragraph_above`` is whether a paragraph was open on the line above the
    *header*, which is the only thing that can make an indented line paragraph
    text at all. The default is what a caller that cannot say should get: the
    answer this helper gave before the rule existed. ``opens_a_paragraph`` and
    ``starts_a_block`` do not pass it and do not need to -- each has already
    refused an indented line as a code block one line earlier, so the question
    cannot reach them. The indent is counted in columns, so one tab reaches
    column four.
    <https://spec.commonmark.org/0.31.2/#indented-code-blocks>

    Kept identical to the helper in the sibling hooks.
    https://github.github.com/gfm/#tables-extension-
    """
    if EMPTY_LIST_ITEM_PATTERN.match(header) is not None:
        return 0
    if ATX_HEADING_LINE_PATTERN.match(header) is not None:
        return 0
    if THEMATIC_BREAK_LINE_PATTERN.match(header) is not None:
        return 0
    if not paragraph_above and count_indent_columns(header) >= 4:
        return 0
    return table_columns(header, delimiter) if is_table_delimiter(delimiter) else 0


def opens_a_paragraph(
    content: str, paragraph_open: bool, previous_content: str = ""
) -> bool:
    """Return whether a line of document text leaves a paragraph open below it.

    HTML block condition 7 is the one condition that may not interrupt a
    paragraph, so classifying it needs to know whether one is open. The test is
    deliberately liberal: anything nonblank that is not a heading, a thematic
    break, a Setext underline or a table's delimiter row leaves a paragraph
    open -- a link reference definition among them, which is measured below.
    Being wrong in that direction only ever *stops* condition 7 from
    opening, which is the behaviour this scan had before it classified
    condition 7 at all. Lines inside a fence, an HTML block or a raw-text
    element never reach here; their caller closes the paragraph outright. Kept
    identical to the helper in the sibling hooks.

    The underline needs the state coming in, which is the one thing the line
    alone does not say. ``=====`` under a paragraph is that paragraph's
    heading underline and closes it; ``=====`` with nothing open is an
    ordinary paragraph of its own, and leaves one open below it.

    A link reference definition is **not** one of them, and saying so reverses
    what this helper used to do. cmark-gfm, the renderer GitHub runs, and
    micromark 4.0.2 both read a definition into the paragraph above it and
    strip it when that paragraph is finalized, so a paragraph *is* open below
    a definition and HTML block condition 7 stays shut. Measured on GitHub's
    own renderer: ``[x]: /url`` over ``<custom>`` over ``## Goal`` paints
    ``<p><custom></p>`` and then ``<h2>Goal</h2>``, and ``[x]: /url`` over a
    four-space line paints that line as a paragraph rather than as code.
    markdown-it 14.3.0 is the one of the three that reads the definition as a
    closed leaf block; this module followed it and counted a heading the page
    does show. Both renderers reproduce the CommonMark 0.31.2 example suite,
    and the suite carries no example of this shape -- so the specification is
    silent here and the page is what counts.
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>

    An indented code block is the fourth shape that needs the state coming in,
    and it is the one the liberal fallback was wrong about in the direction this
    fallback is not allowed to be wrong in. A line indented four columns opens a
    code block only where no paragraph is open; where one is, the line is that
    paragraph's lazy continuation and every rule applies to it. Reading such a
    line as a paragraph held the HTML block condition 7 below it shut and
    counted a ``## Goal`` the page never paints -- measured on GitHub's own
    renderer, which reads a four-space ``x`` over ``<custom>`` over ``## Goal``
    as a code block, an open condition 7 and no heading at all. The indent is
    counted in columns, so a leading tab reaches column four.
    <https://spec.commonmark.org/0.31.2/#indented-code-blocks>

    A table's delimiter row is the third shape that needs the state coming in,
    and it is the Setext underline's twin: it consumes the line above it into
    a table exactly as an underline consumes it into a heading, and leaves no
    paragraph below. ``previous_content`` is that line above, already peeled,
    and is empty when there is none or when the line above sits in a different
    container -- because GFM reads the header row as the line immediately
    above the delimiter row, and the two must agree about the number of cells
    or no table forms at all. Without this the liberal fallback held one
    paragraph open across a whole table, the HTML block condition 7 below it
    was refused, and a ``## Goal`` the page never paints was counted.

    This one is settled against GitHub's own renderer rather than against
    markdown-it 14.3.0, which reads the type-seven tag below a table as a
    *table row* and paints the heading. It is the first place in this module's
    history where the arbiter and the production renderer have been measured
    to part, and the page is what counts.
    https://github.github.com/gfm/#tables-extension-
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
    """
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        return False
    if not paragraph_open and count_indent_columns(content) >= 4:
        return False
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return False
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return False
    if paragraph_open and SETEXT_UNDERLINE_PATTERN.match(content) is not None:
        return False
    if paragraph_open and table_starts_here(previous_content, content):
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
    if (
        open_block is not None
        and open_block.condition.end is None
        and not content.strip(ASCII_HORIZONTAL_WHITESPACE)
    ):
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


def container_interrupts_paragraph(container: Container, content: str) -> bool:
    """Return whether a container opening on a line may interrupt a paragraph.

    A blockquote always may. A list needs two things, and CommonMark states
    them as one rule with two clauses.

    **The item may not be empty.** "In order for a list to interrupt a
    paragraph, the list must not begin with a blank first block." A marker with
    nothing after it is the paragraph's own characters, so ``Words`` then
    ``*`` on the line below is one paragraph of two lines -- and the line after
    *that* is still inside it, which is what keeps a ``<x>`` there from opening
    a type 7 block and hiding the heading under it. ``content`` is the line
    past every container prefix, so a blank one is an empty item.

    **An ordered list must start at 1**, so that a sentence hard-wrapped before
    ``14.`` keeps the number in the sentence instead of turning the rest of the
    document into a list.

    A list that may not interrupt opens nothing at all, and its marker is the
    paragraph's own text. Kept identical to the helper in the sibling hooks.
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
    if container.kind != CONTAINER_KIND_LIST:
        return True
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        # One marker is an exception and it is an exception for a reason that
        # is not about lists at all: ``-`` with nothing after it is also a
        # level 2 Setext underline, and while a paragraph is open CommonMark
        # reads it as the heading. The heading does start a block, so the
        # answer here is the same one the underline would have given.
        # Measured with markdown-it 14.3.0: ``Words`` over ``-`` is an
        # ``<h2>``, while ``Words`` over ``*`` is one paragraph of two lines.
        return container.bullet == "-"
    return container.ordered_start is None or container.ordered_start == 1


def comment_open_below(content: str, position: int) -> str | None:
    """Return ``COMMENT_RUN`` when a comment is still open past ``position``.

    A comment is the one run in ``RAW_TEXT_RUNS`` that can close and open again
    on a single line, so the line has to be walked rather than tested once:
    ``<!-- one --> words <!-- two`` opens a block comment, ends it, and leaves a
    second one open below. Reading only the first delimiter pair answered "no
    run open" there, and a ``<textarea>`` on the next line then opened a run
    inside a comment the page never shows -- so a ``TBD`` written in that
    comment was reported as a placeholder.
    Kept identical to the helper in the sibling hooks.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """
    while True:
        start = content.find("<!--", position)
        if start == -1:
            return None
        end = content.find("-->", start + len("<!--"))
        if end == -1:
            return COMMENT_RUN
        position = end + len("-->")


def raw_text_run_state(
    content: str, open_run: str | None, opens_html_block: bool
) -> tuple[str | None, str | None]:
    """Return the raw HTML run open below a line, and the run the line is in.

    Two values because they are two questions, the pair ``html_block_state``
    asks in the same shape: what the next line inherits, and which run this
    line's characters belong to. A line carrying the closing delimiter is still
    the run's last line, and so is a line carrying both delimiters:
    ``<script><!-- no-source-check: offline --></script>`` holds script data
    rather than a comment, and answering "no run at all" for that line let every
    caller read the body as markup and honour the marker written in it.

    ``opens_html_block`` is whether CommonMark reads this line as part of a raw
    HTML block, and a run may open only where one does. These are the *block*
    forms of raw HTML, so a line that CommonMark keeps inside the paragraph
    above it opens no run: ``<xmp>`` and ``<noembed>`` are in neither HTML block
    condition 1 nor condition 6, so a bare opener on its own line is condition 7
    and may not interrupt a paragraph -- and an ``<xmp>`` written inside an open
    HTML comment therefore opens nothing, while a ``<script>`` written in the
    same place opens condition 1, ends the paragraph, and really does hold raw
    text. Answering that from the element name alone got both of those wrong in
    opposite directions. The caller passes ``line_html_block is not None``.

    The run is returned rather than a bare "yes, this is text" because the two
    callers ask two different things of it. Whether the characters are text
    rather than markup is ``raw_text_run_holds_text`` below, and every hook
    asks it. Whether the page *paints* that text is a second question, asked
    only where a reading score is computed, and it is answered per element
    from the HTML Standard's own rendering rules rather than from this set.

    An opener line is the run's own first line, whether the run closes on it
    or below it. ``<script><!-- no-source-check: offline -->`` with its closer
    two lines down holds script data on that first line exactly as it does on
    the next, and answering "no run here" for the opener let every caller read
    the body as markup. The two branches were settled separately, and why
    the second waited is worth recording: returning the run for *every* line
    was scored and rejected because it would have left a run open below a line
    that already closed it. That objection is about the branch above, where
    ``closing`` is found; in this branch the run really is open below, so the
    line and the state agree.

    An open comment is carried in the same state and is the one run whose
    content is markup: a marker inside a comment is the comment it looks like,
    which is why ``raw_text_run_holds_text`` answers ``False`` for it. It is
    tracked so that a ``<script>`` line written inside a comment opens no run of
    its own -- and so that a run and a comment can never both be open, which is
    what lets a caller strip comments and classify runs in one fixed order
    instead of an order each caller chose for itself.

    The same field carries a third thing, and it is neither a run nor a comment:
    an end tag that has started and not finished. ``</script title="`` ends the
    element's raw text and leaves an HTML parser inside a tag, where the lines
    below are attribute data until the tag's own ``>`` arrives --
    ``closing_tag_run`` spells that state and ``closing_tag_state`` reads it
    back. It is in this field rather than beside it for the reason the comment
    is: three states that exclude one another are one state, and a caller that
    held them apart would have to choose an order to ask them in.
    Kept identical to the helper in the sibling hooks.
    <https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state>
    """
    below, line_run, _ = raw_text_run_boundary(content, open_run, opens_html_block)
    return below, line_run


def raw_text_content_start(content: str, match: "re.Match[str]", key: str) -> int:
    """Return where a raw-text run's *content* begins on its opening line.

    A run opened by one of the eight element names begins after that element's
    own start tag, and an HTML parser reads the whole tag -- name, attributes,
    quoted values and all -- before it enters raw text. So the end-tag spelling
    written inside a quoted attribute value is data:
    ``<script title="</script>">`` opens a run that never closes, and every
    line below it to the end of the file is script data. The other four runs --
    a processing instruction, a CDATA section, a declaration and a comment --
    have no tag to read, so their content begins where their opener ends.

    Measured against ``html.parser``, and this is a place where the two layers
    part company on purpose. CommonMark's HTML block condition 1 ends on a line
    that *contains* ``</script>``, so markdown-it 14.3.0 ends the Markdown block
    on that line and writes an ``<h2>`` under it -- and the page never paints
    that heading, because the browser is still in script data. The block is
    CommonMark's and the run is the page's, and this helper answers for the
    run. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    if key not in RAW_TEXT_ELEMENT_NAMES:
        return match.end()
    start_tag = RAW_TEXT_START_TAG_PATTERN.match(content, match.start())
    return match.end() if start_tag is None else start_tag.end()


def html_tag_close(content: str, index: int) -> int:
    """Return the offset past the ``>`` closing a tag whose name ended at ``index``.

    ``-1`` where the tag does not close in ``content``. This is HTML5's own
    tag-state machine and not a search for a ``>``, because the two give
    different answers and the page follows the machine: a ``>`` written inside a
    quoted attribute value is attribute data, so ``</script title="> x">``
    closes at the *last* ``>`` and not the first. Searching for the character
    ended the tag inside the value and handed the rest of it back to the
    caller as though a reader saw it -- which let a comment spelled in an
    attribute grant an exemption the page never carried.

    The quote characters only open a value after ``=``: HTML5 reads the ``"``
    in ``</script a"b>`` as part of the attribute *name*, so a scanner that
    treated every quote as a delimiter would run past the tag's real end. The
    states below are the spec's, named as the spec names them, and the helper
    is measured against ``html.parser`` rather than reasoned about. Kept
    identical to the helper in the sibling hooks.
    A tag may also *not* end on the line it starts on, and the machine then has
    to be resumed rather than restarted: a line ending inside a quoted attribute
    value is value data, and a line ending between attributes is whitespace.
    ``html_tag_close_state`` is that machine and this is the one-line reading of
    it. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
    """
    return html_tag_close_state(content, index, TAG_STATE_START)[0]


def html_tag_close_state(content: str, index: int, state: str) -> tuple[int, str]:
    """Return where a tag resumed at ``state`` ends, and the state it ends in.

    The offset is ``-1`` where the tag does not close in ``content``, and the
    second value is then the state the next line has to resume from. This is
    ``html_tag_close``'s own machine with its entry state made a parameter and
    its exit state reported, so that an end tag spanning lines is read as one
    tag: ``</script title="`` leaves the machine inside a double-quoted value,
    and every character on the lines below it -- a ``<!--`` included -- is that
    value's data until the quote closes. Kept identical to the helper in the
    sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
    """
    position = index
    while position < len(content):
        character = content[position]
        if state in ("before-attribute-name", "after-attribute-value"):
            if character == ">":
                return position + 1, state
            if character in HTML_TAG_WHITESPACE or character == "/":
                position += 1
                continue
            state = "attribute-name"
            # An ``=`` here is a parse error and becomes the *name*, which is
            # the one character this state may not hand to the state below:
            # reconsumed as a name character it would open a value, and
            # ``</script ="><!-- ... -->`` then lost the ``>`` that ends the
            # tag. Every other character is reconsumed.
            if character == "=":
                position += 1
            continue
        if state == "attribute-name":
            if character == ">":
                return position + 1, state
            if character == "=":
                state = "before-attribute-value"
            elif character in HTML_TAG_WHITESPACE:
                state = "after-attribute-name"
            elif character == "/":
                state = "before-attribute-name"
        elif state == "after-attribute-name":
            if character == ">":
                return position + 1, state
            if character == "=":
                state = "before-attribute-value"
            elif character in HTML_TAG_WHITESPACE:
                pass
            elif character == "/":
                state = "before-attribute-name"
            else:
                state = "attribute-name"
        elif state == "before-attribute-value":
            if character == ">":
                return position + 1, state
            if character == '"':
                state = "attribute-value-double-quoted"
            elif character == "'":
                state = "attribute-value-single-quoted"
            elif character in HTML_TAG_WHITESPACE:
                pass
            else:
                state = "attribute-value-unquoted"
        elif state == "attribute-value-double-quoted":
            if character == '"':
                state = "after-attribute-value"
        elif state == "attribute-value-single-quoted":
            if character == "'":
                state = "after-attribute-value"
        else:  # attribute-value-unquoted
            if character == ">":
                return position + 1, state
            if character in HTML_TAG_WHITESPACE:
                state = "before-attribute-name"
        position += 1
    return -1, state


def raw_text_run_tail(content: str, closer_end: int, key: str) -> int:
    """Return where a closed raw-text run stops holding the line's characters.

    The eight element closers are spelled ``</name`` with a lookahead, so that
    ``</script/`` and ``</script foo>`` close the run as an HTML parser closes
    it. That match ends at the name, and the *tag* ends at its ``>``, so the
    characters a reader sees begin one character further on. The other four
    runs carry their whole delimiter in the match -- ``?>``, ``]]>``, ``>``,
    ``-->`` -- and end where it ends.

    Where the end tag does not close on this line at all, the line has no tail:
    every character after ``</name`` is the tag's own, and handing them back
    read ``</script title="a`` as words a child sees and as a place a comment
    could stand. The other reading -- hand the rest of the line back, which is
    what this helper did before -- was built rather than argued about, and put
    to a generator of 1,536 end tags: it disagrees with ``html.parser`` on 12
    rows against this form's 8, at the same instrument score and the same
    suites.

    Handing the whole line back is only half of what an unfinished end tag
    needs. The other half is the state *below* it, which is
    ``raw_text_run_boundary``'s: an HTML parser goes on reading the tag on the
    lines below, and a comment may not open inside one. Kept identical to the
    helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#end-tag-open-state
    """
    if key not in RAW_TEXT_ELEMENT_NAMES:
        return closer_end
    tag_end = html_tag_close(content, closer_end)
    return len(content) if tag_end == -1 else tag_end


def closing_tag_run(state: str) -> str:
    """Return the run state an end tag left half-read at ``state`` carries.

    Kept identical to the helper in the sibling hooks.
    """
    return CLOSING_TAG_RUN_PREFIX + state


def closing_tag_state(run: str | None) -> str | None:
    """Return the tag state ``run`` carries, or ``None`` where it carries none.

    Kept identical to the helper in the sibling hooks.
    """
    if run is None or not run.startswith(CLOSING_TAG_RUN_PREFIX):
        return None
    return run[len(CLOSING_TAG_RUN_PREFIX) :]

def raw_text_run_boundary(
    content: str, open_run: str | None, opens_html_block: bool
) -> tuple[str | None, str | None, int]:
    """Return a line's raw HTML run state, and where the run ends on this line.

    The first two values are ``raw_text_run_state``'s, unchanged and documented
    there. The third is the offset just past the run's closing delimiter when
    the run closes on this line, and ``-1`` when it does not.

    That third value exists because a run closing is not the same event as a
    line ending. ``<script></script> We plan the trip together`` holds an empty
    script and then twelve words a child reads, and a caller that dropped the
    whole line dropped the words with it -- enough of them to take a document
    under the scoring floor and out of the gate in silence. Only the prose
    extractor asks, for the same reason only it asks
    ``raw_text_run_is_displayed``: the two marker scans care that the
    characters are not markup, and not where the reader's part of the line
    starts. Kept identical to the helper in the sibling hooks.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    if open_run is not None:
        pending = closing_tag_state(open_run)
        if pending is not None:
            # The line is the middle of an end tag that began above it. A tag
            # holds a line ending the way it holds a space -- inside a quoted
            # value it is value data -- so the machine is resumed at the state
            # the line above left it in, with that line ending fed to it.
            end, below = html_tag_close_state(content + "\n", 0, pending)
            if end == -1:
                return closing_tag_run(below), open_run, -1
            end = min(end, len(content))
            return comment_open_below(content, end), open_run, end
        closer = RAW_TEXT_CLOSERS[open_run].search(content)
        if closer is None:
            return open_run, open_run, -1
        tail = raw_text_run_tail(content, closer.end(), open_run)
        end, below = html_tag_close_state(
            content + "\n", closer.end(), TAG_STATE_START
        )
        if open_run in RAW_TEXT_ELEMENT_NAMES and end == -1:
            # The closer started and its *tag* has not finished on this line,
            # which ``raw_text_run_tail`` already says by handing back the whole
            # line. The state below has to say it too: an HTML parser is still
            # reading the tag, so nothing below here opens a comment until the
            # tag's own ``>`` arrives. Clearing the run there read
            # ``</script title="`` over a marker line as a run that had closed
            # and a comment that had opened, and ``has_adult_marker`` skipped a
            # child-facing document on a declaration the page never carried.
            return closing_tag_run(below), open_run, tail
        return (
            comment_open_below(content, closer.end()),
            open_run,
            tail,
        )
    if not opens_html_block:
        return None, None, -1
    for key, opener, closer in RAW_TEXT_RUNS:
        match = opener.match(content)
        if match is None:
            continue
        if key == COMMENT_RUN:
            return comment_open_below(content, match.start()), None, -1
        closing = closer.search(content, raw_text_content_start(content, match, key))
        if closing is not None:
            return (
                comment_open_below(content, closing.end()),
                key,
                raw_text_run_tail(content, closing.end(), key),
            )
        return key, key, -1
    return None, None, -1


def raw_text_run_holds_text(run: str | None) -> bool:
    """Return whether a line inside ``run`` carries text rather than markup.

    Every run in ``RAW_TEXT_RUNS`` but one holds characters the page shows as
    they stand or drops altogether; in neither case is a comment-shaped run on
    the line a comment. The exception is the comment itself, which is in that
    tuple only so that a raw HTML block cannot start inside another one.
    Kept identical to the helper in the sibling hooks.
    """
    return run is not None and run != COMMENT_RUN


def starts_a_block(
    content: str,
    containment_path: tuple[Container, ...],
    opened: tuple[Container, ...],
    previous_path: tuple[Container, ...],
    paragraph_open: bool,
    previous_content: str = "",
) -> bool:
    """Return whether a line begins a block rather than continuing the one above.

    This is where a paragraph ends, and therefore where HTML block condition 7
    is free to open. A blank line ends a paragraph, and so do a heading, a
    thematic break and a Setext underline. So does a container: a list item
    that opens on this line is a new block whatever it holds, and a line whose
    container path is neither the path above it nor a prefix of that path has
    left the paragraph. A prefix *is* a continuation -- an unprefixed line
    under a quoted or listed paragraph is the lazy continuation CommonMark
    reads it as, and treating it as a new block would cut a paragraph in half.

    ``check-session-structure.py`` asks this question under this name, of the
    same six shapes, so the two hooks cannot disagree about where a paragraph
    ends. Kept identical to the helper in that sibling. It is not the question
    ``opens_a_paragraph`` asks above.

    Two of those shapes need the paragraph state, because CommonMark makes both
    of them conditional on one being open. An ordered list may interrupt a
    paragraph only when it starts at 1, so ``2.`` under a sentence is that
    sentence's own text and opens nothing; the rule is the *list's* and not the
    item's, so a ``3.`` under a list already open is its next item and does
    start a block. And a Setext underline may never be a lazy continuation
    line: ``===`` outdented from a quoted or listed paragraph has no root
    paragraph to underline and stays inside the one above it.
    <https://spec.commonmark.org/0.31.2/#paragraphs>
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
    lazy_continuation = (
        paragraph_open
        and len(containment_path) < len(previous_path)
        and containment_path == previous_path[: len(containment_path)]
    )
    if paragraph_open:
        for offset, container in enumerate(opened):
            if container.kind != CONTAINER_KIND_LIST:
                continue
            if container_interrupts_paragraph(container, content):
                break
            depth = len(containment_path) - len(opened) + offset
            if (
                len(previous_path) > depth
                and previous_path[depth].kind == CONTAINER_KIND_LIST
            ):
                # The list is already open above this line, so this is its
                # next item rather than a new list interrupting anything.
                break
            return False
    if not content.strip(ASCII_HORIZONTAL_WHITESPACE):
        return True
    if ATX_HEADING_LINE_PATTERN.match(content) is not None:
        return True
    if THEMATIC_BREAK_LINE_PATTERN.match(content) is not None:
        return True
    if SETEXT_UNDERLINE_PATTERN.match(content) is not None and not lazy_continuation:
        return True
    if table_starts_here(previous_content, content) and not lazy_continuation:
        # A delimiter row consumes the line above it into a table, which is the
        # Setext underline's rule at a different block. Both halves are needed
        # and for the same reason the underline needs both: this says the
        # paragraph above has ended, and ``opens_a_paragraph`` says none is
        # open below. Answering only the second left ``paragraph_open`` true
        # through ``(paragraph_open and not block_starts)``, and the HTML block
        # condition 7 under the table stayed shut.
        # https://github.github.com/gfm/#tables-extension-
        return True
    if any(container.kind == CONTAINER_KIND_LIST for container in opened):
        return True
    return containment_path != previous_path[: len(containment_path)]


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
    if line.strip(ASCII_HORIZONTAL_WHITESPACE):
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
    """Find prohibited placeholder markers in Markdown text.

    A document enters this module here, so this is where its line endings are
    made one thing and where it is cut into lines; see
    ``normalize_line_endings``.
    """
    violations: list[Violation] = []
    is_in_html_comment = False
    # Where the comment that is open below the current line began. CommonMark
    # has two comments and only one of them may cross a block boundary: a
    # ``<!--`` at the start of a line's block content is HTML block condition
    # 2 and runs to the line carrying ``-->`` whatever stands between, while a
    # ``<!--`` written part way along a paragraph line is inline raw HTML and
    # cannot leave the paragraph it opened in. Both renderers agree: measured
    # on GitHub's own and on markdown-it 14.3.0, ``text <!-- a`` over a blank
    # line over ``TODO: x`` paints two paragraphs with the opener *escaped*,
    # so the placeholder is text a reader sees. Reading every ``<!--`` as the
    # block kind hid nine such documents out of seventeen measured.
    # ``check-readability.py`` states the same rule for a whole span in
    # ``comment_span_is_one_block``; this is that rule for a walk that reads
    # one line at a time.
    comment_is_inline = False
    comment_containment_path: tuple[Container, ...] = ()
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    html_block: ActiveHtmlBlock | None = None
    paragraph_open = False
    previous_path: tuple[Container, ...] = ()
    # The line above, carried for the delimiter-row rule in
    # ``opens_a_paragraph``: its peeled content and the container it sat in.
    # Cleared at the top of every iteration, so that any branch which leaves
    # the loop early leaves no header row behind it.
    previous_content = ""
    previous_container: tuple[Container, ...] = ()
    raw_text: str | None = None

    for line_number, raw_line in enumerate(normalize_line_endings(text).split("\n"), start=1):
        above_content, above_container = previous_content, previous_container
        previous_content, previous_container = "", ()
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
            previous_path = ()
            continue

        was_in_html_comment = is_in_html_comment
        # A line CommonMark reads as raw HTML opens no fenced block. Without
        # this the backticks left behind by comment stripping open one, and
        # every placeholder to the end of the file is hidden inside it. The
        # test reads the line with its container prefixes peeled, because a
        # comment nested in a blockquote or a list item opens an HTML block
        # just as the unindented one does -- and hides just as much. A comment
        # is one condition out of several: a ``<div>`` opens a block too, and
        # a line of backticks inside one is raw HTML rather than a fence.
        block_line = container_line(
            raw_line, list_contexts, paragraph_open, previous_path
        )
        block_content = block_line.content
        if html_block is not None and container_path_ended(raw_line, html_block.containment_path):
            # The list item or blockquote holding the block has ended, so the
            # block ended with it, exactly as an unclosed fence does.
            html_block = None
        # Condition 7 is the one HTML block start that may not interrupt a
        # paragraph, so it has to be told when there is no longer one to
        # interrupt. A line that starts a block has closed the paragraph above
        # it, and ``opens_a_paragraph`` cannot say so: it reads one line and
        # answers for the line *below*, so a list item opening on this line
        # inherited the paragraph from the line above and refused the block
        # CommonMark opens inside the new item. The backtick runs under it were
        # then read as a fence rather than as raw HTML, and every placeholder
        # between them went unreported while the page printed them.
        header_above = (
            above_content if above_container == block_line.containment_path else ""
        )
        block_starts = starts_a_block(
            block_content,
            block_line.containment_path,
            block_line.opened,
            previous_path,
            paragraph_open,
            header_above,
        )
        if is_in_html_comment and comment_is_inline and (
            block_line.containment_path != comment_containment_path
            or bool(block_line.opened)
            or block_starts
            or parse_opening_fence(block_content) is not None
            or not opens_a_paragraph(block_content, True, header_above)
        ):
            # The paragraph holding the opener has ended, so the ``<!--`` was
            # never a comment. The five tests are the five ways a paragraph
            # ends under it: the line has left the container the opener sat
            # in, a container opened on this line, an HTML block opened, a
            # fence opened, or the line is one ``opens_a_paragraph`` refuses --
            # a blank line, a heading, a thematic break, a Setext underline, a
            # table's delimiter row.
            #
            # ``paragraph_open`` is *not* asked, and the reason is worth the
            # line: it is set ``False`` on every line of an open HTML block,
            # and an open comment is one of the conditions that makes a line
            # one. Reading it here made the comment end the paragraph and the
            # ended paragraph end the comment. Measured on the document
            # ``Words here <!-- a note`` over ``<xmp>`` over ``TBD`` over
            # ``</xmp>`` over ``end of the note -->``: GitHub paints
            # ``<p>Words here </p>`` and nothing else, so the ``TBD`` is
            # inside the comment, and asking ``paragraph_open`` reported it.
            # ``True`` is passed instead, because a comment that opened inline
            # had a paragraph to open in.
            #
            # ``was_in_html_comment`` is cleared with it: it was read out of
            # this variable a few lines above and would otherwise carry the
            # stale answer into ``in_html_block``.
            is_in_html_comment = False
            was_in_html_comment = False
        html_block, line_html_block = html_block_state(
            block_content,
            block_line.containment_path,
            html_block,
            paragraph_open and not block_starts,
        )
        # Three pieces of state and one order, written here once so that no
        # caller has to rediscover it: CommonMark says which lines are raw HTML
        # at all, the raw-text run says which of those hold text rather than
        # markup, and only then are comments stripped from what is left. Asking
        # the run before the block opened a run on a line CommonMark keeps
        # inside the paragraph above it; stripping before the run read a
        # comment-shaped run a ``<script>`` prints as a real comment. The
        # sibling hooks ask in this same order.
        raw_text, line_raw_text, raw_text_end = raw_text_run_boundary(
            block_content, raw_text, line_html_block is not None
        )
        in_raw_text = raw_text_run_holds_text(line_raw_text)
        run_released_the_line = in_raw_text and raw_text_end != -1
        if run_released_the_line:
            # The run closes part way along this line, and what follows the
            # closer is not the element's content: the browser leaves raw text
            # at the closing tag. ``<script></script><!-- TBD -->`` holds an
            # empty script and then a real comment, and reading the whole line
            # as script data reported a placeholder the comment hides.
            #
            # The run's own characters are *kept* rather than blanked, because
            # this hook reports a placeholder written inside a raw-text
            # element: its rule is about comments and fences, and script data
            # is neither. Only the part after the closer has its comments
            # stripped, which is what the two sibling hooks achieve by blanking
            # -- they ask whether the run's characters are markup, and this one
            # asks whether they are a comment.
            in_raw_text = False
        if in_raw_text:
            # The line is a raw-text element's content, which the page
            # displays as it stands. A comment-shaped run there opens no
            # comment and hides no placeholder, so the line is read whole.
            commentless_line = raw_line
            comment_opened_here = False
        elif run_released_the_line:
            # The run held the head of the line and released the tail, so only
            # the tail is read for comments -- and no comment can be open
            # coming in, because a run opens only at the start of a line.
            split = len(raw_line) - len(block_content) + raw_text_end
            tail, is_in_html_comment, comment_opened_here = strip_html_comments(
                raw_line[split:], False
            )
            commentless_line = raw_line[:split] + tail
        else:
            commentless_line, is_in_html_comment, comment_opened_here = (
                strip_html_comments(raw_line, is_in_html_comment)
            )
        if comment_opened_here:
            # A line CommonMark reads as raw HTML holds no inline content, so a
            # comment opening on one is the block kind. Everywhere else the
            # opener sits inside a paragraph and the comment is inline.
            comment_is_inline = line_html_block is None
            comment_containment_path = block_line.containment_path
        if raw_text_run_holds_text(raw_text):
            # A raw-text run is open below this line, so no comment can be open
            # inside it. Said here as well as above because a run opens part way
            # along its own line -- ``<textarea> <!-- a note`` -- and the
            # stripping above would otherwise carry a comment the page never
            # shows down into the lines the element prints.
            is_in_html_comment = False
        # The comment is one of the conditions the machine tracks; an inline
        # comment opened part way along a line is not a block, so its
        # cross-line state is still consulted here.
        in_html_block = was_in_html_comment or line_html_block is not None

        opening_fence_line = normalize_for_fence_opening(
            commentless_line, list_contexts, paragraph_open, previous_path
        )
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
            previous_path = ()
            continue

        previous_path = block_line.containment_path
        # Written here rather than above, so the fence branch reads the state
        # the line above left and not the one this line would leave. The
        # sibling hook writes it in the same place. It reads the state the line
        # above left rather than ``block_starts``, because a Setext underline
        # starts a block and closes the paragraph it underlines, and answering
        # that from a cleared state would leave a paragraph open under a
        # heading.
        # A line that starts no block leaves the paragraph above it open,
        # whatever its content peels to. The case that needs saying is the
        # empty list item: it may not interrupt a paragraph, so its marker is
        # the paragraph's own text -- but the container walk peels the marker
        # off and hands an empty content down, which reads exactly like a
        # blank line. Measured with markdown-it 14.3.0: ``Words`` then ``*``
        # then ``<x>`` is one paragraph of three lines, and the ``## Goal``
        # below is a heading.
        paragraph_open = (
            False
            if in_html_block
            else (paragraph_open and not block_starts)
            or opens_a_paragraph(block_content, paragraph_open, header_above)
        )
        previous_content = block_content
        previous_container = block_line.containment_path

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


def default_targets(root: Path) -> list[Path]:
    """Return every Markdown file under the scan roots, for a run given none.

    Both sibling hooks walk a default set when they are handed no path, and
    this one did not: it iterated an empty argument list, printed nothing and
    exited zero, so a maintainer who typed the bare command was told the
    repository was clean by a run that had opened no file. The two roots that
    hold no Markdown at all are not an error -- ``docs`` may be the only one
    populated in a downstream adoption -- but all three being empty is, and
    the caller says so rather than reporting the clean result of reading
    nothing.
    """
    found: list[Path] = []
    for name in SCAN_TARGET_ROOTS:
        directory = root / name
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*")):
            # ``rglob("*.md")`` matches the suffix case-sensitively, so on a
            # case-sensitive filesystem a file named with an uppercase suffix
            # was never selected -- while ``resolve_candidate_path`` accepts it
            # when the same file is named on the command line, so the two
            # entry points disagreed about the same file. The pre-commit hook's
            # own ``files:`` regex is lowercase-only for the same reason and is
            # a separate repair.
            if not path.is_file() or path.suffix.lower() != ".md":
                continue
            relative = path.relative_to(root).as_posix()
            if any(relative.startswith(prefix) for prefix in DEFAULT_SCAN_EXCLUDES):
                continue
            found.append(path)
    return found


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Check docs Markdown for prohibited placeholder markers. "
            "With no paths, checks every Markdown file under the scan roots."
        )
    )
    parser.add_argument("paths", nargs="*", help="Markdown files passed by pre-commit.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the placeholder check."""
    args = parse_args(argv)

    targets: Sequence[str | Path] = args.paths
    walked = not args.paths
    if walked:
        targets = default_targets(root)
        if not targets:
            print(
                "no Markdown file was found under "
                + ", ".join(SCAN_TARGET_ROOTS)
                + ", so this run checked nothing. A path that is named and "
                "then yields neither a target nor a refusal is a path this "
                "run passed over in silence. Check the working directory, or "
                "check SCAN_TARGET_ROOTS if this was the default scan.",
                file=sys.stderr,
            )
            return 1

    try:
        violations = scan_files(targets, root=root)
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1

    for violation in violations:
        print(violation.format_message())

    if walked and not violations:
        # The count is the difference between "clean" and "read nothing". The
        # sibling hooks print theirs; a silent pass is what let this one report
        # success on an empty set for as long as it did.
        print(f"Placeholders: {len(targets)} file(s) checked, none found.")

    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
