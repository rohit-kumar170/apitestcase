#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Load environment variables from the .env file
if [ -f /app/.env ]; then
  export $(cat /app/.env | xargs)
fi

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h db -p 5432 -U ${SECRET_USER}; do
  sleep 1
done
echo "PostgreSQL is ready."

python3 manage.py makemigrations
# Run database migrations
python3 manage.py custom_migrate

# Collect static files
python3 manage.py collectstatic --noinput

# Start the Django server
python3 manage.py runserver 0.0.0.0:8000
