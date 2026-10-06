"""Command-line interface: `mnist-mlops <command>`."""

import argparse
import json
import logging
import sys
from collections.abc import Callable, Sequence
from dataclasses import asdict

from pydantic import ValidationError

from mnist_mlops import __version__
from mnist_mlops.entrypoints.container import Container, build_container
from mnist_mlops.infrastructure.logging import configure_logging

logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_CONFIG_ERROR = 2


def _cmd_info(container: Container) -> int:
    info = container.get_build_info()
    sys.stdout.write(json.dumps(asdict(info), indent=2) + "\n")
    return EXIT_OK


_COMMANDS: dict[str, Callable[[Container], int]] = {
    "info": _cmd_info,
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mnist-mlops",
        description="MNIST MLOps project command-line interface.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("info", help="Print build and runtime information as JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    try:
        container = build_container()
    except ValidationError as exc:
        sys.stderr.write(f"Invalid configuration:\n{exc}\n")
        return EXIT_CONFIG_ERROR

    settings = container.settings
    configure_logging(
        level=settings.log_level,
        fmt=settings.log_format,
        static_fields={"service": settings.service_name, "environment": settings.environment},
    )
    logger.info("command started", extra={"command": args.command})
    exit_code = _COMMANDS[args.command](container)
    logger.info("command finished", extra={"command": args.command, "exit_code": exit_code})
    return exit_code


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
