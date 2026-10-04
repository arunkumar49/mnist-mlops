"""Use case: report what is running."""

from mnist_mlops.application.dto import BuildInfo
from mnist_mlops.application.ports import BuildInfoProvider


class GetBuildInfo:
    def __init__(self, provider: BuildInfoProvider) -> None:
        self._provider = provider

    def __call__(self) -> BuildInfo:
        return self._provider.get_build_info()
