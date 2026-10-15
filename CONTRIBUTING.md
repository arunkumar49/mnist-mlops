# Contributing

## Setup

```bash
make install    # create .venv from uv.lock and install git hooks
make check      # lint, types, architecture rules, tests
```

## Workflow

1. Branch from an up-to-date `main`: `git switch main && git pull && git switch -c <type>/<short-name>`.
   Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`, `build`.
2. Keep branches small and short-lived.
3. Use Conventional Commit messages, for example `feat(data): add label distribution check`.
4. Open a PR whose title is also a Conventional Commit; it becomes the squash-merge message.
5. Required checks: `quality`, `test`, `secrets`, `pr-title`. Then squash-merge.

## Where code goes

- A rule that is always true: `domain/`
- A workflow step: a use case in `application/use_cases/`, depending on ports in `application/ports.py`
- An external system (S3, MLflow, PyTorch): an adapter in `infrastructure/`
- Wiring adapters into use cases: only `entrypoints/container.py`

## Rules

- No secrets, access keys or AWS account IDs anywhere in the repo.
- Configuration comes from `MNIST_*` environment variables.
- Significant decisions get an ADR in `docs/adr/`.
- Test coverage stays at or above 90%.
