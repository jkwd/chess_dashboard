build:
	docker compose build --no-cache

up:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml up -d

down:
	docker compose -f docker-compose.yml -f docker-compose-dashboard.yml down

lint:
	docker compose run --rm chess_dagster_daemon flake8 chess_etl chess_etl_tests

test:
	docker compose run --rm chess_dagster_daemon pytest chess_etl_tests

clean:
	docker image rm chess_dashboard-chess_dagster_webserver
	docker image rm chess_dashboard-chess_dagster_daemon
	docker image rm chess_dashboard-superset

jupyter:
	docker exec -it chess_dagster_webserver jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token=''