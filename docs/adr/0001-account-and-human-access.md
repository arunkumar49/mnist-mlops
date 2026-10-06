# ADR-0001: Single AWS account with short-lived human credentials via `aws login`

- Status: Accepted
- Date: 2026-10-02

## Context
Enterprises use AWS Organizations with separate dev/staging/prod accounts and
IAM Identity Center for workforce sign-in. This account is new and holds Free
Tier credits. Enrolling in AWS Organizations upgrades a Free Plan account to the
Paid Plan and forfeits the credits immediately. Account instances of IAM
Identity Center cannot grant access to AWS accounts; that requires an
organization instance.

## Decision
- Use one AWS account for now.
- The root user is protected with MFA, has no access keys, and is used only for root-only tasks.
- Humans use an IAM user (`mlops-admin`) with console access, MFA, and no access keys.
- CLI and SDK access uses `aws login`, which issues short-lived, auto-rotating credentials.
- Workloads and CI use IAM roles only (GitHub via OIDC).
- dev and prod are separated by Terraform stacks, resource naming, and tags.

## Alternatives considered
- Organizations + Identity Center now: the true enterprise pattern, but loses the credits.
- IAM user with access keys: rejected, because long-lived keys are the top cause of account compromise.

## Consequences
- No hard account boundary between dev and prod; an IAM mistake can affect both.
- Migrating to Organizations + Identity Center is planned for Phase 10, or when the credits are used up.
