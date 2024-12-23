#!/bin/bash

# create Admin user, you can read these values from env or anywhere else possible
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"

# Upgrading Superset metastore
superset db upgrade

# setup roles and permissions
superset superset init 

# Setup duckdb connection
superset set_database_uri -d chess_db -u duckdb:///superset_home/chess.duckdb

# Import dashboard and dataset
superset import_datasources -p ./dataset.zip -u ${ADMIN_USERNAME}
superset import-dashboards -p ./dashboard.zip -u ${ADMIN_USERNAME}

# Starting server
/bin/sh -c /usr/bin/run-server.sh