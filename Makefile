init:
	cp .env.example .env

build:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml build --no-cache

up:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml up -d

up-dashboard:
	docker compose -f docker-compose-dashboard.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml down

lint-python:
	docker compose run --rm chess_dagster_user_code ruff check chess_etl chess_etl_tests chess_dbt/models

lint-sql:
	docker compose run --rm chess_dagster_user_code sqlfluff lint --dialect duckdb chess_dbt/models chess_dbt/tests

fix-sql:
	docker compose run --rm chess_dagster_user_code sqlfluff fix --dialect duckdb chess_dbt/models chess_dbt/tests

pytest:
	docker compose run --rm chess_dagster_user_code pytest chess_etl_tests

dbt-unit-test:
	docker compose run --rm chess_dagster_user_code bash -c "cd chess_dbt && dbt compile --target prod && dbt test --target prod --select test_type:unit"

run: up
	docker compose exec chess_dagster_user_code bash -c "sleep 5 && dagster job execute -f chess_etl/definitions.py -j all_assets_job"

clean:
	docker image rm chess_dashboard-chess_dagster_webserver
	docker image rm chess_dashboard-chess_dagster_daemon
	docker image rm chess_dagster_user_code_image
	docker image rm chess_dashboard-streamlit-dashboard