from mnist_mlops.application.dto import BuildInfo
from mnist_mlops.application.use_cases.get_build_info import GetBuildInfo


class FakeBuildInfoProvider:
    """A fake supplier for the test. No settings, no AWS."""

    def __init__(self, info: BuildInfo) -> None:
        self.info = info
        self.calls = 0

    def get_build_info(self) -> BuildInfo:
        self.calls += 1
        return self.info


def test_returns_what_the_port_provides() -> None:
    info = BuildInfo(
        service_name="svc",
        version="1.2.3",
        environment="dev",
        aws_region="ap-south-1",
        git_sha="abc1234",
    )
    provider = FakeBuildInfoProvider(info)

    result = GetBuildInfo(provider)()

    assert result == info
    assert provider.calls == 1
