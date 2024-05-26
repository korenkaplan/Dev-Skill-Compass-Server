#!/bin/sh

# Define a flag file path
FLAG_FILE="/app/initialized_database"

# Function to check if the services are ready
check_services_ready() {
    echo "Running service check..."
    OUTPUT=$(poetry run python manage.py check 2>&1)
    echo "Check command output:"
    echo "$OUTPUT"
    if echo "$OUTPUT" | grep -q "System check identified no issues (0 silenced)."; then
        echo "Services are ready."
        return 0
    else
        echo "Waiting for services to be ready..."
        return 1
    fi
}

slepp 15
# Wait for services to be ready
until check_services_ready; do
    sleep 5
done

# Check if the flag file exists
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
