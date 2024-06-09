from os import getenv, path, getcwd
from dotenv import load_dotenv

from utils.docker import get_postgres_host

def get_connection_dict():
    env_path = path.join(getcwd(), '.env')
    load_dotenv(env_path)

    # Get the host based on the environment
    is_docker=getenv('ENVIRONMENT') == 'docker' or \
              getenv('ENVIRONMENT') == 'docker-testing'
    if is_docker:
        host = get_postgres_host()
    else: 
        host = getenv('POSTGRES_HOST', 'localhost')

    # Get environment variables
    port = int(getenv('POSTGRES_PORT', '5432'))

    user = getenv('POSTGRES_USER', 'postgres')
    passw = getenv('POSTGRES_PASSWORD', 'postgres')
    database_name = getenv('POSTGRES_DBNAME')

    return dict(
        host=host,
        port=port,
        user=user,
        password=passw,
        database_name=database_name
    )

def get_db_uri(has_dbname=True):
    """
    Build the database URI based on the environment variables.

    Returns:
        str: The database URI.
    """
    conn_dict=get_connection_dict()
    
    # Connect to the database
    dsn_str='postgresql'
    credentials=f"{conn_dict['user']}:{conn_dict['password']}"
    route=f"{conn_dict['host']}:{conn_dict['port']}"
    db_name=conn_dict['database_name']

    if has_dbname:
        return f"{dsn_str}://{credentials}@{route}/{db_name}"
    else:
        return f"{dsn_str}://{credentials}@{route}"