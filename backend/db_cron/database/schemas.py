from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import ProgrammingError
import time

from setup.logging import logger
from setup.settings import settings
from database.models import Base

class Database:
    """
    This class represents a database connection and session management object.
    It contains two attributes:
    
    - engine: A callable that represents the database engine.
    - session_maker: A callable that represents the session maker.
    """
    def __init__(self, uri: URL):
        self.uri = uri
    
        self.engine = create_engine(
            uri, poolclass=QueuePool, pool_size=20, max_overflow=10,
        )
        
        self.create_connection()
        self.create_database()

        self.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def connect(self):
        """
        Connects to the database.

        Returns:
            Connection: A connection object for the database.
        """
        with self.engine.connect() as conn:
            yield conn

    def create_connection(self):
        conn = None
        while not conn:
            try:
                conn = self.engine.connect()
                logger.info("Database connection successful")
            
            except OperationalError as e:
                logger.error(e)
                time.sleep(5)

        return conn

    def create_database(self):
        """
        Attempts to create the database if it doesn't exist.

        Args:
            engine: The SQLAlchemy engine object.
            settings: A dictionary containing database connection details.

        Raises:
            DatabaseError: If there's an error checking or creating the database.
        """
        database_name = settings.POSTGRES_DBNAME

        with self.engine.connect() as conn:    
            try:
                # Database doesn't exist, proceed with creation
                ddl_query=text(f"CREATE DATABASE {database_name}")
                conn.execution_options(isolation_level="AUTOCOMMIT")\
                    .execute(ddl_query)
            
                logger.info(f"Database {database_name} created successfully!")
                
            except ProgrammingError:
                logger.warn(f"Database {database_name} already exists. Skipping creation.")


    def init(self):
        """
        Connects to a PostgreSQL database using environment variables for connection details.
    
        Returns:
            Database: A class with engine and conn attributes for the database connection.
            None: If there was an error connecting to the database.
    
        """
        try:
            # Create all tables defined using the Base class
            Base.metadata.create_all(self.engine)
            logger.info('Tables created successfully!')        
        
        except OperationalError as e:
            logger.error(f"Error connecting to database: {e}")
            return None
    
    def __repr__(self) -> str:
        return f"Database(uri={self.uri})" 