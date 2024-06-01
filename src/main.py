""" 
  - Nome do projeto : ETL - CNPJs da Receita Federal do Brasil
  - Objetivo        : Baixar, transformar e carregar dados da Receita Federal do Brasil
"""
from database.schemas import Database
from setup.base import get_sink_folder
from setup.logging import logger
from setup.config import get_database_uri

# Folders and database setup
download_folder, extract_folder = get_sink_folder()

# Get the database URI
db_uri=get_database_uri()

# Create the database object
database=Database(db_uri)
database.init()

logger.info('Hello world')