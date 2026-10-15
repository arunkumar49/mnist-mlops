# ADR-0005: Clean architecture for application code

- Status: Accepted
- Date: 2026-10-07

## Context
The code will grow from a NumPy network to PyTorch training, SageMaker jobs, MLflow
tracking, S3/DVC data access and a FastAPI service. Without structure, model math gets
tangled with AWS calls and HTTP handling, which makes it hard to test and hard to swap
infrastructure.

## Decision
Organise `src/mnist_mlops` into four layers. Dependencies point inward only:

| Layer | Contains | May import |
|---|---|---|
| `domain` | Pure rules (`DigitLabel`, `Prediction`); from Phase 4 the NumPy network | stdlib, NumPy |
| `application` | Use cases and ports (Protocols describing what use cases need) | `domain` |
| `infrastructure` | Adapters implementing ports: config, logging, S3, MLflow, SageMaker, PyTorch | inner layers, frameworks |
| `entrypoints` | CLI, API, job scripts; `container.py` is the single place that wires adapters into use cases | everything |

The rule is enforced in CI by import-linter contracts in `pyproject.toml`.

## Alternatives considered
- Flat package (`model.py`, `train.py`): fastest to start, but couples everything.
- Feature folders (`training/`, `serving/`) without layer rules: the same coupling reappears inside each folder.

## Consequences
- Use cases are tested with in-memory fakes, so most tests need no AWS and run in milliseconds.
- More files and one level of indirection than a flat script.
