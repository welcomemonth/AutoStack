import os
from pathlib import Path

from loguru import logger

import segmapy


def get_package_root():
    """Get the root directory of the installed package."""
    package_root = Path(segmapy.__file__).parent.parent
    for i in (".git", ".project_root", ".gitignore"):
        if (package_root / i).exists():
            break
    else:
        package_root = Path.cwd()

    logger.info(f"Package root set to {str(package_root)}")
    return package_root


ROOT = get_package_root()
CONFIG_ROOT = ROOT / "config"
DEFAULT_WORKSPACE_ROOT = ROOT / "workspace"