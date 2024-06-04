#/bin/bash
# This script is used to run the cron task

# pip install -r /app/requirements.txt
source "/opt/venv/bin/activate"

pip3 list

echo "Cron task is running" 
echo "$(which python3)"
/opt/venv/bin/python3 /app/backend/db_cron/main.py

