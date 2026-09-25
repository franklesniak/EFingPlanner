"""Check tracked files for leaked family values and destination names.

One script, two rules, chosen with ``--rule``:

``--rule family``
    Acceptance criterion ``AC-29-2`` in ``docs/spec/specification.md``, and the
    wider rule that no tracked file carries this family's data. The values are
    the ones the spec's trip-basics BUILD RULE names (Section 2.5): the origin
    city, the home airport's code, the trip-length number, and two roster
    words, plus the home airport's name from the card bullet below that rule.
    They belong on the family's own Trip-Basics card, which is never
    committed. The rule reads every tracked text file except ``docs/spec/``,
    the owner's protected design record, which states the values on purpose.

``--rule destination``
    Acceptance criterion ``AC-16-1``: no destination name in the reusable
    framework. The rule reads every tracked file under ``framework/``, the
    scope the style law (``framework/docs/build_style_and_vocab.md``) gives its
    destination-names ban.

The values are not in this file
-------------------------------
This repository is public, so the family rule cannot hold its values as
text. ``FAMILY_VALUES`` holds a SHA-256 digest of each value's normalized
form, mixed with ``SALT``, and the scan hashes the words and numbers of each
file and compares digests. **A digest hides a value from reading, grepping
and search indexes. It does not hide it from a guess.** The values are
ordinary words, a city and a three-letter code, and anyone who guesses one
can confirm it against its digest; a salt only stops a lookup in a
precomputed table. The design record already prints the values in this
repository, so the digests add no exposure. The hook's output never prints a
matched family value either, because a CI log is readable by anyone who can
read the repository.

``tests/test_check_leaks.py`` reads the design record's BUILD RULE line at
test time and proves that every value it names is listed here, so the list
cannot drift from its source without a failing test.

What a match is
---------------
A file is read as it is written, every character of it: a value inside a
fenced or indented code block, an HTML comment, a link's text or its path
is written in the file all the same, and a comment is still published with
it. A line that holds a character reference, a percent escape or a
backslash is read a second time with those decoded, so ``&#99;`` or ``%63``
does not hide a letter, and a word or number right after a one-letter
backslash escape, such as a regular expression's ``\\b``, ``\\A`` or ``\\s``, is
read without the escape's letter. Each character of the decoded reading
keeps the span of the file it came from, so every hit is reported at the
file's own line and column. A decoded occurrence that covers some of the
same characters of the file as a plain occurrence of the same value is the
same occurrence and counts once; any other decoded occurrence counts on its
own, beside a plain one on the same line. Each file's repository-relative
path is read too, as one more line of the file, by the same loop as its
text, so every way the text is read, the path is read too: a value or a
name in a file's or a folder's name is a hit, escaped or not, and a bare
number in it is a candidate, a binary file's included.

* A **word** value matches a run of letters, or two or three runs in a row
  separated by anything but digits and a blank line, in any case. The last
  run may carry a plural ``s``. Letters are a run, so an apostrophe, a
  hyphen, an underscore, a slash or a digit ends one: a possessive, a
  compound and a link path all hold the word, and a longer word that merely
  contains it does not.
* A **code** value matches a whole run of letters, digits and underscores,
  in its exact case, so the code in lower case, or inside a longer
  identifier, is not a match.
* A **number** value is the trip-length number, and it leaks only where the
  text states it as the trip length, in one of four ways, in any case:

  - followed by ``day``, ``days``, ``night`` or ``nights``, with nothing
    between but spaces, one line break, one hyphen or dash, and the
    Markdown, bracket or quote marks around the number or the unit;
  - followed by the design record's own words for it, "as a trip-length
    cap";
  - after a label for it: "trip length" (or "trip length in days"), or the
    design record's "this family:", joined to the number by marks such as a
    colon, an equals sign, "is", "of", or an opening bracket;
  - in a grep pattern for it: the number, a bracket class or a ``\\s`` or
    ``\\W`` escape, then the unit, as a hand-run leak grep writes it.

  A spelled-out number from one to ninety-nine counts as its digits, and
  digits from any script count as their ASCII digits, read as text, so a
  run of any length is read. A number that is part of a decimal or a
  thousands group is not a match; a comma or a full stop that does not
  follow a digit, as in a CSV field, does not hide one. A bare number is
  not a leak: the design record's grep note lists page numbers, item counts
  and dates as the wider pattern's false positives, and the Batch 2 build
  brief scopes this hook to the number with its unit. The label and the cap
  phrase state the trip length as plainly as a unit does. ``--candidates``
  lists the bare occurrences, in text and in paths, for the grep note's
  hand-read, and does not fail. A word between the number and its unit ("N
  full days"), and a cap with no unit or label ("the trip cannot go past
  N"), are left to that hand-read.
* A **destination** name matches a word that begins with it, in any case,
  so a demonym or a path segment into a pack matches. The names are the five
  ``AC-16-1`` gives, and the name of every folder under ``destinations/``
  that holds a file Git tracks, so a local folder nobody committed adds no
  name and a run in CI reads the same list as a run on a laptop.

Exemptions
----------
An exemption covers one occurrence, never a file. A row names its path, what
was matched, the words around it (up to three either side, on its own line,
the way the self-containment scan in ``tests/test_self_contained_references.py``
binds its rows), how many such occurrences it covers, and why they may stay. A
family row holds a digest of those words, since the words hold the value. A
row names a path its rule reads. A row whose occurrences have gone is
reported as stale, so a row cannot outlive its reason: a run given paths
judges the rows of the files it read, and a walk judges every row, so a
row for a file Git no longer tracks is stale there. ``--exemption-rows``
prints a row for each unexcused match, for a maintainer to review and paste
in with a reason. A destination name in a path is excused by a row whose
context is ``(path)`` and the path, decoded when the name was escaped. A
family value in a path is never excused, because its row would spell the
value: rename the file. No row is printed whose path or words hold a
family value, under either rule.

Output
------
Every line either rule prints passes through ``emit()``, which replaces
each family value in it with ``<family value>``: a hit, a stale row, a
refusal, an error, a candidate and an exemption row. The destination rule
masks as the family rule does, so a framework path or line that holds both
a destination name and a family value prints the name and hides the value.
A malformed value row stops both rules before either prints anything read
from the repository, since a row the data check cannot read masks nothing.
While one stands, an argument error or an unexpected error prints a fixed
line in place of its message, and a row error names the row by number, not
by what it holds.
A value is masked as it is written, escaped or not, and so is an argument
error, which names the argument it could not read. Only ``--hash`` prints
elsewhere, and it prints digests. An unexpected error prints one masked
line, naming its type, where in this script it was raised, and its
message, and exits 2, with no traceback. A bare number is printed as it
stands: it is not a family value, and masking the family's number wherever
it stood, in a session number or a date, would print which number it is.

File access
-----------
Only files inside the repository are read. With no paths, the run walks the
files Git tracks. It refuses, by name, a tracked path in the rule's scope
that is a symbolic link or a junction, that goes through a linked folder,
or that resolves outside the repository, and it refuses the same path when
pre-commit passes it, so a link fails a commit as it fails CI. The hooks
take links as well as files for that reason. A passed path Git does not
track is neither read nor refused, whether it resolves or not, so a local
file such as one under ``.git/`` is never read. A tracked submodule in the
rule's scope is refused by name too: its content is another repository,
which this run cannot read. A file holding a zero byte is binary: its path
is read, and its bytes are skipped, as Git treats them. A file that cannot
be read as UTF-8 stops the run, because a file that was not read has not
been checked. The pre-commit entries end with ``--``, so a file whose name
begins with a hyphen is read as a path, never taken for an option.

In place of a hand-run grep
---------------------------
A grep for the family's values has to name them, so the grep itself leaks
them: into the file that holds it, the shell's history and its output. This
script is the replacement. A build brief or a checklist that asks for the
leak greps runs these calls instead, and they name no value and print none:

* ``python .github/scripts/check-leaks.py --rule family``, which exits 1 and
  prints each unexcused occurrence as a path, line, column and kind;
* ``python .github/scripts/check-leaks.py --rule family --candidates``, the
  grep note's hand-read of bare numbers, which lists positions and exits 0.
  Those positions point at the family's number, so keep that list in a local
  terminal: never paste it into a pull request, an issue or a CI log;
* ``python .github/scripts/check-leaks.py --rule destination``.

A grep for a destination name, for a path into ``destinations/`` or for a
spec section number names nothing private, and may stay a grep.

Known limits
------------
The hook matches forms, not meaning. These pass it, and are left to a
person's read, to ``--candidates``, or to another check:

* A paraphrase or an inference: a cap with no unit or label ("the trip
  cannot go past N"), a word between the number and its unit ("N full
  days"), an ordinal, a number over ninety-nine in words, or a length given
  in weeks.
* A spelling the matcher does not fold: a misspelling, a nickname or an
  abbreviation, letters split by spaces or by an invisible character such
  as a zero-width space, a look-alike letter from another alphabet, the
  code in lower case or inside a longer identifier, and a word value inside
  a longer word.
* An encoding other than a character reference, a percent escape and a
  one-letter backslash escape: ``\\uXXXX``, ``\\xXX``, octal, base64 or a
  cipher, and a character reference split over two lines.
* A value the lists do not hold: a relative the BUILD RULE line does not
  name, and a destination name that is neither one of the five nor a pack
  folder's name, such as a second city or a landmark.
* What the hook does not read: ``docs/spec/``, untracked files, a binary
  file's bytes, a submodule's content (refused, not read), Git history,
  commit messages, branch and tag names, pull request text and issues.
* A deleted file's stale row: pre-commit passes no file for a deletion, so
  only a walk reports it, and CI's walk runs in this script's suite.
* A digest does not stop a guess, as the section above says.

Adding a family's value
-----------------------
Run ``python .github/scripts/check-leaks.py --hash word`` (or ``code`` or
``number``), type the value, and end the input. The value is read from
standard input so it stays out of the shell history. Paste the printed lines
into ``FAMILY_VALUES``.
"""

from __future__ import annotations

import argparse
import bisect
import functools
import hashlib
import html
import os
import re
import stat
import subprocess
import sys
import traceback
import unicodedata
import urllib.parse
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------

#: Mixed into every digest. It is public and it is not a secret; it stops a
#: lookup of these digests in a precomputed table of common words.
SALT = "efingplanner leak check"

#: ``(kind, words, digest)`` for each family value. ``words`` is how many
#: letter runs a word value holds, which bounds how far the scan joins runs;
#: it is 1 for a code and a number. Generate a row with ``--hash``.
FAMILY_VALUES: tuple[tuple[str, int, str], ...] = (
    # The origin city.
    ("word", 1, "62b3feeb7ad9938881a521ceb08da1b58a7dbdef1ebc013d9129d94e094d207b"),
    # The home airport's code.
    ("code", 1, "4af76db67cd33995d834017627c8af91efe99aee3136520561319cf2c0b9837f"),
    # The trip-length number.
    ("number", 1, "ff3ec1d08e7d007a7b904ef466a4fec5c9f6cc6ee0abfc60151eb4de9c79ceeb"),
    # The two roster words.
    ("word", 1, "438c89b4fef2bccad89a5fae9cbb40301ba379e5a02f9cba4f5df064b74ccdb0"),
    ("word", 1, "cb9e4fb9d18f3a7db66394a0aed32ad8e68f736d8c0d01538a1f934253e2ef9b"),
    # The home airport's name, as two words and as one.
    ("word", 2, "e315fe8d70b551c841a46edc193876fdbb34f6cb1e3afda902d85dd960eb7baa"),
    ("word", 1, "8e9662ba76c03835748fa2fbb963d9949bb8d14ac6c16eaceabecfe9e587d5a1"),
)

#: The destination names ``AC-16-1``'s grep part names. The name of every
#: folder under ``destinations/`` is added at run time.
DESTINATION_NAMES = ("Japan", "Tokyo", "Kyoto", "Osaka", "Shinkansen")

#: The reasons the rows below give, each written once.
BRIEF_RULE = "A build brief's leak rule names the values it bans."
BRIEF_GREP = "A build brief's self-check prints the values its grep command looks for."
BRIEF_TRIP_LENGTH_NOTE = (
    "The Batch 1 brief's note on its narrowed trip-length token shows the forms the token matches."
)
BRIEF_PLURAL_NOTE = (
    "The Batch 1 brief's note on plurals and case quotes the forms and the fixture lines it measured."
)
CHANGELOG_PACK_LINE = (
    "Version history: the 0.1.0 Added line records which destination pack shipped. The style law "
    "names it as a permanent exception."
)
STYLE_LAW_RULE = (
    "The style law's destination-names bullet prints the names it bans. The bullet names itself as "
    "a permanent exception."
)

#: ``(path, kind, context digest, count, reason)``. The context digest is
#: ``value_digest("context", words)`` over the words ``occurrence_context``
#: gives: up to three either side of the occurrence, on its own line.
FAMILY_EXEMPTIONS: tuple[tuple[str, str, str, int, str], ...] = (
    (
        "docs/build/_build_prompt_template.md", "word",
        "d6e85956a42ea20d2cf4e4982a012f25e2c11b3ee0b6fd2d39268baf8de5cec8", 1, BRIEF_RULE,
    ),
    (
        "docs/build/_build_prompt_template.md", "code",
        "96b82d47292c00ca147ff91390bfe17e9bdf9fb85f316ce44398eed326cfe18d", 1, BRIEF_RULE,
    ),
    (
        "docs/build/_build_prompt_template.md", "word",
        "d002f4c407e4448570af3e532f0bff70d65a3a20d805f24c5549db5a15036641", 1, BRIEF_RULE,
    ),
    (
        "docs/build/_build_prompt_template.md", "word",
        "e6fae2d0bd2e2313ecd2a8c50e3c965b0a17deb40308771bf86be5fd4718b21b", 1, BRIEF_RULE,
    ),
    (
        "docs/build/_build_prompt_template.md", "number",
        "5c81c94ca37dcdba3546fddd7d5a32c813813ab60288d4e244f551748ee388ea", 1, BRIEF_RULE,
    ),
    (
        "docs/build/_build_prompt_template.md", "word",
        "f0d94a26dd0279d47f9536f87c027242d91b78a6653bc95e80a670f0895bc38f", 3, BRIEF_GREP,
    ),
    (
        "docs/build/_build_prompt_template.md", "code",
        "f0d94a26dd0279d47f9536f87c027242d91b78a6653bc95e80a670f0895bc38f", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch0_build_prompt.md", "word",
        "fb442ccf809f426f48faa87c54bc6653c72358e656b2448926c29f511168287d", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch0_build_prompt.md", "code",
        "932ed8a82be700f3738a897a883b04d9da2769eaf8418743967cbf51beb114eb", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch0_build_prompt.md", "word",
        "228f91f54649b6243d214a3a7aae9f1fcbe7802b500f383f810f44e7539866a8", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch0_build_prompt.md", "word",
        "e6fae2d0bd2e2313ecd2a8c50e3c965b0a17deb40308771bf86be5fd4718b21b", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch0_build_prompt.md", "number",
        "5c81c94ca37dcdba3546fddd7d5a32c813813ab60288d4e244f551748ee388ea", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch0_build_prompt.md", "word",
        "e53f5311742145e972274c662d3d40f0d1819f1f7b14e053231216214679320d", 3, BRIEF_GREP,
    ),
    (
        "docs/build/batch0_build_prompt.md", "code",
        "e53f5311742145e972274c662d3d40f0d1819f1f7b14e053231216214679320d", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "4267c044a7ecbb60cb39f0b0974752ea9fe62c477f564051b67ac3830479a36e", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "code",
        "395988df5a873fbf92979f9e732ff51a22d40fafb1b0a8270cdcefb46f53d418", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "de791b686e14055b4dae02d30ef18e1e88ce389b69d4c5dedbc41c6823dc4169", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "66b5119914b79dddbe86cc3d1071dd88f98631d3db467360a3ddf6477758f364", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "eebb37c794e313606944d8d6a76462792cdab4b787b8a03078d4b6e195805640", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "d6e85956a42ea20d2cf4e4982a012f25e2c11b3ee0b6fd2d39268baf8de5cec8", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "code",
        "96b82d47292c00ca147ff91390bfe17e9bdf9fb85f316ce44398eed326cfe18d", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "ce90a0665dd1f53b929c23f22ab76eed7fda06faefe2ce86556c48395c63c3be", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "f725cef4bfe515d2c3d35c60cc4bff956e5efac10a703ca27395ff0f23bcc66d", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "5c81c94ca37dcdba3546fddd7d5a32c813813ab60288d4e244f551748ee388ea", 1, BRIEF_RULE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "9453e333123e110817f7885e15102c0aa065dbd43462a8d5e97af7430ebd86bb", 3, BRIEF_GREP,
    ),
    (
        "docs/build/batch1_build_prompt.md", "code",
        "9453e333123e110817f7885e15102c0aa065dbd43462a8d5e97af7430ebd86bb", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "9453e333123e110817f7885e15102c0aa065dbd43462a8d5e97af7430ebd86bb", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "e93483b40184bbd8cc56afe4b51b67e5d76159e332c95d79b98b9aa455493852", 1, BRIEF_TRIP_LENGTH_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "70747d3eb5de4563c2839096218470c804e1d66d2549b5537b4eaca8b519306e", 1, BRIEF_TRIP_LENGTH_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "ff0b9de7b7c82ba94bc2c7ca2b956ca39d2cd09f376fa63ba4c00b8381be4fb5", 1, BRIEF_TRIP_LENGTH_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "1b8576accc6f85be3d0a2cc75810bc46d4b1a1ed90f46bc36b69be167ba9402d", 1, BRIEF_TRIP_LENGTH_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "number",
        "fa84f81bbb556710e1a8ed52899f6d0dbbaa884b945511d9fd76a00b1dad6ba1", 1, BRIEF_TRIP_LENGTH_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "0851166053f994d20734974fbd11f7d729cfd66bfb98d1147c0be3c453234dce", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "49d1bcc9f695af9ed78144d379119b525fed04a0a4eaf36cb8c639e592fa13ef", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "0874722845b24550954d839aee86023943134a2442b52513a6ddd4cfe284d50c", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "68b5e2400e8296216742d994240d6e9ad468387d07515af8a85c112d00a1b764", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "09b8b1d0d40207d53f0200337606a1ba38e2b542dd635d5f11e6e2da61c62cb7", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "01a4d6bd6839410efaab7d017b6096f7a00d34e8edcf128ac6e36bd01ec94314", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "05edf04b3960830d826ad89b5b987523e93ab2810b979dd30dedcc4401850eee", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch1_build_prompt.md", "word",
        "8b13d444bb2c038ff0c735ff748fb4d11fe986bcad302cd09052f2e7b6cbc518", 1, BRIEF_PLURAL_NOTE,
    ),
    (
        "docs/build/batch2_build_prompt.md", "word",
        "7694c80e02d5f518db924e7bf109831f6f8422dfbae2f3c01fa9eb27dfdc8914", 3, BRIEF_GREP,
    ),
    (
        "docs/build/batch2_build_prompt.md", "code",
        "7694c80e02d5f518db924e7bf109831f6f8422dfbae2f3c01fa9eb27dfdc8914", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch2_build_prompt.md", "number",
        "86dde9d8578b9b83a7f15dd5d37d80032951298ceab4fb194e603732a1d06de6", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "word",
        "6968a04f4bab347696c0cd23e5d0be3fc8850d16555a4cd502c37a10bb2a8c05", 3, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "code",
        "6968a04f4bab347696c0cd23e5d0be3fc8850d16555a4cd502c37a10bb2a8c05", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "number",
        "ea411721a772a532478f3e1a37d969892bdbe9074c5f4b21e588541656854d61", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "word",
        "c95f89cc63af37e0f2b0abaaaae73c21ad7584c848f2435704f8b1806dd139d9", 3, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "code",
        "c95f89cc63af37e0f2b0abaaaae73c21ad7584c848f2435704f8b1806dd139d9", 1, BRIEF_GREP,
    ),
    (
        "docs/build/batch3_build_prompt.md", "number",
        "ee484b222b56da2b46593f8448dabb70539b0d45aa05114a3b2ee627351f6466", 1, BRIEF_GREP,
    ),
)

#: ``(path, occurrence, context, count, reason)``.
DESTINATION_EXEMPTIONS: tuple[tuple[str, str, str, int, str], ...] = (
    (
        "framework/CHANGELOG.md", "Japan",
        "- The Japan reference pack, and",
        1, CHANGELOG_PACK_LINE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Japan",
        "Batch 1 onward.** Japan, Tokyo, Kyoto, Osaka,",
        1, STYLE_LAW_RULE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Tokyo",
        "1 onward.** Japan, Tokyo, Kyoto, Osaka, and",
        1, STYLE_LAW_RULE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Kyoto",
        "onward.** Japan, Tokyo, Kyoto, Osaka, and Shinkansen",
        1, STYLE_LAW_RULE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Osaka",
        "Japan, Tokyo, Kyoto, Osaka, and Shinkansen appear",
        1, STYLE_LAW_RULE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Shinkansen",
        "Kyoto, Osaka, and Shinkansen appear under `destinations/`",
        1, STYLE_LAW_RULE,
    ),
    (
        "framework/docs/build_style_and_vocab.md", "Japan",
        "the first sessions Japan-concrete on purpose; Batch",
        1, STYLE_LAW_RULE,
    ),
)

# --------------------------------------------------------------------------
# Scope
# --------------------------------------------------------------------------

RULES = ("family", "destination")
KINDS = ("word", "code", "number")
#: The family rule reads every tracked text file except these. The design
#: record states the values on purpose, and it is the owner's to edit.
FAMILY_SKIPPED_PREFIXES = ("docs/spec/",)
#: The destination rule reads only these.
DESTINATION_SCOPE_PREFIXES = ("framework/",)
#: Where the destination packs live. Each folder's name is a destination name.
DESTINATIONS_DIRECTORY = "destinations"
#: How many words either side of an occurrence bind an exemption to it.
CONTEXT_WORDS = 3
#: The longest word value, in letter runs, that ``--hash`` accepts.
MAX_VALUE_WORDS = 3

# --------------------------------------------------------------------------
# Reading words and numbers
# --------------------------------------------------------------------------

#: A run of letters. ``\w`` less digits and the underscore.
LETTER_RUN = re.compile(r"[^\W\d_]+")
#: A run of letters, digits and underscores: the unit a code value must fill.
WORD_RUN = re.compile(r"\w+")
HEX_DIGEST = re.compile(r"[0-9a-f]{64}")

UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
#: The teens are built from their stems and counted from ten, so this table
#: spells no whole number word, and no number, for ``--candidates`` to list.
TEEN_WORDS = ("ten", "eleven", "twelve") + tuple(
    stem + "teen" for stem in ("thir", "four", "fif", "six", "seven", "eigh", "nine")
)
TEENS = {word: 10 + index for index, word in enumerate(TEEN_WORDS)}

TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
#: A number spelled out, from one to ninety-nine. Longer words come first in
#: each group, so ``nineteen`` is not read as ``nine``.
SPELLED_NUMBER = (
    r"(?:(?:" + "|".join(TENS) + r")(?:[- \u00a0]?(?:" + "|".join(UNITS) + r"))?"
    r"|" + "|".join(sorted(TEENS, key=len, reverse=True))
    + r"|" + "|".join(sorted(UNITS, key=len, reverse=True)) + r")"
)
#: A number that does not continue a decimal, a thousands group or a word. An
#: underscore may stand before it, as Markdown's emphasis mark, and so may a
#: comma or a full stop that does not follow a digit, as in a CSV field.
NUMBER_START = r"(?<![^\W_])(?<!\d[.,])"
#: A number that does not go on into a longer number or a word.
NUMBER_END = r"(?![\w]|[.,]\d)"
NUMBER = r"(?P<number>\d+|" + SPELLED_NUMBER + r")"
#: Spaces, and at most one line break with a block quote marker after it.
GAP = r"[ \t\u00a0]*(?:\n[ \t\u00a0>]*)?"
#: Marks that may close around a number, or open around the word after it:
#: Markdown emphasis and code, a bracket, and a quote.
CLOSING_MARKS = r"[*_`~)\]\"'\u2019\u201d]{0,3}"
OPENING_MARKS = r"[*_`~(\[\"'\u2018\u201c]{0,3}"
#: What may stand between a number and its unit: those marks, spaces, one
#: line break (and a block quote marker after it), and one hyphen or dash.
UNIT_SEPARATOR = CLOSING_MARKS + GAP + r"(?:[-\u2010-\u2015][ \t\u00a0]*)?" + OPENING_MARKS
NUMBER_WITH_UNIT = re.compile(
    NUMBER_START + NUMBER + UNIT_SEPARATOR + r"(?:days?|nights?)(?![^\W\d_])",
    re.IGNORECASE,
)
#: "trip length", with a space, a hyphen, a dash or a line break, or joined.
TRIP_LENGTH = r"trip(?:[-\u2010-\u2015]|" + GAP + r")length"
#: The number, then the design record's words for it: "as a trip-length cap".
NUMBER_AS_CAP = re.compile(
    NUMBER_START + NUMBER + CLOSING_MARKS + GAP + r"\(?(?:\*\*|__|\*|_)?as" + GAP + r"a" + GAP
    + TRIP_LENGTH + GAP + r"cap(?![^\W\d_])",
    re.IGNORECASE,
)
#: A label for the number, then the number: "trip length: N", "trip length in
#: days (this family: N)". The label and the number are joined only by marks.
NUMBER_AFTER_LABEL = re.compile(
    r"(?<![^\W\d_])(?:" + TRIP_LENGTH + r"(?:" + GAP + r"in" + GAP + r"days)?|this" + GAP + r"family)"
    + r"(?:" + GAP + r"(?:\*\*|__|[*_`(\[:=]|is(?![^\W\d_])|of(?![^\W\d_])|this" + GAP + r"family))+"
    + GAP + OPENING_MARKS + NUMBER_START + NUMBER + NUMBER_END,
    re.IGNORECASE,
)
#: The number in a grep pattern for the trip length, as the build briefs and
#: the design record's grep note write one: the number, a bracket class or a
#: ``\s`` or ``\W`` escape, then the unit, alone or in an alternation.
NUMBER_IN_PATTERN = re.compile(
    NUMBER_START + NUMBER + r"(?:\[[^\]\n]{0,8}\][?*+]?|\\[sW][?*+]?)\(?(?:\?:)?"
    + r"(?:days?|nights?|day\|night|night\|day)(?![^\W\d_])",
    re.IGNORECASE,
)
#: Each way a trip length is stated, in the order a hit's span is taken from.
#: The unit rule keeps its whole match as the span; the others take the number's.
TRIP_LENGTH_RULES = (
    (NUMBER_WITH_UNIT, False),
    (NUMBER_AS_CAP, True),
    (NUMBER_AFTER_LABEL, True),
    (NUMBER_IN_PATTERN, True),
)
#: A number standing alone, for ``--candidates``.
BARE_NUMBER = re.compile(NUMBER_START + NUMBER + NUMBER_END, re.IGNORECASE)


def spelled_to_int(text: str) -> int:
    """Return the value of a number the ``SPELLED_NUMBER`` pattern matched."""
    words = [word for word in re.split(r"[- \u00a0]+", text.casefold()) if word]
    total = 0
    for word in words:
        total += TENS.get(word) or TEENS.get(word) or UNITS[word]
    return total


def digits_value(text: str) -> str:
    """Return decimal digits as ASCII digits with no leading zero, without ``int()``.

    Python refuses ``int()`` on a string of more than 4,300 digits, and a
    tracked file can hold one, so the digits are normalized as text.
    """
    return "".join(str(unicodedata.decimal(character)) for character in text).lstrip("0") or "0"


def number_value(text: str) -> str:
    """Return a matched number as the digits a number value is hashed from."""
    if text.isdecimal():
        return digits_value(text)
    return str(spelled_to_int(text))


def fold(text: str) -> str:
    """Return ``text`` in the compatibility form a word value is compared in."""
    return unicodedata.normalize("NFKC", text).casefold()


#: How many digests ``value_digest`` keeps. A scan hashes every word, word
#: pair and number of every file, so an unbounded cache would hold every
#: distinct token in the repository; this bound keeps memory flat whatever a
#: file holds, and keeps most of the cache's speed.
DIGEST_CACHE_SIZE = 4096


@functools.lru_cache(maxsize=DIGEST_CACHE_SIZE)
def value_digest(kind: str, normalized: str) -> str:
    """Return the salted digest of one normalized value of ``kind``."""
    return hashlib.sha256(f"{SALT}\x00{kind}\x00{normalized}".encode("utf-8")).hexdigest()


def normalize_value(kind: str, value: str) -> list[str]:
    """Return the normalized forms ``--hash`` records for one value.

    A word value of more than one letter run is recorded twice: as its runs
    joined by a space, and as one joined word, so a spelling without the
    space is found too.
    """
    if kind == "word":
        runs = LETTER_RUN.findall(fold(value))
        if not runs or len(runs) > MAX_VALUE_WORDS:
            raise ValueError(f"a word value holds one to {MAX_VALUE_WORDS} runs of letters")
        forms = [" ".join(runs)]
        if len(runs) > 1:
            forms.append("".join(runs))
        return forms
    if kind == "code":
        code = unicodedata.normalize("NFKC", value.strip())
        if not WORD_RUN.fullmatch(code):
            raise ValueError("a code value is one run of letters, digits and underscores")
        return [code]
    if kind == "number":
        text = value.strip()
        if text.isdecimal():
            return [digits_value(text)]
        if re.fullmatch(SPELLED_NUMBER, text, re.IGNORECASE):
            return [str(spelled_to_int(text))]
        raise ValueError("a number value is written in digits, or spelled out from one to ninety-nine")
    raise ValueError(f"the kind is one of {', '.join(KINDS)}")


# --------------------------------------------------------------------------
# Data checks
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class FamilyValues:
    """The family values as digests, by kind."""

    digests: dict[str, frozenset[str]]
    max_words: int

    @classmethod
    def from_rows(cls, rows: Iterable[tuple[str, int, str]]) -> FamilyValues:
        by_kind: dict[str, set[str]] = {kind: set() for kind in KINDS}
        max_words = 1
        for kind, words, digest in rows:
            by_kind[kind].add(digest)
            max_words = max(max_words, words)
        return cls({kind: frozenset(found) for kind, found in by_kind.items()}, max_words)

    @classmethod
    def from_plain(cls, values: Iterable[tuple[str, str]]) -> FamilyValues:
        """Build the set from plain ``(kind, value)`` pairs. The tests use this."""
        rows: list[tuple[str, int, str]] = []
        for kind, value in values:
            for form in normalize_value(kind, value):
                rows.append((kind, len(form.split(" ")), value_digest(kind, form)))
        return cls.from_rows(rows)


def check_family_values(rows: Sequence[object]) -> list[str]:
    """Return every problem with the ``FAMILY_VALUES`` rows.

    A loader that skips what it cannot read turns a value list into an empty
    one, and an empty list checks nothing while reporting success.
    """
    errors: list[str] = []
    if not rows:
        errors.append("FAMILY_VALUES holds no value, so the family rule would check nothing")
    seen: set[tuple[object, ...]] = set()
    for number, row in enumerate(rows, start=1):
        if not isinstance(row, tuple) or len(row) != 3:
            errors.append(f"FAMILY_VALUES row {number} is not (kind, words, digest)")
            continue
        kind, words, digest = row
        # An error names the row by number and never repeats a field: a
        # field typed in the wrong place could hold a value, and this error
        # prints before any mask can be trusted.
        if kind not in KINDS:
            errors.append(f"FAMILY_VALUES row {number} names an unknown kind; it is one of {', '.join(KINDS)}")
        if not isinstance(words, int) or isinstance(words, bool) or not 1 <= words <= MAX_VALUE_WORDS:
            errors.append(
                f"FAMILY_VALUES row {number} gives a word count that is not a whole number from 1 to {MAX_VALUE_WORDS}"
            )
        elif kind in KINDS and kind != "word" and words != 1:
            errors.append(f"FAMILY_VALUES row {number} gives a {kind} value {words} words; it is 1")
        if not isinstance(digest, str) or not HEX_DIGEST.fullmatch(digest):
            errors.append(f"FAMILY_VALUES row {number} holds no 64-character lowercase hex digest")
        if row in seen:
            errors.append(f"FAMILY_VALUES row {number} repeats an earlier row")
        seen.add(row)
    return errors


def check_exemption_rows(rule: str, rows: Sequence[object]) -> list[str]:
    """Return every problem with one rule's exemption rows."""
    name = "FAMILY_EXEMPTIONS" if rule == "family" else "DESTINATION_EXEMPTIONS"
    errors: list[str] = []
    keys: set[tuple[object, ...]] = set()
    for number, row in enumerate(rows, start=1):
        where = f"{name} row {number}"
        if not isinstance(row, tuple) or len(row) != 5:
            errors.append(f"{where} does not hold five fields")
            continue
        path, matched, context, count, reason = row
        if (
            not isinstance(path, str)
            or not path
            or path.startswith("/")
            or "\\" in path
            or ".." in path.split("/")
        ):
            errors.append(f"{where} names no repository-relative path")
        if rule == "family":
            if matched not in KINDS:
                errors.append(f"{where} names the kind {matched!r}")
            if not isinstance(context, str) or not HEX_DIGEST.fullmatch(context):
                errors.append(f"{where} holds no 64-character lowercase hex context digest")
        else:
            if not isinstance(matched, str) or not matched.strip():
                errors.append(f"{where} names no occurrence")
            elif not isinstance(context, str) or matched not in context:
                errors.append(f"{where} gives a context that does not hold its occurrence")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            errors.append(f"{where} gives the count {count!r}; it is a whole number, at least one")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{where} gives no reason")
        if isinstance(path, str) and path and not in_scope(rule, path):
            # A row for a file the rule never reads can never be used, and so
            # can never be reported stale either.
            errors.append(f"{where} names a path the {rule} rule does not read")
        key = (path, matched, context)
        if key in keys:
            errors.append(f"{where} repeats an earlier row's path, occurrence and context; add to its count")
        keys.add(key)
    return errors


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Hit:
    """One occurrence the rule reports, before exemptions."""

    rule: str
    display_path: str
    line_number: int
    column: int
    #: The family value's kind, or the destination name's casefolded form.
    label: str
    #: The occurrence as written. Held for a destination name only, because a
    #: family value is never kept in text.
    occurrence: str
    #: The exemption key's context: a digest for a family value, the words
    #: themselves for a destination name.
    context: str
    #: What the hit is, for merging the plain and decoded readings.
    value_key: str
    #: Whether the occurrence is in the file's repository-relative path, not
    #: its text. Such a hit's line is 0 and its column counts from the path's
    #: first character.
    in_path: bool = False

    def format_message(self) -> str:
        """Return the hit's message. ``emit()`` masks any family value in it before it prints."""
        shown = self.display_path
        if self.in_path:
            if self.rule == "family":
                return (
                    f"{shown}: the file's path holds {FAMILY_KIND_LABELS[self.label]}. Rename the "
                    "file or its folder; no row can excuse a path, since the row would spell the value."
                )
            return (
                f'{shown}: the file\'s path holds the destination name "{self.occurrence}". '
                "Place files live in the destination pack."
            )
        where = f"{shown}:{self.line_number}:{self.column}"
        if self.rule == "family":
            return (
                f"{where}: {FAMILY_KIND_LABELS[self.label]} is written here. It belongs on the "
                "family's Trip-Basics card, which is never committed."
            )
        return (
            f'{where}: the destination name "{self.occurrence}" is written in a framework file. '
            "Place facts live in the destination pack."
        )


FAMILY_KIND_LABELS = {
    "word": "a family value (a place or a relative)",
    "code": "a family value (the home airport's code)",
    "number": "a family value (the trip-length number, stated as the trip length)",
}


def occurrence_context(text: str, start: int, end: int) -> str:
    """Return the words around ``text[start:end]`` that bind an exemption to it.

    The occurrence is widened to the whole words it stands in, and up to
    ``CONTEXT_WORDS`` words either side are added from the lines it stands
    on, and no further, so an edit to the line above or below leaves the row
    alone. Runs of white space become one space.
    """
    first = text.rfind("\n", 0, start) + 1
    last = text.find("\n", end)
    line = text[first : len(text) if last == -1 else last]
    start -= first
    end -= first
    while start > 0 and not line[start - 1].isspace():
        start -= 1
    while end < len(line) and not line[end].isspace():
        end += 1
    before = line[:start].split()[::-1][:CONTEXT_WORDS][::-1]
    after = line[end:].split()[:CONTEXT_WORDS]
    return " ".join([*before, *line[start:end].split(), *after])


def line_starts_of(text: str) -> list[int]:
    """Return the offset where each line of ``text`` starts."""
    return [0] + [index + 1 for index, character in enumerate(text) if character == "\n"]


class Reading:
    """One reading of a file: its text, and where each of its characters came from.

    The plain reading is the file itself. A decoded reading also holds, for
    each of its characters, the span of the file's characters it was decoded
    from, so a hit in it is placed, and matched against the plain reading's
    hits, by where it stands in the file.
    """

    def __init__(
        self,
        text: str,
        source: str | None = None,
        starts: list[int] | None = None,
        ends: list[int] | None = None,
    ) -> None:
        self.text = text
        self.starts = starts
        self.ends = ends
        self.line_starts = line_starts_of(text if source is None else source)

    def source_span(self, start: int, end: int) -> tuple[int, int]:
        """Return the file's span for this reading's ``text[start:end]``."""
        if self.starts is None or self.ends is None:
            return start, end
        return self.starts[start], self.ends[end - 1]

    def position(self, offset: int) -> tuple[int, int]:
        """Return the file's ``(line, column)`` for this reading's ``offset``."""
        if self.starts is not None:
            offset = self.starts[offset]
        line = bisect.bisect_right(self.line_starts, offset)
        return line, offset - self.line_starts[line - 1] + 1


#: A one-letter backslash escape right before a word or a number: an anchor
#: or class of a regular expression (``\b``, ``\A``, ``\s``, ``\Q`` and the
#: rest, which differ by flavor), or a line break, tab or other control
#: escape. Read as written, its letter joins the word or starts it. The
#: decoded reading drops any such letter, and the plain reading keeps it, so
#: a word that merely starts after a backslash, as in a Windows path, is
#: still read whole in the plain reading.
ESCAPE_BEFORE_WORD = re.compile(r"\\[A-Za-z](?=[^\W_])")


#: A character reference, as ``html.unescape`` finds one.
#: The digits are bounded: no character needs more than seven, and
#: ``html.unescape`` would pass a longer run to ``int()``, which refuses one of
#: more than 4,300 digits.
CHARACTER_REFERENCE = re.compile(r"&(#[0-9]{1,32};?|#[xX][0-9a-fA-F]{1,32};?|[^\t\n\f <&#;]{1,32};?)")
#: A percent escape of an ASCII byte, or a run of escapes of the bytes above
#: it, which UTF-8 decodes together, as ``urllib.parse.unquote`` does.
PERCENT_ESCAPE = re.compile(r"%[0-7][0-9A-Fa-f]|(?:%[89A-Fa-f][0-9A-Fa-f])+")
#: A line break or other control character a decoding can produce.
DECODED_BREAK = re.compile(r"[\r\n\u2028\u2029\x0b\x0c\x1c-\x1e\x85]")


def rewrite(
    text: str, starts: list[int], ends: list[int], pattern: re.Pattern[str], replace: Callable[[re.Match[str]], str]
) -> tuple[str, list[int], list[int]]:
    """Replace each match of ``pattern`` in ``text``, and carry each character's file span along.

    A replacement's characters all take the span of the text they replace.
    """
    out: list[str] = []
    out_starts: list[int] = []
    out_ends: list[int] = []
    last = 0
    for match in pattern.finditer(text):
        out.append(text[last : match.start()])
        out_starts += starts[last : match.start()]
        out_ends += ends[last : match.start()]
        replacement = replace(match)
        out.append(replacement)
        out_starts += [starts[match.start()]] * len(replacement)
        out_ends += [ends[match.end() - 1]] * len(replacement)
        last = match.end()
    out.append(text[last:])
    out_starts += starts[last:]
    out_ends += ends[last:]
    return "".join(out), out_starts, out_ends


def decode_line(line: str, offset: int) -> tuple[str, list[int], list[int]]:
    """Return one line decoded, with each character's span in the file.

    Character references are decoded first and percent escapes second, so a
    reference that spells a percent escape is decoded twice, as before. A
    decoded line break becomes a space, and so does a one-letter backslash
    escape before a letter or a digit.
    """
    starts = list(range(offset, offset + len(line)))
    ends = [start + 1 for start in starts]
    text, starts, ends = rewrite(line, starts, ends, CHARACTER_REFERENCE, lambda match: html.unescape(match.group()))
    text, starts, ends = rewrite(
        text, starts, ends, PERCENT_ESCAPE, lambda match: urllib.parse.unquote(match.group())
    )
    text, starts, ends = rewrite(text, starts, ends, ESCAPE_BEFORE_WORD, lambda _match: " ")
    return rewrite(text, starts, ends, DECODED_BREAK, lambda _match: " ")


def readings(text: str) -> list[Reading]:
    """Return the file as written and, when it holds an escape, decoded.

    The decoded reading keeps one line for each line, and each of its
    characters keeps the span of the file it came from, so a hit in it is
    reported at the file's line and column.
    """
    found = [Reading(text)]
    if "&" in text or "%" in text or "\\" in text:
        parts: list[str] = []
        starts: list[int] = []
        ends: list[int] = []
        offset = 0
        for number, line in enumerate(text.split("\n")):
            if number:
                parts.append("\n")
                starts.append(offset - 1)
                ends.append(offset)
            decoded_line, line_starts, line_ends = decode_line(line, offset)
            parts.append(decoded_line)
            starts += line_starts
            ends += line_ends
            offset += len(line) + 1
        decoded = "".join(parts)
        if decoded != text:
            found.append(Reading(decoded, text, starts, ends))
    return found


def letter_runs(text: str) -> list[tuple[int, int, str]]:
    """Return each run of letters as ``(start, end, folded run)``."""
    return [(match.start(), match.end(), fold(match.group())) for match in LETTER_RUN.finditer(text)]


def joins(text: str, first_end: int, second_start: int) -> bool:
    """Return whether two letter runs may belong to one phrase.

    Anything but a digit and a blank line may stand between them.
    """
    gap = text[first_end:second_start]
    return gap.count("\n") <= 1 and not any(character.isdigit() for character in gap)


def plural_forms(run: str) -> tuple[str, ...]:
    """Return the run, and the run without a plural ``s``."""
    if len(run) > 2 and run.endswith("s"):
        return (run, run[:-1])
    return (run,)


def family_hits_in_reading(reading: Reading, values: FamilyValues) -> list[tuple[int, int, str, str]]:
    """Return ``(start, end, kind, value digest)`` for each family value in ``reading``."""
    text = reading.text
    found: list[tuple[int, int, str, str]] = []
    words = values.digests["word"]
    if words:
        runs = letter_runs(text)
        for index in range(len(runs)):
            for size in range(1, values.max_words + 1):
                last = index + size - 1
                if last >= len(runs):
                    break
                if size > 1 and not joins(text, runs[last - 1][1], runs[last][0]):
                    break
                head = [run for _start, _end, run in runs[index:last]]
                for form in plural_forms(runs[last][2]):
                    digest = value_digest("word", " ".join([*head, form]))
                    if digest in words:
                        found.append((runs[index][0], runs[last][1], "word", digest))
                        break
    codes = values.digests["code"]
    if codes:
        for match in WORD_RUN.finditer(text):
            digest = value_digest("code", unicodedata.normalize("NFKC", match.group()))
            if digest in codes:
                found.append((match.start(), match.end(), "code", digest))
    numbers = values.digests["number"]
    if numbers:
        for start, end, _number_start, digest in trip_lengths(text, numbers):
            found.append((start, end, "number", digest))
    return found


def trip_lengths(text: str, numbers: frozenset[str]) -> list[tuple[int, int, int, str]]:
    """Return ``(start, end, number start, digest)`` for each trip length stated with a listed number.

    A number that two rules both read is reported once, with the span of the
    first rule in ``TRIP_LENGTH_RULES`` that reads it.
    """
    found: dict[int, tuple[int, int, int, str]] = {}
    for pattern, number_span in TRIP_LENGTH_RULES:
        for match in pattern.finditer(text):
            number_start = match.start("number")
            digest = value_digest("number", number_value(match.group("number")))
            if number_start in found or digest not in numbers:
                continue
            if number_span:
                found[number_start] = (number_start, match.end("number"), number_start, digest)
            else:
                found[number_start] = (match.start(), match.end(), number_start, digest)
    return sorted(found.values())


def destination_names(root: Path, tracked: Sequence[str] | None = None) -> tuple[tuple[str, ...], ...]:
    """Return each destination name as its folded letter runs.

    The five names ``AC-16-1`` gives come first, then the name of each folder
    under ``destinations/`` that holds a file Git tracks (``tracked``, or the
    repository's own list). A folder that exists only on this machine adds
    nothing, so a run in CI reads the list a local run reads. Git records a
    linked folder as one file, so a link adds nothing either, and a folder
    whose name holds no letter adds nothing.
    """
    names: list[tuple[str, ...]] = []
    for name in DESTINATION_NAMES:
        names.append(tuple(LETTER_RUN.findall(fold(name))))
    if tracked is None:
        tracked = tracked_files(root)
    prefix = DESTINATIONS_DIRECTORY + "/"
    folders = {
        path[len(prefix) :].split("/", 1)[0]
        for path in tracked
        if path.startswith(prefix) and path.count("/") >= 2
    }
    for folder in sorted(folders):
        runs = tuple(LETTER_RUN.findall(fold(folder)))
        if runs and runs not in names:
            names.append(runs)
    return tuple(names)


def destination_hits_in_reading(
    reading: Reading, names: Sequence[tuple[str, ...]]
) -> list[tuple[int, int, str, str]]:
    """Return ``(start, end, name, name)`` for each destination name in ``reading``.

    A name's last run matches a letter run that begins with it; its earlier
    runs, when it has any, match whole runs.
    """
    text = reading.text
    runs = letter_runs(text)
    found: list[tuple[int, int, str, str]] = []
    for index in range(len(runs)):
        for name in names:
            last = index + len(name) - 1
            if last >= len(runs):
                continue
            if any(runs[index + offset][2] != name[offset] for offset in range(len(name) - 1)):
                continue
            if any(
                not joins(text, runs[position][1], runs[position + 1][0])
                for position in range(index, last)
            ):
                continue
            if runs[last][2].startswith(name[-1]):
                label = " ".join(name)
                found.append((runs[index][0], runs[last][1], label, label))
                break
    return found


#: Finds ``(start, end, label, value key)`` for each occurrence in one reading.
Finder = Callable[[Reading], list[tuple[int, int, str, str]]]


def across_readings(text: str, finder: Finder) -> list[tuple[Reading, int, int, str, str]]:
    """Return ``(reading, start, end, label, value key)`` for each occurrence ``finder`` reports.

    The file is read as written and, when it holds an escape, decoded. A
    decoded occurrence is dropped only when a plain occurrence of the same
    value covers some of the same characters of the file, so one occurrence
    both readings see is reported once, and two occurrences on one line, one
    plain and one escaped, are both reported. The enforcing scan and the
    ``--candidates`` hand-read both read a file this way.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    found: list[tuple[Reading, int, int, str, str]] = []
    plain: dict[str, list[tuple[int, int]]] = {}
    for reading_number, reading in enumerate(readings(text)):
        for start, end, label, value_key in sorted(finder(reading)):
            source_start, source_end = reading.source_span(start, end)
            if not reading_number:
                plain.setdefault(value_key, []).append((source_start, source_end))
            elif any(
                source_start < plain_end and plain_start < source_end
                for plain_start, plain_end in plain.get(value_key, ())
            ):
                continue
            found.append((reading, start, end, label, value_key))
    return found


def find_hits(
    text: str,
    display_path: str,
    rule: str,
    values: FamilyValues | None = None,
    names: Sequence[tuple[str, ...]] = (),
    in_path: bool = False,
) -> list[Hit]:
    """Return every occurrence ``rule`` reports in ``text``, before exemptions.

    ``in_path`` says ``text`` is the file's repository-relative path, which
    ``scan()`` reads through this same loop, as one more line of the file.
    The path's own rules are these flags and no more: its hits are on line
    0; a family hit in it keeps no context, since no row may excuse it; and
    a destination hit's context is ``(path)`` and the path as its reading
    reads it, so a decoded name stands in its own row's context.
    """
    if rule == "family":
        assert values is not None
        family_values = values

        def finder(reading: Reading) -> list[tuple[int, int, str, str]]:
            return family_hits_in_reading(reading, family_values)

    else:

        def finder(reading: Reading) -> list[tuple[int, int, str, str]]:
            return destination_hits_in_reading(reading, names)

    hits: list[Hit] = []
    for reading, start, end, label, value_key in across_readings(text, finder):
        line, column = reading.position(start)
        if rule == "family":
            occurrence = ""
            context = "" if in_path else value_digest("context", occurrence_context(reading.text, start, end))
        else:
            occurrence = reading.text[start:end]
            context = PATH_CONTEXT + reading.text if in_path else occurrence_context(reading.text, start, end)
        hits.append(
            Hit(rule, display_path, 0 if in_path else line, column, label, occurrence, context, value_key, in_path)
        )
    hits.sort(key=lambda hit: (hit.line_number, hit.column))
    return hits


def bare_numbers(text: str, values: FamilyValues) -> list[tuple[int, int]]:
    """Return ``(line, column)`` for each bare trip-length number, for a hand-read.

    A number the family rule already reports as a trip length is left out.
    The file is read as the enforcing scan reads it, decoded too, so an
    escaped number is listed once.
    """
    numbers = values.digests["number"]

    def finder(reading: Reading) -> list[tuple[int, int, str, str]]:
        reported = {start for _start, _end, start, _digest in trip_lengths(reading.text, numbers)}
        found = []
        for match in BARE_NUMBER.finditer(reading.text):
            digest = value_digest("number", number_value(match.group("number")))
            if match.start() not in reported and digest in numbers:
                found.append((match.start(), match.end(), "number", digest))
        return found

    return sorted(reading.position(start) for reading, start, _end, _label, _key in across_readings(text, finder))


#: How a destination row names a path hit: this, then the path, as its context.
PATH_CONTEXT = "(path) "
#: What a message prints in place of a family value.
MASKED_VALUE = "<family value>"


def redact(text: str, values: FamilyValues) -> str:
    """Return ``text`` with each family value in it replaced by ``MASKED_VALUE``.

    ``emit()`` passes every line the script prints through this, under both
    rules, so a path, a context or an error message that holds a value is
    printed masked whichever rule found it. The text is read as written and
    decoded, as a file is, so an escaped value is masked where it is written.
    A bare number is not masked: it is not a family value, and masking the
    family's number wherever it stood, in a session number or a date, would
    print which number it is.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    def finder(reading: Reading) -> list[tuple[int, int, str, str]]:
        return family_hits_in_reading(reading, values)

    merged: list[tuple[int, int]] = []
    found = across_readings(text, finder)
    spans = sorted(reading.source_span(start, end) for reading, start, end, _label, _key in found)
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    shown, last = [], 0
    for start, end in merged:
        shown.append(text[last:start] + MASKED_VALUE)
        last = end
    return "".join(shown) + text[last:]


# --------------------------------------------------------------------------
# Exemptions
# --------------------------------------------------------------------------


@dataclass
class Ledger:
    """What each exemption row may still excuse, and what it has."""

    rows: tuple[tuple[str, str, str, int, str], ...]
    used: list[int]

    @classmethod
    def for_rows(cls, rows: Sequence[tuple[str, str, str, int, str]]) -> Ledger:
        return cls(tuple(rows), [0] * len(rows))

    def excuse(self, hit: Hit) -> bool:
        """Spend one use of the row that names ``hit``, when one is left."""
        matched = hit.label if hit.rule == "family" else hit.occurrence
        for index, (path, row_matched, context, count, _reason) in enumerate(self.rows):
            if (path, row_matched, context) == (hit.display_path, matched, hit.context):
                if self.used[index] < count:
                    self.used[index] += 1
                    return True
                return False
        return False

    def stale(self, scanned: set[str], rule: str, complete: bool = False) -> list[str]:
        """Return a message for each row left partly unused.

        A run given paths judges only the rows of files it read, because
        pre-commit passes only the files a commit changes. A ``complete`` run,
        one that walked every tracked file, also judges a row whose file it
        did not read: Git no longer tracks that file, or it is gone from the
        working tree, so the row excuses nothing and would come back into use
        if the same words came back.
        """
        messages = []
        for index, (path, matched, _context, count, _reason) in enumerate(self.rows):
            if self.used[index] >= count:
                continue
            what = f"a {matched} value" if rule == "family" else f'"{matched}"'
            if path in scanned:
                messages.append(
                    f"{path}: exemption row {index + 1} excuses {count} occurrence(s) of {what} "
                    f"and the file holds {self.used[index]} in those words. Remove the row, or "
                    "correct its count."
                )
            elif complete:
                messages.append(
                    f"{path}: exemption row {index + 1} excuses {count} occurrence(s) of {what} "
                    "in a file this walk did not read, because Git does not track it or it is not "
                    "in the working tree. Remove the row."
                )
        return messages


def exemption_row_lines(hits: Sequence[Hit], values: FamilyValues) -> list[str]:
    """Return a row, as Python source, for each distinct unexcused occurrence.

    The reason is left empty, and a row with no reason fails the data check,
    so a row pasted without one stops the run rather than excusing anything.
    No row is given for a family value in a path, nor for any row whose path
    or words hold a family value, under either rule: the row would spell the
    value, and the family rule would then fail this script.
    """
    counts: dict[tuple[str, str, str], int] = {}
    for hit in hits:
        matched = hit.label if hit.rule == "family" else hit.occurrence
        key = (hit.display_path, matched, hit.context)
        counts[key] = counts.get(key, 0) + 1
    rows = [
        f'    ({path!r}, {matched!r}, {context!r}, {count}, ""),'
        for (path, matched, context), count in counts.items()
    ]
    return [row for row in rows if redact(row, values) == row]


# --------------------------------------------------------------------------
# Files
# --------------------------------------------------------------------------


class FileReadError(RuntimeError):
    """Raised when a candidate file cannot be read."""

    def __init__(self, display_path: str, error: Exception) -> None:
        detail = getattr(error, "strerror", None) or str(error) or "I/O error"
        super().__init__(f"{display_path}: unable to read file ({type(error).__name__}: {detail})")


def path_is_junction(path: Path) -> bool:
    """Return whether ``path`` is a Windows junction, on any supported Python.

    ``Path.is_junction()`` arrived in Python 3.12; before it, the reparse tag
    answers the same question. ``st_reparse_tag`` exists only on Windows,
    where junctions exist, so its absence is a real ``False``.
    """
    checker = getattr(path, "is_junction", None)
    if checker is not None:
        return bool(checker())
    try:
        tag = getattr(path.lstat(), "st_reparse_tag", None)
    except (OSError, ValueError):
        return False
    return tag is not None and tag == getattr(stat, "IO_REPARSE_TAG_MOUNT_POINT", None)


def in_scope(rule: str, relative: str) -> bool:
    """Return whether ``rule`` reads the repository-relative path ``relative``."""
    if rule == "family":
        return not any(relative.startswith(prefix) for prefix in FAMILY_SKIPPED_PREFIXES)
    return any(relative.startswith(prefix) for prefix in DESTINATION_SCOPE_PREFIXES)


def lexical_relative(path_argument: str | Path, root: Path) -> str | None:
    """Return ``path_argument`` as a repository-relative POSIX path, without following links.

    ``None`` means the path does not lie under ``root`` as written.
    """
    path = Path(os.path.normpath(path_argument))
    if not path.is_absolute():
        return path.as_posix()
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return None


def resolve_candidate(path_argument: str | Path, root: Path) -> tuple[Path, str] | str:
    """Resolve a path to a file inside ``root``, or return why it is refused.

    A path is refused when it is a link, when it resolves outside ``root``,
    and when it passes through a linked folder: then Git's name for the file
    and the file actually read differ, and the file would be judged, and
    scoped, by a name that is not its own.
    """
    root = root.resolve()
    path = Path(path_argument)
    candidate = path if path.is_absolute() else root / path
    if candidate.is_symlink() or path_is_junction(candidate):
        return "a link"
    if not candidate.is_file():
        return "not a file"
    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return "outside the repository"
    lexical = lexical_relative(candidate, root)
    if lexical is None or os.path.normcase(lexical) != os.path.normcase(relative.as_posix()):
        return "through a linked folder"
    return resolved, relative.as_posix()


def tracked_files(root: Path) -> list[str]:
    """Return the repository-relative paths Git tracks under ``root``."""
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise FileReadError(str(root), OSError(f"git ls-files failed: {detail}"))
    return sorted(
        name for name in completed.stdout.decode("utf-8", "surrogateescape").split("\0") if name
    )


def tracked_submodules(root: Path) -> set[str]:
    """Return the repository-relative paths Git tracks as submodules (gitlinks) under ``root``."""
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-s", "-z"],
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise FileReadError(str(root), OSError(f"git ls-files failed: {detail}"))
    found = set()
    for entry in completed.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if entry:
            fields, _tab, name = entry.partition("\t")
            if fields.split(" ", 1)[0] == GITLINK_MODE:
                found.add(name)
    return found


#: The mode Git gives a submodule's entry in the index.
GITLINK_MODE = "160000"


def read_text(path: Path, display_path: str) -> str | None:
    """Return a file's text, or ``None`` for a binary file."""
    try:
        data = path.read_bytes()
    except OSError as error:
        raise FileReadError(display_path, error) from error
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise FileReadError(display_path, error) from error


# --------------------------------------------------------------------------
# Run
# --------------------------------------------------------------------------


#: What a candidate line asks of the reader, after where the number stands.
CANDIDATE_READ = "Read it in context; it is a leak only if it states the family's maximum trip length."


@dataclass
class Report:
    """What one run found."""

    hits: list[Hit]
    stale: list[str]
    checked: int
    candidates: list[str]


def scan(
    rule: str,
    targets: Sequence[tuple[Path, str]],
    root: Path,
    values: FamilyValues | None = None,
    exemptions: Sequence[tuple[str, str, str, int, str]] | None = None,
    list_candidates: bool = False,
    complete: bool = False,
) -> Report:
    """Scan resolved ``(path, display path)`` targets and apply the exemptions.

    Each target's path goes through the same loop as its text, as one more
    line of the file, so hits, excusing and candidates cover both; a binary
    file's path is read, and its bytes are skipped. ``complete`` says the
    targets are every tracked file the rule reads, so a row for a file not
    among them is stale.
    """
    if rule == "family" and values is None:
        values = FamilyValues.from_rows(FAMILY_VALUES)
    if exemptions is None:
        exemptions = FAMILY_EXEMPTIONS if rule == "family" else DESTINATION_EXEMPTIONS
    names = destination_names(root) if rule == "destination" else ()
    ledger = Ledger.for_rows(exemptions)
    unexcused: list[Hit] = []
    candidates: list[str] = []
    scanned: set[str] = set()
    checked = 0
    for path, display_path in targets:
        text = read_text(path, display_path)
        # The path is one more line of the file, read by the same loop as the
        # text, so a way of reading added here reads both. A binary file's
        # text is None, and only its path is read.
        for body, in_path in ((display_path, True), (text, False)):
            if body is None:
                continue
            for hit in find_hits(body, display_path, rule, values, names, in_path):
                # A family value in a path is never excused: its row would spell it.
                if (in_path and rule == "family") or not ledger.excuse(hit):
                    unexcused.append(hit)
            if list_candidates and values is not None:
                for line, column in bare_numbers(body, values):
                    where = (
                        f"{display_path}: a bare trip-length number in the file's path, at column {column}."
                        if in_path
                        else f"{display_path}:{line}:{column}: a bare trip-length number."
                    )
                    candidates.append(f"{where} {CANDIDATE_READ}")
        if text is None:
            continue
        checked += 1
        scanned.add(display_path)
    return Report(unexcused, ledger.stale(scanned, rule, complete), checked, candidates)


class ArgumentParser(argparse.ArgumentParser):
    """An argument parser whose error message goes through ``emit()``.

    Its error names the argument it could not read, and a file name passed by
    mistake as an option could hold a family value.
    """

    def error(self, message: str):  # type: ignore[override]
        mask = output_mask()
        if mask is None:
            emit(f"{self.prog}: error: {ARGUMENTS_WITHHELD}", NO_VALUES, error=True)
        else:
            emit(f"{self.prog}: error: {message}", mask, error=True)
        raise SystemExit(2)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = ArgumentParser(
        description=(
            "Check tracked files for this family's values (--rule family) or for "
            "destination names in framework files (--rule destination). With no "
            "paths, checks every tracked file the rule reads."
        )
    )
    parser.add_argument("paths", nargs="*", help="Files passed by pre-commit.")
    parser.add_argument("--rule", choices=RULES, help="Which rule to run.")
    parser.add_argument(
        "--hash",
        choices=KINDS,
        dest="hash_kind",
        help="Read one value of this kind from standard input and print its FAMILY_VALUES rows.",
    )
    parser.add_argument(
        "--candidates",
        action="store_true",
        help="With --rule family, list each bare trip-length number for a hand-read, and exit 0.",
    )
    parser.add_argument(
        "--exemption-rows",
        action="store_true",
        help="Print an exemption row for each unexcused occurrence, and exit 0.",
    )
    return parser.parse_args(argv)


def print_hash_rows(kind: str) -> int:
    value = sys.stdin.read().strip()
    try:
        forms = normalize_value(kind, value)
    except ValueError as error:
        print(f"--hash {kind}: {error}", file=sys.stderr)
        return 1
    for form in forms:
        print(f'    ("{kind}", {len(form.split(" "))}, "{value_digest(kind, form)}"),')
    return 0


def output_mask() -> FamilyValues | None:
    """Return the values every printed line is masked with, or ``None`` while a value row is malformed.

    A row the data check rejects masks nothing, whichever part of it is
    wrong, so while one stands no line that holds repository text prints:
    both rules stop, and an argument error or a crash prints a fixed line in
    place of its message.
    """
    if check_family_values(FAMILY_VALUES):
        return None
    return FamilyValues.from_rows(FAMILY_VALUES)  # type: ignore[arg-type]


#: The mask for a line that holds no repository text.
NO_VALUES = FamilyValues.from_rows(())
#: What an argument error prints in place of its message while a value row is malformed.
ARGUMENTS_WITHHELD = (
    "the arguments could not be read. The message is withheld, since a malformed FAMILY_VALUES row "
    "leaves it unmasked; run with --rule family to see the row"
)


def emit(text: str, values: FamilyValues, error: bool = False) -> None:
    """Print one line of output with every family value in it masked.

    Every line a rule prints goes through here, under both rules: a hit, a
    stale row, a refusal, an error, a candidate and an exemption row. The
    suite fails if any other function but ``print_hash_rows`` calls
    ``print``.
    """
    print(redact(text, values), file=sys.stderr if error else sys.stdout)


#: What prints when even the masked crash line cannot be built.
CRASH_UNMASKABLE = "check-leaks.py: an unexpected error stopped the run, and its message could not be masked"


def crash_line(error: BaseException) -> str:
    """Return one line naming an unexpected error: its type, where in this script, and its message.

    ``emit()`` masks it. No traceback is printed: its frames hold paths and
    text that ``emit()`` would have to mask line by line.
    """
    here = Path(__file__).resolve()
    frames = [frame for frame in traceback.extract_tb(error.__traceback__) if Path(frame.filename).resolve() == here]
    where = f" in {frames[-1].name}(), line {frames[-1].lineno}" if frames else ""
    message = " ".join(str(error).split())
    return f"check-leaks.py: an unexpected error stopped the run{where}: {type(error).__name__}: {message}"


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run one rule, and return the exit status.

    An unexpected error prints one masked line and exits 2, with no
    traceback, since a traceback's paths and text could hold a family value.
    """
    try:
        return run(argv, root)
    except Exception as error:  # noqa: BLE001 - every failure must stay masked
        try:
            mask = output_mask()
            if mask is None:
                emit(CRASH_UNMASKABLE, NO_VALUES, error=True)
            else:
                emit(crash_line(error), mask, error=True)
        except Exception:  # noqa: BLE001 - the masking itself failed, so print nothing from the error
            emit(CRASH_UNMASKABLE, NO_VALUES, error=True)
        return 2


def run(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run one rule, and return the exit status. ``main()`` guards it."""
    args = parse_args(argv)
    if args.hash_kind:
        return print_hash_rows(args.hash_kind)
    # A malformed value row stops both rules before either prints: every
    # line is masked with these values, and a row the check rejects masks
    # nothing.
    errors = check_family_values(FAMILY_VALUES)
    if errors:
        for error in errors:
            emit(error, NO_VALUES, error=True)
        return 1
    values = FamilyValues.from_rows(FAMILY_VALUES)  # type: ignore[arg-type]
    if args.rule is None:
        emit("choose a rule with --rule family or --rule destination", values, error=True)
        return 2
    if args.candidates and args.rule != "family":
        emit("--candidates lists trip-length numbers, so it needs --rule family", values, error=True)
        return 2

    exemptions = FAMILY_EXEMPTIONS if args.rule == "family" else DESTINATION_EXEMPTIONS
    errors = check_exemption_rows(args.rule, exemptions)
    if errors:
        for error in errors:
            emit(error, values, error=True)
        return 1

    root = root.resolve()
    walked = not args.paths
    targets: list[tuple[Path, str]] = []
    refused: list[str] = []
    try:
        tracked = tracked_files(root)
        submodules = tracked_submodules(root)
    except FileReadError as error:
        emit(str(error), values, error=True)
        return 1
    tracked_set = set(tracked)
    arguments: Iterable[str] = tracked if walked else args.paths
    for argument in arguments:
        name = lexical_relative(argument, root)
        if name is None or name not in tracked_set:
            # A path Git does not track is not this repository's content,
            # whether it resolves or not, so it is neither read nor refused.
            continue
        if not in_scope(args.rule, name):
            continue
        if name in submodules:
            # A submodule's content is another repository, which this run
            # cannot read, so it is refused by name, as a link is.
            refused.append(f"{argument} (a submodule)")
            continue
        resolved = resolve_candidate(argument, root)
        if isinstance(resolved, str):
            # A tracked, in-scope path that is a link, goes through a linked
            # folder or resolves outside the repository is refused by name,
            # whether a walk found it or pre-commit passed it. A file deleted
            # from the working tree is not content any more.
            if resolved != "not a file":
                refused.append(f"{argument} ({resolved})")
            continue
        if in_scope(args.rule, resolved[1]):
            targets.append(resolved)
    if refused:
        emit(
            "these tracked paths are links or submodules, go through a linked folder, or resolve "
            "outside the repository, so this run refuses to report on them: " + ", ".join(refused[:5]),
            values,
            error=True,
        )
        return 1
    if walked and not targets:
        emit(
            f"no tracked file is in the {args.rule} rule's scope, so this run checked nothing. "
            "Check the working directory.",
            values,
            error=True,
        )
        return 1

    family_values = values if args.rule == "family" else None
    try:
        report = scan(args.rule, targets, root, family_values, list_candidates=args.candidates, complete=walked)
    except FileReadError as error:
        emit(str(error), values, error=True)
        return 1

    if args.candidates:
        for line in report.candidates:
            emit(line, values)
        return 0
    if args.exemption_rows:
        for line in exemption_row_lines(report.hits, values):
            emit(line, values)
        return 0

    for hit in report.hits:
        emit(hit.format_message(), values)
    for message in report.stale:
        emit(message, values)
    if walked and not report.hits and not report.stale:
        emit(f"{args.rule.capitalize()} leaks: {report.checked} file(s) checked, none found.", values)
    return 1 if report.hits or report.stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
