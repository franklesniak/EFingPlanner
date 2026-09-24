<!-- markdownlint-disable MD013 -->
<!-- audience: builder -->

# Session Inserts: Contract and Add-a-Destination Checklist

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-24
- **Scope:** The destination-pack routing contract. It says which session pulls which insert, which reference files each session points to, what fields every insert slot has to supply, and what it takes to add a new destination pack. It holds routing rather than facts, so it carries no `Last reviewed` stamp.
- **Related:** [Destination pack contents](../README.md)

This file is for whoever builds a destination pack or adds one. The pack's [contents page](../README.md) carries the provided-as-is framing every family reading the pack needs: the facts come from one family, nobody is on call to keep them current, and anything a family relies on gets verified against official sources close to travel.

## The insert and reference contract

This table routes every session that needs place facts to the pack, in session order. The rule under the table says how each session writes its pointer.

| Session | Insert it pulls (`session_inserts/`) | Reference file(s) it points to (`reference/`) |
| --- | --- | --- |
| 05 Good Sources, Bad Sources | none | `trusted_starting_sources.md` |
| 06 Book Research With a Guidebook | none | `trusted_starting_sources.md` (the recommended guidebook) |
| 08 Web Research Practice | none | `trusted_starting_sources.md`, `sample_search_terms.md` |
| 10 Destination Snapshot | `10_snapshot_facts.md` | none |
| 11 Regions and Cities Overview | `11_regions_overview.md` | `regions_overview.md`, `major_cities.md` |
| 12 Weather, Seasons, and Events | `12_seasons_and_events.md` | `seasons_weather_events.md` |
| 16-18 Deep-Dive Cities | `16_18_candidate_cities.md` | `major_cities.md` |
| 19 Other Places Research | `19_other_places_menu.md` | `major_cities.md` |
| 23 Attraction Research Cards | `23_attraction_ideas.md` | `food_basics.md` (for food-type attractions) |
| 30 Trains, Transit, and IC Cards | `30_transport_specifics.md` | `transportation_basics.md` |
| 38 Daily Cost Estimates | none | `money_basics.md` (cash culture, currency) |
| 34 Neighborhoods and Hotel Location | `34_lodging_types.md` | `adult_logistics.md` (occupancy reality) |
| 36-37 Food / Restaurant Shortlist | `36_37_food_ideas.md` | `food_basics.md` |
| 40 Realistic Day Planning | none | `airports_and_arrival_basics.md` (airport-to-city) |
| 42 Reservations and Timed Entries | `42_reservation_examples.md` | none |
| 43 Rest Days, Jet Lag, and Pacing | none | `transportation_basics.md` (walking/stairs) |
| 47 Language and Etiquette | `47_language_etiquette.md` | `language_basics.md`, `etiquette_basics.md` |
| 48 Packing List | none | `seasons_weather_events.md` (seasonal packing) |
| (child travel glossary, all sessions) | `kid_glossary.md` | none |

**Which column a row fills decides how its session writes.** A row with an insert means the session writes the exact phrase *"open this session's Destination Notes"*, and that phrase resolves to the insert. A row whose Insert column reads `none` means the session names the reference in the pack's own words instead, because there is no insert for the phrase to resolve to. Sessions 05, 06 and 08 are that second kind.

Every filename in that table is written as inline code and never as a relative link. Most of the slots and several of the reference files do not exist in any pack yet, so a link to one would dangle and fail the repository's link check. Whichever batch or pack author writes a target adds the link then.

Sessions not in this table (00-04, 07, 09, 13-15, 20-22, 24-29, 31-33, 35, 39, 41, 44-46, 49-54) need no destination facts and are fully neutral -- 54 included, the optional post-trip session, in which the child compares what they predicted against what actually happened on the real trip and names no place. One exception holds until Batch 2: Session 15 needs no destination facts either, but it is not yet neutral in the tree -- it still names the first destination and links into that destination's major cities reference. Converting it is a Batch 2 deliverable; until then, adding a destination means converting that one session by hand. A session can be routed to a pack file without naming a place in its own wording: Sessions 05 and 08 name no place but open the pack's starting-sources list, and Session 38 takes its currency and cash-culture facts from the pack's money reference. Every such pointer is a row in the table above.

## What each insert slot supplies

Every field list below is written destination-neutrally, so this contract copies into a second pack unchanged. A destination's own values belong in the slot files.

| Slot | Consuming session | Fields it must supply |
| --- | --- | --- |
| `10_snapshot_facts.md` | 10 Destination Snapshot | Capital; major land features; currency; main language. Not the time-difference figure -- that is a Trip-Basics card value. |
| `11_regions_overview.md` | 11 Regions and Cities Overview | The regions the pack plans a first trip around, named, with one line saying the destination has more, so the child can start their region notes; then a pointer to the pack's regions reference for how each region feels different and for the geography instances the neutral session may not state -- your destination's shape and size, how weather differs by region, why travel time between regions matters -- and a pointer to the pack's major-cities reference for the route shapes. That regions reference is their canonical home; do not restate them in the slot. No trip shapes, no costs, no pinned travel times. |
| `12_seasons_and_events.md` | 12 Weather, Seasons, and Events | Each season the destination has, named, so the child can label a season chart, with one short line each on what traveling in it is like; then a pointer to the pack's seasons, weather and events reference for the rest -- the big-draw and busiest periods, the congestion windows named as categories to confirm this year, each seasonal hazard with its pacing consequence, and the adult-facing contingency note. That reference is their canonical home; do not restate them in the slot. No pinned dates, prices or forecasts. |
| `16_18_candidate_cities.md` | 16-18 Deep-Dive Cities | Two to four first-trip candidate cities, each with a one-line draw, so the child can start a card per city; then a pointer to the pack's major-cities reference for the kid-magnet ideas and for anything whose opening or availability changes. That reference is their canonical home; do not restate them in the slot. Candidates to research, never a shortlist. |
| `19_other_places_menu.md` | 19 Other Places Research | A menu of further candidate places beyond the deep-dive cities, each with a one-line draw, offered as options to research rather than as a shortlist. Where the pack's major-cities reference already carries that menu, point at it instead of copying it; that reference is their canonical home. |
| `23_attraction_ideas.md` | 23 Attraction Research Cards | Starter attraction ideas as options to research, mixing high-draw named attractions with low-cost everyday ones, each with what kind of visit it is; anything ticketed, timed or permit-gated flagged "verify." No prices, no hours. |
| `30_transport_specifics.md` | 30 Trains, Transit, and IC Cards | The transport modes a child plans around, named (long-distance, local, walking, taxis), so the child can sort a day's travel; then a pointer to the pack's transportation reference for the rest -- the stored-value or travel-card options and whether a visitor can get one now, luggage forwarding and station lockers, any pass whose value depends on the itinerary, and a route-planning tool that works today. That reference is their canonical home; do not restate them in the slot. No fares, no pinned journey times. |
| `34_lodging_types.md` | 34 Neighborhoods and Hotel Location | The lodging categories a family chooses among, one line each, so the child can sort a night's options; then a pointer to the pack's adult-logistics reference for the occupancy reality -- how many people a room holds, and what a larger party has to plan around. That reference is their canonical home; do not restate it in the slot. No prices, no named properties. |
| `36_37_food_ideas.md` | 36-37 Food / Restaurant Shortlist | Food types and dining areas as ideas to research; what a family may have to plan around (dietary needs, group seating). No restaurant recommendations, no prices. |
| `42_reservation_examples.md` | 42 Reservations and Timed Entries | A few experiences that require committing to a date to reserve, each with roughly how far ahead and what kind of gate it is, all framed as categories to re-check rather than current values. No release dates, no prices. |
| `47_language_etiquette.md` | 47 Language and Etiquette | A short set of everyday phrases; the etiquette points a visiting family actually meets; any custom with rules of its own (bathing, photography, sacred sites), described matter-of-factly and never as something the child will get wrong. |
| `kid_glossary.md` | Child travel glossary, all sessions | The destination words a child meets on signs, on menus and on trains, one line each; the units the destination uses (temperature, distance, time format) with a kid-sized conversion for each; one currency example, labeled an example to re-check and carrying the month the pack last stood behind the figure, which is normally older than this file's own `Last reviewed` line. |

Every slot file also carries a `**Last reviewed:** <month year>` line directly below its title -- for example, `**Last reviewed:** September 2026`. Re-checking is optional upkeep, not a maintenance promise.

### How a slot divides from its reference

Nine of the twelve slots sit beside a reference file in the contract table above, and the division between the two is a rule rather than a judgment call. The insert supplies only what the session's own page needs in hand: the enumeration a child fills a worksheet from. Everything else belongs to the reference, and so does every volatile fact: availability, current tools, rules that change, anything the pack itself tells a reader to check rather than memorize. Say so in the slot with a pointer. Where the two ever disagree, the reference wins.

The reason is mechanical. Both files carry their own `Last reviewed` line, so a fact written into both is stamped twice and re-checked once, and the session then meets two freshness claims with one piece of upkeep behind them.

Three slots have no reference file in the contract at all, and those three own their fields outright: `10_snapshot_facts.md`, `42_reservation_examples.md` and `kid_glossary.md`. Where a slot owns its fields outright it is the canonical home, and a volatile fact written there carries the date the pack last stood behind it. It never carries the slot's own `Last reviewed` stamp, which is the month the page was authored and would assert a check nobody made.

The field lists are a floor rather than a ceiling. The batch that writes a slot may find it needs one more field, and should add that field to the table above in the same pass. What it may not do is ship a slot with fewer fields than its row names, or leave a row with no fields at all.

Dividing a row later means editing the row, in the same pass that writes the reference file. Narrow the row first, in the change that writes the reference file, then build the slot to the row as it now stands. Record the narrowing in the curriculum changelog, the way every other contract departure is recorded. Do not narrow a row without writing its reference file in the same pass: a row stripped of a field whose new home does not exist yet routes the child nowhere.

## What is written in this pack, and what is not

The contract table names twelve insert slots and twelve reference files. Both columns are completion targets. A reader given only the insert count would write twelve files and believe the pack was finished. The four bullets below count what *this* pack has built, so they are the one part of this contract that a second pack does not copy; step 1 of the checklist below says what to write instead.

- **Insert slots written (four):** `10_snapshot_facts.md`, `11_regions_overview.md`, `12_seasons_and_events.md` and `kid_glossary.md`.
- **Insert slots not yet written:** the other eight.
- **Reference files written (seven):** `regions_overview.md`, `major_cities.md`, `seasons_weather_events.md`, `transportation_basics.md`, `money_basics.md`, `trusted_starting_sources.md` and `sample_search_terms.md`.
- **Reference files not yet written (five):** `food_basics.md`, `language_basics.md`, `etiquette_basics.md`, `adult_logistics.md` and `airports_and_arrival_basics.md`.

## Adding a destination

1. Create the pack's two contents pages. `destinations/<name>/README.md` carries the provided-as-is framing and lists the pack's reference files and its inserts. `destinations/<name>/session_inserts/README.md` is a destination-neutral copy of this contract. Then create the pack's `reference/` directory and fill in its stable facts, one file per topic, each named as the contract's reference column names it: regions, major cities, seasons, weather and events, transportation, airports, money, language, etiquette, food, adult logistics, trusted starting sources, and sample search terms. Every field list above is written destination-neutral so that a copy of this contract carries the contract and none of the first pack's values. One section is the exception. The four bullets under **What is written in this pack, and what is not** count what the first pack has built, so copying them hands a new pack counts it has not earned and makes an empty pack look part-finished. Delete those four bullets in the copy and recount them for the pack you are starting: nothing is written on day one, so every insert slot and every reference file in the contract table belongs on the not-yet-written lists.
2. Write the small "destination notes" each place-specific session pulls in.
3. Do not edit any framework session, template, guide, or doc, with one temporary exception: Session 15, which the rider above names and which a new destination converts by hand until Batch 2 converts it for everyone.
4. Keep adult-owned legal and safety topics adult-owned.
5. Keep volatile facts -- prices, hours, entry rules -- as "verify on official sources," never fixed.
6. When both contents pages exist, every named insert slot and every named reference file is filled -- and, until Batch 2, Session 15 is converted -- the destination is added. If your destination is not a country, the slots that assume one are not fillable yet: the snapshot slot's `Capital` field and the candidate-cities slot both take their wording from a destination model this repository has not settled, and what either one means for a city, a region, or a route across several countries is undecided. Deciding it by substituting another word is not a fill. The test is the assumption and not this pair of names -- any slot whose field only makes sense for a country is bound by the same undecided question, named here or not. A pack of that shape is not finished until that question is answered.

**Open Question: what a destination is.** The slots above are written for a country. A pack for a city, a region, or a route across several countries has no settled answer for the snapshot slot's `Capital` field or for the candidate-cities slot, and substituting another word is not an answer. Until this is decided, a pack of that shape cannot complete step 6, and any slot whose field only makes sense for a country is bound by it, named here or not. Carried as an open question so a later handoff reads it as a blocker rather than as a detail.
