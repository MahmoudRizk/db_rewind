#!/bin/bash

# set -e

# Install pip requirements
pip install -r /opt/db_rewind/requirements.txt

# Copy env file
cp /opt/db_rewind/build_tests/src/db_rewind.env /opt/db_rewind/.env

# Replace string place holder with postgres version defined in env
sed -i "s/{DB_REWINDER_POSTGRES_VERSION}/$DB_REWINDER_POSTGRES_VERSION/" /opt/db_rewind/.env 

# Start the PostgreSQL service
service postgresql start

# Create database
su - postgres -c "psql -f /opt/db_rewind/build_tests/src/setup_database.sql"

# Setup Database configuration for database rewinding
python3 /opt/db_rewind/build_tests/src/db_rewind_test.py
