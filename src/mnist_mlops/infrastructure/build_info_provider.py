"""Adapter: implements the BuildInfoProvider port using Settings."""

from mnist_mlops.application.dto import BuildInfo
from mnist_mlops.infrastructure.config import Settings


class SettingsBuildInfoProvider:
    def __init__(self, settings: Settings, version: str) -> None:
        self._settings = settings
        self._version = version

    def get_build_info(self) -> BuildInfo:
        return BuildInfo(
            service_name=self._settings.service_name,
            version=self._version,
            environment=self._settings.environment.value,
            aws_region=self._settings.aws_region,
            git_sha=self._settings.git_sha,
        )
