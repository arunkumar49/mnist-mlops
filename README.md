# mnist-mlops

An MNIST digit classifier built the way an enterprise ML team would build it:
first as a from-scratch NumPy MLP, then in PyTorch, trained and served on AWS
with infrastructure as code, data and model versioning, CI/CD, and monitoring.

## Status

| Phase | Scope | Status |
|---|---|---|
| 0 | Foundations: AWS security baseline, budgets, tooling, repo | Done |
| 1 | Repo scaffolding, code quality and CI | Done |
| 2 | Infra foundations as code | Not started |
| 3 | Data versioning and validation | Not started |
| 4 | NumPy MLP from scratch | Not started |
| 5 | PyTorch and SageMaker training | Not started |
| 6 | SageMaker Pipeline and Model Registry | Not started |
| 7 | Serving | Not started |
| 8 | Full CI/CD | Not started |
| 9 | Observability | Not started |
| 10 | Wrap-up and rebuild-from-code | Not started |

## Quick start

```bash
make install               # create .venv from uv.lock, install git hooks
make check                 # lint, types, architecture rules, tests
uv run mnist-mlops info    # print build info as JSON
```

## Code layout

`src/mnist_mlops` follows clean architecture ([ADR-0005](docs/adr/0005-clean-architecture.md)).
Dependencies point inward only, and CI enforces it.
