from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker

from src.database.models import UserDB
from conftest import engine, get_test_users

Session = sessionmaker(bind=engine)

def app():
    with Session() as session:
        session.add_all(get_test_users())
        session.commit()

    with engine.connect() as conn:
        stmt = select(UserDB)
        print(conn.execute(stmt).fetchall())

if __name__ == "__main__":
    app()