"""Tests for the prohibited Markdown placeholder pre-commit hook."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol, cast

from tests._pytest_compat import pytest

HOOK_PATH = (
    Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-prohibited-placeholders.py"
)
HOOK_SPEC = importlib.util.spec_from_file_location("check_prohibited_placeholders", HOOK_PATH)
if HOOK_SPEC is None or HOOK_SPEC.loader is None:
    raise RuntimeError(f"Unable to load placeholder hook module from {HOOK_PATH}")
_placeholder_hook = importlib.util.module_from_spec(HOOK_SPEC)
sys.modules[HOOK_SPEC.name] = _placeholder_hook
HOOK_SPEC.loader.exec_module(_placeholder_hook)


class ViolationLike(Protocol):
    """Attributes exposed by a placeholder-hook violation."""

    display_path: str
    line_number: int
    matched_text: str


class PlaceholderHookModule(Protocol):
    """Typed public surface used from the file-path-loaded placeholder hook."""

    def scan_files(
        self,
        path_arguments: Iterable[str | Path],
        root: Path,
    ) -> list[ViolationLike]: ...

    def main(self, argv: Iterable[str] | None = None, root: Path = ...) -> int: ...

    def find_violations_in_text(self, text: str, display_path: str) -> list[ViolationLike]: ...


placeholder_hook: PlaceholderHookModule = cast(PlaceholderHookModule, _placeholder_hook)


def write_file(path: Path, content: str) -> Path:
    """Create a test file and its parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def scan_single_file(path: Path, root: Path) -> list[ViolationLike]:
    """Scan one file through the public hook path."""
    return placeholder_hook.scan_files([path], root=root)


def _find(text: str) -> list[ViolationLike]:
    """Scan one document through the public text path, with no file in between."""
    return placeholder_hook.find_violations_in_text(text, "x.md")


@pytest.mark.parametrize(
    ("content", "matched_text"),
    [
        ("The value is TBD.\n", "TBD"),
        ("TODO: document the timeout.\n", "TODO:"),
        ("Fix this FIXME marker.\n", "FIXME"),
        ("Remove this XXX marker.\n", "XXX"),
        ("The limit is to be determined.\n", "to be determined"),
        (
            "The timeout uses (default duration to be determined).\n",
            "(default duration to be determined)",
        ),
    ],
)
def test_required_patterns_are_flagged(
    tmp_path: Path,
    content: str,
    matched_text: str,
) -> None:
    """Each required placeholder pattern is prohibited in docs Markdown."""
    path = write_file(tmp_path / "docs" / "spec" / "example.md", content)

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].display_path == "docs/spec/example.md"
    assert violations[0].line_number == 1
    assert violations[0].matched_text == matched_text


@pytest.mark.parametrize(
    "content",
    [
        "Keep this value TBD. <!-- ALLOW-TBD: upstream contract not finalized -->\n",
        "<!-- TODO: this single-line HTML comment is ignored. -->\n",
        "**Open Question:** Should the default be TBD?\n",
        "**Open Questions:** Is the timeout to be determined by callers?\n",
        "**Assumption:** FIXME is quoted from an upstream draft.\n",
        "- **Open Question:** Can this stay TODO: until the spec lands?\n",
        "- **Assumption:** The value is XXX in the source document.\n",
        "1. **Open Question:** Does the limit stay TBD until v2?\n",
        "12. **Assumption:** XXX represents a placeholder index.\n",
        "1) **Open Question:** Does the parenthesized marker stay TBD?\n",
        "12) **Assumption:** XXX in a parenthesized ordered list.\n",
    ],
)
def test_required_allowlist_contexts_are_not_flagged(tmp_path: Path, content: str) -> None:
    """Allowed suppression, comment, Open Question, and Assumption lines pass."""
    path = write_file(tmp_path / "docs" / "spec" / "example.md", content)

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_ordered_allowlist_label_requires_marker_spacing(tmp_path: Path) -> None:
    """A malformed ordered-list marker does not suppress placeholder checks."""
    path = write_file(tmp_path / "docs" / "spec" / "example.md", "1.**Open Question:** TBD\n")

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].line_number == 1
    assert violations[0].matched_text == "TBD"


def test_ordered_allowlist_label_rejects_overlong_digit_marker(tmp_path: Path) -> None:
    """An ordered marker with more than 9 digits is not a CommonMark list marker."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "1234567890. **Open Question:** TBD with an overlong digit marker.\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].line_number == 1
    assert violations[0].matched_text == "TBD"


def test_changelog_markdown_files_are_not_flagged(tmp_path: Path) -> None:
    """CHANGELOG*.md files are exempt from the docs placeholder check."""
    path = write_file(tmp_path / "docs" / "CHANGELOG-2026.md", "The value is TBD.\n")

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_multiline_fenced_code_block_is_not_flagged(tmp_path: Path) -> None:
    """A genuine multi-line fenced code block is excluded from scanning."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "```text",
                "TODO: this is an example inside a fence.",
                "```",
                "The real value is measurable.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


@pytest.mark.parametrize(
    "content",
    [
        "\n".join(
            [
                "- A bullet with a continuation fence:",
                "",
                "    ```text",
                "    TODO: example value",
                "    ```",
                "- Next bullet.",
            ]
        )
        + "\n",
        "\n".join(
            [
                "1. A numbered item with a continuation fence:",
                "",
                "    ```text",
                "    TBD inside a numbered-list fence.",
                "    ```",
                "2. Next numbered item.",
            ]
        )
        + "\n",
        "\n".join(
            [
                "> ```text",
                "> FIXME inside a blockquote fence.",
                "> ```",
            ]
        )
        + "\n",
        "\n".join(
            [
                "- Parent item:",
                "  - Child item with a continuation fence:",
                "",
                "      ```text",
                "      XXX inside a nested-list fence.",
                "      ```",
            ]
        )
        + "\n",
    ],
)
def test_container_fenced_code_blocks_are_not_flagged(
    tmp_path: Path,
    content: str,
) -> None:
    """Fenced code blocks indented under Markdown containers are excluded."""
    path = write_file(tmp_path / "docs" / "spec" / "example.md", content)

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_blockquote_inside_list_item_preserves_list_context(tmp_path: Path) -> None:
    """A blockquote within a list item must not pop the active list context."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "- Parent item with an aside:",
                "  > A quoted aside inside the list item.",
                "",
                "    ```text",
                "    TBD inside a continuation fence after a blockquote.",
                "    ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_list_inside_blockquote_preserves_list_context_across_blank_line(
    tmp_path: Path,
) -> None:
    """A list nested inside a blockquote must not be pruned by a blank blockquote line."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "> 1. Item with a continuation fence:",
                ">",
                ">     ```text",
                ">     TBD inside a blockquote-list continuation fence.",
                ">     ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_blockquote_inside_nested_list_item_fence_is_not_flagged(tmp_path: Path) -> None:
    """A blockquote-wrapped fence inside a nested list item (> past column 3) is excluded."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "- Parent item:",
                "  - Child item with a quoted fence:",
                "",
                "      > ```text",
                "      > XXX inside a nested-list blockquote fence.",
                "      > ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_nested_blockquote_in_blockquote_list_preserves_continuation_fence(
    tmp_path: Path,
) -> None:
    """A nested blockquote aside inside a blockquote-contained list must not break later fences."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "> 1. Item with a nested aside:",
                "> > Note: see the upstream draft.",
                ">",
                ">     ```text",
                ">     TBD inside a continuation fence after a nested blockquote.",
                ">     ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_list_inside_blockquote_inside_list_item_preserves_fence(
    tmp_path: Path,
) -> None:
    """A list nested inside a blockquote that is itself nested inside another list item."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "123. Outer item with content_indent=5.",
                "     > 1. Nested list inside blockquote.",
                "     >",
                "     >     ```text",
                "     >     TBD inside continuation fence.",
                "     >     ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_top_level_four_space_fence_marker_is_not_treated_as_fence(tmp_path: Path) -> None:
    """A top-level 4-space-indented fence marker does not suppress later prose."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "    ```text",
                "TODO: this line remains scannable outside a recognized fence.",
                "    ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].line_number == 2
    assert violations[0].matched_text == "TODO:"


def test_multiline_tilde_fenced_code_block_is_not_flagged(tmp_path: Path) -> None:
    """Tilde fences receive the same multi-line exclusion as backtick fences."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "~~~text",
                "FIXME inside a tilde fence.",
                "~~~",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_multiline_html_comment_is_not_flagged(tmp_path: Path) -> None:
    """A genuine multi-line HTML comment is excluded from scanning."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "<!--",
                "The default is to be determined.",
                "-->",
                "The real value is measurable.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_allow_tbd_on_html_comment_closing_line_preserves_state(tmp_path: Path) -> None:
    """ALLOW-TBD on a line that also closes a multi-line HTML comment keeps state correct."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "<!-- multi-line comment opening",
                "still inside the comment --> <!-- ALLOW-TBD: closing line -->",
                "The value is TBD on a regular line.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].line_number == 3
    assert violations[0].matched_text == "TBD"


def test_allow_tbd_on_fence_opening_line_enters_fence(tmp_path: Path) -> None:
    """ALLOW-TBD on a line that also opens a fenced code block still enters the fence."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "```text <!-- ALLOW-TBD: documented example -->",
                "TBD inside the fenced block should not be flagged.",
                "```",
                "The value is TBD outside the fenced block.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert len(violations) == 1
    assert violations[0].line_number == 4
    assert violations[0].matched_text == "TBD"


def test_todo_task_list_without_colon_is_not_flagged(tmp_path: Path) -> None:
    """GitHub issue-style TODO task items without a colon are allowed."""
    path = write_file(tmp_path / "docs" / "spec" / "example.md", "- [ ] TODO\n")

    violations = scan_single_file(path, tmp_path)

    assert violations == []


def test_markdown_outside_docs_is_not_scanned(tmp_path: Path) -> None:
    """Markdown outside the guarded roots (docs/, framework/, destinations/) is not scanned."""
    path = write_file(tmp_path / "README.md", "The value is TBD.\n")

    violations = scan_single_file(path, tmp_path)

    assert violations == []


@pytest.mark.parametrize("root_dir", ["framework", "destinations"])
def test_curriculum_markdown_is_scanned(tmp_path: Path, root_dir: str) -> None:
    """Built-curriculum Markdown under framework/ and destinations/ is guarded."""
    path = write_file(tmp_path / root_dir / "session-01.md", "The value is TBD.\n")

    violations = scan_single_file(path, tmp_path)

    assert [violation.matched_text for violation in violations] == ["TBD"]


def test_main_reports_actionable_failure_message(
    tmp_path: Path,
    capsys: Any,
) -> None:
    """CLI output includes path, line, matched text, remediation, and suppression syntax."""
    write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "Measured value.",
                "The timeout uses (default duration to be determined).",
            ]
        )
        + "\n",
    )

    result = placeholder_hook.main(["docs/spec/example.md"], root=tmp_path)

    captured = capsys.readouterr()
    assert result == 1
    assert captured.err == ""
    assert (
        "docs/spec/example.md:2: prohibited placeholder " '"(default duration to be determined)"'
    ) in captured.out
    assert "replace with a measurable value" in captured.out
    assert "<!-- ALLOW-TBD: <reason> -->" in captured.out
    assert '.github/instructions/docs.instructions.md "Prohibited Patterns"' in captured.out


def test_an_unclosed_blockquote_fence_ends_with_its_blockquote(tmp_path: Path) -> None:
    """A fence ends with the container that holds it, so the scan resumes after it.

    CommonMark closes an unterminated fenced block at the end of its containing
    block (<https://spec.commonmark.org/0.31.2/#fenced-code-blocks>). Treating
    the fence as open to the end of the file would silence every placeholder in
    the rest of the document.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "> ```text",
                "> An example that is never closed.",
                "",
                "# Real heading",
                "",
                "The limit is TBD.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"]


def test_an_unclosed_list_fence_ends_with_its_list_item(tmp_path: Path) -> None:
    """The same rule for a fence nested under a list item."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "1. An example:",
                "",
                "   ```text",
                "   Never closed.",
                "",
                "The limit is TBD.",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"]


def test_a_blank_line_does_not_end_a_list_nested_fence(tmp_path: Path) -> None:
    """A positive control. Inside a list item a blank line is ordinary fence content."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "\n".join(
            [
                "1. An example:",
                "",
                "   ```text",
                "   first line",
                "",
                "   The limit is TBD.",
                "   ```",
            ]
        )
        + "\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert violations == []


# ---------------------------------------------------------------------------
# Round 6: an HTML block opens no fence here either
# ---------------------------------------------------------------------------


def test_an_html_block_line_with_trailing_backticks_opens_no_fence(tmp_path: Path) -> None:
    """An HTML block runs to its ``-->``, so nothing on those lines opens a fence.

    Treating the backticks left behind by comment stripping as a fence hides
    every placeholder from there to the end of the file.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<!-- note --> ```\n\nThe limit is TBD.\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"]


def test_a_placeholder_beside_a_comment_on_one_line_is_still_flagged(tmp_path: Path) -> None:
    """A positive control. The HTML-block test governs fences, not visibility.

    ``TBD`` after a ``-->`` still prints the characters TBD to the reader, so
    the hook must still report it.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<!-- note --> The limit is TBD.\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"]


def test_a_fence_on_the_line_after_a_comment_still_hides_a_placeholder(
    tmp_path: Path,
) -> None:
    """A positive control. Only the HTML-block line itself opens no fence."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<!-- note -->\n\n```text\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


# ---------------------------------------------------------------------------
# Round 7: a container prefix does not stop an HTML block from being one
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "first_line", "second_line"),
    [
        ("blockquote", "> <!-- note --> ```", "> The limit is TBD."),
        ("nested blockquote", "> > <!-- note --> ```", "> > The limit is TBD."),
        ("bullet", "- <!-- note -->```", "  The limit is TBD."),
        ("ordered item", "1. <!-- note -->```", "   The limit is TBD."),
        ("bullet in a blockquote", "> - <!-- note -->```", ">   The limit is TBD."),
    ],
)
def test_a_container_nested_html_block_opens_no_fence(
    label: str, first_line: str, second_line: str, tmp_path: Path
) -> None:
    """CommonMark decides the block after the container prefix comes off.

    Reading the raw line meant the blockquote or bullet hid the HTML block, so
    the backticks after the comment opened a fence and every placeholder below
    it went unreported.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        f"{first_line}\n{second_line}\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"], (label, violations)


def test_a_real_fence_inside_a_blockquote_still_hides_a_placeholder(tmp_path: Path) -> None:
    """A positive control. Only the HTML-block line is exempt from opening one."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "> ```text\n> The limit is TBD.\n> ```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_placeholder_after_a_blockquoted_comment_is_still_flagged(tmp_path: Path) -> None:
    """A positive control. The HTML-block test governs fences, not visibility."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "> <!-- note --> The limit is TBD.\n",
    )

    violations = scan_single_file(path, tmp_path)

    assert [v.matched_text for v in violations] == ["TBD"]


def test_the_html_block_test_does_not_disturb_list_tracking(tmp_path: Path) -> None:
    """A negative control on the state, not the answer.

    The peel asks a question about one line; it must not advance the list
    contexts that govern the rest of the file. If it did, the real fence in the
    same list item would be peeled against the wrong content column and would
    not be found, and the placeholder inside it would be reported as prose.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "- <!-- note -->\n\n  ```text\n  The limit is TBD.\n  ```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_fence_line_inside_a_div_block_hides_nothing(tmp_path: Path) -> None:
    """Round 8: a comment is one HTML block condition out of several.

    The backticks inside the ``<div>`` are raw HTML, so no fenced block opens.
    Before this, they opened one that never closed, and every placeholder to
    the end of the file went unreported.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<div>\n```\n</div>\n\nThe limit is TBD.\n",
    )

    assert [v.matched_text for v in scan_single_file(path, tmp_path)] == ["TBD"]


def test_a_fence_line_inside_a_blockquoted_div_block_hides_nothing(tmp_path: Path) -> None:
    """The container prefixes are peeled first, as they are for a comment."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "> <div>\n> ```\n\nThe limit is TBD.\n",
    )

    assert [v.matched_text for v in scan_single_file(path, tmp_path)] == ["TBD"]


def test_a_fence_line_inside_a_script_block_hides_nothing(tmp_path: Path) -> None:
    """Start condition 1 runs to the line carrying the matching closing tag."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<script>\n```\n</script>\n\nThe limit is TBD.\n",
    )

    assert [v.matched_text for v in scan_single_file(path, tmp_path)] == ["TBD"]


def test_a_real_fence_after_a_div_block_still_hides_what_it_holds(tmp_path: Path) -> None:
    """A negative control. The block ends at the blank line; the fence is real."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<div>\n</div>\n\n```\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_placeholder_inside_a_div_block_is_still_reported(tmp_path: Path) -> None:
    """A positive control. The HTML-block test governs fences, never visibility.

    Raw HTML is passed through to the page, so a placeholder inside a ``<div>``
    is a placeholder the reader sees.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<div>\nThe limit is TBD.\n</div>\n",
    )

    assert [v.matched_text for v in scan_single_file(path, tmp_path)] == ["TBD"]


def test_an_ordinary_paragraph_starting_with_a_tag_still_opens_its_fence(
    tmp_path: Path,
) -> None:
    """A negative control. ``<b>`` is not one of the block-level element names."""
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<b>bold</b>\n\n```\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


# ---------------------------------------------------------------------------
# Issue 27: the HTML-block findings PR #23 deferred, in the sibling hook
# ---------------------------------------------------------------------------


def test_an_unclosed_html_block_ends_with_its_blockquote(tmp_path: Path) -> None:
    """A leaf block ends with the block that holds it, as an unclosed fence does.

    The HTML-block state had no containment path, so the ``<script>`` stayed
    open past the outdent; a line read as raw HTML opens no fence, so the
    example below was never a fence and its placeholder was reported.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "> <script>\n\n```\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_script_line_inside_a_comment_opens_no_block(tmp_path: Path) -> None:
    """No start condition is tried while an HTML block is open.

    A ``<script>`` written inside a multiline comment opened a second state
    that outlived the ``-->`` and hid every fence below it.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<!-- a note\n<script>\n-->\n\n```\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_fence_inside_a_type_seven_html_block_is_not_a_fence(tmp_path: Path) -> None:
    """A complete tag alone at a block boundary opens a raw HTML block.

    The backticks inside it are raw HTML rather than a fence, so the
    placeholder on the line below is characters on the page and is reported.
    Measured against markdown-it 14.3.0.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "<x-session>\n```\nThe limit is TBD.\n```\n",
    )

    assert [violation.matched_text for violation in scan_single_file(path, tmp_path)] == ["TBD"]


def test_a_nonbreaking_space_does_not_close_a_fence(tmp_path: Path) -> None:
    """CommonMark permits spaces and tabs after a closing fence and nothing else.

    The narrowed pattern keeps the block open, so the placeholder under the
    fake closing fence stays inside the example -- which is where the renderer
    keeps it.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "```\ncode\n```\u00a0\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_fence_whose_container_ends_does_not_leave_a_paragraph_open(tmp_path: Path) -> None:
    """A fence line opens a code block, not a paragraph.

    The paragraph state was written before the opening-fence branch, where a
    fence line reads as ordinary text, so a fence whose blockquote ended on the
    very next line handed a stale open paragraph to the line below it. The
    complete tag there was refused HTML block condition 7, the backticks under
    it opened a fence of their own, and the placeholder inside went unreported.
    Measured against markdown-it 14.3.0: the tag opens a raw HTML block and the
    placeholder is characters on the page.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "> ```\n<x-session>\n```\nThe limit is TBD.\n",
    )

    assert [violation.matched_text for violation in scan_single_file(path, tmp_path)] == ["TBD"]


def test_an_open_paragraph_still_refuses_a_complete_tag(tmp_path: Path) -> None:
    """A negative control. Condition 7 is the one condition that may not interrupt.

    A paragraph really is open above the tag here, so no HTML block opens, the
    backticks below it are a fence, and the placeholder inside is an example.
    Measured against markdown-it 14.3.0.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "Heading\n<x-session>\n```\nThe limit is TBD.\n```\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_a_form_feed_does_not_end_a_line(tmp_path: Path) -> None:
    """CommonMark knows three line endings, and a form feed is none of them.

    The walk cut the document with ``str.splitlines``, which also splits on a
    form feed, a vertical tab and two Unicode separators, so a form feed in
    front of a fence produced a closing fence out of thin air and the example
    below it was reported as a violation. Measured against markdown-it 14.3.0:
    the block never closes and the placeholder stays inside it.
    """
    path = write_file(
        tmp_path / "docs" / "spec" / "example.md",
        "```\ncode\n\x0c```\nThe limit is TBD.\n",
    )

    assert scan_single_file(path, tmp_path) == []


def test_crlf_line_endings_report_what_line_feeds_report() -> None:
    """A negative control, and the one that keeps the new split honest.

    Splitting on ``\\n`` alone is what the sibling hooks do, and it is right
    only because the document's line endings are made one thing first. A
    closing fence carrying a stray ``\\r`` would not close, and the placeholder
    below it would vanish into the block that never ended.
    """
    text = "# T\n\n```\ncode\n```\n\nThe limit is TBD.\n"
    expected = [violation.matched_text for violation in _find(text)]

    assert expected == ["TBD"]
    assert [violation.matched_text for violation in _find(text.replace("\n", "\r\n"))] == expected
# --- round 3: HTML block condition 4 wants a capital ------------------------


def test_a_lowercase_declaration_does_not_open_an_html_block() -> None:
    """Condition 4 took any ASCII letter, and the fence below paid for it.

    ``<!foo>`` closed the paragraph, the complete tag on the next line opened a
    type-seven block, and the fence inside that block stopped being a fence --
    so a placeholder that is code was reported as text. Measured against
    markdown-it 14.3.0: both lines stay in the paragraph, the fence interrupts
    it, and ``TBD`` is inside a code block.
    """
    text = "Pack a snack for the walk.\n<!foo>\n<x>\n```\nTBD\n```\n\nRide your bike.\n"

    assert _find(text) == []


def test_an_uppercase_declaration_still_opens_an_html_block() -> None:
    """A negative control. The condition is real; it just wants a capital.

    Measured against markdown-it 14.3.0: the declaration closes the paragraph,
    the tag opens a block, and everything down to the blank line -- fence
    markers included -- is raw HTML the page prints.
    """
    text = (
        "Pack a snack for the walk.\n<!DOCTYPE html>\n<x>\n```\nTBD\n```\n\nRide your bike.\n"
    )

    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


#: One non-breaking space, spelled through a name for the reason the sibling
#: test modules spell it through one.
NONBREAKING_SPACE = "\u00a0"

#: A three-backtick code fence.
FENCE = "`" * 3


def test_a_nonbreaking_space_line_does_not_leave_a_list() -> None:
    """A line of one U+00A0 is a paragraph, not a blank line.

    A fence opened inside a list item ends where the list item ends. The
    non-breaking space at column 0 has outdented out of the item, so measured
    against markdown-it 14.3.0 the fence ends there and the placeholder below
    it is on the page, where this hook has to report it. ``str.strip`` with no
    argument read the line as blank, kept the fence open, and let the
    placeholder through.
    https://spec.commonmark.org/0.31.2/#blank-line
    """
    text = f"- item\n\n  {FENCE}\n  code\n{NONBREAKING_SPACE}\n  TBD tomorrow.\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


@pytest.mark.parametrize(
    ("label", "filler"),
    [("an empty line", ""), ("three spaces", "   "), ("a tab", "\t")],
)
def test_a_blank_line_does_not_leave_a_list(label: str, filler: str) -> None:
    """The negative control. A blank line is ordinary list content.

    The fence is still open below it, so the placeholder really is inside a
    code block and is not reported.
    """
    text = f"- item\n\n  {FENCE}\n  code\n{filler}\n  TBD tomorrow.\n"
    assert _find(text) == [], label


def test_a_nonbreaking_space_line_does_not_close_an_html_block() -> None:
    """Only a blank line closes an HTML block whose condition has no end tag.

    Condition 6 is still open below a line of one U+00A0, so the backticks
    under it are raw HTML rather than a fence and markdown-it 14.3.0 prints
    the placeholder between them. Closing the block early made the fence real
    and hid a placeholder that is on the page.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    text = f"<div>\nnote\n{NONBREAKING_SPACE}\n{FENCE}\nTBD tomorrow.\n{FENCE}\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


def test_a_blank_line_closes_an_html_block() -> None:
    """The negative control. A real blank line still closes condition 6.

    The fence below it is a real fence, so the placeholder inside it is code.
    """
    text = f"<div>\nnote\n\n{FENCE}\nTBD tomorrow.\n{FENCE}\n"
    assert _find(text) == []


# --- round 7: a block start clears the paragraph above condition 7 ----------


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "a list item opening on the line",
            f"Words above the list.\n- <x-session>\n  {FENCE}\n  TBD tomorrow.\n  {FENCE}\n",
        ),
        (
            "a second list item",
            f"- Words in item one\n- <x-session>\n  {FENCE}\n  TBD tomorrow.\n  {FENCE}\n",
        ),
        (
            "a nested list item",
            f"- Words in item one\n  - <x-session>\n    {FENCE}\n"
            f"    TBD tomorrow.\n    {FENCE}\n",
        ),
        (
            "a blockquote opening on the line",
            f"Words above the quote.\n> <x-session>\n> {FENCE}\n"
            f"> TBD tomorrow.\n> {FENCE}\n",
        ),
        (
            "an ordered list starting at one",
            f"Words above the list.\n1. <x-session>\n   {FENCE}\n"
            f"   TBD tomorrow.\n   {FENCE}\n",
        ),
    ],
)
def test_a_container_opening_on_a_line_lets_condition_seven_open(
    label: str, document: str
) -> None:
    """A container that opens on a line has closed the paragraph above it.

    HTML block condition 7 is the one start that may not interrupt a paragraph,
    and ``opens_a_paragraph`` answers for the line *below* the one it reads, so
    a list item or a blockquote opening on this line inherited the paragraph
    from the line above and refused the block CommonMark opens inside the new
    container. The backtick runs under it were then read as a fence rather than
    as raw HTML, and the placeholder between them went unreported while
    markdown-it 14.3.0 printed it on the page. ``starts_a_block`` is the
    sibling hook's name for the other half of the question, and this hook had
    never been given it.
    <https://spec.commonmark.org/0.31.2/#html-blocks>
    """
    assert [violation.matched_text for violation in _find(document)] == ["TBD"], label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        (
            "a tag under a root paragraph",
            f"Words above.\n<x-session>\n{FENCE}\nTBD tomorrow.\n{FENCE}\n",
        ),
        (
            "a tag outdented out of a list item",
            f"- Words in a list item.\n<x-session>\n{FENCE}\nTBD tomorrow.\n{FENCE}\n",
        ),
        (
            "a tag continuing a list item's paragraph",
            f"- Words in a list item.\n  <x-session>\n  {FENCE}\n"
            f"  TBD tomorrow.\n  {FENCE}\n",
        ),
        (
            "a tag continuing a quoted paragraph",
            f"> Words in a quote.\n> <x-session>\n> {FENCE}\n"
            f"> TBD tomorrow.\n> {FENCE}\n",
        ),
    ],
)
def test_condition_seven_still_may_not_interrupt_a_paragraph(
    label: str, document: str
) -> None:
    """The negative controls, and the ones round 6 measured.

    A line that merely outdents out of a container has not started a block: an
    unprefixed line under a listed paragraph is the lazy continuation
    CommonMark reads it as. No type-seven block opens on any of these, the
    backtick runs really are a fence, and the placeholder inside them is code.
    Clearing the paragraph state on any change of containment path -- rather
    than on a block start -- would open a block on all four.
    <https://spec.commonmark.org/0.31.2/#paragraphs>
    """
    assert _find(document) == [], label


def test_a_setext_underline_still_closes_the_paragraph_it_underlines() -> None:
    """A Setext underline starts a block and closes the paragraph above it.

    It is the shape where the two halves of the model part, so the state handed
    to ``opens_a_paragraph`` is the one the line above left and not the cleared
    one: reading a cleared state would leave a paragraph open under a heading
    and shut condition 7 on the line below.
    <https://spec.commonmark.org/0.31.2/#setext-headings>
    """
    text = f"Words above\n===\n<x-session>\n{FENCE}\nTBD tomorrow.\n{FENCE}\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


def test_a_list_item_holding_a_real_fence_is_still_a_fence() -> None:
    """The control that keeps the fence model intact.

    A list item whose content is prose and then a fenced block still holds a
    fenced block; nothing on those lines opens an HTML block, so the
    placeholder inside the fence is code and is not reported.
    """
    text = f"Words above the list.\n- An exercise\n\n  {FENCE}\n  TBD tomorrow.\n  {FENCE}\n"
    assert _find(text) == []


# --- round 8: list interruption, leaf blocks, raw text (4004076354,
# --- 4004076363, 4004076367) ------------------------------------------------


def test_a_link_reference_definition_lets_condition_seven_open() -> None:
    """A definition is a leaf block, so no paragraph blocks the block below it.

    ``<x-session>`` opens a type-seven HTML block, the backtick runs under it
    are raw HTML rather than a fence, and the page prints the placeholder. The
    liberal fallback called the definition a paragraph, held the block shut,
    read the runs as a fence, and reported nothing at all.
    <https://spec.commonmark.org/0.31.2/#link-reference-definitions>
    """
    text = f"[x]: /url\n<x-session>\n{FENCE}\nTBD tomorrow.\n{FENCE}\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a paragraph above the tag", f"Words above.\n<x-session>\n{FENCE}\nTBD.\n{FENCE}\n"),
        ("a label with no destination", f"[x]:\n<x-session>\n{FENCE}\nTBD.\n{FENCE}\n"),
    ],
)
def test_a_paragraph_still_holds_condition_seven_shut(label: str, document: str) -> None:
    """The positive controls. Condition 7 may not interrupt a paragraph.

    With one open the backtick runs really are a fence and the placeholder
    inside them is code, which is what markdown-it 14.3.0 shows. A label with
    no destination on its own line is no definition at all.
    """
    assert _find(document) == [], label


def test_an_ordered_list_above_one_opens_no_block() -> None:
    """A list may interrupt a paragraph only when an ordered one starts at 1.

    So ``2. <x-session>`` under an open sentence is that sentence's own text,
    no type-seven block opens, and the backtick runs below it pair as a code
    span the page prints as code. Round 7 recorded this shape as the one
    condition-7 case still disagreeing; it agrees now.
    <https://spec.commonmark.org/0.31.2/#list-items>
    """
    text = f"Words above the list.\n2. <x-session>\n   {FENCE}\n   TBD.\n   {FENCE}\n"
    assert _find(text) == []


def test_an_ordered_list_at_one_still_opens_the_block() -> None:
    """The positive control. A list starting at 1 does interrupt.

    The item closes the paragraph, condition 7 opens inside it, the backtick
    runs are raw HTML, and the page prints the placeholder.
    """
    text = f"Words above the list.\n1. <x-session>\n   {FENCE}\n   TBD.\n   {FENCE}\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


def test_a_comment_inside_a_raw_text_element_hides_nothing() -> None:
    """Comment-shaped text inside a textarea is displayed text.

    Python's ``html.parser`` reports it as data rather than as a comment, so
    the page prints the placeholder and the hook has to report it. Stripping it
    as a comment hid a placeholder the child can read.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    text = "<textarea>\n<!-- TBD tomorrow. -->\n</textarea>\n"
    assert [violation.matched_text for violation in _find(text)] == ["TBD"]


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a div, whose content is markup", "<div>\n<!-- TBD tomorrow. -->\n</div>\n"),
        ("a pre, whose content is markup", "<pre>\n<!-- TBD tomorrow. -->\n</pre>\n"),
        (
            "a script name written inside a comment",
            "<!-- a note\n<script>\n-->\n\nWords with no placeholder.\n",
        ),
    ],
)
def test_a_real_comment_still_hides_its_placeholder(label: str, document: str) -> None:
    """The positive controls, and the one that bounds the new state.

    ``pre`` and ``div`` hold markup, so the run really is a comment and the
    placeholder inside it is not on the page. A ``<script>`` written inside a
    comment opens no raw-text run, so the comment still ends at its ``-->``.
    """
    assert _find(document) == [], label


def test_raw_text_run_state_names_the_run_the_line_is_in() -> None:
    """The helper's contract, kept identical across the three hooks.

    It returns the run below the line and the run the line is *in*, the pair
    ``html_block_state`` returns. This hook asks only the first question of it
    -- are these characters text rather than markup -- and reads the answer
    through ``raw_text_run_holds_text``.
    """
    hook = cast(Any, _placeholder_hook)
    state, line_run = hook.raw_text_run_state("<textarea>", None, True)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = hook.raw_text_run_state("some words", "textarea", False)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = hook.raw_text_run_state("</textarea>", "textarea", False)
    assert (state, line_run) == (None, "textarea")
    # A run that opens and closes on one line is the run that line is in.
    state, line_run = hook.raw_text_run_state("<script>a</script>", None, True)
    assert (state, line_run) == (None, "script")
    # A line CommonMark keeps inside the paragraph above it opens no run.
    state, line_run = hook.raw_text_run_state("<xmp>", None, False)
    assert (state, line_run) == (None, None)
    # The comment may open part way along a line, and may close and open again.
    state, line_run = hook.raw_text_run_state("<!-- one --> x <!-- two", None, True)
    assert (state, line_run) == (hook.COMMENT_RUN, None)
    state, line_run = hook.raw_text_run_state("<!-- one -->", None, True)
    assert (state, line_run) == (None, None)
    assert hook.raw_text_run_holds_text("textarea")
    assert hook.raw_text_run_holds_text("script")
    assert not hook.raw_text_run_holds_text(hook.HTML_BLOCK_COMMENT)
    assert not hook.raw_text_run_holds_text(None)


def test_a_condition_seven_opener_inside_an_open_comment_opens_no_run() -> None:
    """An ``<xmp>`` written inside an open comment is inside the comment.

    ``xmp`` is in neither HTML block condition 1 nor condition 6, so a bare
    opener on its own line is condition 7 and may not interrupt a paragraph.
    The comment that opened part way along the line above it is therefore still
    open, the page shows no ``TBD``, and the hook must report none. Measured
    against markdown-it 14.3.0 and ``html.parser``: the whole run is one
    comment.
    """
    hook = cast(Any, _placeholder_hook)
    document = (
        "Words here <!-- a note\n<xmp>\nTBD\n</xmp>\nend of the note -->\n"
    )
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_a_condition_one_opener_inside_an_open_comment_ends_the_comment() -> None:
    """The same shape with ``<script>``, which may interrupt a paragraph.

    Condition 1 ends the paragraph, so the ``<!--`` above it never closes and is
    escaped text rather than a comment; the ``TBD`` is script data, which is not
    a comment either, and the hook reports it. This is the over-application
    control for the test above: a rule that refuses every run under an open
    comment fails here.
    """
    hook = cast(Any, _placeholder_hook)
    document = (
        "Words here <!-- a note\n<script>\nTBD\n</script>\nend of the note -->\n"
    )
    assert [v.line_number for v in hook.find_violations_in_text(document, "doc.md")] == [3]


def test_a_comment_closed_and_reopened_on_one_line_stays_open() -> None:
    """``<!-- one --> words <!-- two`` leaves a comment open below it.

    Reading only the first delimiter pair answered "no run open", a
    ``<textarea>`` on the next line opened a raw-text run, and the lines under it
    stopped being stripped -- so a ``TBD`` inside a real comment was reported.
    """
    hook = cast(Any, _placeholder_hook)
    document = "<!-- one --> words <!-- two\n<textarea>\nTBD\n</textarea> -->\n"
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_a_comment_closed_on_one_line_leaves_nothing_open() -> None:
    """The narrowing control for the test above.

    One complete comment on a line leaves no comment open, so the
    ``<textarea>`` below it really does open a run and the ``TBD`` it prints is
    reported. A rule that treats every line holding ``<!--`` as leaving a
    comment open fails here.
    """
    hook = cast(Any, _placeholder_hook)
    document = "<!-- one --> words\n\n<textarea>\nTBD\n</textarea>\n"
    assert [v.line_number for v in hook.find_violations_in_text(document, "doc.md")] == [4]


def test_a_comment_shaped_run_inside_a_one_line_element_is_not_a_comment() -> None:
    """``<script><!-- TBD --></script>`` holds script data, not a comment.

    The run opens and closes on one line. Returning "no run at all" for that
    line let the body be read as markup, and the comment-shaped run hid the
    token the page prints.
    """
    hook = cast(Any, _placeholder_hook)
    document = "<script><!-- TBD --></script>\n"
    assert [v.line_number for v in hook.find_violations_in_text(document, "doc.md")] == [1]


def test_a_real_one_line_comment_still_hides_its_placeholder() -> None:
    """The over-application control: ``<div>`` is not a raw-text element.

    Its content is markup, the comment inside it is a comment, and the token is
    hidden. A rule that reads every one-line element as raw text fails here.
    """
    hook = cast(Any, _placeholder_hook)
    assert hook.find_violations_in_text("<div><!-- TBD --></div>\n", "doc.md") == []


def test_a_comment_opened_on_a_run_opener_line_does_not_outlive_the_run() -> None:
    """``<textarea> <!-- a note`` opens a run, and the comment dies with it.

    Everything after the opener is the element's content, so the ``<!--`` there
    is characters the page prints. Leaving the open-comment flag standing
    carried a comment the page never shows past the ``</textarea>`` and hid a
    real ``TBD`` below it.
    """
    hook = cast(Any, _placeholder_hook)
    document = "<textarea> <!-- a note\nwords\n</textarea>\n\nTBD\n"
    assert [v.line_number for v in hook.find_violations_in_text(document, "doc.md")] == [5]


# ---------------------------------------------------------------------------
# Round 11: spaces or tabs, and an opener line
# ---------------------------------------------------------------------------


def test_a_tab_separated_reference_definition_is_a_definition() -> None:
    """The placeholder copy, kept identical to the siblings'."""
    hook = cast(Any, _placeholder_hook)
    assert hook.LINK_REFERENCE_DEFINITION_PATTERN.match("[a]:\t/url")
    assert hook.LINK_REFERENCE_DEFINITION_PATTERN.match('[a]: /url\t"t"\t')
    assert hook.LINK_REFERENCE_DEFINITION_PATTERN.match("\t[a]: /url") is None
    assert hook.LINK_REFERENCE_DEFINITION_PATTERN.match("   [a]: /url")


def test_a_tab_after_a_block_quote_marker_is_peeled() -> None:
    """A fenced example inside a block quote whose marker is followed by a tab
    is still a fenced example, so the token in it is not a placeholder."""
    hook = cast(Any, _placeholder_hook)
    quoted = ">\t```\n> TBD\n> ```\n"
    assert hook.find_violations_in_text(quoted, "doc.md") == []
    assert hook.find_violations_in_text("> TBD\n", "doc.md") != []


def test_an_opener_line_belongs_to_the_run_it_opens() -> None:
    """``<textarea><!-- TBD -->`` with its closer below prints the token.

    The run opens on that line and stays open, so the comment-shaped thing on
    it is the element's own content. Returning no classification for the
    opener line hid a placeholder the page shows.
    """
    hook = cast(Any, _placeholder_hook)
    document = "<textarea><!-- TBD -->\nx\n</textarea>\n"
    assert [v.line_number for v in hook.find_violations_in_text(document, "doc.md")] == [1]


def test_a_placeholder_in_a_real_comment_is_still_allowed() -> None:
    """The control in the other direction: a ``<div>`` holds inline content, so
    the comment in it is a comment and the token in it is not reported."""
    hook = cast(Any, _placeholder_hook)
    document = "<div><!-- TBD -->\nx\n</div>\n"
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_a_run_outlives_the_container_its_block_died_with() -> None:
    """A raw-text run is the page's construct, so a container does not end it.

    The reviewer's shape: an unclosed ``<script>`` inside a blockquote, the
    container ending, and a comment-shaped run below it. Measured with
    markdown-it 14.3.0 read by ``html.parser``: the page holds no comment at
    all, because the renderer wrote the ``<script>`` into the output and the
    parser stays in raw text to the end of the file. So the ``TBD`` below is
    not inside a comment and the hook is right to report it. Clearing the run
    at the container boundary would have hidden it.
    """
    hook = cast(Any, _placeholder_hook)
    for opener in ("> <script>\n> var total = 1;\n", "> <textarea>\n> some text\n"):
        document = opener + "\n<!-- TBD: a note -->\n\nTail words here.\n"
        assert [v.matched_text for v in hook.find_violations_in_text(document, "doc.md")] == [
            "TBD"
        ], opener


def test_a_closed_run_frees_the_comment_below_its_container() -> None:
    """The control in the other direction: a run that closes inside the
    blockquote leaves a real comment below it, and the token in it is
    allowed."""
    hook = cast(Any, _placeholder_hook)
    document = (
        "> <script>\n> var total = 1;\n> </script>\n\n<!-- TBD: a note -->\n\nTail.\n"
    )
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_a_closer_below_the_container_still_closes_the_run() -> None:
    """The run ends where the page ends it.

    markdown-it writes the ``</script>`` into the output below the
    ``</blockquote>``, so the element really does close there and the comment
    after it is a real comment. The run has to survive the container boundary
    for this to work.
    """
    hook = cast(Any, _placeholder_hook)
    document = "> <script>\n\n</script>\n\n<!-- TBD: a note -->\n\nTail.\n"
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_an_empty_list_item_does_not_interrupt_a_paragraph() -> None:
    """The placeholder copy of the empty-item rule, kept identical.

    ``Words`` then ``*`` then ``<x>`` is one paragraph of three lines, so the
    backticks under it open a real fenced block and the placeholder inside it
    is an example. Closing the paragraph at the empty marker let the tag open a
    type 7 block, and the fence below was read as raw HTML.
    """
    hook = cast(Any, _placeholder_hook)
    fence = "`" * 3
    document = f"Words\n* \n<x>\n\n{fence}\nTBD\n{fence}\n"
    assert hook.find_violations_in_text(document, "doc.md") == []


def test_an_item_with_content_still_interrupts_in_the_placeholder_hook() -> None:
    """The over-application control for the copy above, read off the rule.

    Kept identical to the assertions in the sibling suites."""
    hook = cast(Any, _placeholder_hook)
    star = hook.Container(kind=hook.CONTAINER_KIND_LIST, bullet="*")
    dash = hook.Container(kind=hook.CONTAINER_KIND_LIST, bullet="-")
    first = hook.Container(kind=hook.CONTAINER_KIND_LIST, ordered_start=1)
    assert not hook.container_interrupts_paragraph(star, "")
    assert hook.container_interrupts_paragraph(star, "item")
    assert hook.container_interrupts_paragraph(dash, "")
    assert not hook.container_interrupts_paragraph(first, "")
