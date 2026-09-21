<!-- markdownlint-disable MD013 -->

# The Framework

This folder is the reusable half of the project. It holds the curriculum a child works through and everything an adult needs to run it. What it does not hold is facts about any particular place, or any one family's answers.

New here? [The overview](docs/overview.md) is the page to read first.

## The three layers

The project is built in three layers, and each has a different lifecycle.

1. **The framework** is the reusable curriculum: the guides, the blank templates, the generic session skeletons, the executive-function rationale and the roadmap logic. It is written once and then reused by every family and every destination. It holds no destination facts and no trip data, except in the later-phase sessions named on the leak-exemption list, one of which still carries the first destination's facts until a later batch converts it.
2. **A destination knowledge pack**, one per place. It holds the stable facts about that place, plus the short "destination notes" inserts that the generic sessions pull in. A pack is written once for a destination and reused across any number of trips there.
3. **A trip**, one per trip. This is one family's filled-in work, and it is **never committed**. The family copies a blank trip starter kit out of the repository and fills it in a binder or a Google Docs folder.

Only the first two layers live in this repository. The third one is yours, and it stays with you.

## Curriculum version

**Curriculum version: 0.2.0.** What changed between revisions is in the [curriculum changelog](CHANGELOG.md).

Which log is which: the curriculum changelog is the version history of these reusable materials, and it is committed here. A **decision log** is a record of one family's trip decisions, it lives in their own binder or Docs folder, and it is never committed. If you are using the curriculum, the decision log is yours and the changelog is not.

## What "reusable" means here

Done, for modularity, means this: a family can copy the blank kit and a destination pack, fill in their own Trip-Basics card, write a new destination's reference facts and inserts, and reuse the whole curriculum unchanged, without editing any framework file and without editing the first destination.

Two bounds sit on that promise today. They clear on different events, so neither one retires the other.

**The first is the leak-exemption list**, and a later batch clears it. Five already-built later-phase sessions are on it. One of them still names the first destination and links into its pack, so that one session has to be converted by hand before a second destination is finished. The other four carry no destination fact at all; they are on the list only because nobody has verified them yet. So the count of framework files a second destination forces you to edit is one, and four more get read.

**The second is the shape of the destination**, and only a decision clears it. The pack contract assumes a destination that is a country. A second destination that is a country needs no framework edit beyond that one session. For a city, a region, or a route across several countries, the pack slots that assume a country have no settled meaning yet, and somebody has to answer that before a pack of that shape can be finished.

## Two kinds of reuse

Two different things both get called reuse, and they cost very different amounts.

- **Parameter reuse.** Another family with the same origin assumptions, travelling to the same destination, changes only their own Trip-Basics card. Near-zero cost, and it is the reuse most families are after. "The same origin assumptions" is carrying weight in that sentence: the origin logistics layer below lists what a family travelling from somewhere else swaps.
- **Destination reuse.** Another place needs a whole new destination pack: its reference facts, its session inserts, its word list. That is a project rather than an edit, and it is the only thing the heavier machinery exists for.

One further boundary belongs beside that promise. Everything here assumes English-literate adults and a child who reads English or is read to in English. Every session, worksheet, template and guide is written in English, and nothing in this repository translates them. A family who does not read English, or a child who does not read and has nobody to read to them, needs translation and reading support this project does not build and does not plan to.

## The origin logistics layer

A fourth thing this repository names but does not build separately: the **origin logistics layer**. Passport rules, the home airport, the U.S. Department of State reference, and the currency the budget pages are written in all assume a family travelling from the United States.

A family travelling from elsewhere swaps three things in the framework:

- The passport authority named in Session 00 and in the parent guide.
- The home-airport and time-zone fields on the Trip-Basics card, together with the two sentences of adult help beside them, which name US time zones and daylight saving.
- The home currency on the budget surfaces. The rough budget band on the current family travel assumptions page, the budget estimate template, and the first-pass budget session all write amounts with a dollar sign. Swap the symbol for your own currency; nothing else on those pages changes.

The destination pack carries the same assumption in its own layer. A pack's child word list and its money reference convert prices into US dollars, the word list gives Fahrenheit and miles beside the local units, and its trusted-sources list names a US government travel page as the adult-owned entry and safety source. A pack written for a family from somewhere else converts into that family's money and units, and names that family's own government page instead.

Beyond the origin logistics layer, nothing in the framework assumes an origin country.

## Where everything is

- [How to start a trip](how_to_start_a_trip.md) is the four steps a family begins with.
- [How to use Markdown files](docs/how_to_use_markdown_files.md) is for a reader who has not opened a Markdown file before.
- [Project roadmap](PROJECT_ROADMAP.md) holds the three paths and the honest stopping points.
- [Parent guide](parent_guide/README.md) and [student guide](student_guide/README.md) are the two reading toolkits.
- [Trip starter kit](trip_starter/README.md) holds the blanks a family copies out.
- `framework/templates/` holds the blank forms the sessions use, and `framework/sessions/` holds the sessions themselves.
- `framework/docs/` holds this folder's reference pages: [overview](docs/overview.md), [design principles](docs/design_principles.md), [source trustworthiness](docs/source_trustworthiness.md), [citation style](docs/citation_style.md), [AI use rules](docs/ai_use_rules.md), the [framework glossary](docs/glossary.md), [privacy and safety](docs/privacy_and_safety.md), and [build style and vocabulary](docs/build_style_and_vocab.md) for whoever authors a batch.
- The destination packs sit in their own top-level `destinations` folder, one folder per place. Send a family to the pack for where they are going. This page holds no facts about any destination, by design.
