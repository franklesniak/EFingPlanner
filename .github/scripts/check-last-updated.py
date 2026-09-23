"""Check that a pull request bumps `Last Updated` on every Markdown file it changes.

The documentation style guide (`.github/instructions/docs.instructions.md`,
"Synchronizing `Last Updated` and `Version` on Content Changes") already makes
this a MUST: a commit that changes the rendered content or meaning of a
document carrying the metadata header block bumps its `Last Updated` field to
that commit's UTC date, and any `**Version:**` date segment follows it. The
rule was being missed often enough -- sixteen review findings across seven pull
requests -- that it is enforced here instead of left to reviewers.

What is checked
---------------
For each `.md` or `.mdc` file that the pull request adds, modifies or renames,
and that carries a metadata bullet of the form ``- **Last Updated:** YYYY-MM-DD``
on the head:

1. If the file's content changed (see "Mechanical changes" below), the field
   must be on or after the latest UTC author date among the pull request's
   commits that changed the file's content, merges included. A merge counts only
   when its content differs from every parent, meaning someone wrote new content
   while merging; merging the base branch in adds nothing. Keying on commit
   dates, not on today's date, means a second change on the same day passes
   without a redundant edit, and a check re-run on a later day cannot start
   failing.
2. If the file carries ``**Version:** <major>.<minor>.<YYYYMMDD>.<revision>``,
   the ``<YYYYMMDD>`` segment must equal the field.

Mechanical changes
------------------
The guide exempts changes that do not alter rendered content: line-ending
normalization, end-of-file newline fixes and trailing-whitespace-only fixes. It
also says the trailing-whitespace exemption does not apply to a Markdown hard
line break (two or more trailing spaces), because that whitespace renders. So
two versions of a file are compared after normalizing CRLF to LF, collapsing a
trailing run of two or more spaces to exactly two, removing a shorter trailing
run, and removing trailing blank lines. Equal after that means mechanical.

What is not checked
-------------------
Files without the metadata bullet, deleted files, and anything outside the pull
request's own commits. The check does not judge which content is "meaningful":
any non-mechanical change requires the bump, which is what the guide says.

Usage
-----
    python .github/scripts/check-last-updated.py --base <base-commit> [--head <commit>]

Exit status: 0 when every in-scope file passes, 1 when any fails, 2 on a usage
or git error. A git error is never reported as a pass.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys

LAST_UPDATED = re.compile(r"^- \*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})\s*$", re.M)
VERSION = re.compile(r"^\*\*Version:\*\* \d+\.\d+\.(\d{8})\.\d+\s*$", re.M)
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^\s*(`{3,}|~{3,})[ \t]*$")
STATUS = re.compile(r"^[ACDMRTUXB]\d*$")


class GitError(RuntimeError):
    """A git command failed; the caller must not treat this as a pass."""


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise GitError("git %s: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def show(commit: str, path: str) -> str | None:
    """Return the file at a commit, or None when the path is not in that commit.

    Absence is decided by `git ls-tree`, which prints nothing for a path that is not
    in the tree and fails for a bad commit. Any failure, of either command, raises
    GitError, so an unexpected git error can never be read as "file absent".
    """
    if not git("ls-tree", commit, "--", path).strip():
        return None
    return git("show", "%s:%s" % (commit, path))


def outside_fences(text: str) -> str:
    """Blank out fenced blocks so an example metadata block is never read as the real one.

    Follows CommonMark's fence rules: a fence opens with three or more backticks or
    tildes (a backtick fence's info string may not contain a backtick) and closes only
    on the same character, at least as long, followed by nothing but spaces or tabs.
    So a four-backtick fence around a triple-backtick example, which the docs guide
    prescribes, stays one fence.
    """
    out, fence = [], None
    for line in text.split("\n"):
        if fence is None:
            m = FENCE_OPEN.match(line)
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                out.append("")
            else:
                out.append(line)
            continue
        m = FENCE_CLOSE.match(line)
        if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
            fence = None
        out.append("")
    return "\n".join(out)


def normalize(text: str) -> str:
    """Remove only the differences the style guide calls mechanical.

    A hard line break is two or more spaces immediately before the line end
    (CommonMark), so it is decided by those spaces alone: they become a two-space
    marker, and any other trailing spaces or tabs are dropped.
    """
    lines = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        spaces = len(line) - len(line.rstrip(" "))
        lines.append(line.rstrip(" \t") + ("  " if spaces >= 2 else ""))
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def field(text: str) -> str | None:
    m = LAST_UPDATED.search(outside_fences(text))
    return m.group(1) if m else None


def version_date(text: str) -> str | None:
    m = VERSION.search(outside_fences(text))
    return m.group(1) if m else None


def name_status(tokens: list[str], i: int) -> tuple[str, str | None, str, int]:
    """Read one NUL-separated name-status entry at tokens[i]: (status, before, after, next index).

    A rename carries the old and new paths. A copy carries its source and the new path,
    but the new file did not exist before, so it is compared with nothing (before None).
    `--follow` can report an added file as a copy of a similar one.
    """
    status = tokens[i]
    if status[0] == "R":
        return status, tokens[i + 1], tokens[i + 2], i + 3
    if status[0] == "C":
        return status, None, tokens[i + 2], i + 3
    return status, tokens[i + 1], tokens[i + 1], i + 2


def changed_files(base: str, head: str) -> list[tuple[str | None, str]]:
    """(path on base or None, path on head) for each added, modified or renamed Markdown file.

    `-z` makes git print every path verbatim, NUL-separated. Without it, git quotes and
    escapes names with non-ASCII bytes, tabs, quotes or backslashes, and a quoted name
    passed back to git matches nothing, so the file would be skipped.
    """
    raw = git("diff", "--name-status", "-z", "-M", "%s..%s" % (base, head), "--", "*.md", "*.mdc")
    tokens = [t for t in raw.split("\0") if t]
    out, i = [], 0
    while i < len(tokens):
        status, before, after, i = name_status(tokens, i)
        if status[0] == "R":
            out.append((before, after))
        elif status[0] in "AMC":
            out.append((before if status[0] == "M" else None, after))
    return out


def history(base: str, head: str, path: str) -> list[tuple[str, str, list[str], str | None, str]]:
    """(commit, author date, parents, path before, path after) for each PR commit that touched the file.

    Merge commits are included. `--diff-merges=first-parent` makes a merge list what it
    changed relative to the pull request's own line; git's default history
    simplification already drops a merge that took the file unchanged from one parent.
    `--follow` tracks renames, and each entry carries that commit's own paths.
    """
    raw = git("log", "--follow", "--name-status", "-z", "-M", "--diff-merges=first-parent",
              "--format=@@%H %aI %P", "%s..%s" % (base, head), "--", path)
    tokens = [t.lstrip("\n") for t in raw.split("\0")]
    tokens = [t for t in tokens if t]
    out, header, i = [], None, 0
    while i < len(tokens):
        # Paths are consumed by name_status(), so only a header or a status reaches here.
        if tokens[i].startswith("@@"):
            fields = tokens[i][2:].split(" ")
            header = (fields[0], fields[1], fields[2:])
            i += 1
            continue
        if header is None or not STATUS.match(tokens[i]):
            raise GitError("unexpected git log output near %r" % tokens[i][:60])
        _, before, after, i = name_status(tokens, i)
        out.append((header[0], header[1], header[2], before, after))
    return out


def required_date(base: str, head: str, path: str) -> dt.date | None:
    """UTC author date of the newest PR commit that changed the file's content.

    Every PR commit that touched the file is considered, merges included, and the
    latest qualifying author date wins. A non-merge commit qualifies when its content
    differs from its parent's. A merge qualifies only when its content differs from
    every parent's, meaning someone wrote new content while merging; a merge that took
    the content from one side adds nothing, because that side's commits carry their
    own dates. A clean merge that combines edits to the same file from both sides also
    qualifies. When both sides follow the rule, both changed the `Last Updated` line,
    so such a merge conflicts, and resolving it is an authored change.
    """
    dates = []
    for sha, when, parents, before_path, after_path in history(base, head, path):
        after = show(sha, after_path)
        if after is None:
            continue
        befores = []
        for parent in parents:
            content = show(parent, before_path) if before_path else None
            if content is None and before_path and len(parents) > 1:
                content = show(parent, after_path)
            befores.append(normalize(content or ""))
        if befores and all(b != normalize(after) for b in befores):
            dates.append(dt.datetime.fromisoformat(when).astimezone(dt.timezone.utc).date())
    return max(dates) if dates else None


def check(base: str, head: str) -> list[str]:
    merge_base = git("merge-base", base, head).strip()
    problems = []
    for old_path, path in changed_files(merge_base, head):
        head_text = show(head, path)
        if head_text is None:
            continue
        value = field(head_text)
        if value is None:
            continue
        base_text = show(merge_base, old_path) if old_path else None
        if base_text is not None and normalize(base_text) == normalize(head_text):
            continue
        need = required_date(merge_base, head, path)
        if need is None:
            # Fail closed: the content differs from the base, so some commit changed it.
            problems.append("%s: its content changed, but no pull request commit could be found that "
                            "changed it, so the required date is unknown." % path)
        elif dt.date.fromisoformat(value) < need:
            problems.append("%s: Last Updated is %s, but this pull request changed its content in a "
                            "commit dated %s (UTC). Set it to %s or later." % (path, value, need, need))
        vd = version_date(head_text)
        if vd is not None and vd != value.replace("-", ""):
            problems.append("%s: the Version date segment is %s, but Last Updated is %s. They must match."
                            % (path, vd, value))
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--base", required=True, help="the pull request's base commit")
    parser.add_argument("--head", default="HEAD", help="the pull request's head commit (default HEAD)")
    args = parser.parse_args(argv)
    try:
        problems = check(args.base, args.head)
    except GitError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    for p in problems:
        print(p)
    if problems:
        print("\n%d Last Updated problem(s). See .github/instructions/docs.instructions.md, "
              "\"Synchronizing `Last Updated` and `Version` on Content Changes\"." % len(problems))
        return 1
    print("Last Updated check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
