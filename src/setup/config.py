from dotenv import load_dotenv
from os import path, getcwd, getenv
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError

from utils.docker import get_postgres_host
from setup.logging import logger

def get_database_uri():
    """
    Get the database URI based on the environment variables or default paths.

    Returns:
        URL: A URL object with the database connection details.
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
        
        return URL(
            drivername='postgresql',
            username=user,
            password=passw,
            host=host,
            port=port,
            database=database_name,
            query={ 'client_encoding': 'utf8' }
        )

    except OperationalError as e:
        logger.error(f"Error creating database URI: {e}")