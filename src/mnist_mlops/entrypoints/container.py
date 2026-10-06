"""Composition root: the one place that creates real suppliers and hands them to use cases."""

from dataclasses import dataclass

from mnist_mlops import __version__
from mnist_mlops.application.use_cases.get_build_info import GetBuildInfo
from mnist_mlops.infrastructure.build_info_provider import SettingsBuildInfoProvider
from mnist_mlops.infrastructure.config import Settings, get_settings


@dataclass(frozen=True, slots=True)
class Container:
    """Everything an entrypoint needs, fully wired."""

    settings: Settings
    get_build_info: GetBuildInfo


def build_container(settings: Settings | None = None) -> Container:
    """Wire the application. Tests may pass their own Settings; normally the environment is read."""
    resolved = settings if settings is not None else get_settings()
    provider = SettingsBuildInfoProvider(settings=resolved, version=__version__)
    return Container(settings=resolved, get_build_info=GetBuildInfo(provider))
