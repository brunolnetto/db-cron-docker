import uuid
from datetime import datetime
from secrets import token_urlsafe

from setup.settings import settings
from database.core import Database
from models.token import TokensDB
from repositories.token_repository import TokenRepository

# Get the database URI
db_uri=settings.SQLALCHEMY_DATABASE_URI

# Create the database object
database=Database(db_uri)

with database.session_maker() as session:
    token=TokensDB(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        token=token_urlsafe(),
    )
    TokenRepository(session).create_token(token)

