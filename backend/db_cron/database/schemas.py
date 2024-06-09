from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy import create_engine, pool
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database

from setup.logging import logger
from database.models import Base
from .utils import get_db_uri

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
            uri,
            poolclass=pool.QueuePool,   # Use connection pooling
            pool_size=20,               # Adjust pool size based on your workload
            max_overflow=10,            # Adjust maximum overflow connections
            pool_recycle=3600           # Periodically recycle connections (optional)
        )

        self.session_maker = sessionmaker(
            autocommit=False, 
            autoflush=False, 
            bind=self.engine
        )

        self.create_database()
        self.test_connection()
        self.init()

    def test_connection(self):
        """

        Tests the connection to the database.

        Raises:
            Exception: If there's an error connecting to the database.
        """

        # Test the connection
        try:
            with self.engine.connect() as conn:
                query = text("SELECT 1")

                # Test the connection
                conn.execute(query)

                logger.info('Connection to the database established!')
        
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")

    def create_database(self):
        """
        Attempts to create the database if it doesn't exist.

        Args:
            engine: The SQLAlchemy engine object.
            settings: A dictionary containing database connection details.

        Raises:
            DatabaseError: If there's an error checking or creating the database.
        """
        # Get the database URI
        db_uri = get_db_uri()
        
        # Create the database if it does not exist
        if not database_exists(db_uri): 
            create_database(db_uri)


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