.PHONY: install migrate test lint format

install:
	python -m venv .venv && \
	. .venv/bin/activate && \
	pip install -r requirements.txt

migrate:
	alembic upgrade head

test:
	pytest -s -x --cov=app tests

lint:
	flake8 app tests

format:
	black . && isort .