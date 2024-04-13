import os
import subprocess
from EasIlastik.find_ilastik import find_ilastik
from EasIlastik.utils import get_image_paths

def run_ilastik(input_path : str,
                project_path : str,
                result_base_path : str,
                ilastik_script_path : str = find_ilastik(),
                export_source : str ="Simple Segmentation",
                output_format : str ="png"):
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
    
    if export_source not in ALLOWED_SOURCES:
        raise ValueError(f"Invalid export_source. Allowed values are {ALLOWED_SOURCES}")
    
    if output_format not in ALLOWED_FORMATS:
        raise ValueError(f"Invalid output_format. Allowed values are {ALLOWED_FORMATS}")
    
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