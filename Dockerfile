# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Expose Streamlit & jupyter default port
EXPOSE 8501 8888

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# set the PYTHONPATH required for using the repository
ENV PYTHONPATH "${PYTHONPATH}:$pwd"

# Set the entrypoint to streamlit
ENTRYPOINT ["streamlit", "run"]

# Command for the entrypoint
CMD ["src/app.py"]