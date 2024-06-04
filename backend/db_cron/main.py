from setup.logging import logger
from setup.settings import settings
from database.schemas import Database

# Get the database URI
db_uri=settings.SQLALCHEMY_DATABASE_URI
print(db_uri)
# Create the database object
database=Database(db_uri)
# database.setup()
# database.init()

logger.info('Hello world')