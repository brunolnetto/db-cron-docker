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

def setup_database(database: Database) -> None:
    # Get environment variables
    # Get the host based on the environment
    user = getenv('POSTGRES_USER', 'postgres')
    passw = getenv('POSTGRES_PASSWORD', 'postgres')
    database_name = getenv('POSTGRES_NAME')

    # Create the database engine and session maker
    setup_query=f"""
    CREATE DATABASE {database_name} IF NOT EXISTS
        WITH
        OWNER = {user}
        ENCODING = 'UTF8'
        CONNECTION LIMIT = -1;

    CREATE DATABASE "{database_name}_Test" IF NOT EXISTS
        WITH
        OWNER = "$POSTGRES_USER"
        ENCODING = 'UTF8'
        CONNECTION LIMIT = -1;

    CREATE USER "{user}" WITH PASSWORD "{passw}";
    GRANT pg_read_all_data, pg_write_all_data ON DATABASE "{name}_test" TO "{user}";
    """

    try:
        with database.engine.connect() as conn:
            conn.execute(setup_query)
            logger.info('Database setup completed!')
    except OperationalError as e:
        logger.error(f"Error setting up database: {e}")

def init_database() -> Union[Database, None]:
    """
    Connects to a PostgreSQL database using environment variables for connection details.

    Returns:
        Database: A NamedTuple with engine and conn attributes for the database connection.
        None: If there was an error connecting to the database.
    
    """
    env_path = path.join(getcwd(), '.env')
    load_dotenv(env_path)
    
    # Get the host based on the environment
    if getenv('ENVIRONMENT') == 'docker':
        host = get_postgres_host()
    else: 
        host = getenv('POSTGRES_HOST', 'localhost')

    try:
        # Get environment variables
        port = int(getenv('POSTGRES_PORT', '5432'))
        user = getenv('POSTGRES_USER', 'postgres')
        passw = getenv('POSTGRES_PASSWORD', 'postgres')
        database_name = getenv('POSTGRES_NAME')
        
        # Connect to the database
        db_uri = f'postgresql://{user}:{passw}@{host}:{port}/{database_name}'

        # Create the database engine and session maker
        timeout=5*60*60 # 5 hours
        database_obj = create_database(db_uri, session_timeout=timeout)

        # Create all tables defined using the Base class
        Base.metadata.create_all(database_obj.engine)
        
        logger.info('Connection to the database established!')
        return database_obj
    
    except OperationalError as e:
        logger.error(f"Error connecting to database: {e}")
        return None

