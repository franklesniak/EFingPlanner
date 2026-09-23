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
   failing.
2. If the file carries ``**Version:** <major>.<minor>.<YYYYMMDD>.<revision>``
   and its content changed, the ``<YYYYMMDD>`` segment must equal the field, and
   ``<revision>`` must follow the guide's convention against the published
   baseline, the file on the base branch tip: ``N + 1`` when the baseline has the
   same ``<major>.<minor>.<YYYYMMDD>`` at revision ``N``, otherwise ``0``.
3. If the base version carried the field and the head does not, the field was
   removed or moved out of the metadata header block, which fails.
4. The field must not be earlier than the base version's field. A rebased or
   cherry-picked commit can keep an old author date; the field still may not
   move backwards.

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
block, do not count. Relative link and image targets are compared as repository
paths, resolved from each version's own directory, so moving a file to another
directory changes its content exactly when a relative reference now points
somewhere else.

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
import posixpath
import re
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

    Each answer holds the rendered HTML (`html`), the `Last Updated` field
    (`lastUpdated`) and the `Version` date segment (`version`); see the helper for
    exactly what each one means. Answers are cached by text. Any failure raises
    RenderError, so a renderer problem can never read as "mechanical" or "no field".
    """

    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.cache: dict[str, dict[str, Any]] = {}

    def __call__(self, text: str) -> dict[str, Any]:
        if text not in self.cache:
            self.cache[text] = self.ask(text)
        return self.cache[text]

    def ask(self, text: str) -> dict[str, Any]:
        if self.process is None:
            try:
                self.process = subprocess.Popen([NODE, HELPER], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                text=True, encoding="utf-8", errors="surrogateescape")
            except OSError as exc:
                raise RenderError("cannot start %s %s: %s" % (NODE, HELPER, exc)) from exc
        assert self.process.stdin is not None and self.process.stdout is not None
        try:
            # ensure_ascii escapes everything else, including undecodable bytes carried as surrogates.
            self.process.stdin.write(json.dumps(text, ensure_ascii=True) + "\n")
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


REFERENCE = re.compile(r"""\b(href|src)=("[^"]*"|'[^']*')""")
NOT_RELATIVE = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]*:|/|#|\?|$)")


def rendered(text: str, path: str) -> str:
    """The text as CommonMark renders it at `path`, with trailing whitespace removed from each line.

    Two versions with equal output differ only mechanically: in line endings, the
    end-of-file newline, or trailing whitespace that renders nothing. A hard line break
    renders as `<br />`, so removing or adding one is still a content change.

    Every relative `href` and `src` is rewritten to a path from the repository root,
    resolved from the directory of `path`, so a relative reference compares by the file
    it points to. Moving a file therefore changes its content exactly when one of its
    references now points somewhere else. URLs with a scheme, root-relative paths and
    fragment-only or query-only links do not depend on the file's directory and are
    kept as they are.
    """
    directory = posixpath.dirname(path)

    def resolve(m: re.Match[str]) -> str:
        quote, url = m.group(2)[0], m.group(2)[1:-1]
        if NOT_RELATIVE.match(url):
            return m.group(0)
        cut = min([i for i in (url.find("?"), url.find("#")) if i >= 0], default=len(url))
        target, rest = url[:cut], url[cut:]
        return "%s=%s/%s%s%s" % (m.group(1), quote, posixpath.normpath(posixpath.join(directory, target)),
                                 rest, quote)

    return REFERENCE.sub(resolve, cast(str, render(text)["html"]))


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


def required_date(base: str, head: str, path: str) -> dt.date | None:
    """UTC author date of the newest PR commit that changed the file's content.

    Every PR commit that touched the file is considered, merges included, and the
    latest qualifying author date wins. Content is compared as rendered (see
    `rendered()`). A non-merge commit qualifies when its content differs from its
    parent's. A merge, of any number of parents, qualifies only when its content
    differs from git's own clean merge of all its parents (see `clean_merge()`): an
    automatic merge adds nothing, because each side's commits carry their own dates,
    while a conflict resolution or an edit made during the merge is authored.
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
            befores.append(rendered(content or "", own or name))
        if len(parents) >= 2:
            automatic = clean_merge(parents, name)
            authored = rendered(automatic or "", name) != rendered(after, name)
        else:
            authored = bool(befores) and all(b != rendered(after, name) for b in befores)
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
                problems.append("%s: the base version has a Last Updated field in its metadata header block, "
                                "and this pull request removed it or moved it out of that block. Restore it, "
                                "with the date of the change." % path)
            continue
        base_value = field(base_text) if base_text is not None else None
        if base_value is not None and dt.date.fromisoformat(value) < dt.date.fromisoformat(base_value):
            problems.append("%s: Last Updated moved back from %s to %s. It must not be earlier than the "
                            "base version's date." % (path, base_value, value))
        if base_text is not None and old_path and rendered(base_text, old_path) == rendered(head_text, path):
            continue
        need = required_date(merge_base, head, path)
        if need is None:
            # Fail closed: the content differs from the base, so some commit changed it.
            problems.append("%s: its content changed, but no pull request commit could be found that "
                            "changed it, so the required date is unknown." % path)
        elif dt.date.fromisoformat(value) < need:
            problems.append("%s: Last Updated is %s, but this pull request changed its content in a "
                            "commit dated %s (UTC). Set it to %s or later." % (path, value, need, need))
        date_is_stale = need is None or dt.date.fromisoformat(value) < need
        head_version = version(head_text)
        if head_version is None:
            continue
        major, minor, date, revision = head_version
        if date != value.replace("-", ""):
            problems.append("%s: the Version date segment is %s, but Last Updated is %s. They must match."
                            % (path, date, value))
        # The revision depends on the date, so it is checked only once both dates are right.
        if date_is_stale or date != value.replace("-", ""):
            continue
        # The published baseline is the file on the base branch tip, not on the merge base.
        published = show(base, old_path) if old_path else None
        baseline = version(published) if published is not None else None
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
