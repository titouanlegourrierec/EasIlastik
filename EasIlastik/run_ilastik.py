# Copyright (C) 2026 Titouan Le Gourrierec
"""Module to run Ilastik in headless mode and process the results."""

import logging
import subprocess
from pathlib import Path

import cv2
import h5py
import numpy as np

from easilastik.find_ilastik import find_ilastik
from easilastik.utils import get_image_paths


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

ALLOWED_SOURCES = ["Probabilities", "Simple Segmentation", "Uncertainty", "Features", "Labels"]
ALLOWED_FORMATS = [
    "bmp",
    "gif",
    "hdr",
    "jpeg",
    "jpg",
    "pbm",
    "pgm",
    "png",
    "pnm",
    "ppm",
    "ras",
    "tif",
    "tiff",
    "xv",
    "bmp sequence",
    "gif sequence",
    "hdr sequence",
    "jpeg sequence",
    "jpg sequence",
    "pbm sequence",
    "pgm sequence",
    "png sequence",
    "pnm sequence",
    "ppm sequence",
    "ras sequence",
    "tif sequence",
    "tiff sequence",
    "xv sequence",
    "multipage tiff",
    "multipage tiff sequence",
    "hdf5",
    "compressed hdf5",
    "numpy, dvid",
]

##################################################################################################
#   This function is used to run Ilastik in headless mode with the specified parameters.
##################################################################################################


def run_ilastik(
    input_path: str,
    model_path: str,
    result_base_path: str,
    ilastik_script_path: str | None = find_ilastik(),
    export_source: str = "Simple Segmentation",
    output_format: str = "png",
) -> None:
    """
    Execute the Ilastik software in headless mode with the specified parameters.

    Parameters
    ----------
    input_path : str
        The path to the image file or folder to be processed.
    model_path : str
        The path to the Ilastik project file.
    result_base_path : str
        The base path where the result will be saved.
    ilastik_script_path : str, optional
        The path to the Ilastik script. If not provided, it will attempt to find the path automatically.
    export_source : str, optional
        The type of data to export. Default is "Simple Segmentation". Must be one of
        ["Probabilities", "Simple Segmentation", "Uncertainty", "Features", "Labels"].
    output_format : str, optional
        The format of the output file. Default is "png". Must be one of["bmp", "gif", "hdr", "jpeg",
        "jpg", "pbm", "pgm", "png", "pnm", "ppm", "ras", "tif", "tiff", "xv", "bmp sequence", "gif sequence",
        "hdr sequence", "jpeg sequence", "jpg sequence", "pbm sequence", "pgm sequence", "png sequence",
        "pnm sequence", "ppm sequence", "ras sequence", "tif sequence", "tiff sequence", "xv sequence",
        "multipage tiff", "multipage tiff sequence", "hdf5", "compressed hdf5", "numpy, dvid"].

    Raises
    ------
    FileNotFoundError
        If the input_path does not exist.
    ValueError
        If the export_source or output_format is not valid.
    RuntimeError
        If there is an error during the Ilastik execution.
    """
    if ilastik_script_path is None:
        logger.error("ilastik_script_path is None. Please provide the path to the Ilastik script.")
        return

    if not Path(input_path).is_file() and not Path(input_path).is_dir():
        msg = f"input_path '{input_path}' is not a valid file or directory."
        raise FileNotFoundError(msg)

    if export_source not in ALLOWED_SOURCES:
        msg = f"Invalid export_source. Allowed values are {ALLOWED_SOURCES}"
        raise ValueError(msg)

    if output_format not in ALLOWED_FORMATS:
        msg = f"Invalid output_format. Allowed values are {ALLOWED_FORMATS}"
        raise ValueError(msg)

    if export_source == "Probabilities" and output_format not in {  # noqa: PLR2004
        "hdf5",
        "compressed hdf5",
        "hdr",
        "tiff",
        "multipage tiff",
    }:
        msg = (
            f"Invalid output_format '{output_format}' for export_source 'Probabilities'."
            "Allowed formats are: ['hdf5', 'compressed hdf5', 'hdr', 'tiff', 'multipage tiff']"
        )
        raise ValueError(msg)

    # Check if result_base_path exists, if not, create it
    if not Path(result_base_path).exists():
        Path(result_base_path).mkdir(parents=True, exist_ok=True)

    # Check if input_path is a directory or a file
    if Path(input_path).is_dir():
        image_arg = get_image_paths(input_path)
    elif Path(input_path).is_file():
        image_arg = [input_path]

    logger.info("image_arg: %s", image_arg)
    # Arguments to execute Ilastik in headless mode
    ilastik_args = [
        ilastik_script_path,
        "--headless",
        "--project=" + model_path,
        "--export_source=" + export_source,
        "--output_format=" + output_format,
        "--output_filename_format=" + result_base_path + "{nickname}_" + export_source.replace(" ", "_"),
        *image_arg,
    ]

    # Execute the Ilastik command in headless mode with the specified arguments
    try:
        subprocess.run(ilastik_args, check=True)  # noqa: S603
        msg = f"Conversion of {input_path} completed successfully."
        logger.info(msg)
    except subprocess.CalledProcessError as err:
        logger.exception("Error during conversion")
        msg = "Error during Ilastik execution. See console output for details."
        raise RuntimeError(msg) from err


######################################################################################################
#    These functions are used to process the results given by Ilastik by manually choosing the
#                  probability threshold from which the result is conclusive.
######################################################################################################


def process_single_file(
    file_path: str,
    threshold: float,
    below_threshold_color: list,
    channel_colors: list,
    *,
    deletion: bool = True,
) -> None:
    """
    Create a color image from a single .h5 file.

    Parameters
    ----------
    file_path : str
        Path to the .h5 file.
    threshold : float
        Threshold value for color mapping. Pixels with maximum value greater than this threshold will
        be colored according to the color map.
    below_threshold_color : list
        RGB color for values below the threshold. Must be a list of 3 integers between 0 and 255.
    channel_colors : list
        List of RGB colors for each channel. Each color must be a list of 3 integers between 0 and 255.
    deletion : bool, optional
        If True, the original .h5 file will be deleted after processing. Default is True.

    Raises
    ------
    FileNotFoundError
        If the file at file_path does not exist.
    ValueError
        If below_threshold_color or channel_colors are not in the correct format, or if the file
        does not contain 'exported_data', or if the length of channel_colors does not match
        the number of channels in the data.
    """
    if not Path(file_path).exists():
        msg = f"File at {file_path} does not exist"
        raise FileNotFoundError(msg)

    if (
        not isinstance(below_threshold_color, list)
        or len(below_threshold_color) != 3
        or not all(isinstance(i, int) and 0 <= i <= 255 for i in below_threshold_color)
    ):
        msg = "below_threshold_color must be a list of 3 integers between 0 and 255 (RGB color format)"
        raise ValueError(msg)

    if not isinstance(channel_colors, list) or not all(
        isinstance(color, list) and len(color) == 3 and all(isinstance(i, int) and 0 <= i <= 255 for i in color)
        for color in channel_colors
    ):
        msg = "channel_colors must be a list of lists of 3 integers between 0 and 255 (RGB color format)"
        raise ValueError(msg)

    # Open the file
    try:
        f = h5py.File(file_path, "r")
    except OSError as err:
        msg = f"Could not open file at {file_path}"
        raise ValueError(msg) from err

    # Ensure the file contains 'exported_data'
    if "exported_data" not in f:  # noqa: PLR2004
        f.close()
        msg = f"File at {file_path} does not contain 'exported_data'"
        raise ValueError(msg)

    data = f["exported_data"]

    # Check if the length of channel_colors is equal to the number of channels in data
    if len(channel_colors) != data.shape[-1]:
        f.close()
        msg = (
            "The length of channel_colors must be equal to the number of channels in the data"
            "(there must be as many colors as labels annotated in the Ilastik project)."
            f"Expected {data.shape[-1]}, got {len(channel_colors)}"
        )
        raise ValueError(msg)

    # Find the index of the channel with the highest value for each pixel
    indices = np.argmax(data, axis=-1)
    indices = indices.astype(int)

    # Find the maximum value for each pixel
    max_values = np.max(data, axis=-1)

    # Create a color map
    colors = np.array([below_threshold_color, *channel_colors])

    # Convert the below_threshold_color to a numpy array and add two new axes to match the shape
    # of max_values[..., np.newaxis]
    below_threshold_color_array = np.array(below_threshold_color)[np.newaxis, np.newaxis, :]

    # Use numpy's take function to create a color map. The color map is an array of colors corresponding
    # to the indices.
    color_map = np.take(colors, indices + 1, axis=0)

    # Use numpy's where function to create the color image. If the maximum value of a pixel is greater than the
    # threshold, the pixel's color is taken from the color map. Otherwise, the pixel's color is set to
    # below_threshold_color.
    color_image = np.where(max_values[..., np.newaxis] > threshold, color_map, below_threshold_color_array)

    # Convert the color image to uint8 type for compatibility with OpenCV's imwrite function.
    color_image_uint8 = color_image.astype(np.uint8)

    # Save the color image
    new_path = Path(file_path).with_suffix(".png")
    cv2.imwrite(str(new_path), cv2.cvtColor(color_image_uint8, cv2.COLOR_RGB2BGR))  # cv2 uses BGR color format

    # Close the h5 file
    f.close()

    if deletion:
        # Delete the h5 file
        Path(file_path).unlink()


def color_treshold_probabilities(
    file_path: str, threshold: float, below_threshold_color: list, channel_colors: list
) -> np.ndarray:
    """
    Create a color image from a single .h5 file.

    Parameters
    ----------
    file_path : str
        Path to the .h5 file.
    threshold : float
        Threshold value for color mapping. Pixels with maximum value greater than this threshold will be colored
        according to the color map.
    below_threshold_color : list
        RGB color for values below the threshold. Must be a list of 3 integers between 0 and 255.
    channel_colors : list
        List of RGB colors for each channel. Each color must be a list of 3 integers between 0 and 255.

    Returns
    -------
    color_image_uint8 : np.ndarray
        The color image as a numpy array in uint8 format. The color image is in BGR format, which is compatible with
        OpenCV's imwrite function.

    Raises
    ------
    FileNotFoundError
        If the file at file_path does not exist.
    ValueError
        If below_threshold_color or channel_colors are not in the correct format, or if the file
        does not contain 'exported_data', or if the length of channel_colors does not match
        the number of channels in the data.
    """
    if not Path(file_path).exists():
        msg = f"File at {file_path} does not exist"
        raise FileNotFoundError(msg)

    if (
        not isinstance(below_threshold_color, list)
        or len(below_threshold_color) != 3
        or not all(isinstance(i, int) and 0 <= i <= 255 for i in below_threshold_color)
    ):
        msg = "below_threshold_color must be a list of 3 integers between 0 and 255 (RGB color format)"
        raise ValueError(msg)

    if not isinstance(channel_colors, list) or not all(
        isinstance(color, list) and len(color) == 3 and all(isinstance(i, int) and 0 <= i <= 255 for i in color)
        for color in channel_colors
    ):
        msg = "channel_colors must be a list of lists of 3 integers between 0 and 255 (RGB color format)"
        raise ValueError(msg)

    # Open the file
    try:
        f = h5py.File(file_path, "r")
    except OSError as err:
        msg = f"Could not open file at {file_path}"
        raise ValueError(msg) from err

    # Ensure the file contains 'exported_data'
    if "exported_data" not in f:  # noqa: PLR2004
        f.close()
        msg = f"File at {file_path} does not contain 'exported_data'"
        raise ValueError(msg)
    data = f["exported_data"]

    # Check if the length of channel_colors is equal to the number of channels in data
    if len(channel_colors) != data.shape[-1]:
        f.close()
        msg = (
            "The length of channel_colors must be equal to the number of channels in the data (there must be as many "
            f"colors as labels annotated in the Ilastik project). Expected {data.shape[-1]}, got {len(channel_colors)}"
        )
        raise ValueError(msg)

    # Find the index of the channel with the highest value for each pixel
    indices = np.argmax(data, axis=-1)
    indices = indices.astype(int)

    # Find the maximum value for each pixel
    max_values = np.max(data, axis=-1)

    # Create a color map
    colors = np.array([below_threshold_color, *channel_colors])

    # Convert the below_threshold_color to a numpy array and add two new axes to match the shape
    # of max_values[..., np.newaxis]
    below_threshold_color_array = np.array(below_threshold_color)[np.newaxis, np.newaxis, :]

    # Use numpy's take function to create a color map. The color map is an array of colors corresponding
    # to the indices.
    color_map = np.take(colors, indices + 1, axis=0)

    # Use numpy's where function to create the color image. If the maximum value of a pixel is greater than the
    # threshold, the pixel's color is taken from the color map. Otherwise, the pixel's color is set to
    # below_threshold_color.
    color_image = np.where(max_values[..., np.newaxis] > threshold, color_map, below_threshold_color_array)

    color_image_uint8 = color_image.astype(np.uint8)
    color_image_uint8 = cv2.cvtColor(color_image_uint8, cv2.COLOR_RGB2BGR)

    # Close the h5 file
    f.close()

    return color_image_uint8


def treshold_probabilities(
    file_or_dir_path: str,
    threshold: float,
    below_threshold_color: list,
    channel_colors: list,
    *,
    deletion: bool = True,
) -> None:
    """
    Process .h5 file(s) to create color images based on probability thresholds.

    Parameters
    ----------
    file_or_dir_path : str
        Path to the .h5 file or directory containing .h5 files.
    threshold : float
        Threshold value for color mapping.
    below_threshold_color : list
        RGB color for values below the threshold.
    channel_colors : list
        List of RGB colors for each channel.

    """
    if Path(file_or_dir_path).is_dir():
        # If the path is a directory, apply the function to all .h5 files in the directory
        for file in Path(file_or_dir_path).iterdir():
            if file.suffix == ".h5":  # noqa: PLR2004
                process_single_file(
                    str(file),
                    threshold,
                    below_threshold_color,
                    channel_colors,
                    deletion=deletion,
                )
    else:
        # If the path is not a directory, assume it's a file and apply the function to it
        process_single_file(file_or_dir_path, threshold, below_threshold_color, channel_colors, deletion=deletion)


###############################################################################################################
#     This functions is used to run Ilastik in headless mode and automatically treshold probabilities
###############################################################################################################


def run_ilastik_probabilities(
    input_path: str,
    model_path: str,
    result_base_path: str,
    threshold: int,
    below_threshold_color: list,
    channel_colors: list,
    *,
    deletion: bool = True,
    ilastik_script_path: str | None = find_ilastik(),
) -> None:
    """
    Execute Ilastik in headless mode to generate probability maps and color images based on a specifiedthreshold.

    Parameters
    ----------
    input_path : str
        The path to the image file or folder to be processed.
    model_path : str
        The path to the Ilastik project file.
    result_base_path : str
        The base path where the result will be saved.
    ilastik_script_path : str, optional
        The path to the Ilastik script. If not provided, it will attempt to find the path automatically.
    threshold : int
        The threshold above which a channel's value must be for the pixel to take its color.
    below_threshold_color : list
        The color for pixels where the maximum value is below the threshold. Must be a list of 3 integers between
        0 and 255.
    channel_colors : list
        The colors for the channels. Must be a list of lists, where each inner list is a list of 3 integers between
        0 and 255.
    """
    # Run Ilastik to create h5 files
    run_ilastik(
        input_path,
        model_path,
        result_base_path,
        ilastik_script_path,
        export_source="Probabilities",
        output_format="hdf5",
    )

    # Create color images from the h5 files
    treshold_probabilities(result_base_path, threshold, below_threshold_color, channel_colors, deletion=deletion)
