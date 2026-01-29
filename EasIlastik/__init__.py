# Copyright (C) 2026 Titouan Le Gourrierec
"""
easilastik: Easy integration of Ilastik segmentation models in Python.

Provides
    1. A user-friendly interface to load and use pre-trained Ilastik models in Python applications.
    2. Seamless integration with Python to create custom workflows for image processing.
    3. Support for single image files or image folders.
    4. Robust error handling mechanisms to facilitate debugging and issue resolution when using Ilastik models.

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided with the code, and a standalone reference guide
available from the `EasIlastik homepage : https://github.com/titouanlegourrierec/EasIlastik/wiki`.
"""

__author__ = "Titouan Le Gourrierec"
__email__ = "titouanlegourrierec@icloud.com"

import logging
import subprocess
import sys
from importlib.metadata import version

import requests

from .run_ilastik import (
    color_treshold_probabilities,
    run_ilastik,
    run_ilastik_probabilities,
)


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


__version__ = version(__name__)
__all__ = ["color_treshold_probabilities", "run_ilastik", "run_ilastik_probabilities"]


def check_for_update() -> None:
    """Check if an update is available."""
    try:
        current_version = __version__
        if current_version == "unknown":  # noqa: PLR2004
            return  # Exit if the installed version cannot be obtained

        response = requests.get("https://pypi.org/pypi/easilastik/json", timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        package_data = response.json()
        latest_version = package_data["info"]["version"]

        if latest_version != current_version:
            logger.info("A new version of your package is available!")
            user_input = input("Do you want to install the update? (yes/y to confirm): ").strip().lower()
            if user_input in {"yes", "y"}:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "easilastik"])  # noqa: S603
                logger.info("The package has been updated successfully.")
            else:
                logger.info("Update skipped.")
    except Exception:
        logger.exception("An error occurred while checking for updates")


# Call the update check function at the start of the package
check_for_update()
