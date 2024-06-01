""" 
  - Nome do projeto : ETL - CNPJs da Receita Federal do Brasil
  - Objetivo        : Baixar, transformar e carregar dados da Receita Federal do Brasil
"""

from setup.base import (
    get_sink_folder, 
    init_database, 
    setup_database,
)

# Folders and database setup
download_folder, extract_folder = get_sink_folder()
database = init_database()
setup_database(database)
