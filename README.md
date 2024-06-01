# db-cron

A cron task with database. This repository is intended for Linux users.

## Installation

1. Clone the repository;
2. Run `pip install virtualenv && virtualenv .venv`;
3. Run `source .venv/bin/activate`;
4. Run `pip install -r requirements.txt`;
5. Run `docker compose up -d`;
6. Run `make up`;
7. Run `make log-cron`;

On step 7, you should see the following message:

```   
(...)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "db-cron-task" (172.31.0.2), port 5433 failed: Connection timed out
	Is the server running on that host and accepting TCP/IP connections?

```
