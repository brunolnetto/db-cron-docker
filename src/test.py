from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine, text

from setup.settings import settings

def create_database(uri: str, database_name: str) -> None:
  """
  Creates the database with the required owner and permissions.

  Args:
      uri: The database connection URI.

  Raises:
      OperationalError: If there's an error creating the database.
  """
  engine = create_engine(uri, poolclass=QueuePool)
  with engine.connect() as conn:
      conn.execution_options(isolation_level="AUTOCOMMIT").execute(text(f"""
      CREATE DATABASE {database_name}
          WITH
          OWNER = postgres
          ENCODING = 'UTF8'
          CONNECTION LIMIT = -1;

      CREATE USER postgres WITH PASSWORD 'postgres';
      GRANT pg_read_all_data, pg_write_all_data ON DATABASE postgres TO postgres;
      """))
  print('Database setup completed!')

def connect_to_database(settings: dict) -> sessionmaker:
  """
  Connects to the PostgreSQL database using settings.

  Args:
      settings: A dictionary containing database connection details.

  Returns:
      A sessionmaker object for interacting with the database.

  Raises:
      OperationalError: If there's an error connecting to the database.
  """
  host = settings.get('POSTGRES_DOCKER_HOST', settings['POSTGRES_HOST'])
  port = settings['POSTGRES_PORT']
  user = settings['POSTGRES_USER']
  passw = settings['POSTGRES_PASSWORD']
  database_name = settings['POSTGRES_DBNAME']

  uri = f'postgresql://{user}:{passw}@{host}:{port}/{database_name}'

  engine = create_engine(
      uri,
      poolclass=QueuePool,
      pool_size=20,     # Adjust pool size as needed
      max_overflow=10,  # Adjust max overflow as needed
  ) 

  try:
      engine.connect()
      print('Connection to the database established!')
      return sessionmaker(autocommit=False, autoflush=False, bind=engine)
  except OperationalError as e:
      print(f"Error connecting to database: {e}")
      raise  # Re-raise the exception for better handling


if __name__ == '__main__':
  # Create the database if it doesn't exist
  uri=f'postgresql://postgres:postgres@localhost:{settings.POSTGRES_PORT}'
  database_name=settings.POSTGRES_DBNAME
  create_database(uri, database_name)

  # Get a session maker for interacting with the database
  session_maker = connect_to_database(settings)
