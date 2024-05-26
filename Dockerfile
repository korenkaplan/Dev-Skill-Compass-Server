FROM python:3.12-slim-bullseye
LABEL authors="Koren Kaplan"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential cron postgresql-client

# Install Poetry
RUN pip install poetry

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Copy the current directory contents into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies (including Django)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Expose port 8000 for Django
EXPOSE 8000

# Command to run migrations and start both cron and Django server
#CMD  [ "sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py crontab add && cron && poetry run python manage.py runserver 0.0.0.0:8000 && python manage.py initialize_database"]



