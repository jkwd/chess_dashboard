build:
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

test:
	docker-compose up -d chess_dagster
	docker exec -it chess_dagster pytest chess_etl_tests
	docker-compose down

jupyter-up:
	docker exec -it chess_dagster jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token=''