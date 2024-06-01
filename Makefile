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

kill-db: ## Kill the database container. Usage: make kill-db
	docker inspect db-cron-task | jq -r '.[0].State.Pid' | sudo xargs kill

kill-cron: ## Kill the database container. Usage: make kill-db
	docker inspect cron-task | jq -r '.[0].State.Pid' | sudo xargs kill

kill: kill-db kill-cron ## Kill the database and cron containers. Usage: make kill

up: ## Start the containers. Usage: make up
	docker-compose up -d

down: ## Stop the containers. Usage: make down
	docker-compose down

ps: ## List the containers. Usage: make ps
	docker ps -a

prune: ## Remove all containers. Usage: make prune
	docker system prune -a

build: ## Build the containers. Usage: make build
	docker-compose build

log-cron: ## Show the logs of the crawler container. Usage: make log-cron
	docker logs -f cron-task

lint: ## perform inplace lint fixes
	ruff check --fix .

