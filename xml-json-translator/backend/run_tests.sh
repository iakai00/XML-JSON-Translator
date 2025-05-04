#!/bin/bash

# Run tests inside Docker
docker-compose run --rm backend pytest "$@"

# Exit with the same status as the test command
exit $?