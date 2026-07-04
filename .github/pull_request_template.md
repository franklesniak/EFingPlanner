## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Dependencies update
- [ ] Configuration/tooling change

## Checklist

<!-- Review and check all items before submitting -->

### General

- [ ] I have read the [contributing guidelines](https://github.com/franklesniak/EFingPlanner/blob/HEAD/CONTRIBUTING.md)
- [ ] My code follows the coding standards in `.github/instructions/`
- [ ] My changes follow `.github/copilot-instructions.md` and any applicable `.github/instructions/*`
- [ ] No secrets, real PII, or production credentials appear in any committed file
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code where necessary, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added or updated tests where appropriate
- [ ] New and existing tests pass locally (where applicable)

### Pre-commit Verification (if configured)

- [ ] If this repository uses pre-commit, I ran `pre-commit run --all-files` and all checks pass
- [ ] If pre-commit made auto-fixes, I reviewed and committed them

<!-- template-sync: begin data-ci-reference-only -->
### Data-File-Specific (if applicable)

- [ ] Retained data-file checks pass locally through `pre-commit run --all-files` or the matching targeted pre-commit hooks
- [ ] No secrets, real PII, or production credentials appear in any committed data file or fixture

<!-- template-sync: end data-ci-reference-only -->
<!-- template-sync: begin schema-reference-only -->
### Schema-Specific (if applicable)

- [ ] If a schema under `schemas/` was modified, the matching `schemas/examples/<schema-name>/{valid,invalid}/` fixtures were updated in the same commit
- [ ] If a schema under `schemas/` was modified, `pytest tests/test_schema_examples.py -v` still passes
- [ ] If a `check-jsonschema` hook was added, removed, or renamed, related validation documentation was reviewed and updated where needed; any updates to protected instruction files (e.g., `.github/copilot-instructions.md`) were coordinated with maintainers per the protected-instruction-files rule

<!-- template-sync: end schema-reference-only -->
<!-- template-sync: begin github-actions-reference-only -->
### GitHub Actions-Specific (if applicable)

- [ ] If a GitHub Actions workflow was modified, `actionlint` passes (run via `pre-commit run actionlint --all-files`)

<!-- template-sync: end github-actions-reference-only -->

## Additional Notes

<!-- Add any additional information that reviewers should know -->

## Related Issues

<!-- Link any related issues using #issue_number -->

Closes #
