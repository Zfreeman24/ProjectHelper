#!/bin/bash

# Start the authentication service in the background
python ./services/authentication_service.py &

# Start the project generation service in the background
python ./services/project_generation_service.py &

# Wait for any process to exit
wait -n

# Exit with the status of the process that exited first
exit $?
