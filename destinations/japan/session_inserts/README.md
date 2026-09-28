<!-- markdownlint-disable MD013 -->
<!-- audience: builder -->

# Session Inserts: The Routing Contract

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-28
- **Scope:** The destination-pack routing contract. It says which session pulls which insert, which reference files each session points to, and what fields every insert slot has to supply. The steps for adding a destination pack are in the framework's add-a-destination guide. It holds routing rather than facts, so it carries no `Last reviewed` stamp.
- **Related:** [Destination pack contents](../README.md), [How to add a destination](../../../framework/how_to_add_a_destination.md), [Cross-reference map](../../../framework/cross_reference_map.md)

This file is for whoever builds a destination pack or adds one. The pack's [contents page](../README.md) carries the provided-as-is framing every family reading the pack needs: the facts come from one family, nobody is on call to keep them current, and anything a family relies on gets verified against official sources close to travel.

## The insert and reference contract

This table routes every session that needs place facts to the pack, in session order. The rule under the table says how each session writes its pointer. The framework's [cross-reference map](../../../framework/cross_reference_map.md) mirrors this table and the parent-facing one, with every pack file named generically, and this contract is the canonical copy.

| Session | Insert it pulls (`session_inserts/`) | Reference file(s) it points to (`reference/`) |
| --- | --- | --- |
| 05 Good Sources, Bad Sources | none | [`trusted_starting_sources.md`](../reference/trusted_starting_sources.md) |
| 06 Book Research With a Guidebook | none | [`trusted_starting_sources.md`](../reference/trusted_starting_sources.md) (the guidebooks it names) |
| 08 Web Research Practice | none | [`trusted_starting_sources.md`](../reference/trusted_starting_sources.md), [`sample_search_terms.md`](../reference/sample_search_terms.md) |
| 10 Destination Snapshot | [`10_snapshot_facts.md`](10_snapshot_facts.md) | none |
| 11 Regions and Cities Overview | [`11_regions_overview.md`](11_regions_overview.md) | [`regions_overview.md`](../reference/regions_overview.md), [`major_cities.md`](../reference/major_cities.md) |
| 12 Weather, Seasons, and Events | [`12_seasons_and_events.md`](12_seasons_and_events.md) | [`seasons_weather_events.md`](../reference/seasons_weather_events.md) |
| 16-18 Deep-Dive Cities | [`16_18_candidate_cities.md`](16_18_candidate_cities.md) | [`major_cities.md`](../reference/major_cities.md) |
| 19 Other Places Research | [`19_other_places_menu.md`](19_other_places_menu.md) | [`major_cities.md`](../reference/major_cities.md) |
| 23 Attraction Research Cards | [`23_attraction_ideas.md`](23_attraction_ideas.md) | [`food_basics.md`](../reference/food_basics.md) (for food-type attractions), [`major_cities.md`](../reference/major_cities.md) (the attraction menu) |
| 30 Trains, Transit, and Travel Cards | [`30_transport_specifics.md`](30_transport_specifics.md) | [`transportation_basics.md`](../reference/transportation_basics.md) |
| 34 Neighborhoods and Hotel Location | [`34_lodging_types.md`](34_lodging_types.md) | [`adult_logistics.md`](../reference/adult_logistics.md) (occupancy reality) |
| 36-37 Food / Restaurant Shortlist | [`36_37_food_ideas.md`](36_37_food_ideas.md) | [`food_basics.md`](../reference/food_basics.md) |
| 38 Daily Cost Estimates | none | [`money_basics.md`](../reference/money_basics.md) (cash culture, currency) |
| 40 Realistic Day Planning | none | [`airports_and_arrival_basics.md`](../reference/airports_and_arrival_basics.md) (airport-to-city) |
| 42 Reservations and Timed Entries | [`42_reservation_examples.md`](42_reservation_examples.md) | [`access_and_pricing_watch.md`](../reference/access_and_pricing_watch.md) (the other fast-changing items to re-check) |
| 43 Rest Days, Jet Lag, and Pacing | none | [`transportation_basics.md`](../reference/transportation_basics.md) (walking/stairs) |
| 47 Language and Etiquette | [`47_language_etiquette.md`](47_language_etiquette.md) | [`language_basics.md`](../reference/language_basics.md), [`etiquette_basics.md`](../reference/etiquette_basics.md), [`money_basics.md`](../reference/money_basics.md) (cash) |
| 48 Packing List | none | [`seasons_weather_events.md`](../reference/seasons_weather_events.md) (seasonal packing) |
| 49 Travel Readiness Checklist | none | [`safety_and_emergency.md`](../reference/safety_and_emergency.md) (the official source for the emergency numbers, the local kinds of help, the two staying-found phrases) |
| (child travel glossary, all sessions) | [`kid_glossary.md`](kid_glossary.md) | none |

**Which column a row fills decides how its session writes.** A row with an insert means the session writes the exact phrase *"open this session's Destination Notes"*, and that phrase resolves to the insert. A row whose Insert column reads `none` means the session names the reference in the pack's own words instead, because there is no insert for the phrase to resolve to.

Every filename in this page's tables is a relative link, because every slot and every reference file the contract names now exists in this pack. A new pack that copies this contract starts with none of its files, so its copy writes each filename as inline code until that pack's own file exists, and converts it to a link in the same change that writes the file. The repository's link check then never meets a route that goes nowhere.

Sessions not in this table (00-04, 07, 09, 13-15, 20-22, 24-29, 31-33, 35, 39, 41, 44-46, 50-54) need no destination facts and are fully neutral. Session 54, the optional post-trip session, is one of them: the child compares what they predicted with what happened on the trip, and names no place. A session can be routed to a pack file without naming a place in its own wording: Sessions 05 and 08 name no place but open the pack's trusted starting sources list, and Session 38 takes its currency and cash-culture facts from the pack's money basics page. Every such pointer is a row in the table above.

### Parent-facing pages

The parent-guide pages in the table below mention destination facts an adult needs: local hazards, emergency numbers, lodging priced per person, children's fares, and which airport to land at. Each stays destination-neutral and names the pack file generically, so each gets a row here on the same terms as a session. A parent page names the reference in the pack's own words, as a reference-routed session does, and says what to do if the pack lacks the file: use a current official source, checked and dated.

| Parent-facing page | Insert it pulls | Reference file(s) it points to (`reference/`) |
| --- | --- | --- |
| Adult-only logistics | none | [`adult_logistics.md`](../reference/adult_logistics.md) (entry specifics, luggage help), [`safety_and_emergency.md`](../reference/safety_and_emergency.md) (local natural hazards) |
| Safety and emergency guidance | none | [`safety_and_emergency.md`](../reference/safety_and_emergency.md) (the official source for the emergency numbers, local terms for help, local natural hazards) |
| Money and budget guidance | none | [`money_basics.md`](../reference/money_basics.md) (lodging priced per person, children's fares) |
| Flights from your home airport | none | [`airports_and_arrival_basics.md`](../reference/airports_and_arrival_basics.md) (which airport to land at, arrival-day transit) |

## What each insert slot supplies

Every field list below is written destination-neutrally, so this contract copies into a second pack unchanged. A destination's own values belong in the slot files.

| Slot | Consuming session | Fields it must supply |
| --- | --- | --- |
| [`10_snapshot_facts.md`](10_snapshot_facts.md) | 10 Destination Snapshot | Capital; major land features; currency; main language. Not the time-difference figure. That is a Trip-Basics card value. |
| [`11_regions_overview.md`](11_regions_overview.md) | 11 Regions and Cities Overview | The regions the pack plans a first trip around, named, with one line saying the destination has more, so the child can start their region notes; then a pointer to the pack's regions reference for how each region feels different and for three geography instances the neutral session may not state (your destination's shape and size, how weather differs by region, and why travel time between regions matters), and a pointer to the pack's major cities reference for the route shapes. That regions reference is their canonical home; do not restate them in the slot. No trip shapes, no costs, no pinned travel times. |
| [`12_seasons_and_events.md`](12_seasons_and_events.md) | 12 Weather, Seasons, and Events | Each season the destination has, named, so the child can label a season chart, with one short line each on what traveling in it is like; then a pointer to the pack's seasons, weather and events reference for the rest: the big-draw and busiest periods, the congestion windows named as categories to confirm this year, each seasonal hazard with its pacing consequence, and the adult-facing contingency note. That reference is their canonical home; do not restate them in the slot. No pinned dates, prices or forecasts. |
| [`16_18_candidate_cities.md`](16_18_candidate_cities.md) | 16-18 Deep-Dive Cities | Two to four first-trip candidate cities, each with a one-line draw, so the child can start a card per city; then a pointer to the pack's major cities reference for the kid-magnet ideas and for anything whose opening or availability changes. That reference is their canonical home; do not restate them in the slot. Candidates to research, never a shortlist. |
| [`19_other_places_menu.md`](19_other_places_menu.md) | 19 Other Places Research | A menu of further candidate places beyond the deep-dive cities, each with a one-line draw, offered as options to research rather than as a shortlist, and sorted into three kinds: well-known places, places kids often love, and everyday places that cost little. The slot names the places and sorts them into the three kinds itself. For each place's detail, point at the pack's major cities reference instead of copying it; that reference is the detail's canonical home. |
| [`23_attraction_ideas.md`](23_attraction_ideas.md) | 23 Attraction Research Cards | Starter attraction ideas as options to research, mixing high-draw named attractions with low-cost everyday ones, each with what kind of visit it is; anything ticketed, timed or permit-gated flagged "verify." No prices, no hours. |
| [`30_transport_specifics.md`](30_transport_specifics.md) | 30 Trains, Transit, and Travel Cards | The transport modes a child plans around, named (long-distance, local, walking, taxis), so the child can sort a day's travel; then a pointer to the pack's transportation reference for the rest: the stored-value or travel-card options and whether a visitor can get one now, luggage forwarding and station lockers, any pass whose value depends on the itinerary, and a route-planning tool that works today. That reference is their canonical home; do not restate them in the slot. No fares, no pinned journey times. |
| [`34_lodging_types.md`](34_lodging_types.md) | 34 Neighborhoods and Hotel Location | The lodging categories a family chooses among, one line each, so the child can sort a night's options; then a pointer to the pack's adult logistics page for the occupancy reality: how many people a room holds, and what a larger party has to plan around. That reference is their canonical home; do not restate it in the slot. No prices, no named properties. |
| [`36_37_food_ideas.md`](36_37_food_ideas.md) | 36-37 Food / Restaurant Shortlist | Food types and dining areas as ideas to research; what a family may have to plan around (dietary needs, group seating). No restaurant recommendations, no prices. |
| [`42_reservation_examples.md`](42_reservation_examples.md) | 42 Reservations and Timed Entries | A few experiences that require committing to a date to reserve, each with roughly how far ahead and what kind of gate it is, all framed as categories to re-check rather than current values. No release dates, no prices. |
| [`47_language_etiquette.md`](47_language_etiquette.md) | 47 Language and Etiquette | A short set of everyday phrases; the etiquette points a visiting family meets; any custom with rules of its own (bathing, photography, sacred sites), described matter-of-factly and never as something the child will get wrong. |
| [`kid_glossary.md`](kid_glossary.md) | Child travel glossary, all sessions | The destination words a child meets on signs, on menus and on trains, one line each; the units the destination uses (temperature, distance, time format) with a kid-sized conversion for each; one currency example, labeled an example to re-check and carrying the month the pack last stood behind the figure, which is normally older than this file's own `Last reviewed` line. |

<!-- density-exempt: X, not Y -- the batch 1 brief gives this rule in exactly this form, ending "not a maintenance promise" -->
Every slot file also carries a `**Last reviewed:** <month year>` line directly below its title -- for example, `**Last reviewed:** September 2026`. Re-checking is optional upkeep, not a maintenance promise.

### How a slot divides from its reference

<!-- density-exempt: X, not Y -- the rule the batch 1 brief's entry for this page gives for dividing a slot from its reference, with the precedence it fixes: if the two ever disagree, the reference wins -->
Ten of the twelve slots sit beside a reference file in the contract table above, and a fixed rule divides the two, so every author splits them the same way. The insert supplies only what the session's own page needs in hand: the enumeration a child fills a worksheet from. Everything else belongs to the reference, and so does every volatile fact: availability, current tools, rules that change, anything the pack itself tells a reader to re-check before relying on it. Say so in the slot with a pointer. Where the two ever disagree, the reference wins.

The reason is mechanical. Both files carry their own `Last reviewed` line, so a fact written into both is stamped twice and re-checked once, and the session then meets two freshness claims with one piece of upkeep behind them.

Two slots have no reference file in the contract at all: [`10_snapshot_facts.md`](10_snapshot_facts.md) and [`kid_glossary.md`](kid_glossary.md). Those two own their fields outright, and so does [`42_reservation_examples.md`](42_reservation_examples.md). Its one reference, the access and pricing watch, lists the categories to re-check and carries no examples, so the slot is the only home for its examples and their booking horizons. Where a slot owns its fields outright it is the canonical home, and a volatile fact written there carries the date the pack last stood behind it. It never borrows the slot's own `Last reviewed` stamp as that date, because the stamp covers the whole page and would assert a check of that fact nobody made.

The field lists are the minimum, and an author may add to them. The batch that writes a slot may find it needs one more field, and should add that field to the table above in the same pass. Every slot it ships must still carry every field its row names, and every row must keep at least one field.

Dividing a row later means editing the row, in the same pass that writes the reference file. Narrow the row first, in the change that writes the reference file, then build the slot to the row as it now stands. Record the narrowing in the curriculum changelog, the way every other contract departure is recorded. Do not narrow a row without writing its reference file in the same pass: a row stripped of a field whose new home does not exist yet routes the child nowhere.

## What is written in this pack, and what is not

The contract tables name twelve insert slots and fourteen reference files. Both columns are completion targets. A reader given only the insert count would write twelve files and believe the pack was finished. The four bullets below count what *this* pack has built, so they are the one part of this contract that a second pack recounts for itself. A new pack's copy of this contract deletes the four bullets and recounts them for that pack, so an empty pack reads as empty. On day one, every insert slot and every reference file in the contract tables goes on the second and fourth bullets, the lists of what is still to write.

- **Insert slots written (twelve):** [`10_snapshot_facts.md`](10_snapshot_facts.md), [`11_regions_overview.md`](11_regions_overview.md), [`12_seasons_and_events.md`](12_seasons_and_events.md), [`16_18_candidate_cities.md`](16_18_candidate_cities.md), [`19_other_places_menu.md`](19_other_places_menu.md), [`23_attraction_ideas.md`](23_attraction_ideas.md), [`30_transport_specifics.md`](30_transport_specifics.md), [`34_lodging_types.md`](34_lodging_types.md), [`36_37_food_ideas.md`](36_37_food_ideas.md), [`42_reservation_examples.md`](42_reservation_examples.md), [`47_language_etiquette.md`](47_language_etiquette.md) and [`kid_glossary.md`](kid_glossary.md).
- **Insert slots not yet written:** none.
- **Reference files written (fourteen):** [`regions_overview.md`](../reference/regions_overview.md), [`major_cities.md`](../reference/major_cities.md), [`seasons_weather_events.md`](../reference/seasons_weather_events.md), [`transportation_basics.md`](../reference/transportation_basics.md), [`airports_and_arrival_basics.md`](../reference/airports_and_arrival_basics.md), [`money_basics.md`](../reference/money_basics.md), [`language_basics.md`](../reference/language_basics.md), [`etiquette_basics.md`](../reference/etiquette_basics.md), [`food_basics.md`](../reference/food_basics.md), [`adult_logistics.md`](../reference/adult_logistics.md), [`safety_and_emergency.md`](../reference/safety_and_emergency.md), [`access_and_pricing_watch.md`](../reference/access_and_pricing_watch.md), [`trusted_starting_sources.md`](../reference/trusted_starting_sources.md) and [`sample_search_terms.md`](../reference/sample_search_terms.md).
- **Reference files not yet written:** none.

## Adding a destination

The steps for building a new destination pack are in the framework's [add-a-destination guide](../../../framework/how_to_add_a_destination.md).

A pack covers one country, and a trip to a city or a region inside that country uses its pack; the [add-a-destination guide](../../../framework/how_to_add_a_destination.md#what-a-pack-is-and-what-it-covers) records what a trip across several countries does as an Open Question.
