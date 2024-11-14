FROM apache/superset:latest

USER root

RUN pip install duckdb duckdb-engine

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_PASSWORD $ADMIN_PASSWORD
ENV ADMIN_EMAIL $ADMIN_EMAIL

COPY ./superset-init.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY superset_config.py /app/
# COPY dashboard.zip /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset

ENTRYPOINT [ "/superset-init.sh" ]