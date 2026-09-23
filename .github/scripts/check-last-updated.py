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
   must be on or after the UTC author date of the newest non-merge commit in the
   pull request that changed the file's content. Keying on the commit date, not
   on today's date, means a second change on the same day passes without a
   redundant edit, and a check re-run on a later day cannot start failing.
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
FENCE = re.compile(r"^\s*(```|~~~)")


class GitError(RuntimeError):
    """A git command failed; the caller must not treat this as a pass."""


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise GitError("git %s: %s" % (" ".join(args), result.stderr.strip()))
    return result.stdout


def show(commit: str, path: str) -> str | None:
    """Return the file at a commit, or None when it does not exist there."""
    result = subprocess.run(["git", "show", "%s:%s" % (commit, path)],
                            capture_output=True, text=True, encoding="utf-8")
    return result.stdout if result.returncode == 0 else None


def outside_fences(text: str) -> str:
    """Blank out fenced blocks so an example metadata block is never read as the real one."""
    out, fenced = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
            out.append("")
            continue
        out.append("" if fenced else line)
    return "\n".join(out)


def normalize(text: str) -> str:
    """Remove only the differences the style guide calls mechanical."""
    lines = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.rstrip(" \t")
        trailing = line[len(stripped):]
        lines.append(stripped + ("  " if trailing.count(" ") >= 2 and "\t" not in trailing else ""))
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def field(text: str) -> str | None:
    m = LAST_UPDATED.search(outside_fences(text))
    return m.group(1) if m else None


def version_date(text: str) -> str | None:
    m = VERSION.search(outside_fences(text))
    return m.group(1) if m else None


def changed_files(base: str, head: str) -> list[tuple[str | None, str]]:
    """(path on base or None, path on head) for each added, modified or renamed Markdown file."""
    out = []
    raw = git("diff", "--name-status", "-M", "%s..%s" % (base, head), "--", "*.md", "*.mdc")
    for line in raw.splitlines():
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("R"):
            out.append((parts[1], parts[2]))
        elif status[0] in "AM":
            out.append((parts[1] if status[0] == "M" else None, parts[1]))
    return out


def history(base: str, head: str, path: str, merges: bool) -> list[tuple[str, str, str | None, str]]:
    """(commit, author date, path before, path after) for each PR commit that touched the file, newest first.

    `--follow` tracks renames, and `--name-status` gives each commit's own paths, so a
    commit made before a rename is compared under the name the file had then.
    """
    args = ["log", "--follow", "--name-status", "-M", "--format=@@%H %aI"]
    # A merge commit prints no file list unless asked; first-parent shows what it changed
    # relative to the pull request's own line, which is the change this check needs.
    args.append("--diff-merges=first-parent" if merges else "--no-merges")
    raw = git(*args, "%s..%s" % (base, head), "--", path)
    out, commit = [], None
    for line in raw.splitlines():
        if line.startswith("@@"):
            commit = line[2:].split(" ", 1)
        elif line.strip() and commit:
            parts = line.split("\t")
            if parts[0].startswith("R"):
                before, after = parts[1], parts[2]
            elif parts[0].startswith("C"):
                # `--follow` can report a new file as a copy of a similar one. The file did not
                # exist before this commit, so it is compared with nothing, like an added file.
                before, after = None, parts[2]
            else:
                before, after = parts[1], parts[1]
            out.append((commit[0], commit[1], before, after))
            commit = None
    return out


def required_date(base: str, head: str, path: str) -> dt.date | None:
    """UTC author date of the newest PR commit that changed the file's content.

    Non-merge commits are searched first. A change that arrived only through a merge
    commit (for example, a conflict resolution) falls back to the merge commit, so a
    content change is never left without a required date.
    """
    for merges in (False, True):
        for sha, when, before_path, after_path in history(base, head, path, merges):
            parent = git("rev-parse", sha + "^").strip()
            after = show(sha, after_path)
            before = show(parent, before_path) if before_path else None
            if after is None:
                continue
            if normalize(before or "") != normalize(after):
                return dt.datetime.fromisoformat(when).astimezone(dt.timezone.utc).date()
    return None


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
