from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from tests.conftest import engine
from database.models import UserDB

Session = sessionmaker(bind=engine)

def app():
    with Session() as session:
        session.add_all(
            [
                UserDB(
                    username="John Smith",
                    email="john@mail.com",
                    password="mypwd1234!",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
                UserDB(
                    username="Amy Johnson",
                    email="amy@mail.com",
                    password="mypwd1234?",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                ),
            ]
        )
        session.commit()

    with engine.connect() as conn:
        stmt = select(UserDB)
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()