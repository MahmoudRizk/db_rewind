#!/bin/bash

export DB_REWINDER_POSTGRES_VERSION="$1"; 
docker-compose -f ./build_tests/docker-compose.yml up --exit-code-from db-rewind-container;
exit $?