"""Plain data objects passed in and out of use cases."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BuildInfo:
    """What is running, and where."""

    service_name: str
    version: str
    environment: str
    aws_region: str
    git_sha: str | None
