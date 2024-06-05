import os
import glob

def get_image_paths(image_folder : str) -> list:
    """
    This function retrieves the paths of all image files in a specified folder.

    Parameters:
    image_folder (str): The path to the folder containing the images.

    Returns:
    list: A list of paths to the image files.
    """

    # Use glob to get all file paths in the image_folder
    image_paths = glob.glob(os.path.join(image_folder, '*'))
    
    return image_paths