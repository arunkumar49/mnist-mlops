# ADR-0004: Public GitHub repository

- Status: Accepted
- Date: 2026-10-02

## Context
Branch protection, environment approval gates, and generous Actions minutes are
needed for an enterprise-style workflow. On GitHub's free plan these are
available for public repositories; private repositories need a paid plan.

## Decision
Host the project in a public repository. Enable secret scanning with push
protection and Dependabot alerts. Enforce gitleaks in pre-commit and CI.

## Consequences
Everything committed is public. Secrets, access keys, and account IDs must
never be committed; configuration that identifies the account is supplied at
runtime from SSM Parameter Store or CI variables.