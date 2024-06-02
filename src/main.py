""" 
  - Nome do projeto : ETL - CNPJs da Receita Federal do Brasil
  - Objetivo        : Baixar, transformar e carregar dados da Receita Federal do Brasil
"""

from setup.logging import logger
from setup.config import get_database_uri
from database.schemas import Database

# Get the database URI
db_uri=get_database_uri()

# Create the database object
database=Database(db_uri)
database.init()

logger.info('Hello world')