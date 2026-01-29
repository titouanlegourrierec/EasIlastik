# Copyright (C) 2026 Titouan Le Gourrierec
"""Find the Ilastik executable on the current operating system."""

import logging
import os
import platform
import time
from pathlib import Path


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

TIME_OUT = 60


def get_os() -> str:
    """
    Return the name of the operating system on which the Python interpreter is running.

    Returns
    -------
    str
        The name of the operating system. Possible values are 'Linux', 'Darwin' (for MacOS), or 'Windows'.
    """
    return platform.system()


def find_file(filename: str, start_path: str) -> str:
    """
    Search for a specified file starting from a specified path.

    Parameters
    ----------
    filename : str
        The name of the file to search for.
    start_path : str
        The path to start the search from.

    Returns
    -------
    str
        The path to the file if found, else None.
    """
    start_time = time.time()

    try:
        for root, _, files in os.walk(start_path):
            if time.time() - start_time > TIME_OUT:
                logger.warning("Search timed out.")
                return ""
            if filename in files:
                return str(Path(root) / filename)
    except Exception:
        msg = f"An error occurred while searching for {filename}"
        logger.exception(msg)
        return ""

    return ""


def find_ilastik() -> str | None:
    """
    Search for the Ilastik executable file on the current operating system.

    Returns
    -------
    str | None
        The path to the Ilastik executable if found, else None.
    """
    os_name = get_os()

    if os_name in {"Darwin", "Linux"}:
        filename = "run_ilastik.sh"
        start_path = "/Applications" if os_name == "Darwin" else "/"  # noqa: PLR2004
    elif os_name == "Windows":  # noqa: PLR2004
        filename = "ilastik.exe"
        start_path = "C:\\"
    else:
        msg = f"Unsupported OS: {os_name}"
        logger.error(msg)
        return None

    return find_file(filename, start_path)
