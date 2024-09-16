- [Chess Dashboard](#chess-dashboard)
  - [Run locally](#run-locally)
  - [Running Dagster Job](#running-dagster-job)
  - [Architecture](#architecture)
  - [Architecture Diagram](#architecture-diagram)
  - [Pipeline Lineage](#pipeline-lineage)

# Chess Dashboard
## Run locally
To run locally, you'll need:
1. [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. [Github account](https://github.com/)
3. [Docker](https://docs.docker.com/engine/install/)
4. [Docker Compose](https://docs.docker.com/compose/install/)

Clone the repo and run the following commands to start the data pipeline:
```
https://github.com/jkwd/chess_dashboard.git
cd chess_dashboard
make build
make up
```

Go to [http://localhost:3000](http://localhost:3000) to view the Dagster UI.

Go to [http://localhost:8088/](http://localhost:8088/) to view the Apache Superset UI.

## Running Dagster Job
TODO

## Architecture
The data engineering project stack contains the following:
1. [dltHub](https://dlthub.com/): Ingestion Layer to load the data into the data warehouse
2. [Dagster](https://dagster.io/): To schedule and orchestrate the DAGs
3. [Postgres](https://www.postgresql.org/): To store and persist Dagster details
4. [DuckDB](https://duckdb.org/): Data Warehouse
5. [Apache Superset](https://superset.apache.org/): Dashboard Layer

## Architecture Diagram
TODO

## Pipeline Lineage
TODO