# Contributing to This Project

Thank you for your interest in contributing. This document describes the retained contributor workflow, validation expectations, and pull-request readiness checks for this repository.


## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/franklesniak/EFingPlanner.git
cd EFingPlanner
```

### 2. Install Node.js Dependencies

Install Node.js dependencies for Markdown linting scripts:

```bash
npm install
```

Git hooks are managed by pre-commit.

### Install Python

`pre-commit` is installed and run through `pip`/`pipx`, and the template-sync helper scripts run on Python, so a working Python 3 interpreter is required even when your project does not adopt the Python module:

```bash
python --version
```


### 3. Install Pre-commit

Install `pre-commit` globally using **one** of the following. With `pip`:

```bash
pip install pre-commit
```

Or, for isolated tooling, with `pipx`:

```bash
pipx install pre-commit
```

`pre-commit` manages isolated hook environments, so it does not need to be installed as a project runtime dependency.

### 4. Install Git Hooks

```bash
pre-commit install
```

### 5. Run Pre-commit Manually

Run all hooks across the whole repository:

```bash
pre-commit run --all-files
```

Or run hooks against only the staged changes:

```bash
pre-commit run
```

Run the all-files form before opening a pull request.

## Git Hooks

This repository uses pre-commit for git hooks. Configured hooks include:

- **Formatting:** trailing whitespace and end-of-file fixes.
- **Markdown linting:** markdownlint and local Markdown link validation.
- **Data-file validation:** `check-json` for strict `.json` files, `check-yaml`, and `actionlint` for GitHub Actions workflows.
<!-- template-sync: begin yaml-reference-only -->
- **YAML style validation:** `yamllint` configured by `.yamllint.yml`.
<!-- template-sync: end yaml-reference-only -->
- **Schema validation:** When schema-backed modules (the schema or template-sync support module) are retained, `check-jsonschema` and `check-metaschema` validate retained schema-backed configuration, including template-sync schemas.
<!-- template-sync: begin schema-reference-only -->
- **Worked-example schema validation:** `check-jsonschema` and `check-metaschema` also cover the worked-example schema and its valid fixtures. See [`schemas/README.md`](schemas/README.md) for the worked example and downstream removal checklist.
<!-- template-sync: end schema-reference-only -->
- **Safety:** large file detection.

**`check-json` validates strict `.json` only.** It does **not** validate `.jsonc`. JSONC files are allowed only when the consuming tool supports JSONC; downstream repositories that need stricter `.jsonc` enforcement should add JSONC-aware tooling rather than retrofitting `check-json`.

<!-- template-sync: begin json-reference-only -->
See [`.github/instructions/json.instructions.md`](.github/instructions/json.instructions.md) for the full JSON/JSONC dialect policy.
<!-- template-sync: end json-reference-only -->
<!-- template-sync: begin yaml-reference-only -->
See [`.github/instructions/yaml.instructions.md`](.github/instructions/yaml.instructions.md) for YAML authoring standards.
<!-- template-sync: end yaml-reference-only -->

**`actionlint` first-run-on-restricted-networks caveat.** The `actionlint` pre-commit hook builds the `actionlint` binary from source on first install, which downloads a Go toolchain. On networks that block Go module downloads, the first-run install can fail. CI is the shared enforcement environment, so contributors who hit a network restriction locally can rely on CI to enforce this hook. The same caveat is documented inline in `.pre-commit-config.yaml` and in [`.github/TEMPLATE_DESIGN_DECISIONS.md`](https://github.com/franklesniak/copilot-repo-template/blob/HEAD/.github/TEMPLATE_DESIGN_DECISIONS.md).


If you need to bypass hooks temporarily, which is not recommended:

```bash
git commit --no-verify -m "your message"
```

## Manual Validation

### Markdown Linting

```bash
npm run lint:md
npm run lint:md:links
npm run lint:md:nested
```

<!-- template-sync: begin template-sync-support-reference-only -->
### Template-Sync Validation

When template-sync support is retained, use the downstream validator after module pruning or marker changes:

```bash
python .template-sync/scripts/validate_downstream_adoption.py --require-marker
```

For cleanup planning, run the excluded-module reporter:

```bash
python .template-sync/scripts/report_excluded_module_references.py
```
<!-- template-sync: end template-sync-support-reference-only -->

## Code Quality Standards

### Pre-commit Discipline

**Always run pre-commit checks before committing code.**

Pre-commit hooks are not optional. They enforce:

- Formatting and end-of-file hygiene.
- Markdown linting and local Markdown link validation.
- Data-file validation for strict `.json`, YAML parsing, and GitHub Actions workflows.
<!-- template-sync: begin yaml-reference-only -->
- YAML style validation through `yamllint`.
<!-- template-sync: end yaml-reference-only -->
- Schema validation for retained schema-backed file families.

> **Network and dialect notes:**
>
> - First-run hook setup may require network access.
> - `check-json` validates strict `.json` files only and does **not** validate `.jsonc`.
> - CI runs the same hooks and is the shared enforcement environment.
> - Auto-fixes produced by hooks **must** be committed with the related change.

See `.pre-commit-config.yaml` for the complete list of configured hooks.

**Workflow:**

1. Make your code changes.
2. Run `pre-commit run --all-files`.
3. Review and commit all auto-fixes as part of your change.
4. Push to GitHub.

**If pre-commit CI fails:**

1. Pull the latest branch.
2. Run `pre-commit run --all-files` locally.
3. Integrate the auto-fixes into the commit that introduced the change.
4. Push again.

CI is a safety net, not a substitute for local checks.

### Language-Specific Guidelines

This repository includes coding standards for retained languages and data file formats:

- **Markdown/Documentation:** [`.github/instructions/docs.instructions.md`](.github/instructions/docs.instructions.md)
- **Git attributes:** [`.github/instructions/gitattributes.instructions.md`](.github/instructions/gitattributes.instructions.md)
<!-- template-sync: begin json-reference-only -->
- **JSON/JSONC:** [`.github/instructions/json.instructions.md`](.github/instructions/json.instructions.md)
<!-- template-sync: end json-reference-only -->
<!-- template-sync: begin yaml-reference-only -->
- **YAML:** [`.github/instructions/yaml.instructions.md`](.github/instructions/yaml.instructions.md)
<!-- template-sync: end yaml-reference-only -->

These standards apply to all contributions in the retained file families and are enforced by the repository's pre-commit hooks and CI workflows.

### Template Taxonomy Updates

When a change adds, removes, renames, moves, or changes the primary purpose of a template-managed file, update the downstream sync path mapping in `TEMPLATE_UPDATE_PROCEDURE.md` as part of the same change. See [Reviewing the Template Sync Module Taxonomy](https://github.com/franklesniak/copilot-repo-template/blob/HEAD/TEMPLATE_MAINTENANCE.md#reviewing-the-template-sync-module-taxonomy) for the maintainer checklist.

### Data-File and Schema Validation

Data files and GitHub Actions workflow files are first-class validation surfaces. Contributor expectations:

- Run `pre-commit run --all-files` before opening a PR.
- Strict `.json` files must pass `check-json`; `.jsonc` is intentionally not validated by that hook.
- YAML files must pass `check-yaml`.
<!-- template-sync: begin yaml-reference-only -->
- YAML files must also pass `yamllint` when the YAML module is retained.
<!-- template-sync: end yaml-reference-only -->
- GitHub Actions workflow files must pass `actionlint`.
- Schema-backed files must pass `check-jsonschema`, and retained schemas must pass `check-metaschema` where configured.
<!-- template-sync: begin schema-reference-only -->
- The worked-example schema contracts under `schemas/examples/<schema>/{valid,invalid}/` are tested by [`tests/test_schema_examples.py`](tests/test_schema_examples.py); when changing a schema or its example fixtures, run `pytest tests/test_schema_examples.py -v`.

See [`schemas/README.md`](schemas/README.md) for schema conventions and the canonical downstream removal checklist for the worked example.
<!-- template-sync: end schema-reference-only -->

### CI Workflows

This repository includes retained GitHub Actions workflows that run automatically:

- **Pre-commit CI** (`.github/workflows/precommit-ci.yml`) - Runs the aggregate `pre-commit run --all-files` gate over every hook in `.pre-commit-config.yaml`.
- **Auto-fix Pre-commit** (`.github/workflows/auto-fix-precommit.yml`) - Automatically commits pre-commit auto-fixes on Copilot-agent branches when the workflow conditions match.
- **Markdown Lint** (`.github/workflows/markdownlint.yml`) - Validates Markdown formatting and local links.
<!-- template-sync: begin data-ci-reference-only -->
- **Data CI** (`.github/workflows/data-ci.yml`) - Runs retained baseline placeholder, data-file, GitHub Actions, template-sync, and schema validation hooks.
<!-- template-sync: end data-ci-reference-only -->

The **Auto-fix Pre-commit** workflow is scoped specifically to the GitHub Copilot Coding Agent. Human-authored PRs and PRs on non-`copilot/**` branches are not affected; their authors must run `pre-commit run --all-files` locally and integrate the fixes themselves before pushing.

### Workflow Version Pinning

When editing files under `.github/workflows/`, follow the [**Workflow Version Pinning**](.github/copilot-instructions.md#workflow-version-pinning) rule in the repo-wide constitution. In short:

- Keep third-party action versions directly in `uses:` lines so Dependabot can update them.
- Do **not** mirror a `uses:` version into a workflow-level `env:` variable, comment, cache key, file path, or shell literal.
- For tool versions that Dependabot does not manage, a workflow-level `env:` value is a fine single source of truth across multiple steps.
- If a Dependabot-managed dependency genuinely cannot be expressed without duplication, add a narrowly scoped `.github/dependabot.yml` `ignore:` entry with a YAML comment explaining why.

## Making Changes

### 1. Create a Branch

```bash
git checkout -b your-feature-branch
```

### 2. Make Your Changes

Follow the coding standards for the language or file type you are changing.

### 3. Run Pre-commit Hooks

```bash
pre-commit run --all-files
```

Fix any issues that are reported.

### 4. Run Tests

Before submitting a pull request, ensure the retained test suites pass locally.

#### Test Requirements

- The tests wired into CI (the Data CI schema-guard checks and the Markdown checks) must pass. The broader template-sync QA suite under `tests/` is not CI-gated.

### 5. Commit Your Changes

```bash
git add .
git commit -m "Your descriptive commit message"
```

Pre-commit hooks will run automatically. If they make changes, review them and commit again.

### 6. Push Your Branch

```bash
git push origin your-feature-branch
```

### 7. Open a Pull Request

Open a PR on GitHub and fill out the PR template checklist.

## Pull Request Guidelines

When submitting a pull request:

- [ ] Confirm `pre-commit run --all-files` passes locally.
- [ ] Include tests for new functionality.
- [ ] Update documentation as needed.
- [ ] Ensure all CI checks pass.
- [ ] Confirm no secrets, credentials, tokens, or connection strings were committed.

## Questions or Issues?

If you have questions or encounter issues:

1. Check existing [Issues](https://github.com/franklesniak/EFingPlanner/issues).
2. Review the retained documentation in `.github/instructions/`.
3. Open a new issue with a clear description of the problem.

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). See [LICENSE](LICENSE) and [LICENSING.md](LICENSING.md).
