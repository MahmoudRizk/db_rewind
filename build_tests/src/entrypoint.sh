#!/bin/bash

set -e

# Clone db_rewind repo
git clone https://github.com/MahmoudRizk/db_rewind /opt/db_rewind

# Pull latest from remote repo
git -C /opt/db_rewind pull

# Install pip requirements
pip install -r /opt/db_rewind/requirements.txt

# Copy env file
cp /opt/db_rewind.env /opt/db_rewind/.env

# Start the PostgreSQL service
service postgresql start

# Create database & test data
su - postgres -c "psql -f /opt/setup_database.sql"

# Setup Database configuration for database rewinding
python3 /opt/db_rewind_test.py
