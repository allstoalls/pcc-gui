"""Resolve the installed compiler without starting a core bootstrap build."""

import os
from pathlib import Path
import shutil


def compiler_path() -> Path:
    requested = os.environ.get("PCC1") or os.environ.get("PCC_CURRENT_PCC1") or "pcc1"
    executable = shutil.which(requested)
    if executable is None:
        raise RuntimeError(
            f"Compiler {requested!r} is not executable. Install pcc1 from the core "
            "checkout into ~/.local/bin, add that directory to PATH, or set "
            "PCC1=/absolute/path/to/pcc1. GUI tests never bootstrap the compiler."
        )
    return Path(executable).absolute()
