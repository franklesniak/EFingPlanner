<!-- markdownlint-disable MD013 -->
<!-- audience: parent -->

# How to Add a Destination

To use this curriculum for a country that has no pack yet, you build a destination pack for it. You add the new pack's files, and every framework file and the existing pack stay as they are.

This page is for the adult who builds the pack. It says what a pack covers, lists the steps, and ends with how to share a finished pack.

## What a pack is, and what it covers

A destination pack holds the reference facts and the short Destination Notes for one country. The sessions are written for any destination. When a session needs a fact about a place, it sends the child to the pack.

A trip to a city or a region inside a country uses that country's pack. The sessions still say "your destination", and the child narrows the trip down as they go. So a pack's snapshot notes name the country's capital, and its candidate cities are cities in that country.

**Open Question:** what a trip across several countries does is not settled. Each session opens one pack's Destination Notes, and nothing yet says how one trip would use two packs. The next step belongs to the first maintainer or reusing family who wants a trip across several countries: settle how a trip uses two packs, write the answer into this page and into the routing contract, and record it in the [curriculum changelog](CHANGELOG.md). Until then, nothing waits on it. No answer is owed by any date, and it blocks no pack for a single country. The [framework README](README.md) names the same bound.

The existing pack is written for a family traveling from the United States. It converts prices into US dollars and names a US government page for entry and safety. Write your pack for the family who will use it. The framework README's [origin logistics layer](README.md#the-origin-logistics-layer) says what that changes.

## The routing contract

The routing contract is the rulebook a pack is built to. It says which session reads which pack file, what fields each Destination Notes slot must supply, and how a slot divides from its reference file. Every pack carries its own copy, at `destinations/<pack>/session_inserts/README.md`. Open that file in the existing pack before you start, and keep it open while you work. Where this page and the contract differ, the contract wins.

The [cross-reference map](cross_reference_map.md) mirrors the contract's routing rows from the framework side, with every pack file named generically.

## The steps

Work in your own copy of this repository, such as a fork on GitHub or a downloaded copy on your computer. Every page is a plain Markdown file; [how to use these Markdown files](docs/how_to_use_markdown_files.md) explains the format. Do the steps in order, and copy every filename exactly as the contract writes it. For the shape of each new page, look at the matching page in the existing pack.

1. **Make the pack's folder and its two contents pages.** Make one folder for your country under `destinations/`, written here as `destinations/<pack>/`. Its `README.md` is the pack's contents page. Start it from a copy of the existing pack's contents page. Keep the first two lines, the provided-as-is banner and the hidden note just above the banner, and replace the rest with your own list of reference files and Destination Notes. A hidden note is a line that starts with `<!--`: a reader never sees it, and the repository's checks read it. Then copy the routing contract whole into `destinations/<pack>/session_inserts/README.md`, and change its **Last Updated** line to the day you make the copy. The contract's own notes say what else to change in your copy, starting with the four bullets that count what the pack has written.
2. **Write each reference file the contract names.** They go in `destinations/<pack>/reference/`, one file per topic, each named as the contract's reference column names it: regions, major cities, seasons, weather and events, transportation, airports, money, language, etiquette, food, adult logistics, safety and emergency, the access and pricing watch, trusted starting sources, and sample search terms. Put one `**Last reviewed:** <month year>` line directly below each file's title, with the month written out, such as `**Last reviewed:** September 2026`. It's an honesty stamp: the month someone last checked the page against its sources. Checking again later is optional upkeep. Write these pages for a child of roughly 9 to 11, in short sentences and everyday words, because the repository's reading-level check scores them. Step 5 names the one exception.
3. **Write each Destination Notes slot to the contract's schema.** The slots go in `destinations/<pack>/session_inserts/`, one file for each slot the contract names. Give each slot every field its row lists, and follow the contract's rule for what stays in the reference file. Each slot carries its own `Last reviewed` line too, and each is written for the child, like the reference files.
4. **Put every fact in your own pack.** If a session seems to need a change for your country, the fact goes in your pack, in the slot or reference file the contract routes that session to. The framework files and the other packs stay as they are.
5. **Keep adult-owned topics adult-owned.** Entry rules, money, booking and safety planning are for the grown-ups. The adult logistics reference is written for them throughout. Keep the hidden note `<!-- audience: adult -->` as its second line, as the existing pack's adult logistics reference has it, so the checks read it as an adult page. On a page that is mostly for the child, such as the safety and emergency reference, put the grown-ups' part last, under a heading that reads "For parents".
6. **Write every fast-changing fact as something to verify.** Prices, hours, entry rules and ticketing change. Write each one with the three parts of the Verify-Don't-Trust rule: check with official sources close to travel, record the date you checked, and adults verify before booking. The rule's home is the [source trustworthiness](docs/source_trustworthiness.md) page.
7. **Call the pack done when every file is written and filled.** The destination is added when both contents pages exist and every insert slot and every reference file the contract names is filled, with no placeholder notes left in any of them.

A family then uses the new pack the way [how to start a trip](how_to_start_a_trip.md) describes.

## Sharing a destination pack

This project is shared by one family, and nobody is on call to review or maintain it. This section describes how sharing could work if someone ever takes that on. It makes no promise of review, triage or a reply.

**To offer a pack,** open an issue or a pull request on this repository, with the pack in its own folder under `destinations/<pack>/`. A pull request also runs this repository's automatic checks on the new pages.

**A pack ready to share meets every step on this page.** Two more things go with it. Write etiquette and culture matter-of-factly and respectfully, the way one neighbor describes a custom to another. And keep family data out of the whole pack: no home airport, no names, no booked dates and no budget figures.

**To flag a stale fact,** open an issue that names the file and what changed. Checking it again depends on someone volunteering to do it.
