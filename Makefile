init:
	cp .env.example .env_1

build:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml build --no-cache

up:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml up -d

up-dashboard:
	docker compose -f docker-compose-dashboard.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml down

lint-python:
	docker compose run --rm chess_dagster_daemon ruff check chess_etl chess_etl_tests chess_dbt/models

lint-sql:
	docker compose run --rm chess_dagster_daemon sqlfluff lint --dialect duckdb chess_dbt/models chess_dbt/tests

fix-sql:
	docker compose run --rm chess_dagster_daemon sqlfluff fix --dialect duckdb chess_dbt/models chess_dbt/tests

pytest:
	docker compose run --rm chess_dagster_daemon pytest chess_etl_tests

dbt-unit-test:
	docker compose run --rm chess_dagster_daemon bash -c "cd chess_dbt && dbt docs generate --target prod && dbt test --target prod --select test_type:unit"

clean:
	docker image rm chess_dashboard-chess_dagster_webserver
	docker image rm chess_dashboard-chess_dagster_daemon
	docker image rm chess_dashboard-superset

jupyter:
	docker exec -it chess_dagster_webserver jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token=''