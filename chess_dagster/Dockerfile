FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

# Download stockfish
# RUN apt-get update && apt-get install --no-install-recommends --assume-yes stockfish

# Create directory for dbt profile
RUN mkdir -p /root/.dbt

# Copy dbt profile
COPY profiles.yml /root/.dbt/profiles.yml

# Set working directory for DAGSTER_HOME
RUN mkdir -p /opt/dagster/app

ENV DAGSTER_HOME=/opt/dagster/app

WORKDIR $DAGSTER_HOME

# Copy source code
COPY . .

# Install dependencies
RUN pip install .[dev]

# Expose port 3000 for UI
EXPOSE 3000

# Start the dagster webserver
CMD [ "dagster-webserver", "-h", "0.0.0.0", "-p", "3000" ]
