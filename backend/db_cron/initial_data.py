import logging

from sqlmodel import Session

from setup.settings import settings
from database.schemas import Database
from database.db import init_db

uri = settings.SQLALCHEMY_DATABASE_URI
engine = Database(uri).engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()