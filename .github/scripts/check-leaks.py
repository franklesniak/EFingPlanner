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
does not hide a letter, and a word that follows a backslash escape such as
the word boundary in a grep pattern is read without the escape's letter.

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

  A spelled-out number from one to ninety-nine counts as its digits. A
  number that is part of a decimal or a thousands group is not a match. A
  bare number is not a leak: the design record's grep note lists page
  numbers, item counts and dates as the wider pattern's false positives, and
  the Batch 2 build brief scopes this hook to the number with its unit. The
  label and the cap phrase state the trip length as plainly as a unit does.
  ``--candidates`` lists the bare occurrences for the grep note's hand-read,
  and does not fail. A word between the number and its unit ("N full
  days"), and a cap with no unit or label ("the trip cannot go past N"), are
  left to that hand-read.
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
row whose occurrences have gone is reported as stale, so a row cannot
outlive its reason. ``--exemption-rows`` prints a row for each unexcused
match, for a maintainer to review and paste in with a reason.

File access
-----------
Only files inside the repository are read. With no paths, the run walks the
files Git tracks and refuses a symbolic link, a junction, or a path that
resolves outside the repository, by name. When pre-commit passes paths, such
a path is skipped. A file holding a zero byte is binary and is skipped, as
Git treats it. A file that cannot be read as UTF-8 stops the run, because a
file that was not read has not been checked.

In place of a hand-run grep
---------------------------
A grep for the family's values has to name them, so the grep itself leaks
them: into the file that holds it, the shell's history and its output. This
script is the replacement. A build brief or a checklist that asks for the
leak greps runs these calls instead, and they name no value and print none:

* ``python .github/scripts/check-leaks.py --rule family``, which exits 1 and
  prints each unexcused occurrence as a path, line, column and kind;
* ``python .github/scripts/check-leaks.py --rule family --candidates``, the
  grep note's hand-read of bare numbers, which lists positions and exits 0;
* ``python .github/scripts/check-leaks.py --rule destination``.

A grep for a destination name, for a path into ``destinations/`` or for a
spec section number names nothing private, and may stay a grep.

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
import re
import stat
import subprocess
import sys
import unicodedata
import urllib.parse
from collections.abc import Iterable, Sequence
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
SESSION_15_UNTIL_CONVERTED = (
    "Temporary: Session 15 is on the style law's leak-exemption list until the Batch 2 build converts "
    "it (docs/build/batch2_build_prompt.md, section 4.1b). Once the conversion lands, the hook reports "
    "this row as stale until it is removed."
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
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "japan",
        "the [major cities reference](../../../destinations/japan/reference/major_cities.md), two blank [City",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Japan",
        "Research two Japan cities, one card",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Tokyo",
        "City Research Card. Tokyo is a great",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Tokyo",
        "Pick **two** cities: Tokyo is a strong",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "japan",
        "(the [major cities reference](../../../destinations/japan/reference/major_cities.md) lists good candidates",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Kyoto",
        "good candidates like Kyoto and Osaka).",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Osaka",
        "like Kyoto and Osaka).",
        1, SESSION_15_UNTIL_CONVERTED,
    ),
    (
        "framework/sessions/phase_03_choose_places/15_city_research_cards.md", "Tokyo",
        "Keep Tokyo as a gentle",
        1, SESSION_15_UNTIL_CONVERTED,
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
#: underscore may stand before it, as Markdown's emphasis mark.
NUMBER_START = r"(?<![^\W_]|[.,])"
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


def number_value(text: str) -> str:
    """Return a matched number as the digits a number value is hashed from."""
    if text.isdigit():
        return str(int(text))
    return str(spelled_to_int(text))


def fold(text: str) -> str:
    """Return ``text`` in the compatibility form a word value is compared in."""
    return unicodedata.normalize("NFKC", text).casefold()


@functools.lru_cache(maxsize=None)
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
        if text.isdigit():
            return [str(int(text))]
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
        if kind not in KINDS:
            errors.append(f"FAMILY_VALUES row {number} names the kind {kind!r}")
        if not isinstance(words, int) or isinstance(words, bool) or not 1 <= words <= MAX_VALUE_WORDS:
            errors.append(f"FAMILY_VALUES row {number} gives {words!r} words; it is 1 to {MAX_VALUE_WORDS}")
        elif kind != "word" and words != 1:
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

    def format_message(self) -> str:
        where = f"{self.display_path}:{self.line_number}:{self.column}"
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


class Reading:
    """One reading of a file: its text, and where each line starts."""

    def __init__(self, text: str) -> None:
        self.text = text
        self.line_starts = [0] + [index + 1 for index, character in enumerate(text) if character == "\n"]

    def position(self, offset: int) -> tuple[int, int]:
        line = bisect.bisect_right(self.line_starts, offset)
        return line, offset - self.line_starts[line - 1] + 1


#: A backslash escape that can stand right before a word or a number: a
#: regular expression's word boundary, or a line break, tab or other control
#: escape. Read as written, its letter joins the word or starts it.
ESCAPE_BEFORE_WORD = re.compile(r"\\[bBnrtfv](?=[^\W_])")


def readings(text: str) -> list[Reading]:
    """Return the file as written and, when it holds an escape, decoded.

    The decoded reading keeps one line for each line, so its line numbers are
    the file's. A decoded line break becomes a space, and so does a backslash
    escape before a letter or a digit.
    """
    found = [Reading(text)]
    if "&" in text or "%" in text or "\\" in text:
        lines = []
        for line in text.split("\n"):
            if "&" in line or "%" in line or "\\" in line:
                line = urllib.parse.unquote(html.unescape(line))
                line = ESCAPE_BEFORE_WORD.sub(" ", line)
                line = re.sub(r"[\r\n\u2028\u2029\x0b\x0c\x1c-\x1e\x85]", " ", line)
            lines.append(line)
        decoded = "\n".join(lines)
        if decoded != text:
            found.append(Reading(decoded))
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


def find_hits(
    text: str,
    display_path: str,
    rule: str,
    values: FamilyValues | None = None,
    names: Sequence[tuple[str, ...]] = (),
) -> list[Hit]:
    """Return every occurrence ``rule`` reports in ``text``, before exemptions.

    The file is read as written and, when it holds an escape, decoded. A hit
    the decoded reading adds is kept only beyond the count the plain reading
    already found for the same value on the same line.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    hits: list[Hit] = []
    counted: dict[tuple[int, str], int] = {}
    for reading_number, reading in enumerate(readings(text)):
        seen_here: dict[tuple[int, str], int] = {}
        if rule == "family":
            assert values is not None
            raw = family_hits_in_reading(reading, values)
        else:
            raw = destination_hits_in_reading(reading, names)
        for start, end, label, value_key in sorted(raw):
            line, column = reading.position(start)
            key = (line, value_key)
            seen_here[key] = seen_here.get(key, 0) + 1
            if reading_number and seen_here[key] <= counted.get(key, 0):
                continue
            context = occurrence_context(reading.text, start, end)
            if rule == "family":
                occurrence = ""
                context = value_digest("context", context)
            else:
                occurrence = reading.text[start:end]
            hits.append(
                Hit(rule, display_path, line, column, label, occurrence, context, value_key)
            )
        if not reading_number:
            counted = seen_here
    hits.sort(key=lambda hit: (hit.line_number, hit.column))
    return hits


def bare_numbers(text: str, values: FamilyValues) -> list[tuple[int, int]]:
    """Return ``(line, column)`` for each bare trip-length number, for a hand-read.

    A number the family rule already reports, with its unit, is left out.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    reading = Reading(text)
    numbers = values.digests["number"]
    reported = {number_start for _start, _end, number_start, _digest in trip_lengths(text, numbers)}
    found = []
    for match in BARE_NUMBER.finditer(text):
        if match.start() in reported:
            continue
        if value_digest("number", number_value(match.group("number"))) in numbers:
            found.append(reading.position(match.start()))
    return found


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

    def stale(self, scanned: set[str], rule: str) -> list[str]:
        """Return a message for each row of a scanned file left partly unused."""
        messages = []
        for index, (path, matched, _context, count, _reason) in enumerate(self.rows):
            if path in scanned and self.used[index] < count:
                what = f"a {matched} value" if rule == "family" else f'"{matched}"'
                messages.append(
                    f"{path}: exemption row {index + 1} excuses {count} occurrence(s) of {what} "
                    f"and the file holds {self.used[index]} in those words. Remove the row, or "
                    "correct its count."
                )
        return messages


def exemption_row_lines(hits: Sequence[Hit]) -> list[str]:
    """Return a row, as Python source, for each distinct unexcused occurrence.

    The reason is left empty, and a row with no reason fails the data check,
    so a row pasted without one stops the run rather than excusing anything.
    """
    counts: dict[tuple[str, str, str], int] = {}
    for hit in hits:
        matched = hit.label if hit.rule == "family" else hit.occurrence
        key = (hit.display_path, matched, hit.context)
        counts[key] = counts.get(key, 0) + 1
    return [
        f'    ({path!r}, {matched!r}, {context!r}, {count}, ""),'
        for (path, matched, context), count in counts.items()
    ]


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


def resolve_candidate(path_argument: str | Path, root: Path) -> tuple[Path, str] | str:
    """Resolve a path to a file inside ``root``, or return why it is refused."""
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
) -> Report:
    """Scan resolved ``(path, display path)`` targets and apply the exemptions."""
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
        if text is None:
            continue
        checked += 1
        scanned.add(display_path)
        for hit in find_hits(text, display_path, rule, values, names):
            if not ledger.excuse(hit):
                unexcused.append(hit)
        if list_candidates and values is not None:
            for line, column in bare_numbers(text, values):
                candidates.append(
                    f"{display_path}:{line}:{column}: a bare trip-length number. Read it in "
                    "context; it is a leak only if it states the family's maximum trip length."
                )
    return Report(unexcused, ledger.stale(scanned, rule), checked, candidates)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
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


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run one rule, and return the exit status."""
    args = parse_args(argv)
    if args.hash_kind:
        return print_hash_rows(args.hash_kind)
    if args.rule is None:
        print("choose a rule with --rule family or --rule destination", file=sys.stderr)
        return 2
    if args.candidates and args.rule != "family":
        print("--candidates lists trip-length numbers, so it needs --rule family", file=sys.stderr)
        return 2

    errors = check_family_values(FAMILY_VALUES) if args.rule == "family" else []
    exemptions = FAMILY_EXEMPTIONS if args.rule == "family" else DESTINATION_EXEMPTIONS
    errors += check_exemption_rows(args.rule, exemptions)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    root = root.resolve()
    walked = not args.paths
    targets: list[tuple[Path, str]] = []
    refused: list[str] = []
    try:
        arguments: Iterable[str] = tracked_files(root) if walked else args.paths
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1
    for argument in arguments:
        if walked and not in_scope(args.rule, argument):
            continue
        resolved = resolve_candidate(argument, root)
        if isinstance(resolved, str):
            # A walk refuses a link and a path outside the repository by name.
            # A tracked file deleted from the working tree is not content any
            # more, and pre-commit's own paths are skipped when refused.
            if walked and resolved != "not a file":
                refused.append(f"{argument} ({resolved})")
            continue
        if in_scope(args.rule, resolved[1]):
            targets.append(resolved)
    if walked and refused:
        print(
            "these tracked paths are links or resolve outside the repository, so this run "
            "refuses to report on them: " + ", ".join(refused[:5]),
            file=sys.stderr,
        )
        return 1
    if walked and not targets:
        print(
            f"no tracked file is in the {args.rule} rule's scope, so this run checked nothing. "
            "Check the working directory.",
            file=sys.stderr,
        )
        return 1

    try:
        report = scan(args.rule, targets, root, list_candidates=args.candidates)
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1

    if args.candidates:
        for line in report.candidates:
            print(line)
        return 0
    if args.exemption_rows:
        for line in exemption_row_lines(report.hits):
            print(line)
        return 0

    for hit in report.hits:
        print(hit.format_message())
    for message in report.stale:
        print(message)
    if walked and not report.hits and not report.stale:
        print(f"{args.rule.capitalize()} leaks: {report.checked} file(s) checked, none found.")
    return 1 if report.hits or report.stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
