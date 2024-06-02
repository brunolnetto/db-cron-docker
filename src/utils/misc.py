from sys import stdout
from shutil import rmtree
from os import makedirs

from src.setup.logging import logger

def repeat_token(token: str, n: int):
    """
    Repeat a token n times.

    Args:
        token (str): The token to repeat.
        n (int): The number of times to repeat the token.

    Returns:
        token (str): The token repeated n times.
        n (int): The number of times to repeat the token.
    """

    return ''.join([token] * n)

def invert_dict_list(dict_: dict):
    """
    Inverts a dictionary where the values are lists of keys.
    
    Args:
        dict_ (dict): The dictionary to be inverted.
        
    Returns:
        dict: The inverted dictionary where the keys are the values from the original dictionary
              and the values are the corresponding keys from the original dictionary.
    """
    inverted_dict = dict()
    for key, values_list in dict_.items():
        for value in values_list:
            if value not in inverted_dict:
                inverted_dict[value] = [key]
            else: 
                inverted_dict[value].append(key)
    
    return inverted_dict
    
def makedir(
    folder_name: str, 
    is_verbose: bool = False
):
    """
    Creates a new directory if it doesn't already exist.

    Args:
        folder_name (str): The name of the folder to create.
        is_verbose (bool, optional): Whether to log verbose information. Defaults to False.
    """
    if not path.exists(folder_name):
        makedirs(folder_name)
        
        if(is_verbose):
            logger.info('Folder: \n' + repr(str(folder_name)))

    else:
        if(is_verbose):
            logger.warn(f'Folder {repr(str(folder_name))} already exists!')

def update_progress(index, total, message):
    """
    Updates and displays a progress message.

    Args:
        index (int): The current index.
        total (int): The total number of items.
        message (str): The message to display.
    """
    percent = (index * 100) / total
    curr_perc_pos = f"{index:0{len(str(total))}}/{total}"
    progress = f'{message} {percent:.2f}% {curr_perc_pos}'
    
    stdout.write(f'\r{progress}')
    stdout.flush()

def convert_to_bytes(size_str):
  """
  This function converts a size string (e.g., "22K", "321M") into bytes.

  Args:
      size_str (str): The size string to convert.

  Returns:
      int: The size in bytes, or None if the format is invalid.
  """
  size_value = float(size_str[:-1])  # Extract numerical value
  size_unit = size_str[-1].upper()  # Get the unit (K, M, G)

  unit_multiplier = {
      'K': 1024,
      'M': 1024 * 1024,
      'G': 1024 * 1024 * 1024
  }

  if size_unit in unit_multiplier:
    return int(size_value * unit_multiplier[size_unit])
  else:
    return None  # Handle invalid units

def remove_folder(folder: str):
    """
    Removes a folder and all its contents.

    Args:
        folder (str): The path to the folder to remove.

    Raises:
        Exception: If an error occurs while deleting the folder.
    """
    try:
        rmtree(folder)
    except Exception as e:
        logger.error(f"Error deleting folder {folder}: {e}")