#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python src/manage.py migrate

# Insert test data in database
echo "Insert test data in database"
python src/manage.py loaddata --format=json fill_test_data.json

# Start server
echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000