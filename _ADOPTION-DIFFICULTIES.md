<!-- markdownlint-disable MD013 -->
# Adoption Difficulties Journal

This journal records process and difficulty evidence from first adoption. It does not replace `_TODO-repo-init.md` decision state, and it does not replace `.template-sync/marker.yml` sync state.

Use `_TODO-repo-init.md` for maintainer decisions and unresolved policy questions. Use `.template-sync/marker.yml` for retained modules, local overrides, protected-file decisions, and reviewed template commit state. Use this journal for what made the adoption hard, risky, blocked, or surprising.

After context loss, interruption, or compaction, reread this journal, `_TODO-repo-init.md`, `.template-sync/marker.yml` when present, and the current repository state before continuing.

## Entries

### 2026-07-05 PR #5 review - This journal file was missing despite being listed as a delivered artifact

- **What happened:** The PR #5 description ("Adoption artifacts" section) lists `_ADOPTION-DIFFICULTIES.md` as created, but the file was never committed to the `chore/template-initialization` branch (`git log --all -- _ADOPTION-DIFFICULTIES.md` returns nothing; only `_TODO-repo-init.md` and the template `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md` exist). It was (re)created during the PR #5 review loop at the maintainer's request.
- **Why it mattered:** The PR body's claimed deliverables did not match the tree, so the first-adoption difficulty evidence the template process expects was absent.
- **Impact or risk:** Loss of adoption context; a reviewer trusting the PR description would assume the journal already existed.
- **Resolution or workaround:** Recreated the file from `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md` and back-filled the entries below from the review-loop findings.
- **Follow-up:** When a PR body claims an adoption artifact, confirm it is staged and committed before merge.
- **Related files:** `_ADOPTION-DIFFICULTIES.md`, `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md`, `_TODO-repo-init.md`
- **Related commands:** `git log --oneline --all -- _ADOPTION-DIFFICULTIES.md`

### 2026-07-05 PR #5 review - OWNER/REPO placeholders left unreplaced (CI blocker)

- **What happened:** The `Check for OWNER/REPO Placeholders` required check failed. `.github/scripts/replace-template-placeholders.py scan` flagged unreplaced `OWNER/REPO` tokens in `.github/ISSUE_TEMPLATE/config.yml` (lines 11, 22, 31, 52), `.github/ISSUE_TEMPLATE/bug_report.yml` (line 45), and `CONTRIBUTING.md` (lines 6, 27, 30, 332, 334). The user-facing URLs had already been substituted to `franklesniak/EFingPlanner`, but leftover `OWNER/REPO` tokens survived inside `# CUSTOMIZE:` instructional comments and in CONTRIBUTING.md's clone/issues commands. The scanner treats any `OWNER/REPO` token in a retained-path file as a hard failure regardless of comment context.
- **Why it mattered:** These files are "retained-path" replacement targets, so a single leftover token keeps CI red.
- **Impact or risk:** Red required check; broken clone/issue links would ship if merged as-is.
- **Resolution or workaround:** Removed the now-obsolete `# CUSTOMIZE: replace OWNER/REPO` comments (substitution is complete) and replaced CONTRIBUTING.md's clone/issues commands with real `franklesniak/EFingPlanner` URLs. Verified: `python .github/scripts/replace-template-placeholders.py scan --repo-root . --repository franklesniak/EFingPlanner` now prints "Placeholder scan passed."
- **Follow-up:** Adoption should run placeholder replacement to completion (including comment-embedded tokens), or delete the didactic `# CUSTOMIZE` comments as part of substitution.
- **Related files:** `.github/ISSUE_TEMPLATE/config.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `CONTRIBUTING.md`, `.github/scripts/replace-template-placeholders.py`, `.github/workflows/check-placeholders.yml`
- **Related commands:** `python .github/scripts/replace-template-placeholders.py scan --repo-root . --repository franklesniak/EFingPlanner`

### 2026-07-05 PR #5 review - Markdown CI broke on editable install after Python metadata was removed (CI blocker)

- **What happened:** The `markdownlint` job (`.github/workflows/markdownlint.yml`) failed at its "Install Python dependencies" step running `pip install -e ".[dev]"`. Adoption intentionally stripped all Python packaging metadata from `pyproject.toml` (keeping only `[tool.pytest.ini_options]`), so setuptools flat-layout auto-discovery aborts with: "Multiple top-level packages discovered in a flat-layout: ['schemas', 'templates', 'node_modules']." The workflow still assumed an installable package with a `dev` extra.
- **Why it mattered:** The hard failure occurred before any Markdown linting ran, so the whole Markdown/toolchain gate was red and unenforced.
- **Impact or risk:** Red required check; the nested-Markdown regression and toolchain-EOL tests never executed.
- **Resolution or workaround:** Replaced `pip install -e ".[dev]"` with a direct install of what the retained pytest step needs (`pip install pytest "jsonschema>=4.18.0" "PyYAML>=6.0.3"`), mirroring the direct-install pattern already used in `.github/workflows/data-ci.yml`. This keeps the "Markdown-only, not a Python package" design intent recorded in `pyproject.toml`. The `jsonschema` dependency is required because the `-k passes_nested_markdown_lint` selection runs `.template-sync/scripts/materialize_downstream_adoption.py`, whose validation helper imports `jsonschema`; the now-deleted `[dev]` extra used to supply it. A first pass that omitted `jsonschema` passed on a contaminated local venv but failed in CI ("ERROR: jsonschema is unavailable"), so the dependency set was re-verified in a clean venv containing only `pytest jsonschema PyYAML`.
- **Follow-up:** Adoption that removes Python packaging metadata must also update every workflow that assumed `pip install -e ".[dev]"`, and must re-derive the exact runtime dependency set the retained tests need (here: `jsonschema` and `PyYAML`). Verify in a clean virtualenv, not a developer venv that may already have the packages.
- **Related files:** `.github/workflows/markdownlint.yml`, `pyproject.toml`, `.github/workflows/data-ci.yml`
- **Related commands:** `npm run lint:md`, `pip install pytest "PyYAML>=6.0.3"`

### 2026-07-05 PR #5 review - CONTRIBUTING.md still declared the old MIT license

- **What happened:** Adoption replaced the repository license (`LICENSE`, `LICENSING.md`) with CC BY-NC-SA 4.0, but `CONTRIBUTING.md` still stated "your contributions will be licensed under the same license as the project (MIT License)" and carried a template-adopter comment block referencing MIT.
- **Why it mattered:** Contradictory licensing terms; an outside contributor reading the contribution guide would agree to MIT while the project is CC BY-NC-SA 4.0.
- **Impact or risk:** Legal/licensing ambiguity for contributed content.
- **Resolution or workaround:** Updated the contribution statement to CC BY-NC-SA 4.0 with pointers to `LICENSE` and `LICENSING.md`; removed the obsolete MIT template-adopter comment.
- **Follow-up:** A license change during adoption should sweep every license reference (README, CONTRIBUTING, package.json, issue templates).
- **Related files:** `CONTRIBUTING.md`, `LICENSE`, `LICENSING.md`

### 2026-07-05 PR #5 review - Broken references to the deleted PowerShell module

- **What happened:** Adoption deleted the PowerShell module (`.github/instructions/powershell.instructions.md`, `.github/workflows/powershell-ci.yml`, `.github/linting/PSScriptAnalyzerSettings.psd1`) but left references to those deleted paths in `.github/copilot-instructions.md` (the modular-instructions list line for PowerShell, plus a Pester note) and `CONTRIBUTING.md` (a PowerShell linting bullet, a "PowerShell Validation" section, a "PowerShell CI" workflow bullet, and a "PowerShell Tests" section). The PowerShell line in `.github/copilot-instructions.md` lacked a `template-sync` reference-only marker, so the marker-based trimming that removed the JSON/YAML reference blocks skipped it.
- **Why it mattered:** Canonical agent guidance points future agents at files that no longer exist; the contributor guide advertised PowerShell CI/validation that was removed.
- **Impact or risk:** Confusing/incorrect guidance. Not a CI failure.
- **Resolution or workaround:** Removed the PowerShell references from `CONTRIBUTING.md` (not a protected file). `.github/copilot-instructions.md` is a protected instruction file, so its PowerShell reference removal was escalated to the maintainer for explicit authorization before editing rather than changed unilaterally.
- **Follow-up:** The upstream template should wrap the PowerShell instruction-list line and the Pester note in `.github/copilot-instructions.md` with `template-sync` reference-only markers so downstream trimming removes them automatically when the PowerShell module is excluded.
- **Related files:** `.github/copilot-instructions.md`, `CONTRIBUTING.md`
- **Related commands:** `ls .github/instructions/ .github/workflows/`

### 2026-07-05 PR #5 review - check-jsonschema version pinned in two places

- **What happened:** `.github/workflows/data-ci.yml` installed `check-jsonschema==0.37.3` as a hardcoded pin, duplicating the `rev: "0.37.3"` in `.pre-commit-config.yaml`. `tests/test_dependabot_schema.py::test_regression_check_jsonschema_matches_pinned_pre_commit_rev` asserts the installed version equals the pre-commit rev, so the next Dependabot bump of the pre-commit hook would break Data CI until someone also hand-edited data-ci.yml.
- **Why it mattered:** One logical version was expressed in two files that Dependabot updates asymmetrically, creating latent CI breakage.
- **Impact or risk:** Future red Data CI after an otherwise-correct Dependabot bump.
- **Resolution or workaround:** Added `.github/scripts/pinned-check-jsonschema-rev.py` (mirrors the test's extraction logic) and changed data-ci.yml to derive the install version from the single pinned source in `.pre-commit-config.yaml`.
- **Follow-up:** Prefer deriving tool versions from one Dependabot-managed source rather than duplicating pins across a workflow and config.
- **Related files:** `.github/workflows/data-ci.yml`, `.github/scripts/pinned-check-jsonschema-rev.py`, `.pre-commit-config.yaml`, `tests/test_dependabot_schema.py`
- **Related commands:** `python .github/scripts/pinned-check-jsonschema-rev.py`

### 2026-07-05 PR #5 review - Prohibited-placeholder hook did not cover its documented curriculum paths

- **What happened:** The `check-prohibited-placeholders` hook in `.pre-commit-config.yaml` was scoped to `files: ^docs/.*\.md$`, and `.github/scripts/check-prohibited-placeholders.py` `is_scan_target()` hardcoded `parts[0] == "docs"`. Yet an inline comment claimed "the built curriculum lives under framework/ and destinations/, which this hook still guards." Those roots do not exist yet (curriculum authoring is future work) and were not actually guarded.
- **Why it mattered:** Once curriculum content lands under `framework/` and `destinations/`, prohibited placeholders (TODO/TBD/FIXME) would silently pass unchecked, contradicting the documented intent.
- **Impact or risk:** Future unguarded placeholders in shipped curriculum. Not a current CI failure.
- **Resolution or workaround:** Expanded the hook `files:` regex to `^(docs|framework|destinations)/.*\.md$` and updated `is_scan_target()` to accept those roots (docs/spec/ still excluded via the hook `exclude:`). Added regression tests for `framework/` and `destinations/`.
- **Follow-up:** Keep the hook scope and the checker's accepted roots in sync with the documented content layout as curriculum directories are created.
- **Related files:** `.pre-commit-config.yaml`, `.github/scripts/check-prohibited-placeholders.py`, `tests/test_check_prohibited_placeholders.py`
- **Related commands:** `python -m pytest tests/test_check_prohibited_placeholders.py -q`
