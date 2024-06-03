#/bin/bash
# This script is used to run the cron task

pip install -r /app/requirements.txt

echo "Cron task is running" 
python3 /app/backend/db_cron/main.py

