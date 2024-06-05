from typing import Any

from sqlmodel import Session

from db_cron.database.models import TokensDB

def create_token(*, session: Session, token_obj: TokensDB):
    session.add(token_obj)
    session.commit()
    session.refresh(token_obj)
