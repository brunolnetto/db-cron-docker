from os import getenv
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv

from setup.logging import logger
from database.models import Base

from utils.misc import makedir 

class Database:
  """
  This class represents a database connection and session management object.
  It contains two attributes:
  
  - engine: A callable that represents the database engine.
  - session_maker: A callable that represents the session maker.
  """
  def __init__(self, uri: URL):
    self.uri = uri
    self.engine = create_engine(uri)
    self.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
  
  def init(self):
    """
    Connects to a PostgreSQL database using environment variables for connection details.

    Returns:
        Database: A NamedTuple with engine and conn attributes for the database connection.
        None: If there was an error connecting to the database.
    
    """
    try:
        # Create all tables defined using the Base class
        Base.metadata.create_all(self.engine)
        
        logger.info('Connection to the database established!')
        
        self._setup()
    
    except OperationalError as e:
        logger.error(f"Error connecting to database: {e}")
        return None

  def _setup(self) -> None:
    """
    Sets up the database with the required tables and permissions.

    Returns:
        None: If the database setup was successful.
    """
    load_dotenv()

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
    GRANT pg_read_all_data, pg_write_all_data ON DATABASE "{database_name}_test" TO "{user}";
    """

    try:
        with self.engine.connect() as conn:
            conn.execute(setup_query)
            logger.info('Database setup completed!')
    except OperationalError as e:
        logger.error(f"Error setting up database: {e}")
  
  def connect(self):
    """
    Connects to the database.

    Returns:
        Connection: A connection object for the database.
    """
    with self.engine.connect() as conn:
      yield conn