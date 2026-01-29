# Copyright (C) 2026 Titouan Le Gourrierec
"""Utility functions for EasIlastik package."""

from pathlib import Path


def get_image_paths(image_folder: str) -> list:
    """
    Get a list of image file paths from the specified folder.

    Parameters
    ----------
    image_folder : str
        The path to the folder containing the images.

    Returns
    -------
    list
        A list of paths to the image

    """
    return list(Path(image_folder).glob("*"))
