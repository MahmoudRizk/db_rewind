#!/bin/bash

docker-compose -f ./build_tests/docker-compose.yml up --exit-code-from db-rewind-container
exit $?