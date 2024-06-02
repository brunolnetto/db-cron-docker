from logging.config import fileConfig
from alembic import context

from src.database.models import Base
from src.database.schemas import Database
from src.setup.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Get environment variables
if settings.ENVIRONMENT == 'docker':
    host = settings.POSTGRES_DOCKER_HOST
else:
    host = settings.POSTGRES_HOST

port = settings.POSTGRES_PORT
user = settings.POSTGRES_USER
passw = settings.POSTGRES_PASSWORD
database_name = settings.POSTGRES_DBNAME

# Connect to the database
uri = f'postgresql://postgres:postgres@{host}:{port}'

database = Database(uri)

config.attributes['sqlalchemy.url'] = uri

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Create the database
    database.setup()
    database.init()

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = database.engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        database.setup()
        database.init()

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
