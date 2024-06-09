from setup.logging import logger
from setup.settings import settings
#from database.schemas import Database

# Get the database URI
db_uri=settings.SQLALCHEMY_DATABASE_URI_NO_DBNAME

# Create the database object
#database=Database(db_uri)
logger.info('Hello world')