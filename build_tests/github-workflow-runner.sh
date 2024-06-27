#!/bin/bash

# Simulate a command's output
output=$(sudo docker-compose -f ./build_tests/docker-compose.yml up --exit-code-from db-rewind-container)
echo $output

# Check if "exited with code 0" exists in the output
if echo "$output" | grep -q "exited with code 0"; then
  echo "E2E test done successfully."
  exit 0
else
  # If the string is not found, exit with code 1
  echo "Error: E2E test failed using docker compose."
  exit 1
fi