<!-- markdownlint-disable MD013 -->

# Batch 3 build brief — the rest of the Japan pack

## What this file is

This is the build brief for **Batch 3**, the batch that finishes the Japan knowledge pack.
It is a build instruction, not shipped curriculum. It lives outside `framework/` and
`destinations/` so a family reading the materials never meets it.

It carries every Batch 3 requirement and the adjudicated answer to every open question
raised against the batch, so an authoring run does not need the archived specification in
the ordinary case. The brief keeps a recovery path for when it is itself defective:
re-read the brief, then consult the specification for that one missing detail, then record
the gap here so the next run does not repeat the lookup.

## Source of truth

- **The archived design record** is `docs/spec/specification.md`. It is the origin of the
  requirements below and it is **not** a file this batch edits.
- **The built repository wins where the two disagree.** Batch 1 and Batch 2 made decisions
  the archived record does not carry, and those decisions are law now. The departures
  table in section 4 lists every one that touches this batch.
- **The routing contract is `destinations/japan/session_inserts/README.md`.** It is the
  operative specification for every slot this batch fills, and the route for every
  reference file it writes. Read it before
  drafting anything. Where this brief and the contract disagree about a slot's fields,
  the contract wins and the disagreement is a defect in this brief worth recording.

## Build track

**Full Build.** The neutral-skeleton and insert apparatus is live and has been since
Batch 1. This batch writes destination facts into the destination pack, which is the one
place in this repository where naming Japan is correct rather than a leak.

---

## 0. What this batch is, in one paragraph

Fifteen new files, and five edits to built ones. Seven of the new files are **reference
files** under `destinations/japan/reference/`, which hold stable orienting facts a reader
consults directly. Eight are **insert slots**
under `destinations/japan/session_inserts/`, which are the small Destination Notes a
session pulls in when a child is told to open them. Every slot's required fields are
already written in the contract; this batch fills them. When the last slot is filled, the
claim the whole three-layer structure rests on becomes testable for the first time: a
family can run the full curriculum on this pack without anyone editing a framework file.

**This is the batch where the pack stops being half-built.** Six sessions in the Core path
currently route to files no pack has. Until they exist, a child who follows the routing
lands nowhere, and the contract is a promise rather than a route.

---

## 1. Hard rules that govern every file in this batch

These six are the ones this batch is most likely to break. They are not a summary of the
BUILD RULES at the end of this brief; those bind too.

### 1.1 The pack states facts. That is its job, and it is the inverse of every other batch

Batches 1 and 2 spent their review rounds keeping Japan out of `framework/`. **This batch
is the other half of that trade.** A pack file that refuses to name Tokyo is not being
careful; it is failing to be a destination pack, and it leaves the session that routes to
it with nothing.

So: name cities, name regions, name foods, name transit modes, name real attractions. The
leak greps that gate `framework/` do not run against `destinations/`, and the destination
name in a pack heading is correct.

**What stays out is family data, not place facts.** See rule 1.6.

### 1.2 Categories, never current values

This is the rule that decides whether a pack file is still true in three years.

**Never write:** a price, a fare, an admission fee, an exchange rate, an opening hour, a
reservation release date, a tax amount, a permit fee, a visa requirement stated as
settled, or a size threshold quoted as a number.

**Write instead:** the category, what makes it change, and how a reader checks it today.
"Some attractions now require a timed-entry reservation, and which ones changes -- check
the attraction's own site" is durable. The same sentence with three named attractions and
their current booking windows is stale the season after it ships.

**The one sanctioned exception is the currency example in `kid_glossary.md`**, which Batch
1 already built: one illustrative conversion, labeled an example to re-check, carrying the
month the pack last stood behind it. Do not add a second exception anywhere.

**Named things are not values.** Naming teamLab as an operator whose venues open, close
and move is a category. Naming one venue and its hours is a value. The archived record
makes this distinction explicitly for teamLab, and it generalizes: name the thing, never
pin its state.

### 1.3 Every reference file and every slot carries a freshness stamp

The form is a `**Last reviewed:** <month year>` line directly below the title -- for
example, `**Last reviewed:** September 2026`. The built pack is consistent on this and the
contract states it.

**It is an honesty stamp, not a maintenance promise.** It says when one family last
looked. Nobody is on call. Do not write a sentence anywhere in this batch that implies the
pack is kept current, and do not write a review cadence.

### 1.4 Matter-of-fact and respectful, never marveling

The archived record names this as the check that bites the etiquette and language content
hardest, and the acceptance criterion for it is human rather than grep-assisted, which
means it is on the author.

**The test:** would a Japanese ten-year-old reading this page recognize their own ordinary
life in it, or would they find themselves described as a curiosity? Bathing customs,
shoe-removal, queueing, quiet trains and shrine etiquette are how a place works. Write
them the way you would write "in the United States you tip at restaurants" -- a practical
thing a visitor needs to know.

**Specifically banned:** "exotic", "bizarre", "strange", "fascinating", "unlike anything
you've seen", and any sentence whose work is to make the reader marvel. Also banned is the
apologetic register that treats a custom as a hazard the child will fail. A child who
reads that they will probably get it wrong stops wanting to go.

### 1.5 Adult-owned topics stay adult-owned, and the pack says so on the page

Entry and visa rules, passport validity, travel insurance, health requirements, travel
advisories, emergency monitoring, payment, and booking are adult-owned throughout this
curriculum. The pack carries the facts a family needs; it never hands the child the
decision.

Write the ownership into the sentence rather than into a footnote: "An adult checks the
current entry rules on the official government source close to travel" carries both the
fact and the owner. A page that states an entry rule and then adds "ask a grown-up" at the
bottom has already taught the child the rule is settled.

### 1.6 No family data, in any file, ever

No home airport and no airport code. No origin city. No maximum trip length. No named
relatives and no roster. No dates, no budget figures, no lodging names, no confirmation
numbers.

This is not softened by the pack being the destination layer. The pack describes Japan for
any reusing family; the moment it describes *this* family, it stops being reusable and
starts being a privacy problem in a public repository.

**The check:** `grep -rwE 'Chicago|ORD|grandmother|uncle' destinations/` and
`grep -rwE '17[ -]?(day|night)s?' destinations/` both find nothing.

### 1.7 Reader economy: the built pack already carries a lot

Six reference files and four slots already exist. Several of them already hold content
this batch's files would otherwise duplicate, and duplication here is not a style
complaint -- it produces two homes for one fact, which decay apart.

**Before writing any section, read the built file that neighbours it.** Section 3.2 gives
the division-of-labour rule and section 5 names the specific overlaps that already exist.

---

## 2. Scope boundary

### In scope

| | What | Count |
| --- | --- | --- |
| A | New `destinations/japan/reference/` files | **7** |
| B | New `destinations/japan/session_inserts/` slot files | **8** |
| C | Edit: `destinations/japan/session_inserts/README.md`, the routing contract | 1 |
| D | Edit: `destinations/japan/README.md`, the pack contents page | 1 |
| E | Edit: `destinations/japan/reference/transportation_basics.md` (`B3-4`) | 1 |
| F | Edit: `destinations/japan/session_inserts/kid_glossary.md` (`B3-6`) | 1 |
| G | Edit: `framework/CHANGELOG.md` | 1 |

**Twenty files touched, fifteen of them created.** Groups E and F are edits to built pack
files that sections 4 and 5 require; they are listed here because the file-scope rule below
means a file absent from this table does not get written, however plainly some other
section asks for it.

The seven reference files are `airports_and_arrival_basics.md`, `language_basics.md`,
`etiquette_basics.md`, `food_basics.md`, `adult_logistics.md`, `safety_and_emergency.md`
and `access_and_pricing_watch.md`. The archived record's pack tree names the first five.
The sixth comes from Batch 2 (`I-2`) and the seventh from `B3-1`.

### Not in scope, and do not build it "to unblock" something

- **Any file under `framework/`** except `CHANGELOG.md`. If a framework session reads
  wrongly against a pack file you are writing, that is a finding to record in section 8,
  not an edit to make. The session layer is closed to this batch.
- **Session 54, `framework/examples/`, `cross_reference_map.md`,
  `how_to_add_a_destination.md`.** All Batch 4.
- **The closing whole-repo consistency pass.** Batch 4.
- **A second destination pack.** The reusability claim is tested by the contract being
  fillable, not by filling it twice.
- **`CONTRIBUTING.md`.** Optional and aspirational, adjudicated in Batch 4.
- **Re-reviewing or re-dating any built pack file.** Bumping a `Last reviewed` line you
  did not otherwise change is a false claim that someone re-checked the facts.

### The batch gate

Batch 3 ends at the per-batch quality pass, which this run can perform: the validation
gates in section 9, plus the human-review rows in section 7 that an adversarial review
subagent stands in for under this project's recorded pilot deferral. **There is no
child-run gate on this batch.** The design-validation gate was Batch 0's and it cleared on
the recorded no-child fallback; nothing in this brief may write otherwise.

---

## 3. The contract is the specification

### 3.1 The two kinds of file, and why the difference matters

A **reference file** is read directly by whoever needs it -- a child researching, or an
adult checking logistics. It is organized by topic and it can be long enough to be useful.

A **slot file** is what the phrase *"open this session's Destination Notes"* resolves to.
It is consumed inside one session, at one moment, by a child who is mid-task. It is short,
it supplies exactly the fields the contract names, and it points at the reference file for
anything a curious reader wants beyond that.

**The failure mode is writing a slot as a small reference file.** A slot that explains
four regions in a paragraph each has stopped being a note the child opens and become a
page they read instead of working. The built slots -- `10_snapshot_facts.md`,
`11_regions_overview.md`, `12_seasons_and_events.md` -- are the model for length and
register. Read all three before drafting a new one.

### 3.2 The division-of-labour rule

**The slot names. The reference explains.** The contract states this per slot and it holds
generally: a slot supplies the named items the child needs in hand to start, then points
at the reference file for the depth, and **does not restate what the reference carries.**

Worked through on `34_lodging_types.md`: the slot names the lodging categories a family
chooses among, one line each, so the child can sort a night's options. The occupancy
reality -- how many people a room holds, what a larger party plans around -- lives in
`adult_logistics.md` and the slot points there. A slot that explains occupancy itself has
created a second home for a fact that will be edited in only one of them.

**Where the reference does not exist yet, the slot still points at it by name.** All six
reference files in this batch are being written in this same batch, so by the end of the
batch every pointer resolves.

### 3.3 Inline code becomes a link when the target lands

The contract currently writes every filename as inline code, because most targets did not
exist and a link to a missing file fails the repository's link check. The contract says
outright that whichever batch writes a target adds the link then.

**That is this batch.** By the end of it every target the contract names exists, so every
filename in it can become a link. Convert each inline-code filename in the
contract to a relative link as its target is created, and do the conversion in the same
change that creates the file, so the contract is never describing a route it cannot walk.

**No filename should still be inline code when this batch ships.** Every target the
contract names will exist. If one does not, because you could not build it or because the
contract names something this brief missed, say so in section 8 rather than leaving a
silent inline-code entry that reads like an oversight.

---

## 4. Decisions this batch inherits, and the questions it settles

The first group is inherited: decisions Batch 1 or Batch 2 already made that a reader of
the archived record would not expect. The second group is settled here.

### 4.1 Inherited departures

| | The archived record says | The built repository does | Why |
| --- | --- | --- | --- |
| **I-1** | The adult-logistics reference is `adult_logistics_japan.md` | **`adult_logistics.md`** | Batch 1's contract registers the unsuffixed name, and Batch 2 corrected a scope list that carried the suffixed variant. A place-suffixed filename inside a place's own folder is redundant, and worse, it does not copy into a second pack. A pack author following the suffixed name would create a file no session routes to |
| **I-2** | Session 49 needs no destination facts | It gets a row routing it to **`safety_and_emergency.md`** | Batch 2's `D-item-5`. The session's staying-found teaching rests on local institution types, emergency phrases and emergency numbers, all of which are destination facts. The file is new: the archived record's pack tree has no safety file at all |
| **I-3** | The contract routes only child-facing session files | It also routes **parent-facing** files | Batch 2's `D-X-2`. `adult_only_logistics.md`, `safety_emergency_guidance.md` and `money_budget_guidance.md` each need destination-specific items, and each stays neutral, so the routing needs to be honest rather than implied |
| **I-4** | Sessions 16-18 pull `16_18_candidate_cities.md` | Unchanged, but the schema is fixed: **2-4 candidates, one-line draw each** | Batch 2's session contracts were written against exactly that schema and nothing more. A slot that supplies eight candidates with three paragraphs each breaks three sessions that were authored to it |

### 4.2 Questions this batch settles

Each was checked against the escalation gate before being answered here. None qualifies:
each turns on repository state or on the archived record's own text, not on a value
judgment only the owner can make.

| | The question | The answer | Why |
| --- | --- | --- | --- |
| **B3-1** | The archived record asks for a short "access and pricing watch" checklist in the pack, cross-linked from three places and carrying its own freshness stamp. The built pack README carries a prose note covering the same categories. Is the note the watch? | **No. The watch gets its own file, `access_and_pricing_watch.md`**, and the pack README's note keeps its place as the short framing and links to it | Three things are asked of the watch that the note cannot do. It must be cross-linked *to* from the reservation, transit and budget surfaces, and a link into the middle of a README section is the kind of pointer that rots. It must carry its own `Last reviewed` stamp, and the README carries none. And it must list categories in a form a reader can work down before travel, which is a checklist rather than a paragraph. **This makes seven new reference files, not six** -- the count in section 2 includes it |
| **B3-2** | Batch 2 rules that no built page prints an emergency number. Does that bind the pack? | **No. The pack states the emergency numbers, verify-framed.** The framework session never prints one | Batch 2's own Session 49 text reads "**The pack has them**", and instructs the child to write the number on their card only after an adult checks it on a current official page. The rule is about the printable card and the session, and it depends on the pack carrying the numbers. A pack that also withholds them leaves the instruction pointing at nothing |
| **B3-3** | Where does the bathing-custom content live: `etiquette_basics.md`, the `47_language_etiquette.md` slot, or both? | **`etiquette_basics.md` carries it. The slot names it in one line and points there** | Section 3.2's rule, applied. The custom has rules of its own and an adult-owned age judgment attached, which is reference depth. A child mid-Session-47 needs to know it exists and that the pack explains it |
| **B3-4** | The built `transportation_basics.md` already has a "Getting there and the arrival day" section. Does `airports_and_arrival_basics.md` duplicate it or replace it? | **Neither. The airport file takes the arrival-day material and the transport file's section becomes a pointer** | One fact, one home. The arrival-day content is airport content that landed early because the airport file did not exist yet. Moving it is an edit to a built file, so it is named here explicitly: the transport file's section is reduced to a one-clause reminder plus a link, per the reader-economy rule |
| **B3-5** | The built `major_cities.md` already carries "Other places people research" and "Fun things to consider". Do `19_other_places_menu.md` and `23_attraction_ideas.md` duplicate them? | **No. Both slots name a short set and point at `major_cities.md` for the rest** | The contract already says this for slot 19 in as many words. Slot 23 takes the same treatment for the same reason. What the slots add is the framing each session needs, which the reference does not carry |
| **B3-6** | Does this batch extend `kid_glossary.md` with the new terms its files introduce (ryokan, takkyubin, koban, konbini, goshuin)? | **Yes, and it is an edit to a built file, so it is in scope and listed** | The glossary is the child's route to any destination word they meet. A slot that uses `takkyubin` while the glossary does not define it has left a ten-year-old with an unglossed word. Check each term before adding: Batch 1 built the glossary and several are already there |
| **B3-7** | The archived record names specific high-draw attractions and specific everyday options. Are those names requirements or examples? | **Requirements for the category, examples for the instance** | The record's own teaching point is that famous is not the only good, and it names everyday options precisely so the pack carries them. Write the categories it names. Within a category, an instance that has closed or moved gets replaced rather than preserved, because a pack naming a closed venue teaches the opposite of verify-don't-trust |

**B3-1 adds a file the archived record does not name**, so the counts in sections 0 and 2
are seven reference files rather than the five in the record's pack tree plus Batch 2's
addition. If a later reader counts the tree and gets a smaller number, this row is why.

---

## 5. The seven reference files

Every file opens with the `markdownlint-disable MD013` comment, an H1, and the
`**Last reviewed:**` line, matching the built pack. Every file is destination-facing prose
that a child or an adult reads directly.

**Register:** the built pack is written for a mixed audience and says which parts are the
adult's. Follow it. Child-readable where the child reads it, plain-adult where the content
is adult-owned, and never spec-voice.

### 5.1 `airports_and_arrival_basics.md`

**What it is for:** Session 40 routes here by reference for the airport-to-city question,
and the arrival day is the one day of a trip whose shape is set by logistics rather than
by choice.

Must carry:

- **The multi-gateway point, which is the reason this file exists.** Where a destination
  city has more than one international gateway, which one the family lands at changes
  arrival-day fatigue substantially -- one is materially closer to the city than the other,
  and the difference is more than an hour of extra transit with a tired party. Name the
  gateways. **Do not pin the transit time**, name that it differs and that current options
  are checked.
- **Airport-to-city transit as a category:** what kinds of option exist (train, express
  service, bus, taxi), what makes one better for a family with luggage, and that current
  services and prices are verified close to travel.
- **The arrival day as a plannable thing.** Getting from the airport to where you are
  staying and settling in is the day's main activity. This connects to the day-card
  pacing work, where day one and often day two are marked Easy.
- **What is adult-owned here:** the actual transit booking, and any airport service that
  has to be reserved.
- **The luggage connection:** forwarding and coin lockers change what an arrival day can
  hold. One clause and a link to `transportation_basics.md`, which is their home.

**Moved in from `transportation_basics.md`:** its "Getting there and the arrival day"
section, per `B3-4`. Reduce that section to a one-clause reminder and a link.

### 5.2 `language_basics.md`

**What it is for:** Session 47 routes here by reference. A child who has never met a
non-Latin script needs an orientation, not a language course.

Must carry:

- **What the writing system looks like in practice**, at the level a visitor meets it:
  that more than one script is in use, that station and major signage commonly carries
  romanized text, and that menus and smaller signs often do not.
- **Everyday phrases a visiting family actually uses**, written with a pronunciation
  guide a ten-year-old can read aloud. Greeting, thank you, excuse me, please, yes and no,
  "do you speak English", "where is the bathroom", and how to ask for the bill. Keep the
  set small enough to learn.
- **The translation-tool rule, which is a research skill rather than a language point:**
  use translation **to understand, not to trust**. Anything that matters gets checked
  against an official English source or an adult. This mirrors the source-trust teaching
  and belongs here because this is where the child reaches for the tool.
- **Which sources are reliably English and which are not.** The archived record is
  specific that some official transit pages, restaurant-review sites and some attraction
  pages are Japanese-first or only partly translated, and that a child who lands on one
  should not conclude they did something wrong. Name the categories, name the language
  toggle, and keep the instance list short because it moves.
- **One line of reassurance, not effusive:** visitors get by. Staff in tourist-facing
  places commonly have some English, and pointing and politeness carry a lot.

### 5.3 `etiquette_basics.md`

**What it is for:** Session 47 routes here by reference, and this is the file rule 1.4
bites hardest.

Must carry:

- **The everyday points a visiting family meets**, matter-of-factly: shoes, quiet on
  trains, queueing, how rubbish is handled, how money is handed over, and how to behave at
  a shrine or temple.
- **Photography limits.** Some private areas restrict photographs, some neighborhoods
  have posted rules, and the general instruction is to watch for and follow posted signs.
  Name the category and one example. Do not write a list of locations, which changes.
- **Bathing customs** (`B3-3`). Public and hot-spring bathing is a genuine part of the
  place, and it has rules of its own: bathing is nude rather than in swimwear, facilities
  are commonly separated by gender, washing happens before entering the shared water, and
  the towel stays out of it. Many facilities restrict visible tattoos, with cover-ups,
  private or rental baths, and tattoo-friendly facilities as the usual ways around that.
  - **The age question is adult-owned and has no national answer.** Whether and how a
    ten-year-old takes part, given the gender-separated norm, is a judgment adults make.
    There is **no single national age**: it is set locally and posted at each facility,
    commonly somewhere in the middle childhood range, and some places have changed theirs
    in recent years. **Write it verify-framed -- read the sign at the bath you visit -- and
    do not pin a number.**
  - A family that wants to bathe together looks for a private or family bath.
- **Onsen and sento named and distinguished**, one line each, and both added to the child
  glossary per `B3-6`.
- **The register check, written into the file's own framing:** these are how a place
  works, and a visitor who gets one wrong is corrected kindly rather than disgraced. Say
  it once, plainly, near the top.

### 5.4 `food_basics.md`

**What it is for:** Sessions 23 and 36-37 route here by reference. It is the food
orientation behind both the attraction cards that are food experiences and the restaurant
work.

Must carry:

- **The kinds of eating place a family meets**, by category with one line each: the
  conveyor-belt sushi place, the noodle shop, the department-store food hall, the
  convenience store as a genuine and good option, the izakaya and what makes it an
  adult-evening place, and the set-meal restaurant.
- **How ordering commonly works**, including ticket machines, plastic or photo menus, and
  that many places are cash-preferring. Point at `money_basics.md` for the cash culture
  rather than restating it.
- **Planning around dietary needs and group seating**, which is the practical thing a
  family with a mixed party has to solve. Keep it category-level: what to check, and that
  checking is done in advance for anything that matters.
- **The everyday-delight framing that the "famous is not the only good" teaching rests
  on.** Convenience-store food, vending machines, a food hall -- these are real experiences
  rather than consolation prizes, and the pack is where that gets said.
- **No restaurant recommendations and no prices.** The contract states this for the slot
  and it binds the reference too.

### 5.5 `adult_logistics.md`

**What it is for:** Session 34 routes here by reference for the occupancy reality, and the
parent-facing guide pages route here by name under `I-3`.

**Register: this file is adult-facing throughout.** Say so at the top. It is the one pack
file a child has no task in.

Must carry:

- **The occupancy reality, which is the reason Session 34 routes here.** Rooms are
  commonly smaller than a US family expects and are priced and capped **per person**
  rather than per room. A larger or multi-generational party often cannot put everyone in
  one room, connecting rooms are not a given, and this shapes both the budget and which
  lodging types work. State it as the category and what to verify per property.
- **Lodging types from the adult side**, which is the depth behind the slot's one-line
  categories: what a traditional inn involves (set meal times, per-person pricing, shared
  bathing facilities), what apartment-style and licensed rental lodging involves, and what
  a family hotel offers.
- **Booking-lead reality as a category**, not a calendar: peak periods book out far ahead
  at high prices, and adults book early. Point at `seasons_weather_events.md` for which
  periods those are.
- **The taxes that are in motion**, named as categories to verify at booking and before
  travel: the departure tax, the mechanics of tax-free shopping for visitors, and
  city-level lodging and bathing taxes. **No amounts, no effective dates.**
- **Entry authorization, adult-owned and carefully framed.** As of the last review, US
  visitors get visa-free short stays and nothing extra is required. A future electronic
  authorization has been legislated and is not live. **Carry the scam warning**: because a
  scheme has been announced, sites selling an authorization will appear, and nothing is
  required and nothing is for sale. Verify the current requirement on the official
  government source close to travel. Do not pin a requirement, a fee, or a date.
- **A pointer to `access_and_pricing_watch.md`** for the whole fast-moving category.

### 5.6 `safety_and_emergency.md`

**What it is for:** Session 49 routes here (`I-2`), and the parent-facing safety guidance
routes here by name (`I-3`). **This file has two audiences and must mark which part is
which**, because the child reads part of it and the adult owns the rest.

**The child-facing part.** Short, calm, and reassuring. Two notes, both in the register the
archived record sets:

- **The earthquake note.** Japan has earthquakes and is one of the most prepared places in
  the world for them -- buildings and trains are built for them, and there are clear safety
  routines. If you feel one, stay calm and follow the adults and staff around you. **Keep
  it to a few sentences.** It is reassurance rather than a drill, and a long version
  becomes the frightening thing it exists to prevent.
- **The "if you ever get separated" note**, in the same register, placed next to it. Most
  of the time you are with your family. If you cannot find them: do what today's one rule
  says, which a grown-up names each morning and is usually to stay where you are, then
  find a uniformed helper. Name the kinds of helper -- a station worker, a shop or security
  worker with a nametag, a convenience store, a neighborhood police post -- with the local
  words, and add each to the child glossary per `B3-6`.
- **Point at the card the child makes in Session 49.** Do not restate the card's contents.

**The emergency numbers** (`B3-2`). The pack states them, in the child-facing part, with
the verify frame attached in the same breath: these are the numbers, an adult confirms
them on a current official page before they go on the child's card, and the date they
checked goes on the card. Say who can place the call -- an adult, a shop worker, or the
police post -- because a ten-year-old's real question is whether they have to do it
themselves.

**The adult-facing part**, marked with its own heading:

- Two romanized emergency phrases a child could say or show, with a pronunciation guide.
- What stays adult-owned: advisories, monitoring, insurance, medical coverage, and
  contacts. One clause each and a pointer, not a treatment.
- **The lodging-card exception, stated carefully.** The child's separation card is the one
  place in this project where lodging name, address and phone number and a parent's phone
  number may appear, and it carries **no** passport number, birthdate, confirmation number
  or home address. The card is a copy-out artifact and is never committed. State the
  boundary; the card's own rules live with the card.

**Do not** write a drill, a scenario, or anything that reads as rehearsal for harm. The
rehearsal instruction -- that an adult walks through it once, calmly -- belongs to the
session's parent notes and is already there.

### 5.7 `access_and_pricing_watch.md`

**What it is for** (`B3-1`): one short page listing the **categories** to re-verify before
travel, so a family has a single thing to work down instead of remembering which facts
were volatile.

**It lists categories and never current values, which is what makes it un-decayable.**
Carry its own `Last reviewed` stamp.

The categories, each one line, each with what specifically changes:

- Timed-entry and reservation systems, which keep expanding to new attractions.
- Permit systems, including the mountain-climbing permit and fee.
- Stored-value transit card availability, which has changed repeatedly: which visitor
  options exist and work at all, including mobile versions and the known difficulty of
  adding them on phones bought outside the country.
- Rail-pass value, which shifted enough that the old advice stopped holding.
- Tourist and dual pricing, where some attractions, transit and venues have begun charging
  visitors a different price than residents, and which is expanding.
- Neighborhood access and photography limits.
- Child fare rules and age bands, which feed the budget work.
- Entry authorization for US visitors, with the scam warning from 5.5.
- The travel-related taxes in motion, from 5.5.

**Open the file by saying why it exists**, in one or two sentences: this category has been
changing unusually fast, so it is "re-check close to travel" rather than "set it once",
which is a slightly stronger instruction than the general verify habit.

**Cross-link it from three places**, which the archived record names: the reservation
surface, the transit surface, and the budget child-fare note. Those are framework sessions
this batch may not edit, so the links this batch creates run **from** the pack:
`access_and_pricing_watch.md` is linked from `transportation_basics.md` (already in scope
under `B3-4`), `adult_logistics.md`, and the `42_reservation_examples.md` slot. Record in section 8 that
the three framework-side pointers are a Batch 4 item.

---

## 6. The eight insert slots

Every slot opens with the `markdownlint-disable MD013` comment, an H1, and the
`**Last reviewed:**` line. Every slot is short. Read `10_snapshot_facts.md`,
`11_regions_overview.md` and `12_seasons_and_events.md` first: they are the built model
for length, register and how a slot points at its reference.

**The contract's field list is the specification for each slot.** What follows adds the
framing each consuming session needs, which the contract does not carry.

### 6.1 `16_18_candidate_cities.md`

Consumed by Sessions 16, 17 and 18. **Fields:** two to four first-trip candidate cities,
each with a one-line draw; then a pointer to `major_cities.md` for the kid-magnet ideas
and for anything whose opening or availability changes.

- **Candidates to research, never a shortlist.** The sessions are built on the child
  choosing, with one near-certain anchor kept for a first trip and free choice among the
  rest. A slot that ranks them has made the choice.
- **The anchor is named here, not in the session.** Session 16 says the Destination Notes
  name the anchor and the session never does. So this slot must actually mark which
  candidate is the first-trip anchor, or Session 16 points at an absent fact.
- **Stay at two to four** (`I-4`). Three sessions were authored against that range.

### 6.2 `19_other_places_menu.md`

Consumed by Session 19. **Fields:** a menu of further candidate places beyond the
deep-dive cities, each with a one-line draw, offered as options to research.

- **Point at `major_cities.md` rather than copying its menu** (`B3-5`). The contract says
  this in as many words; the built reference already carries "Other places people
  research".
- **Carry the three kinds the session is built on:** well-known places, high-draw kid
  options, and **low-cost everyday high-engagement options**. The third is the one a slot
  author drops, and it is the one the session's teaching point rests on.
- **Leave room for the child's own discovery.** One line saying the menu is a starting
  point and a place they found themselves counts.

### 6.3 `23_attraction_ideas.md`

Consumed by Session 23. **Fields:** starter attraction ideas as options to research,
mixing high-draw named attractions with low-cost everyday ones, each with what kind of
visit it is; anything ticketed, timed or permit-gated flagged "verify". No prices, no
hours.

- **Both halves of the mix are required** (`B3-7`). The high-draw names are the ones a
  child already wants; the everyday options -- a long-distance train ride taken as an
  experience, conveyor-belt sushi, capsule-toy machines, vending machines, game centres,
  a themed cafe, a major aquarium -- are what makes "famous is not the only good" true
  rather than asserted.
- **The stamp book belongs here.** A shrine and temple stamp book is a real collection
  that grows during the trip and has built-in etiquette, because it is a religious
  practice: visit respectfully first, there is a small fee, and the custom is verified
  currently. It is also a natural thing for the child to plan with their own spending
  money, which connects to the budget teaching.
- **Name operators, not venues, where venues move** (`B3-7` and rule 1.2). The immersive
  art operator whose venues open, close and relocate is named as an operator with a
  pointer to its official site, never as one fixed venue.
- **Flag the advance-booking cases** as the teaching example they are: these are what
  Session 42's reservation work is about.

### 6.4 `30_transport_specifics.md`

Consumed by Session 30. **Fields:** the transport modes a child plans around, named
(long-distance, local, walking, taxis), so the child can sort a day's travel; then a
pointer to `transportation_basics.md` for the rest.

- **Name the modes and stop.** The stored-value card options, luggage forwarding, station
  lockers, pass value and route-planning tools all live in the reference. The slot points.
- **Session 30 carries the second predict-then-verify anchor**, where the child guesses a
  train time between two of their cities before checking a current planner. The slot must
  therefore make clear that a route planner is the thing to check, without pinning any
  journey time. **A slot that states a journey time has answered the exercise.**

### 6.5 `34_lodging_types.md`

Consumed by Session 34. **Fields:** the lodging categories a family chooses among, one
line each; then a pointer to `adult_logistics.md` for the occupancy reality.

- **Categories the child can sort:** the business or family hotel, the traditional inn,
  apartment-style and licensed rental lodging, and the hostel or guesthouse.
- **One line each, and no prices and no named properties.**
- **The occupancy reality is pointed at, not explained** (section 3.2). It is the clearest
  case in the batch of a fact with one home.

### 6.6 `36_37_food_ideas.md`

Consumed by Sessions 36 and 37, both Conditional Core. **Fields:** food types and dining
areas as ideas to research; what a family may have to plan around. No restaurant
recommendations, no prices.

- **Dining areas as areas, not addresses:** the kind of district a family finds food in,
  and what distinguishes them.
- **Point at `food_basics.md`** for how ordering works and for the everyday-delight
  framing.
- **Both sessions are conditional**, so the slot must read as complete for a family that
  does 36 and skips 37, and the other way round.

### 6.7 `42_reservation_examples.md`

Consumed by Session 42. **Fields:** a few experiences that require committing to a date to
reserve, each with roughly how far ahead and what kind of gate it is, all framed as
categories to re-check rather than current values. No release dates, no prices.

- **"Roughly how far ahead" is the hard part of this slot.** Write the shape -- some open a
  fixed window before the date, some sell out the moment they open, some are lotteries --
  and never a current window, which is exactly the value that moves.
- **Link `access_and_pricing_watch.md` from here** (5.7).
- **This slot has no reference file.** The contract's Reference column reads `none`, so
  Session 42 writes the Destination Notes phrase and nothing else, and this slot carries
  its own depth rather than pointing.

### 6.8 `47_language_etiquette.md`

Consumed by Session 47, Conditional Core. **Fields:** a short set of everyday phrases; the
etiquette points a visiting family actually meets; any custom with rules of its own
(bathing, photography, sacred sites), described matter-of-factly and never as something
the child will get wrong.

- **Name the customs with rules of their own, one line each, and point at
  `etiquette_basics.md`** (`B3-3`). The bathing content in particular is reference depth
  with an adult-owned judgment attached.
- **The phrase set here is the pocket version** of `language_basics.md`'s: the handful a
  child would actually try, with the pronunciation guide. Do not reproduce the full set.
- **This is the slot `AC-16-1`'s human half bites hardest.** Read rule 1.4 again before
  drafting it, and read it again after.

---

## 7. Acceptance criteria governing every file in this batch

| ID | Tier | What it checks here |
| --- | --- | --- |
| `AC-22-1` | human | The pack gives orientation, defines concepts, suggests research questions, points to trusted sources, and makes **no** final recommendations and no itinerary |
| `AC-29-1` | human | Every slot the contract names exists and supplies its named fields; no orphan slots; every place-needing session is routed to something that exists |
| `AC-29-2` | grep + human | No trip, origin or roster values anywhere in `destinations/` |
| `AC-16-1` | grep + human | The human half: cultural and etiquette content reads matter-of-fact, never marveling. **Bites `etiquette_basics.md` and `47_language_etiquette.md` hardest** |
| `AC-21-3` | human | Adult-owned responsibilities clearly marked; legal, safety and current requirements never stated as fixed without a verify frame |
| Freshness | automatic | Every new reference file and every new slot carries a `**Last reviewed:** <month year>` line below its title |
| `AC-GLOBAL-3` | automatic | Markdownlint passes except MD013 and MD034; MD040 and MD026 stay enabled and pass; **all relative links resolve** |
| `AC-GLOBAL-4` | automatic | No trip data committed |
| `AC-GLOBAL-5` | human | All Markdown meaningful and non-thin; no stub slots |
| `AC-GLOBAL-6` | human | No copyrighted guidebook content. **This bites here:** a pack describing attractions and food is the batch most likely to reproduce someone's guidebook. Write from category knowledge and point at official sources |
| `AC-3.1-1` | human | Child-read parts on target for reading level; warm and non-othering |
| Reader economy | human | No fact has two homes. Each new file's overlap with its built neighbour is a pointer, not a restatement |

---

## 8. The changelog record, and what to do with findings you cannot fix

**`framework/CHANGELOG.md` gets this batch's entry**, under `Unreleased`, and it records:

- **What was added**, by group: the seven reference files, the eight slots, and what the
  pack can do now that it could not before.
- **The departures.** `B3-1`'s extra file, and the inherited `I-1` filename correction if
  no earlier entry already carries it. Check before writing: Batch 2's record may already
  have it, and a duplicate entry is worse than none because it reads as a second change.
- **The contract conversion**: inline-code filenames became links, and the pack is now
  fully routed.
- **The edits to built files**: the transport file's arrival-day section (`B3-4`), the
  glossary additions (`B3-6`), and the pack contents page.
- **What is still owed**: the three framework-side pointers to the watch file, which are
  Batch 4's (5.7).

**Findings you cannot fix belong in this brief's own record, not in a framework edit.**
This batch may not touch `framework/` beyond the changelog. If a session reads wrongly
against a pack file -- it asks for a fact the contract does not route, or it names a
reference the pack does not have -- write it down as a Batch 4 item in the changelog's
"still owed" line and in the run's decision record. **Do not fix it by widening this
batch's scope**, and do not fix it by bending the pack file to match a session that is
wrong.

---

## 9. Validation gates and definition of done

### Gates, all four, before every pull request

```text
pre-commit run --all-files
npm run lint:md
npm run lint:md:nested
npm run lint:md:links
```

**All four.** The link check is the one that gets skipped, and it is the one that catches
a contract link converted before its target exists.

### The batch's own checks

```text
grep -rwE 'Chicago|ORD|grandmother|uncle' destinations/
grep -rwE '17[ -]?(day|night)s?' destinations/
grep -rLn 'Last reviewed' destinations/japan/reference/ destinations/japan/session_inserts/
grep -rn '`[a-z_0-9]*\.md`' destinations/japan/session_inserts/README.md
```

The first two find nothing. The third lists files with no freshness stamp and should name
only `README.md` in each directory, which carry routing rather than facts. The fourth
lists filenames still written as inline code in the contract, and after this batch it
should be empty (section 3.3).

### Done when

- All twenty files created or edited, each to its specification in sections 5 and 6.
- Every contract row routes to a file that exists, and every contract filename is a link.
- The four gates pass, and the batch's own checks return what section 9 says they should.
- Every new file carries its freshness stamp.
- An adversarial review subagent has read the pack's child-facing parts against rule 1.4
  and `AC-3.1-1`, and its findings are fixed. This stands in for the human read under the
  recorded pilot deferral; it does not replace it, and the deferral flag stays.
- `framework/CHANGELOG.md` carries the entry in section 8.
- Pull requests merged through the project's review loop, CI green.

---

## BUILD RULES (hard constraints)

- **Build at the repository root.** Leave `docs/spec/` and the repository's template and CI
  infrastructure untouched.
- **File scope.** This run may create and edit only the files named in section 2. A file
  absent from that list does not get written. If the work seems to require one that is
  absent, that is a finding for section 8, not a permission.
- **Protected instruction files are never edited.** `.github/copilot-instructions.md`,
  anything under `.github/instructions/` or `.cursor/rules/`, and the root agent files
  (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.hermes.md`). If a fix appears to require one,
  stop and escalate.
- **No secrets, no credentials, no tokens** in any file or any commit.
- **The destination-leak rule is on for `framework/` and off for `destinations/`.** That is
  the whole point of the split. Naming Japan in a pack file is correct; naming it in a
  framework session is a defect.
- **Never weaken a check to make something pass**, and never use `--no-verify`.
- **No formatting-only or lint-only commits.** Auto-fixes ride with the change that caused
  them.
- **Every volatile fact is verify-framed**, per rule 1.2. This is the rule a reviewer will
  test most, because it is the one that decides whether the pack is worth shipping to
  anyone else.

---

## Stop and hand off

**Stop when section 9's "done when" list is satisfied.** Hand back: a short build report
naming every file created and edited, the findings recorded under section 8 that Batch 4
inherits, and the state of the contract -- specifically, that every row now routes to a
file that exists, which is the first moment in this project that has been true.

**Do not proceed into Batch 4.** Batch 4 is the optional tier and the closing whole-repo
consistency pass: Session 54, the worked examples, the cross-reference map, the
add-a-destination guide, the optional-item adjudications, and the final pass over every
built file. It is a different kind of work and it wants a fresh context window and its own
brief.
