# db-cron

A cron task with database. This repository is intended for Linux users.

## Installation

1. Clone the repository;
2. Run `pip install virtualenv && virtualenv .venv`;
3. Run `source .venv/bin/activate`;
4. Run `pip install -r requirements.txt`;
5. Rename `.env.template` for `.env` and alter required credentials if needed;
6. Run `docker compose up -d`;
7. Run `make up`;
8. Run `make log-cron`;

