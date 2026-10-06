from mnist_mlops.application.dto import BuildInfo
from mnist_mlops.infrastructure.build_info_provider import SettingsBuildInfoProvider
from mnist_mlops.infrastructure.config import Environment, Settings


def test_maps_settings_to_build_info() -> None:
    settings = Settings(environment=Environment.DEV, git_sha="abcdef1")

    info = SettingsBuildInfoProvider(settings=settings, version="9.9.9").get_build_info()

    assert info == BuildInfo(
        service_name="mnist-mlops",
        version="9.9.9",
        environment="dev",
        aws_region="ap-south-1",
        git_sha="abcdef1",
    )
