IMAGE_NAME = chess_dashboard
STREAMLIT_PORT = 8501
JUPYTER_PORT = 8888
CONTAINER_NAME = chess_dashboard_container
VOLUME = $(shell pwd):/app

build:
	docker build -t $(IMAGE_NAME) .

up:
	docker run --rm -d -p $(STREAMLIT_PORT):$(STREAMLIT_PORT) -p $(JUPYTER_PORT):$(JUPYTER_PORT) -v $(VOLUME) --name $(CONTAINER_NAME) $(IMAGE_NAME)

down:
	docker stop $(CONTAINER_NAME)

clean:
	docker rmi -f $(IMAGE_NAME)

jupyter:
	jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''
