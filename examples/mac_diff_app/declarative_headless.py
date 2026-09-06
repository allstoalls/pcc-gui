"""Deterministic non-window entry for the canonical declarative app."""

import pcc_gui  # noqa: F401  pcc1 compiles the framework into this program's closure
from declarative_app import run_app


def main() -> int:
    return run_app(0)


main()
