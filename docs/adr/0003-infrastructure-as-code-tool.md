# ADR-0003: Terraform for infrastructure as code

- Status: Proposed
- Date: 2026-10-02

## Context
All AWS resources must be defined in code, reviewed in pull requests,
scanned for misconfigurations, and reproducible across dev and prod.

## Decision
Use Terraform 1.11+ with an S3 remote backend and S3 native state locking.
Use one root module per environment (`infra/envs/dev`, `infra/envs/prod`)
built from shared modules (`infra/modules`). Scan with Checkov in CI.

## Alternatives considered
- AWS CDK (Python): same language as the app and CloudFormation-managed state,
  but AWS-only, needs Node.js and a bootstrap stack.
- OpenTofu: open-source Terraform fork; a drop-in option if licensing matters.

## Consequences
The state bucket must be created once by a small bootstrap configuration.
`terraform plan` output is posted to pull requests for review.