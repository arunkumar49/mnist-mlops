# Changelog

All notable changes are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Clean-architecture package layout, enforced by import-linter.
- Typed settings (pydantic-settings) and structured JSON logging.
- `mnist-mlops info` command.
- Domain types `DigitLabel` and `Prediction` with validation.
- ruff, mypy (strict), pytest with a 90% coverage gate.
- Pre-commit hooks: lint, types, secret scanning, Conventional Commits.
- CI: quality, test, secrets and PR-title checks.
- Ruleset protecting `main`, code owners, PR and issue templates.
