FROM python:3.12-slim-bullseye
LABEL authors="Koren Kaplan"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential cron postgresql-client wget unzip ca-certificates \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && update-ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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

# django-crontab logfile
RUN mkdir /cron
RUN touch /cron/django_cron_log

# Expose port 8000 for Django
EXPOSE 8000

CMD service cron start && python manage.py runserver 0.0.0.0:8000
