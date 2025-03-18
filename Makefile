.DEFAULT_GOAL := all

toml_sort:
	toml-sort pyproject.toml --all --in-place

isort:
	poetry run isort .

black:
	poetry run black .

docker-lint:
	docker compose -f ./docker-compose.local-tests.yml up --build lint 


#test

tests:
	poetry run pytest


docker-tests:
	docker compose -f ./docker-compose.local-tests.yml up --build test

docker-makemigrations:
	docker compose exec api /bin/bash -c "alembic revision --autogenerate"

docker-migrate:
	docker compose exec api /bin/bash -c "alembic upgrade head"

# dev 

python-dev: 
	poetry run uvicorn src.main:api

docker-dev: 
	docker compose up --build

