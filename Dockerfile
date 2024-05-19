FROM python:3.12-slim-bullseye
LABEL authors="Koren Kaplan"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential

# Install Poetry
RUN pip install poetry

# Copy the current directory contents into the container at /app
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies (including Django)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Install dotenv
RUN poetry add python-dotenv

# Expose port 8000 for Django
EXPOSE 8000

# Run the development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
