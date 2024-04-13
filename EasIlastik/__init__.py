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
    Documentation is available in two forms: docstrings provided with the code, and a standalone reference guide available from the `EasIlastik homepage ...`.
"""

__version__ = "0.0.1"

import xmlrpc.client
import sys

def get_installed_version():
    """Gets the currently installed version of the package."""
    try:
        import EasIlastik  # Import your package to get its version
        return EasIlastik.__version__
    except Exception as e:
        print("An error occurred while getting the installed version:", e)
        return None

def check_for_update():
    """Checks if an update is available."""
    try:
        current_version = get_installed_version()
        if current_version is None:
            return  # Exit if the installed version cannot be obtained

        client = xmlrpc.client.ServerProxy('https://pypi.org/pypi')
        package_data = client.package_releases('EasIlastik')
        latest_version = package_data[0]  # The latest version is the first element of the list

        if latest_version != current_version:
            print("A new version of your package is available!")
            print("You can update it by running: pip install --upgrade EasIlastik")
    except Exception as e:
        print("An error occurred while checking for updates:", e)

# Call the update check function at the start of your application
check_for_update()