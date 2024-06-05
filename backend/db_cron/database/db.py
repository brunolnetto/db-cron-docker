from sqlmodel import Session, create_engine, select
import secrets

from setup.settings import settings
from database.models import TokensDB
from crud import create_token

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)
    token_obj = TokensDB(
        token=secrets.token_urlsafe(32),    
    )
    create_token(session=session, token_obj=token_obj)
