FROM python:3.10-slim

RUN mkdir -p /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/app

WORKDIR $DAGSTER_HOME

COPY . .

RUN pip install -e ".[dev]"

EXPOSE 3000

CMD [ "dagster-webserver", "-h", "0.0.0.0", "-p", "3000" ]
