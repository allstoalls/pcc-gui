"""Canonical native entrypoint for the declarative mac diff application."""

import pcc_gui  # noqa: F401  pcc1 compiles the framework into this program's closure
from declarative_app import run_app


def main() -> int:
    return run_app(1)


main()
