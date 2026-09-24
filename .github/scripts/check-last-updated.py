"""Check that a pull request bumps `Last Updated` on every Markdown file it changes.

The documentation style guide (`.github/instructions/docs.instructions.md`,
"Synchronizing `Last Updated` and `Version` on Content Changes") makes this a
MUST: a commit that changes the rendered content or meaning of a document
carrying the metadata header block bumps its `Last Updated` field to that
commit's UTC date, and any `**Version:**` date segment follows it. The rule was
being missed often enough -- sixteen review findings across seven pull
requests -- that a check now guards it. The check judges the pull request's
head, as the guide's finalization point does, rather than each commit: the
head's field must match the newest pull request commit that changed the
content, as "What is checked" below states exactly. An earlier commit that
skipped the bump passes once a later one makes it.

What is checked
---------------
For each `.md` or `.mdc` file that the pull request adds, modifies or renames,
and that carries a metadata bullet of the form ``- **Last Updated:** YYYY-MM-DD``
in its metadata header block on the head (found where the guide's placement
rules put the block, so an example elsewhere is never taken for it; see "How
Markdown is read"):

1. If the file's content changed (see "Mechanical changes" below), the field
   must be on or after the latest UTC author date among the pull request's
   commits that changed the file's content, merges included. A merge counts only
   when its content differs from git's own clean merge of its parents, meaning
   someone wrote new content or resolved a conflict while merging; an automatic
   merge, such as merging the base branch in, adds nothing. Keying on commit
   dates, not on today's date, means a second change on the same day passes
   without a redundant edit, and a check re-run on a later day cannot start
   failing. A renamed file's history is followed under each earlier name,
   including a rename made as a copy and a later deletion, a chain of copies
   (each step as git's copy detection finds it), a deletion followed by a
   restoration, and a rename made in a merge commit. A rename is what git's
   rename detection reports, which keeps at least half of the content by
   default; a file rewritten below that counts as a new file, whose history
   starts at the commit that added it. The field must also not be later than
   the latest commit date (UTC) of those commits, unless it equals the base's
   own value: a future date would let later edits skip the bump.
2. If the file carries ``**Version:** <major>.<minor>.<YYYYMMDD>.<revision>``
   and its content changed, the ``<YYYYMMDD>`` segment must equal the field, and
   ``<revision>`` must follow the guide's convention against the published
   baseline, the file on the base branch tip (under its new name if the base
   branch renamed it after the fork): ``N + 1`` when the baseline has the
   same ``<major>.<minor>.<YYYYMMDD>`` at revision ``N``, otherwise ``0``.
3. If the base version carried the field and the head does not, the field was
   removed or moved out of the metadata header block, which fails.
4. The field must not be earlier than the base version's field. A rebased or
   cherry-picked commit can keep an old author date; the field still may not
   move backwards.
5. The field must be a real calendar date in ``YYYY-MM-DD`` form. An impossible
   date such as ``2026-02-30``, and a ``Last Updated`` item of another shape in
   the block, such as ``2026/03/05``, are reported. So is a Version value too
   long to read as numbers.
6. If the head's file has no field but the base branch tip's copy has one, the
   base branch added the block after the fork. When the pull request changes the
   file's content, it is reported: merge the base branch in, then set the field.

A file whose rendered content already equals the base branch tip's (under its
name there) is skipped: it adds nothing to the merge, as when the pull request
repeats a change that has already landed.

Mechanical changes
------------------
The guide exempts changes that do not alter rendered content: line-ending
normalization, end-of-file newline fixes and trailing-whitespace-only fixes. It
also says the trailing-whitespace exemption does not apply to a Markdown hard
line break (two or more trailing spaces, or a trailing backslash), because that
whitespace renders. So both versions of a file are rendered, and the output is
compared after trailing whitespace is removed from each output line. Equal
output means mechanical. A hard line break renders as `<br />`, so adding or
removing one still counts. Trailing spaces that CommonMark does not render as a
break, such as at the end of a paragraph, after a heading or inside a code
block, do not count. Relative references in Markdown links and images are
compared as repository paths, resolved from each version's own directory by the
URL Standard's path rules (as a browser resolves them), so moving a file to
another directory changes its content exactly when a relative reference now
points somewhere else. Every URL is first cleaned as the URL Standard's parser
cleans it: white space around it, and tabs and newlines inside it, are dropped.
Raw HTML is not read. The repository's markdownlint configuration rejects it
(MD033), and reading it as a browser does takes the whole HTML parser, so it is
compared as written, and a file whose raw HTML holds a tag is tied to its
directory: moving that file counts as a content change. So does respelling raw
HTML, even in a way a browser reads the same. HTML that is only comments ties
nothing.

How Markdown is read
--------------------
`render-markdown.js`, next to this script, parses and renders Markdown with
markdown-it in CommonMark mode. `lint-nested-markdown.js` uses the same library,
with its default preset. The helper also finds the metadata header block where
the guide's placement rules put it and reads the fields from there. It runs as
one Node process for the whole run, so the check needs Node and the
repository's `node_modules` (`npm ci`).

What is not checked
-------------------
Files without the metadata bullet, deleted files, and anything outside the pull
request's own commits. The check does not judge which content is "meaningful":
any non-mechanical change requires the bump, which is what the guide says.
Author dates are trusted, because whoever makes a commit sets them: a backdated
commit can satisfy the check, including one that rewrites a file below git's
rename threshold, or one that brings back content from a file an earlier commit
deleted. Where the walk cannot follow a file's history, the commit it stops at
still counts as a change, because it differs from what the walk compares it
with; with honest dates that commit is later than every edit it hides, so an
edit is missed only when a later commit carries an earlier author date. The
check is a drift guard, not a trust boundary.

Usage
-----
    python .github/scripts/check-last-updated.py --base <base-commit> [--head <commit>]

Exit status: 0 when every in-scope file passes, 1 when any fails, 2 on a usage,
git or renderer error. An error is never reported as a pass.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from typing import Any, cast

NODE = "node"
HELPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "render-markdown.js")


class CheckError(RuntimeError):
    """A tool the check depends on failed; the caller must not treat this as a pass."""


class GitError(CheckError):
    """A git command failed."""


class RenderError(CheckError):
    """The Markdown renderer failed or gave an answer that is not usable."""


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


class Renderer:
    """Markdown rendered by `render-markdown.js`, through one Node process for the whole run.

    Each answer holds the rendered HTML (`html`), with relative references resolved
    from the document's path, the `Last Updated` field (`lastUpdated`) and the whole
    `Version` value (`version`); see the helper for exactly what each one means.
    Answers are cached by text and path. Any failure raises RenderError, so a renderer
    problem can never read as "mechanical" or "no field".
    """

    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.cache: dict[tuple[str, str], dict[str, Any]] = {}

    def __call__(self, text: str, path: str = "") -> dict[str, Any]:
        if (text, path) not in self.cache:
            self.cache[(text, path)] = self.ask(text, path)
        return self.cache[(text, path)]

    def ask(self, text: str, path: str) -> dict[str, Any]:
        if self.process is None:
            try:
                self.process = subprocess.Popen([NODE, HELPER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                text=True, encoding="utf-8", errors="surrogateescape")
            except OSError as exc:
                raise RenderError("cannot start %s %s: %s" % (NODE, HELPER, exc)) from exc
        assert self.process.stdin is not None and self.process.stdout is not None
        try:
            # ensure_ascii escapes everything else, including undecodable bytes carried as surrogates.
            self.process.stdin.write(json.dumps({"text": text, "path": path}, ensure_ascii=True) + "\n")
            self.process.stdin.flush()
            line = self.process.stdout.readline()
        except OSError as exc:
            raise RenderError("%s: %s" % (HELPER, exc)) from exc
        if not line:
            raise RenderError("%s stopped without an answer (exit status %s)" % (HELPER, self.process.poll()))
        try:
            answer = json.loads(line)
        except ValueError as exc:
            raise RenderError("%s gave an answer that is not JSON: %s" % (HELPER, exc)) from exc
        # Every key must be present: a missing `lastUpdated` must not read as "no field".
        if not (isinstance(answer, dict) and {"html", "lastUpdated", "version"} <= set(answer)
                and isinstance(answer["html"], str)
                and all(answer[k] is None or isinstance(answer[k], str) for k in ("lastUpdated", "version"))):
            raise RenderError("%s gave an unexpected answer: %.200r" % (HELPER, answer))
        return answer

    def close(self) -> None:
        if self.process is not None:
            if self.process.stdin is not None:
                self.process.stdin.close()
            self.process.wait()
            self.process = None


render = Renderer()


def rendered(text: str, path: str) -> str:
    """The text as CommonMark renders it at `path`, with trailing whitespace removed from each line.

    Two versions with equal output differ only mechanically: in line endings, the
    end-of-file newline, or trailing whitespace that renders nothing. A hard line break
    renders as `<br />`, so removing or adding one is still a content change. Relative
    references in Markdown links and images are resolved from the directory of `path`,
    so moving a file changes its content exactly when one of them now points somewhere
    else. Raw HTML is compared as written, and when it holds a tag it ties the output to
    the directory of `path`.
    """
    return cast(str, render(text, path)["html"])


def field(text: str) -> str | None:
    return cast("str | None", render(text)["lastUpdated"])


def version(text: str) -> tuple[int, int, str, int] | None:
    """(major, minor, YYYYMMDD, revision) from the metadata header's Version line, or None."""
    value = cast("str | None", render(text)["version"])
    if value is None:
        return None
    major, minor, date, revision = value.split(".")
    return int(major), int(minor), date, int(revision)


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


def path_at(commit: str, later: str, path: str) -> str:
    """The name `later` has for the file that `commit` calls `path`.

    A rename-aware diff of the whole tree is used, as in `path_in()`, so a rename on the
    way from `commit` to `later` gives the new name. Otherwise the name is unchanged;
    if `later` deleted the file, `show()` finds nothing there.
    """
    raw = git("diff", "--name-status", "-z", "-M", commit, later)
    tokens = [t for t in raw.split("\0") if t]
    i = 0
    while i < len(tokens):
        status, before, after, i = name_status(tokens, i)
        if before == path and status[0] == "R":
            return after
    return path


def copy_source(parent: str, commit: str, path: str) -> str | None:
    """The file in `parent` that git's copy detection names as the source of `path` in `commit`.

    `--find-copies-harder` lets every file of the parent be a source, not only the files the
    commit changed, and git takes the most similar one. None when git finds no source, as when
    the file is restored after a deletion.
    """
    raw = git("diff", "--name-status", "-z", "-C", "--find-copies-harder", parent, commit)
    tokens = [t for t in raw.split("\0") if t]
    i = 0
    while i < len(tokens):
        if tokens[i][0] in "CR":
            if tokens[i + 2] == path:
                return tokens[i + 1]
            i += 3
        else:
            i += 2
    return None


def required_date(base: str, head: str, path: str, origin: str | None = None) -> dt.date | None:
    """UTC author date of the newest PR commit that changed the file's content."""
    changes = content_changes(base, head, path, origin)
    return max((authored for authored, _ in changes), default=None)


def content_changes(base: str, head: str, path: str,
                    origin: str | None = None) -> list[tuple[dt.date, dt.date]]:
    """(author date, committer date), in UTC, of every PR commit that changed the file's content.

    Every PR commit that touched the file is considered, merges included. Content is
    compared as rendered (see `rendered()`). A non-merge commit qualifies when its
    content differs from its parent's. A merge, of any number of parents, qualifies
    only when its content differs from git's own clean merge of all its parents (see
    `clean_merge()`), read under the name that clean merge gives the file, since the
    merge commit may rename it: an automatic merge adds nothing, because each side's
    commits carry their own dates, while a conflict resolution or an edit made during
    the merge is authored.

    `origin` is the file's name on the base, when the file existed there. Where the diff
    against the child loses the file, as at a copy, the parent's name is the copy's source,
    as git's copy detection finds it (see `copy_source()`), so a chain of copies, renames
    and edits is followed one step at a time. Where git finds no source, as at a
    restoration, it is the name a rename-aware diff from the base gives `origin`. A commit
    that lacks the file, as between a deletion and a restoration, passes the name on to its
    parents. So the history before the copy or the deletion still counts, under each
    earlier name. Content brought back from a file that an earlier commit deleted is not
    traced to that file; the commit that brings it back is dated instead (see "What is not
    checked").
    """
    # Walk every PR commit children-first, carrying the file's name backwards: the head
    # knows it as `path`, and each parent's name comes from a rename-aware diff against
    # its child, which is reliable because the two commits are adjacent. This reaches
    # commits on merged side branches, where the file may have its older name.
    head_sha = git("rev-parse", head).strip()
    names: dict[str, str | None] = {head_sha: path}
    changes = []
    log = git("log", "--topo-order", "--format=%H %aI %cI %P", "%s..%s" % (base, head))
    for row in log.splitlines():
        sha, authored_at, committed_at, *parents = row.split()   # a root commit has no parents
        name = names.get(sha)
        if name is None:
            continue
        after = show(sha, name)
        if after is None:
            for parent in parents:
                carried = path_in(parent, sha, name)   # absent here: pass the name on
                if origin is not None and (carried is None or show(parent, carried) is None):
                    carried = path_at(base, parent, origin)   # the name came from a restoration: find the file again
                names.setdefault(parent, carried)
            continue
        befores = []
        for parent in parents:
            own = path_in(parent, sha, name)
            if own is None and origin is not None:
                # Added here, as by a copy: follow the most similar file in the parent, or else the base file.
                own = copy_source(parent, sha, name) or path_at(base, parent, origin)
            names.setdefault(parent, own)
            content = show(parent, own) if own else None
            befores.append(rendered(content or "", own or name))
        if len(parents) >= 2:
            tree = clean_merge(parents)
            own = path_in(tree, sha, name)   # the merge commit itself may rename the file
            automatic = show(tree, own) if own else None
            authored = rendered(automatic or "", own or name) != rendered(after, name)
        else:
            # A root commit, as on an unrelated history, has no parent, so it adds the file.
            authored = all(b != rendered(after, name) for b in befores or [rendered("", name)])
        if authored:
            changes.append((utc_date(authored_at), utc_date(committed_at)))
    return changes


def calendar_date(value: str | None) -> dt.date | None:
    """The field's date, or None when there is none or it is not a real calendar date.

    The helper checks only the YYYY-MM-DD shape, so a value such as 2026-02-30 reaches here.
    """
    if value is None:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:   # 2026-02-30, or a value of another shape such as 2026/03/05
        return None


def utc_date(stamp: str) -> dt.date:
    return dt.datetime.fromisoformat(stamp).astimezone(dt.timezone.utc).date()


def clean_merge(parents: list[str]) -> str:
    """The tree of git's own merge of the parents, conflict markers included.

    The parents are merged in order, one at a time, as git's octopus strategy does.
    `git merge-tree --write-tree` exits 0 for a clean merge and 1 when there are
    conflicts, printing the resulting tree either way; anything else is a git error.
    Between steps, the intermediate tree is recorded with `git commit-tree` as an
    unreferenced commit, so the next step has a commit to merge against. No branch or
    ref changes, and a fixed identity is supplied because CI runners configure none.
    """
    env = dict(os.environ, GIT_AUTHOR_NAME="check-last-updated", GIT_AUTHOR_EMAIL="check@localhost",
               GIT_COMMITTER_NAME="check-last-updated", GIT_COMMITTER_EMAIL="check@localhost")
    current, tree = parents[0], ""
    for index, other in enumerate(parents[1:], start=1):
        # --allow-unrelated-histories: the merge already exists, so recompute it even when its
        # parents share no history, as `git merge --allow-unrelated-histories` made it.
        result = subprocess.run(["git", "merge-tree", "--write-tree", "--allow-unrelated-histories", current, other],
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
    return tree


def check(base: str, head: str) -> list[str]:
    merge_base = git("merge-base", base, head).strip()
    problems = []
    for old_path, path in changed_files(merge_base, head):
        head_text = show(head, path)
        if head_text is None:
            continue
        # The published baseline is the file on the base branch tip, not on the merge base,
        # under the name it has there if the base branch renamed it after the fork. An added
        # file is looked for at its own path, since the base branch may have added it too.
        published_path = path_at(merge_base, base, old_path) if old_path else path
        published = show(base, published_path)
        if published is not None and rendered(published, published_path) == rendered(head_text, path):
            continue   # the base branch already has this content, so the file adds nothing to the merge
        value = field(head_text)
        base_text = show(merge_base, old_path) if old_path else None
        if value is None:
            if base_text is not None and field(base_text) is not None:
                problems.append("%s: the base version has a Last Updated field in its metadata header block, "
                                "and this pull request removed it or moved it out of that block. Restore it, "
                                "with the date of the change." % path)
            elif (published is not None and field(published) is not None
                  and (base_text is None or rendered(base_text, old_path or path) != rendered(head_text, path))):
                # The base branch added the block after the fork; a clean merge would keep its
                # older date over this pull request's newer content.
                problems.append("%s: the base branch has added a Last Updated field to this file since this pull "
                                "request forked, and this pull request changes its content. Merge the base branch "
                                "in, then set the field to the date of the change." % path)
            continue
        day = calendar_date(value)
        if day is None:
            problems.append("%s: Last Updated reads %r, which is not a real calendar date in YYYY-MM-DD form. Set "
                            "it to the UTC date of the change." % (path, value))
            continue   # every other rule needs the date
        base_value = field(base_text) if base_text is not None else None
        base_day = calendar_date(base_value)
        if base_day is not None and day < base_day:
            problems.append("%s: Last Updated moved back from %s to %s. It must not be earlier than the "
                            "base version's date." % (path, base_value, value))
        if base_text is not None and old_path and rendered(base_text, old_path) == rendered(head_text, path):
            continue
        changes = content_changes(merge_base, head, path, old_path)
        need = max((authored for authored, _ in changes), default=None)
        made = max((committed for _, committed in changes), default=None)
        date_is_wrong = True
        if need is None or made is None:
            # Fail closed: the content differs from the base, so some commit changed it.
            problems.append("%s: its content changed, but no pull request commit could be found that "
                            "changed it, so the required date is unknown." % path)
        elif day < need:
            problems.append("%s: Last Updated is %s, but this pull request changed its content in a "
                            "commit dated %s (UTC). Set it to %s or later." % (path, value, need, need))
        elif day > made and value not in (base_value, field(published) if published is not None else None):
            # A date later than the change would let later edits skip the bump. The base's own
            # value is allowed, because this pull request did not set it.
            problems.append("%s: Last Updated is %s, which is later than the last commit that changed its "
                            "content, made on %s (UTC). Set it to %s." % (path, value, made, need))
        else:
            date_is_wrong = False
        try:
            head_version = version(head_text)
        except ValueError:   # a component too long for int(), past Python's digit limit
            problems.append("%s: its Version value cannot be read as numbers. Write it as "
                            "<major>.<minor>.<YYYYMMDD>.<revision>, each part a short whole number." % path)
            continue
        if head_version is None:
            continue
        major, minor, date, revision = head_version
        if date != value.replace("-", ""):
            problems.append("%s: the Version date segment is %s, but Last Updated is %s. They must match."
                            % (path, date, value))
        # The revision depends on the date, so it is checked only once both dates are right.
        if date_is_wrong or date != value.replace("-", ""):
            continue
        try:
            baseline = version(published) if published is not None else None
        except ValueError:
            baseline = None   # an unreadable Version on the base branch counts as none
        if baseline is not None and baseline[:3] == head_version[:3]:
            expected, why = baseline[3] + 1, "the base branch already has %d.%d.%s.%d" % baseline
        else:
            expected, why = 0, ("the base branch has %d.%d.%s.%d" % baseline if baseline
                                else "the base branch has no Version for this file")
        if revision != expected:
            problems.append("%s: Version is %d.%d.%s.%d, but %s, so the revision must be %d."
                            % (path, major, minor, date, revision, why, expected))
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
    except CheckError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    finally:
        render.close()
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
