#/bin/bash
# This script is used to run the cron task

# alembic revision --autogenerate -m 'Initial migration' && alembic upgrade head
python3 /app/src/db_cron/main.py
# echo "Cron task is running" 
