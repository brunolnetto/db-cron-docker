from pydantic_core import MultiHostUrl
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from database.utils import get_db_uri
from pydantic import (
    PostgresDsn,
    computed_field,
)
from dotenv import load_dotenv
import os

from typing import Union

from warnings import warn
import toml

# Default database values
DEFAULT_PASSWORD = "changethis"
POSTGRES_DSN_SCHEME = "postgresql+psycopg2"

# Project settings 
toml_file = "pyproject.toml"
current_folder = os.path.dirname(__file__)
tom_path=os.path.join(current_folder, '..', '..', '..', toml_file)

with open(tom_path, "r") as f:
    config = toml.load(f)

env_path=os.path.join(current_folder, '..', '..', '..', '.env')

# Settings class
class Settings(BaseSettings):
    """App settings."""

    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_ignore_empty=True, 
        extra="ignore"
    )

    VERSION: str = config["tool"]["poetry"]["version"]
    PROJECT_NAME: str = config["tool"]["poetry"]["name"]
    
    ENVIRONMENT: str = "development"
    
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DOCKER_HOST: str = "db-cron-task" if ENVIRONMENT == "docker" else ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = DEFAULT_PASSWORD
    POSTGRES_DBNAME: str = ""

    LOG_FILES_HORIZON: int = 5

    def _check_default_postgres_password(self, var_name: str, value: Union[str, None]) -> None:
        if value == DEFAULT_PASSWORD:
            message = (
                f'The value of {var_name} is "{DEFAULT_PASSWORD}", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "development":
                warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    # Postgres settings
    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        load_dotenv()
        return get_db_uri()
    
# Instantiate the settings
settings = Settings()