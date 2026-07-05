# EFingPlanner

**A self-guided executive-function ("EF-ing") curriculum for kids — roughly ages 9–11 — that teaches how to break a big, scary project into doable steps by planning a real family trip to Japan.**

The trip is the hook; the real subject is *executive function*: planning, sequencing, estimating, tracking progress, making decisions with incomplete information, and knowing what to do when you get stuck. A child works through short Markdown "sessions" mostly on their own, with light adult coaching, and comes out the other side having actually planned a trip — and having practiced the skills that make any large project less overwhelming.

## Status

Early. This repository currently holds the **design record** for the curriculum, not the finished curriculum. The sessions, guides, and reference pages are authored from that design record as a separate, ongoing effort.

- The authoritative design is in [docs/spec/specification.md](docs/spec/specification.md) — an *archived design record*. Once the curriculum is built, the built repository supersedes the spec on any conflict.
- The curriculum content (the `framework/` and `destinations/japan/` trees described below) is **not built yet**. Follow the repository's issues for build progress.

## How the finished curriculum is meant to be used

By design, using the curriculum requires **no software** — no Node, Python, package managers, or command-line tools. You will be able to:

- read the Markdown sessions directly on GitHub,
- print them, or
- copy them into a document editor (e.g., Google Docs) and fill them in.

A child copies the blank "trip starter kit" out of the repository and does their real trip work **outside** version control; the family's actual trip details are never committed here.

## Planned repository layout

The design (spec §9) organizes the repository into three layers:

- `framework/` — Layer 1: the reusable, destination-agnostic curriculum (sessions, templates, student and parent guides).
- `destinations/japan/` — Layer 2: the Japan knowledge pack (stable reference facts and the notes the generic sessions pull in).
- the **trip layer** — Layer 3: the family's real trip work, copied out of a blank starter kit and *never committed*.

Only `framework/` and `destinations/japan/` will be built in this repository; the trip layer lives on the family's own computer.

## Repository housekeeping

Everything above is the *content*. The rest of the repository is lightweight maintainer tooling that keeps the Markdown healthy — it is **not** required to use the curriculum:

- `docs/spec/` — the archived design record.
- `.markdownlint.jsonc`, `.github/workflows/` — Markdown linting and offline link-checking.
- `.pre-commit-config.yaml`, `.template-sync/`, `schemas/` — pre-commit hooks and the template-sync support this repository was created from.

## Contributing and community

- [Contributing guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)

## License

The contents of this repository are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** — see [LICENSE](LICENSE).

**Educators and nonprofits:** classroom, school, library, homeschool-co-op, and nonprofit use is explicitly welcome. Most such use is already permitted by the license, and the author will grant a free license for good-faith educational use that falls outside it, on request via the contact links on the maintainer's public GitHub profile ([@franklesniak](https://github.com/franklesniak)). The copyright holder may grant separate permissions without changing the public license that applies to everyone else. See [LICENSING.md](LICENSING.md) for details.
