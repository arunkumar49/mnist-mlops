"""Ports: what the use cases need from the outside world, described as interfaces."""

from typing import Protocol

from mnist_mlops.application.dto import BuildInfo


class BuildInfoProvider(Protocol):
    """Anything with a get_build_info() method fits this port."""

    def get_build_info(self) -> BuildInfo: ...
