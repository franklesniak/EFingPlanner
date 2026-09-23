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
   when its content differs from git's own clean merge of its parents, meaning
   someone wrote new content or resolved a conflict while merging; an automatic
   merge, such as merging the base branch in, adds nothing. Keying on commit
   dates, not on today's date, means a second change on the same day passes
   without a redundant edit, and a check re-run on a later day cannot start
   failing.
2. If the file carries ``**Version:** <major>.<minor>.<YYYYMMDD>.<revision>``,
   the ``<YYYYMMDD>`` segment must equal the field.
3. If the base version carried the field and the head does not, the field was
   removed, which fails.
4. The field must not be earlier than the base version's field. A rebased or
   cherry-picked commit can keep an old author date; the field still may not
   move backwards.

Mechanical changes
------------------
The guide exempts changes that do not alter rendered content: line-ending
normalization, end-of-file newline fixes and trailing-whitespace-only fixes. It
also says the trailing-whitespace exemption does not apply to a Markdown hard
line break (two or more trailing spaces, or a trailing backslash), because that
whitespace renders. So two versions of a file are compared after normalizing
CRLF to LF, collapsing a trailing run of two or more spaces to exactly two,
marking whitespace that followed an unescaped final backslash, removing other
trailing whitespace, and removing trailing blank lines. Equal after that means
mechanical.

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
import os
import re
import subprocess
import sys

LAST_UPDATED = re.compile(r"^- \*\*Last Updated:\*\* (\d{4}-\d{2}-\d{2})\s*$", re.M)
VERSION = re.compile(r"^\*\*Version:\*\* \d+\.\d+\.(\d{8})\.\d+\s*$", re.M)
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
COMMENT_OPEN = re.compile(r"^ {0,3}<!--")
NO_BREAK = "\x00no-break"   # marks a final backslash that trailing whitespace kept from breaking


class GitError(RuntimeError):
    """A git command failed; the caller must not treat this as a pass."""


def git(*args: str) -> str:
    """Run git and return its output, or raise GitError.

    Output is decoded as UTF-8 with `surrogateescape`, so bytes that are not UTF-8 (Linux
    allows them in names and files) round-trip instead of failing. A decoding failure can
    otherwise leave stdout empty or raise outside this function, and an empty result would
    read as "file absent". Missing stdout is therefore an error too.
    """
    result = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8",
                            errors="surrogateescape")
    if result.returncode != 0 or result.stdout is None:
        raise GitError("git %s: %s" % (" ".join(args), (result.stderr or "").strip()))
    return result.stdout


def show(commit: str, path: str) -> str | None:
    """Return the file at a commit, or None when the path is not in that commit.

    Absence is decided by `git ls-tree`, which prints nothing for a path that is not
    in the tree and fails for a bad commit. The path is passed with `:(literal)`, so a
    name such as `:foo.md` is never read as pathspec magic. Any failure, of either
    command, raises GitError, so an unexpected git error can never be read as "file absent".
    """
    if not git("ls-tree", commit, "--", ":(literal)" + path).strip():
        return None
    return git("show", "%s:%s" % (commit, path))


def outside_fences(text: str) -> str:
    """Blank out fenced blocks so an example metadata block is never read as the real one.

    Follows CommonMark's fence rules: a fence line has at most three leading spaces; a
    fence opens with three or more backticks or tildes (a backtick fence's info string
    may not contain a backtick) and closes only on the same character, at least as
    long, followed by nothing but spaces or tabs.
    So a four-backtick fence around a triple-backtick example, which the docs guide
    prescribes, stays one fence.

    HTML comment blocks are blanked too, because they render nothing: outside a fence,
    a line starting with up to three spaces and `<!--` opens one, and the line that
    contains `-->` closes it (CommonMark's HTML block condition 2).
    """
    out, fence, comment = [], None, False
    for line in text.split("\n"):
        if comment:
            out.append("")
            comment = "-->" not in line
            continue
        if fence is None:
            if COMMENT_OPEN.match(line):
                out.append("")
                comment = "-->" not in line.split("<!--", 1)[1]
                continue
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

    CommonMark has two hard line breaks. Two or more spaces immediately before the
    line end become a two-space marker. A backslash immediately before the line end is
    the other; when an unescaped final backslash (an odd run of backslashes) was
    followed by whitespace, that line did not break, so a marker keeps it distinct
    from the breaking form. Any other trailing spaces or tabs are dropped.
    """
    lines = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        spaces = len(line) - len(line.rstrip(" "))
        stripped = line.rstrip(" \t")
        backslashes = len(stripped) - len(stripped.rstrip("\\"))
        if spaces >= 2 and stripped:
            lines.append(stripped + "  ")
        elif backslashes % 2 == 1 and stripped != line:
            lines.append(stripped + NO_BREAK)
        else:
            lines.append(stripped)
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

    A rename carries the old and new paths. A copy, which git reports only when copy
    detection is on, carries its source and the new path, but the new file did not
    exist before, so it is compared with nothing (before None).
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
        elif status[0] in "AMCT":
            # T is a type change, such as a file replaced by a symlink: still checked.
            out.append((before if status[0] in "MT" else None, after))
    return out


def path_in(parent: str, commit: str, path: str) -> str | None:
    """The name `parent` has for the file that `commit` calls `path`, or None if it has none.

    A rename-aware diff of the whole tree is used, because limiting the diff to `path`
    would hide the old name and turn every rename into an addition.
    """
    raw = git("diff", "--name-status", "-z", "-M", parent, commit)
    tokens = [t for t in raw.split("\0") if t]
    i = 0
    while i < len(tokens):
        status, before, after, i = name_status(tokens, i)
        if after == path:
            if status[0] in "AC":
                return None
            return before
    return path   # unchanged between the two commits, so the parent has the same name


def required_date(base: str, head: str, path: str) -> dt.date | None:
    """UTC author date of the newest PR commit that changed the file's content.

    Every PR commit that touched the file is considered, merges included, and the
    latest qualifying author date wins. A non-merge commit qualifies when its content
    differs from its parent's. A two-parent merge qualifies only when its content
    differs from git's own clean merge of the two parents, recomputed with
    `git merge-tree`: an automatic merge adds nothing, because each side's commits
    carry their own dates, while a conflict resolution or an edit made during the
    merge is authored. A merge with more than two parents qualifies when its content
    differs from every parent's.
    """
    # Walk every PR commit children-first, carrying the file's name backwards: the head
    # knows it as `path`, and each parent's name comes from a rename-aware diff against
    # its child, which is reliable because the two commits are adjacent. This reaches
    # commits on merged side branches, where the file may have its older name.
    head_sha = git("rev-parse", head).strip()
    names: dict[str, str | None] = {head_sha: path}
    dates = []
    log = git("log", "--topo-order", "--format=%H %aI %P", "%s..%s" % (base, head))
    for row in log.splitlines():
        sha, when, *parents = row.split(" ")
        name = names.get(sha)
        if name is None:
            continue
        after = show(sha, name)
        if after is None:
            continue
        befores = []
        for parent in parents:
            own = path_in(parent, sha, name)
            names.setdefault(parent, own)
            content = show(parent, own) if own else None
            befores.append(normalize(content or ""))
        if len(parents) >= 2:
            automatic = clean_merge(parents, name)
            authored = normalize(automatic or "") != normalize(after)
        else:
            authored = bool(befores) and all(b != normalize(after) for b in befores)
        if authored:
            dates.append(dt.datetime.fromisoformat(when).astimezone(dt.timezone.utc).date())
    return max(dates) if dates else None


def clean_merge(parents: list[str], path: str) -> str | None:
    """The file as git's own merge of the parents writes it, conflict markers included.

    The parents are merged in order, one at a time, as git's octopus strategy does.
    `git merge-tree --write-tree` exits 0 for a clean merge and 1 when there are
    conflicts, printing the resulting tree either way; anything else is a git error.
    Between steps, the intermediate tree is recorded with `git commit-tree` as an
    unreferenced commit, so the next step has a commit to merge against. No branch or
    ref changes, and a fixed identity is supplied because CI runners configure none.
    """
    env = dict(os.environ, GIT_AUTHOR_NAME="check-last-updated", GIT_AUTHOR_EMAIL="check@localhost",
               GIT_COMMITTER_NAME="check-last-updated", GIT_COMMITTER_EMAIL="check@localhost")
    current, tree = parents[0], None
    for index, other in enumerate(parents[1:], start=1):
        result = subprocess.run(["git", "merge-tree", "--write-tree", current, other],
                                capture_output=True, text=True, encoding="utf-8", errors="surrogateescape")
        if result.returncode not in (0, 1) or result.stdout is None:
            raise GitError("git merge-tree: %s" % (result.stderr or "").strip())
        tree = result.stdout.split("\n", 1)[0].strip()
        if index < len(parents) - 1:
            step = subprocess.run(["git", "commit-tree", tree, "-p", current, "-p", other,
                                   "-m", "check-last-updated: temporary merge step"],
                                  capture_output=True, text=True, encoding="utf-8",
                                  errors="surrogateescape", env=env)
            if step.returncode != 0 or step.stdout is None:
                raise GitError("git commit-tree: %s" % (step.stderr or "").strip())
            current = step.stdout.strip()
    return show(tree, path) if tree else None


def check(base: str, head: str) -> list[str]:
    merge_base = git("merge-base", base, head).strip()
    problems = []
    for old_path, path in changed_files(merge_base, head):
        head_text = show(head, path)
        if head_text is None:
            continue
        value = field(head_text)
        base_text = show(merge_base, old_path) if old_path else None
        if value is None:
            if base_text is not None and field(base_text) is not None:
                problems.append("%s: the base version has a Last Updated field, and this pull request "
                                "removed it. Restore it, with the date of the change." % path)
            continue
        base_value = field(base_text) if base_text is not None else None
        if base_value is not None and dt.date.fromisoformat(value) < dt.date.fromisoformat(base_value):
            problems.append("%s: Last Updated moved back from %s to %s. It must not be earlier than the "
                            "base version's date." % (path, base_value, value))
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
    # A name holding bytes that are not UTF-8 is carried as surrogates; print it escaped.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
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
