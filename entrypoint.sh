#!/bin/sh

# Define a flag file path
FLAG_FILE="/app/initialized_database"

sleep 60
if [ ! -f "$FLAG_FILE" ]; then
    # Initialize the database (your custom command)
    poetry run python manage.py initialize_database

    # Create the flag file to indicate initialization is complete
    touch "$FLAG_FILE"

    # Stop and remove the container
    echo "Initialization complete. Stopping and removing container..."
    docker stop database_init
    docker rm database_init

    # Exit the script
    exit 0
fi
