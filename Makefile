build:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml build --no-cache

up:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml down

lint-python:
	docker compose run --rm chess_dagster_daemon flake8 chess_etl chess_etl_tests chess_dbt/models

lint-sql:
	docker compose run --rm chess_dagster_daemon sqlfluff lint --dialect duckdb chess_dbt/models chess_dbt/tests

fix-sql:
	docker compose run --rm chess_dagster_daemon sqlfluff fix --dialect duckdb chess_dbt/models chess_dbt/tests

test:
	docker compose run --rm chess_dagster_daemon pytest chess_etl_tests

clean:
	docker image rm chess_dashboard-chess_dagster_webserver
	docker image rm chess_dashboard-chess_dagster_daemon
	docker image rm chess_dashboard-superset

jupyter:
	docker exec -it chess_dagster_webserver jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token=''