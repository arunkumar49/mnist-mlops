# mnist-mlops

An MNIST digit classifier built the way an enterprise ML team would build it:
first as a from-scratch NumPy MLP, then in PyTorch, trained and served on AWS
with infrastructure as code, data and model versioning, CI/CD, and monitoring.

## Status

| Phase | Scope | Status |
|---|---|---|
| 0 | Foundations: AWS security baseline, budgets, tooling, repo | In progress |
| 1 | Repo scaffolding and first CI | Not started |
| 2 | Infra foundations as code | Not started |
| 3 | Data versioning and validation | Not started |
| 4 | NumPy MLP from scratch | Not started |
| 5 | PyTorch and SageMaker training | Not started |
| 6 | SageMaker Pipeline and Model Registry | Not started |
| 7 | Serving | Not started |
| 8 | Full CI/CD | Not started |
| 9 | Observability | Not started |
| 10 | Wrap-up and rebuild-from-code | Not started |

## Ground rules

- No secrets, access keys, or AWS account IDs in this repository.
- All AWS resources are created from code and can be destroyed and recreated.
- Every significant decision is recorded in `docs/adr/`.

## Local prerequisites

WSL2 (Ubuntu 24.04), Docker Desktop with WSL integration, AWS CLI v2.32+,
uv with Python 3.12, Terraform 1.11+, GitHub CLI.

AWS access uses short-lived credentials from `aws login --profile mnist`.