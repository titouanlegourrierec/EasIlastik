import platform
import time
import os

def get_os():
    """
    This function returns the name of the operating system on which the Python interpreter is running.

    Returns:
    str: The name of the operating system. Possible values are 'Linux', 'Darwin' (for MacOS), or 'Windows'.
    """

    return platform.system()


def find_file(filename, start_path):
    """
    This function searches for a specified file starting from a specified path.

    Parameters:
    filename (str): The name of the file to search for.
    start_path (str): The path to start the search from.

    Returns:
    str: The path to the file if found, else None.
    """

    start_time = time.time()

    for root, dirs, files in os.walk(start_path):
        if time.time() - start_time > 60:
            return None
        if filename in files:
            return os.path.join(root, filename)

    return None


def find_ilastik():
    """
    This function searches for the Ilastik executable file on the current operating system.

    Returns:
    str: The path to the Ilastik executable if found, else None.
    """

    os_name = get_os()

    if os_name == 'Darwin' or os_name == 'Linux':
        filename = 'run_ilastik.sh'
        start_path = '/Applications' if os_name == 'Darwin' else '/'
    elif os_name == 'Windows':
        filename = 'ilastik.exe'
        start_path = 'C:\\'
    else:
        print(f'Unsupported OS: {os_name}')
        return None

    return find_file(filename, start_path)