#!/bin/bash
set -e

# Wait for Prefect server to be available
until curl -s $PREFECT_API_URL/health > /dev/null; do
  echo "Waiting for Prefect server at $PREFECT_API_URL..."
  sleep 2
done

# Create work pool if it doesn't exist
if ! prefect work-pool inspect general-work-pool --type docker > /dev/null 2>&1; then
  echo "Creating work pool 'general-work-pool'..."
  prefect work-pool create --type docker general-work-pool
else
  echo "Work pool 'general-work-pool' already exists."
fi

# Start a worker for the pool
echo "Starting Prefect worker for 'general-work-pool'..."
prefect worker start --pool general-work-pool --name one_for_all --type "docker"