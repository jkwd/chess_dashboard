- [Chess Dashboard](#chess-dashboard)
  - [Architecture](#architecture)
  - [Architecture Diagram](#architecture-diagram)
  - [Run locally](#run-locally)
  - [Running Dagster Job](#running-dagster-job)

# Chess Dashboard
## Architecture
The data engineering project stack contains the following:
1. [dltHub](https://dlthub.com/): Ingestion Layer to load the data into the data warehouse
2. [Dagster](https://dagster.io/): To schedule and orchestrate the DAGs
3. [Postgres](https://www.postgresql.org/): To store and persist Dagster details
4. [DuckDB](https://duckdb.org/): Data Warehouse
5. [Streamlit](https://streamlit.io/): Dashboard Layer

## Architecture Diagram
![](img/architecture.png)

## Run locally
To run locally, you'll need:
1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/)
4. [Docker Compose](https://docs.docker.com/compose/install/)

Clone the repo, create a `.env` file and run the following commands to start the data pipeline:
```
https://github.com/jkwd/chess_dashboard.git
cd chess_dashboard
cp .env.example .env
```

Edit the `CHESS_USERNAME` in the `.env` file to your username

```
make build
make up
```

Go to [http://localhost:3000](http://localhost:3000) to view the Dagster UI.

Go to [http://localhost:8501/](http://localhost:8501/) to view the Streamlit Dashboard

## Running Dagster Job
TODO