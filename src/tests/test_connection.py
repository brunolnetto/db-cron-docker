from sqlalchemy.sql import text

from tests.conftest import engine

## To run this script, you need to have a PostgreSQL server running. 
# docker run --rm -d --name postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres
# docker exec -it postgres psql -U myuser -c 'CREATE DATABASE mydb;'

def app():
    with engine.connect() as conn:
        stmt = text("select * from pg_database")
        print(conn.execute(stmt).fetchall())


if __name__ == "__main__":
    app()