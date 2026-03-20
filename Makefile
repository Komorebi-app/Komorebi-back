.SILENT:

all: help

up:
	docker compose up -d db
	@if [ "$(dev)" = "1" ]; then \
		pip install -r requirements.txt; \
		POSTGRES_HOST=localhost python manage.py migrate; \
		POSTGRES_HOST=localhost python manage.py runserver 0.0.0.0:5555; \
	else \
		docker compose up -d api; \
	fi

down:
	docker compose down

migrations:
	POSTGRES_HOST=localhost python manage.py makemigrations

check: check-lint check-test
check-lint:
	pylint $$(git ls-files '*.py')
check-test:
	POSTGRES_HOST=localhost pytest

run:
ifndef cmd
	$(error cmd must be set, make run cmd=cmd.gx)
else
	docker exec -it komorebi-api python manage.py $(cmd)
endif

help:
	echo "Usage: make <command>"
	echo ""
	echo "    up           Start docker-compose in detached mode"
	echo "    down         Stop docker-compose"
	echo "    migrations   Run Django app migrations"
	echo "    check        Run pylint & pytest"
	echo "    check-lint   Run pylint"
	echo "    check-test   Run pytest"
	echo "    run          Run arbitrary Django manage.py command (ex: make run cmd=\"createsuperuser\")"
	echo "    help         Show this help message"
	echo ""
