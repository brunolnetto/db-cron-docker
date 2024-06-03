FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy your application code
COPY .env .
COPY backend/ .
COPY scripts/ .

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/backend"

# Install dependencies:
COPY requirements.txt .

# Install uv
RUN pip install uv
RUN uv pip install -r requirements.txt --system

# Install the required packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install cron python3 python3-pip postgresql-client

# Cron jobs
RUN echo '* * * * * bash /app/scripts/cron_task.sh >> /var/log/cron.log 2>&1' > cron-config

# Give execution rights on the cron job
RUN chmod 0644 cron-config

# Apply cron job
RUN crontab cron-config

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD echo "starting" && \
    echo "continuing" && \
    (cron) && \
    echo "tailing..." && \
    : >> /var/log/cron.log && \
    tail -f /var/log/cron.log
