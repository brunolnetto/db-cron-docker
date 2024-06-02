from os import getenv, path, getcwd
from dotenv import load_dotenv
from typing import Union
from psycopg2 import OperationalError

from setup.logging import logger
from database.models import Base
from database.schemas import Database
from database.engine import create_database
from utils.docker import get_postgres_host
from utils.misc import makedir


def get_sink_folder():
    """
    Get the output and extracted file paths based on the environment variables or default paths.

    Returns:
        Tuple[str, str]: A tuple containing the output file path and the extracted file path.
    """
    env_path = path.join(getcwd(), '.env')
    load_dotenv(env_path)

    root_path = path.join(getcwd(), 'data')
    default_output_file_path = path.join(root_path, 'DOWNLOAD_FILES')
    default_input_file_path = path.join(root_path, 'EXTRACTED_FILES')

    # Read details from ".env" file:
    output_route = getenv('DOWNLOAD_PATH', default_output_file_path)
    extract_route = getenv('EXTRACT_PATH', default_input_file_path)

    # Create the output and extracted folders if they do not exist
    output_folder = path.join(root_path, output_route)
    extract_folder = path.join(root_path, extract_route)

    makedir(output_folder)
    makedir(extract_folder)

    return output_folder, extract_folder
