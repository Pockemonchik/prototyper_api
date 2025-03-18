# PROTOTYPER_API

Сервис для предоставления данных по REST API для проекта prototyper

## Getting started

Скачайте проект:

```
git clone --recurse-submodules https://
```

Для настройки проекта для локальной разработки выолните следующие шаги:

1. Создать файл .env.dev и поместить в него переменные полученныe от разработчка
   Пример - example.env.dev

2. Запустить проект:

- Для Linux:

```
sudo docker compose up -d --build

```

- Для Windows (docker desktop)

```
docker-compose up -d --build

```

4. Установить python зависимости локально, для корректной работы среды разработки:

- Установить python==3.12 и pip
- Установить poetry (https://python-poetry.org/docs/)

- Выполнить команды:

```
poetry config virtualenvs.in-project true

poetry install

```

- В своей ide указать интерпретатор ./venv/bin/python

## Test and lint

Для тестирования Создать файл .env.test и поместить в него переменные полученныe от разработчка
Пример - example.env.test

- Прогон тестов:

```
sudo docker compose -f ./docker-compose.local-tests.yml up --build test

```

Для Windows (docker desktop)

```
docker-compose -f ./docker-compose.local-tests.yml up --build test

```

- Прогон линтеров:

```
sudo docker compose -f ./docker-compose.local-tests.yml up --build lint

```

Для Windows (docker desktop)

```
docker-compose -f ./docker-compose.local-tests.yml up --build lint

```

- Тестирование на производительность

```
poetry run locust -f ./tests/perfomance/locust/locustfile.py

```

## Logs and Metrics

##### Логирование

Логи пишутся в файл loguru.log в корне проекта.
Чтобы настроить уровни логирования необходимо изменить
перменную LOGGER_LEVELS в .env.\*.

LOGGER_LEVELS='["INFO","DEBUG","ERROR","WARNING"]'
Убрать один из елементов массива выше.

##### Метрики

Consumers отдают метрики по адресу localhost:8002/metrics

Dashboard для импорта в Graphana для метрик по консумерам

- docs/graphana/faststream_dashboard.json

Rest Api отдает метрики по адресу localhost:8000/metrics

Dashboard для импорта в Graphana для метрик по api

- docs/graphana/fastapi_dashboard.json

## Usage

##### REST API

Для получение данных реализовано REST API.

Документация (swagger) c описанием методов и примерами данных для запросов
располагается по адресу http://localhost:8000/docs

Реализованы следующие методы:

-
-
