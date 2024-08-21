FROM python:3.10-slim

WORKDIR /app

# Copy your code and workspace to /opt/dagster/app
COPY . /app

# Install packages
RUN pip install -e ".[dev]"

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
