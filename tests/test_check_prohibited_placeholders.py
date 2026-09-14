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
