# Stage 1: Install dependencies
FROM python:3.12-slim-bullseye

WORKDIR /app

# Install the required packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get -y --fix-missing install cron python3 python3-pip postgresql-client

# Activate the virtual environment and install dependencies
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install uv
COPY requirements.txt .
RUN pip3 install virtualenv

# Create a virtual environment in the container
RUN pip3 install -r requirements.txt

# Copy your application code
COPY .env .
COPY backend/ .
COPY scripts/ .
COPY alembic.ini .

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
