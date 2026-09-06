"""Use the core's provenance-checked archives from this standalone checkout."""

import os
from pathlib import Path


pytest_plugins = ["tests.python.conftest"]


def pytest_configure(config):
    # Native probes live in pytest temporary directories, outside the package.
    root = str(Path(__file__).resolve().parents[1])
    sites = os.environ.get("PCC_PACKAGE_SITE", "").split(os.pathsep)
    os.environ["PCC_PACKAGE_SITE"] = os.pathsep.join(
        [root, *(site for site in sites if site and site != root)]
    )
