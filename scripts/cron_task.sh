#/bin/bash
# This script is used to run the cron task

# pip install -r /app/requirements.txt
source "/opt/venv/bin/activate"

echo "Cron task is running" 
/opt/venv/bin/python3 /app/backend/app/main.py

