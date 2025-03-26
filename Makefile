.DEFAULT_GOAL := all

toml_sort:
	toml-sort pyproject.toml --all --in-place

isort:
	poetry run isort .

black:
	poetry run black .

ruff:
	poetry run ruff check .

docker-lint:
	sudo docker compose -f ./docker-compose.local-tests.yml up --build lint 


#test

tests:
	poetry run pytest


docker-tests:
	sudo docker compose -f ./docker-compose.local-tests.yml up --build test

docker-makemigrations:
	sudo docker compose exec api /bin/bash -c "alembic revision --autogenerate"

docker-migrate:
	sudo docker compose exec api /bin/bash -c "alembic upgrade head"

docker-exec-tests:
	sudo docker compose exec api /bin/bash -c "pytest -s"

# dev 

python-dev: 
	poetry run uvicorn src.main:api

docker-dev: 
	sudo docker compose up --build

