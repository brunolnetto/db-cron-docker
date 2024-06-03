.PHONY: build run stop ps host

OMIT_PATHS := "backend/tests/*"

define PRINT_HELP_PYSCRIPT
import re, sys

regex_pattern = r'^([a-zA-Z_-]+):.*?## (.*)$$'

for line in sys.stdin:
	match = re.match(regex_pattern, line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean-logs: # Removes log info. Usage: make clean-logs
	rm -fr build/ dist/ .eggs/
	find . -name '*.log' -o -name '*.log' -exec rm -fr {} +

clean-test: # Remove test and coverage artifacts
	rm -fr .tox/ .testmondata* .coverage coverage.* htmlcov/ .pytest_cache

clean-cache: # remove test and coverage artifacts
	find . -name '*cache*' -exec rm -rf {} +

clean: clean-logs clean-test clean-cache ## Add a rule to remove unnecessary assets. Usage: make clean

env: ## Creates a virtual environment. Usage: make env
	pip install virtualenv
	virtualenv .venv

install: ## Installs the python requirements. Usage: make install
	pip install uv
	uv pip install -r requirements.txt

search: ## Searchs for a token in the code. Usage: make search token=your_token
	grep -rnw . \
	--exclude-dir=venv \
	--exclude-dir=.git \
	--exclude=poetry.lock \
	-e "$(token)"

replace: ## Replaces a token in the code. Usage: make replace token=your_token
	sed -i 's/$(token)/$(new_token)/g' $$(grep -rl "$(token)" . \
		--exclude-dir=venv \
		--exclude-dir=.git \
		--exclude=poetry.lock)

minimal-requirements: ## Generates minimal requirements. Usage: make minimal-requirements
	python3 scripts/clean_packages.py requirements.txt requirements.txt

db-ip: ## Get the database IP. Usage: make db-ip
	docker inspect db-cron-task | jq -r '.[0].NetworkSettings.Networks[].IPAddress'

kill-container: ## Kill the database container. Usage: make kill-db
	docker inspect $(container) | jq -r '.[0].State.Pid' | sudo xargs kill

kill-db: ## Kill the database container. Usage: make kill-db
	$(MAKE) kill-container container=db-cron-task

kill-cron: ## Kill the database container. Usage: make kill-db
	$(MAKE) kill-container container=cron-task

logs: ## Show the logs of the  container. Usage: make log-cron
	docker logs -f $(container)

logs-db: ## Show the logs of the db-cron-task container. Usage: make log-cron
	$(MAKE) logs container="db-cron-task"

logs-cron: ## Show the logs of the cron-task container. Usage: make log-cron
	$(MAKE) logs container="cron-task"

kill: kill-db kill-cron ## Kill the database and cron containers. Usage: make kill

migrations: ## Create the migrations. Usage: make migrations
	alembic revision --autogenerate -m "Create a baseline migrations"
	alembic upgrade head

exec: ## Execute a command in the container. Usage: make exec container="cron-task" command="ls -la"
	docker exec -it $(container) $(command)

ls: ## Execute a bash in the container. Usage: make bash
	$(MAKE) exec container=$(container) command="ls -la"

ls-cron: ## Execute a bash in the container. Usage: make bash
	$(MAKE) ls container='cron-task'

bash: ## Execute a bash in the container. Usage: make bash
	$(MAKE) exec container=$(container) command="/bin/bash"

bash-cron: ## Execute a bash in the cron-task container. Usage: make bash-cron
	$(MAKE) bash container=cron-task

bash-db: ## Execute a bash in the db-cron-task container. Usage: make bash-db
	$(MAKE) bash container=db-cron-task

test: ## Run the tests. Usage: make test
	pytest -v --cov=backend --cov-report=term-missing --cov-fail-under=100 --cov-config=.coveragerc backend/tests

up: ## Start the containers. Usage: make up
	docker-compose up -d

down: ## Stop the containers. Usage: make down
	docker-compose down

restart: down build up ## Restart the containers. Usage: make restart

ps: ## List the containers. Usage: make ps
	docker ps -a

prune: ## Remove all containers. Usage: make prune
	docker system prune

build: ## Build the containers. Usage: make build
	docker-compose build

lint: ## perform inplace lint fixes
	ruff check --fix .

