from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database

from backend.db_cron.setup.logging import logger
from backend.db_cron.setup.settings import settings
from backend.db_cron.database.models import Base

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

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            logger.info("New Database Created" + database_exists(self.engine.url)) 
        else:
            logger.info("Database Already Exists")

        self.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def setup(self) -> None:
        """
        Sets up the database with the required tables and permissions.
    
        Returns:
            None: If the database setup was successful.
        """
        database_name=settings.POSTGRES_DBNAME
        user=settings.POSTGRES_USER
        passw=settings.POSTGRES_PASSWORD
    
        # Create the database engine and session maker
        setup_query=text(f"""
        CREATE DATABASE {database_name}
            WITH
            OWNER = postgres
            ENCODING = 'UTF8'
            CONNECTION LIMIT = -1;
    
        CREATE USER {user} WITH PASSWORD '{passw}';
        GRANT pg_read_all_data, pg_write_all_data ON DATABASE {database_name} TO {user};
        """)

        try:
            with self.engine.connect() as conn:
                conn.execute(setup_query)
                logger.info('Database setup completed!')
        except OperationalError as e:
            logger.error(f"Error setting up database: {e}")

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
            logger.info('Connection to the database established!')        
        
        except OperationalError as e:
            logger.error(f"Error connecting to database: {e}")
            return None

    def connect(self):
        """
        Connects to the database.

        Returns:
            Connection: A connection object for the database.
        """
        with self.engine.connect() as conn:
            yield conn
    
    def __repr__(self) -> str:
        return f"Database(uri={self.uri})" 