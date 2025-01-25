__doc__ = """
    EasIlastik
    ==========

    This module provides functionalities to simplify the usage of Ilastik models in Python.

    Provides
      1. A user-friendly interface to load and use pre-trained Ilastik models in Python applications.
      2. Seamless integration with Python to create custom workflows for image processing.
      3. Support for single image files or image folders.
      4. Robust error handling mechanisms to facilitate debugging and issue resolution when using Ilastik models.

    How to use the documentation
    ----------------------------
    Documentation is available in two forms: docstrings provided with the code, and a standalone reference guide available from the `EasIlastik homepage : https://github.com/titouanlegourrierec/EasIlastik/wiki`.
"""

__version__ = "1.0.2"
__author__ = "Titouan Le Gourrierec"
__email__ = "titouanlegourrierec@icloud.com"
__all__ = ["run_ilastik", "run_ilastik_probabilities", "color_treshold_probabilities"]

import subprocess
import sys

import requests

from .run_ilastik import color_treshold_probabilities  # noqa
from .run_ilastik import run_ilastik  # noqa
from .run_ilastik import run_ilastik_probabilities  # noqa


def get_installed_version():
    """Gets the currently installed version of the package."""
    try:
        import EasIlastik  # Import your package to get its version

        return EasIlastik.__version__
    except Exception as e:
        print("An error occurred while getting the installed version:", e)
        return "unknown"  # Return a default version string


def check_for_update():
    """Checks if an update is available."""
    try:
        current_version = get_installed_version()
        if current_version == "unknown":
            return  # Exit if the installed version cannot be obtained

        response = requests.get("https://pypi.org/pypi/EasIlastik/json")
        response.raise_for_status()  # Raise an exception for HTTP errors
        package_data = response.json()
        latest_version = package_data["info"]["version"]

        if latest_version != current_version:
            print("A new version of your package is available!")
            user_input = input("Do you want to install the update? (yes/y to confirm): ").strip().lower()
            if user_input in ["yes", "y"]:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "EasIlastik"])
                print("The package has been updated successfully.")
            else:
                print("Update skipped.")
    except Exception as e:
        print("An error occurred while checking for updates:", e)


# Call the update check function at the start of the package
check_for_update()
