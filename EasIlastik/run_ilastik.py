import os
import subprocess
import numpy as np
import h5py
import cv2
from EasIlastik.find_ilastik import find_ilastik
from EasIlastik.utils import get_image_paths

##########################################################################################################################################

############               This function is used to run Ilastik in headless mode with the specified parameters.                 ##########

##########################################################################################################################################

def run_ilastik(input_path : str,
                project_path : str,
                result_base_path : str,
                ilastik_script_path : str = find_ilastik(),
                export_source : str = "Simple Segmentation",
                output_format : str = "png"):
    """
    Execute the Ilastik software in headless mode with the specified parameters.

    Parameters:
    input_path (str): The path to the image file or folder to be processed.
    project_path (str): The path to the Ilastik project file.
    result_base_path (str): The base path where the result will be saved.
    ilastik_script_path (str, optional): The path to the Ilastik script. If not provided, it will attempt to find the path automatically.
    export_source (str, optional): The type of data to export. Default is "Simple Segmentation".
        Must be one of ["Probabilities", "Simple Segmentation", "Uncertainty", "Features", "Labels"].
    output_format (str, optional): The format of the output file. Default is "png".
        Must be one of ["bmp", "gif", "hdr", "jpeg", "jpg", "pbm", "pgm", "png", "pnm", "ppm", "ras",
        "tif", "tiff", "xv", "bmp sequence", "gif sequence", "hdr sequence", "jpeg sequence",
        "jpg sequence", "pbm sequence", "pgm sequence", "png sequence", "pnm sequence",
        "ppm sequence", "ras sequence", "tif sequence", "tiff sequence", "xv sequence",
        "multipage tiff", "multipage tiff sequence", "hdf5", "compressed hdf5", "numpy, dvid"].

    Returns:
    None

    Raises:
    ValueError: If export_source or output_format is not in the allowed list.
    subprocess.CalledProcessError: If there is an error during the execution of the Ilastik command.
    """

    if ilastik_script_path is None:
        print("ilastik_script_path is None. Please check the path format at ...")
        return
    
    ALLOWED_SOURCES = ["Probabilities", "Simple Segmentation", "Uncertainty", "Features", "Labels"]
    ALLOWED_FORMATS = ["bmp", "gif", "hdr", "jpeg", "jpg", "pbm", "pgm", "png", "pnm", "ppm", "ras",
                    "tif", "tiff", "xv", "bmp sequence", "gif sequence", "hdr sequence", "jpeg sequence",
                    "jpg sequence", "pbm sequence", "pgm sequence", "png sequence", "pnm sequence",
                    "ppm sequence", "ras sequence", "tif sequence", "tiff sequence", "xv sequence",
                    "multipage tiff", "multipage tiff sequence", "hdf5", "compressed hdf5", "numpy, dvid"]
    
    if not os.path.isfile(input_path) and not os.path.isdir(input_path):
        raise FileNotFoundError(f"input_path '{input_path}' is not a valid file or directory")

    if export_source not in ALLOWED_SOURCES:
        raise ValueError(f"Invalid export_source. Allowed values are {ALLOWED_SOURCES}")
    
    if output_format not in ALLOWED_FORMATS:
        raise ValueError(f"Invalid output_format. Allowed values are {ALLOWED_FORMATS}")
    
    if export_source == "Probabilities" and output_format not in ["hdf5", "compressed hdf5", "hdr", "tiff", "multipage tiff"]:
        raise ValueError(f"Invalid output_format '{output_format}' for export_source 'Probabilities'. Allowed formats are: ['hdf5', 'compressed hdf5', 'hdr', 'tiff', 'multipage tiff']")
    
    # Check if result_base_path exists, if not, create it
    if not os.path.exists(result_base_path):
        os.makedirs(result_base_path)

    # Check if input_path is a directory or a file
    if os.path.isdir(input_path):
        image_arg = get_image_paths(input_path)
        # Arguments to execute Ilastik in headless mode
        ilastik_args = [
            ilastik_script_path,
            "--headless",
            "--project=" + project_path,
            "--export_source=" + export_source,
            "--output_format=" + output_format,
            "--output_filename_format=" + result_base_path + "{nickname}_" + export_source.replace(" ", "_"),
            *image_arg
        ]
        
    else:
        image_arg = input_path
        # Arguments to execute Ilastik in headless mode
        ilastik_args = [
            ilastik_script_path,
            "--headless",
            "--project=" + project_path,
            "--export_source=" + export_source,
            "--output_format=" + output_format,
            "--output_filename_format=" + result_base_path + "{nickname}_" + export_source.replace(" ", "_"),
            image_arg
        ]

    # Execute the Ilastik command in headless mode with the specified arguments
    try:
        subprocess.run(ilastik_args, check=True)
        print(f"Conversion of {input_path} completed successfully")
    except subprocess.CalledProcessError as e:
        print("Error during conversion : ", e)
        raise RuntimeError("Error during Ilastik execution. See console output for details.")




##########################################################################################################################################

############              These functions are used to process the results given by Ilastik by manually choosing the             ##########
############                            probability threshold from which the result is conclusive.                              ##########

##########################################################################################################################################

def process_single_file(file_path,
                        threshold,
                        below_threshold_color,
                        channel_colors,
                        deletetion = True):
    """
    Processes a single .h5 file and creates a color image from it.

    Parameters:
    file_path (str): Path to the .h5 file.
    threshold (float): Threshold value for color mapping. Pixels with maximum value greater than this threshold will be colored according to the color map.
    below_threshold_color (list): RGB color for values below the threshold. Must be a list of 3 integers between 0 and 255.
    channel_colors (list): List of RGB colors for each channel. Each color must be a list of 3 integers between 0 and 255.
    deletion (bool): If True, the original .h5 file will be deleted after processing. Default is True.

    Returns:
    None. The function saves the color image in the same location as the input file with a .png extension.

    Raises:
    FileNotFoundError: If the file at file_path does not exist.
    ValueError: If below_threshold_color or channel_colors do not meet the requirements, or if the file at file_path could not be opened or does not contain 'exported_data'.
    """
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File at {file_path} does not exist")
    
    if not isinstance(below_threshold_color, list) or len(below_threshold_color) != 3 or not all(isinstance(i, int) and 0 <= i <= 255 for i in below_threshold_color):
        raise ValueError("below_threshold_color must be a list of 3 integers between 0 and 255 (RGB color format)")
    
    if not isinstance(channel_colors, list) or not all(isinstance(color, list) and len(color) == 3 and all(isinstance(i, int) and 0 <= i <= 255 for i in color) for color in channel_colors):
        raise ValueError("channel_colors must be a list of lists of 3 integers between 0 and 255 (RGB color format)")

    # Open the file
    try:
        f = h5py.File(file_path, 'r')
    except IOError:
        raise ValueError(f"Could not open file at {file_path}")

    # Ensure the file contains 'exported_data'
    if 'exported_data' not in f:
        f.close()
        raise ValueError(f"File at {file_path} does not contain 'exported_data'")

    data = f['exported_data']

    # Check if the length of channel_colors is equal to the number of channels in data
    if len(channel_colors) != data.shape[-1]:
        f.close()
        raise ValueError(f"The length of channel_colors must be equal to the number of channels in the data (there must be as many colors as labels annotated in the Ilastik project). Expected {data.shape[-1]}, got {len(channel_colors)}")

    # Find the index of the channel with the highest value for each pixel
    indices = np.argmax(data, axis=-1)
    indices = indices.astype(int)

    # Find the maximum value for each pixel
    max_values = np.max(data, axis=-1)

    # Create a color map
    colors = np.array([below_threshold_color] + channel_colors)

    # Convert the below_threshold_color to a numpy array and add two new axes to match the shape of max_values[..., np.newaxis]
    below_threshold_color_array = np.array(below_threshold_color)[np.newaxis, np.newaxis, :]

    # Use numpy's take function to create a color map. The color map is an array of colors corresponding to the indices.
    color_map = np.take(colors, indices + 1, axis=0)

    # Use numpy's where function to create the color image. If the maximum value of a pixel is greater than the threshold, 
    # the pixel's color is taken from the color map. Otherwise, the pixel's color is set to below_threshold_color.
    color_image = np.where(max_values[..., np.newaxis] > threshold, color_map, below_threshold_color_array)

    # Convert the color image to uint8 type for compatibility with OpenCV's imwrite function.
    color_image_uint8 = color_image.astype(np.uint8)

    # Save the color image
    file_name, extension = os.path.splitext(file_path)
    new_path = file_name + ".png"
    cv2.imwrite(new_path, cv2.cvtColor(color_image_uint8, cv2.COLOR_RGB2BGR))  # cv2 uses BGR color format

    # Close the h5 file
    f.close()

    if deletetion:
        # Delete the h5 file
        os.remove(file_path)

def color_treshold_probabilities(file_path,
                                 threshold,
                                 below_threshold_color,
                                 channel_colors):
    """
    Processes a single .h5 file and creates a color image from it.

    Parameters:
    file_path (str): Path to the .h5 file.
    threshold (float): Threshold value for color mapping. Pixels with maximum value greater than this threshold will be colored according to the color map.
    below_threshold_color (list): RGB color for values below the threshold. Must be a list of 3 integers between 0 and 255.
    channel_colors (list): List of RGB colors for each channel. Each color must be a list of 3 integers between 0 and 255.

    Returns:
    color_image_uint8 (numpy.ndarray): The color image as a numpy array in uint8 format. The color image is in BGR format, which is compatible with OpenCV's imwrite function.

    Raises:
    FileNotFoundError: If the file at file_path does not exist.
    ValueError: If below_threshold_color or channel_colors do not meet the requirements, or if the file at file_path could not be opened or does not contain 'exported_data'.
    """
        
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File at {file_path} does not exist")
    
    if not isinstance(below_threshold_color, list) or len(below_threshold_color) != 3 or not all(isinstance(i, int) and 0 <= i <= 255 for i in below_threshold_color):
        raise ValueError("below_threshold_color must be a list of 3 integers between 0 and 255 (RGB color format)")
    
    if not isinstance(channel_colors, list) or not all(isinstance(color, list) and len(color) == 3 and all(isinstance(i, int) and 0 <= i <= 255 for i in color) for color in channel_colors):
        raise ValueError("channel_colors must be a list of lists of 3 integers between 0 and 255 (RGB color format)")

    # Open the file
    try:
        f = h5py.File(file_path, 'r')
    except IOError:
        raise ValueError(f"Could not open file at {file_path}")

    # Ensure the file contains 'exported_data'
    if 'exported_data' not in f:
        f.close()
        raise ValueError(f"File at {file_path} does not contain 'exported_data'")

    data = f['exported_data']

    # Check if the length of channel_colors is equal to the number of channels in data
    if len(channel_colors) != data.shape[-1]:
        f.close()
        raise ValueError(f"The length of channel_colors must be equal to the number of channels in the data (there must be as many colors as labels annotated in the Ilastik project). Expected {data.shape[-1]}, got {len(channel_colors)}")

    # Find the index of the channel with the highest value for each pixel
    indices = np.argmax(data, axis=-1)
    indices = indices.astype(int)

    # Find the maximum value for each pixel
    max_values = np.max(data, axis=-1)

    # Create a color map
    colors = np.array([below_threshold_color] + channel_colors)

    # Convert the below_threshold_color to a numpy array and add two new axes to match the shape of max_values[..., np.newaxis]
    below_threshold_color_array = np.array(below_threshold_color)[np.newaxis, np.newaxis, :]

    # Use numpy's take function to create a color map. The color map is an array of colors corresponding to the indices.
    color_map = np.take(colors, indices + 1, axis=0)

    # Use numpy's where function to create the color image. If the maximum value of a pixel is greater than the threshold, 
    # the pixel's color is taken from the color map. Otherwise, the pixel's color is set to below_threshold_color.
    color_image = np.where(max_values[..., np.newaxis] > threshold, color_map, below_threshold_color_array)

    color_image_uint8 = color_image.astype(np.uint8)
    color_image_uint8 = cv2.cvtColor(color_image_uint8, cv2.COLOR_RGB2BGR)

    # Close the h5 file
    f.close()

    return color_image_uint8


def treshold_probabilities(file_or_dir_path,
                           threshold,
                           below_threshold_color,
                           channel_colors,
                           deletetion = True):
    """
    Creates a color image from a single .h5 file or all .h5 files in a directory.

    Parameters:
    file_or_dir_path (str): Path to the .h5 file or directory containing .h5 files.
    threshold (float): Threshold value for color mapping.
    below_threshold_color (list): RGB color for values below the threshold.
    channel_colors (list): List of RGB colors for each channel.

    Returns:
    None. The function saves the color image(s) in the same location as the input file(s) with a .png extension.
    """
    if os.path.isdir(file_or_dir_path):
        # If the path is a directory, apply the function to all .h5 files in the directory
        for filename in os.listdir(file_or_dir_path):
            if filename.endswith(".h5"):
                file_path = os.path.join(file_or_dir_path, filename)
                process_single_file(file_path, threshold, below_threshold_color, channel_colors, deletetion)
    else:
        # If the path is not a directory, assume it's a file and apply the function to it
        process_single_file(file_or_dir_path, threshold, below_threshold_color, channel_colors, deletetion)

##########################################################################################################################################

############           This functions is used to run Ilastik in headless mode and automatically treshold probabilities          ##########

##########################################################################################################################################

def run_ilastik_probabilities(input_path : str,
                              project_path : str,
                              result_base_path : str,
                              threshold : int,
                              below_threshold_color : list,
                              channel_colors : list,
                              deletetion : bool = True,
                              ilastik_script_path : str = find_ilastik()):
    """
    Process the images by first running Ilastik to create h5 files in which each channel represent the probabilities that the pixel is part of this class,
    then creating color images from these files.

    Parameters:
    input_path (str): The path to the image file or folder to be processed.
    project_path (str): The path to the Ilastik project file.
    result_base_path (str): The base path where the result will be saved.
    ilastik_script_path (str, optional): The path to the Ilastik script. If not provided, it will attempt to find the path automatically.
    threshold (int): The threshold above which a channel's value must be for the pixel to take its color.
    below_threshold_color (list): The color for pixels where the maximum value is below the threshold. Must be a list of 3 integers between 0 and 255.
    channel_colors (list): The colors for the channels. Must be a list of lists, where each inner list is a list of 3 integers between 0 and 255.

    Returns:
    None
    """
    # Run Ilastik to create h5 files
    run_ilastik(input_path, project_path, result_base_path, ilastik_script_path, export_source="Probabilities", output_format="hdf5")

    # Create color images from the h5 files
    treshold_probabilities(result_base_path, threshold, below_threshold_color, channel_colors, deletetion)