#!/bin/bash

# Script variables
APP_CONTAINER_NAME="videos-app"
APP_CONTAINER_PORT="5000"
MAX_ATTEMPTS=10
INTERVAL_SEC=3

# cp .env.example .env
# docker-compose -f docker-compose.e2e_tests.yml up -d
# APP_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $APP_CONTAINER_NAME)


# health_check_command() {
#   curl -s -o /dev/null -w "%{http_code}" "$APP_IP:$APP_CONTAINER_PORT/healthcheck"
# }

# # HEALTHCHECK
# echo "Waiting for App to start..."

# while [ "$(health_check_command)" -ne 200 ] && [ $MAX_ATTEMPTS -gt 0 ]; do   
#   sleep $INTERVAL_SEC
#   ((MAX_ATTEMPTS -= 1))
#   echo "$MAX_ATTEMPTS attempts left"
# done

# # Final check
# if [ "$(health_check_command)" -ne 200 ]; then
#   echo "App has not started after $(( MAX_ATTEMPTS * INTERVAL_SEC )) seconds. Exiting..."
#   exit 1
# fi

# echo "App started successfully!"

# echo "Performing E2E Tests..."

# status_code=$(curl -s -o /dev/null -w "%{http_code}" $APP_IP:$APP_CONTAINER_PORT/healthcheck)
# echo $status_code

# docker-compose -f docker-compose.e2e_tests.yml down

# if [ "$status_code" -eq 200 ]; then
#   echo "E2E Tests Passed Successfully!"
#   exit 0
# else
#   echo "E2E Tests FAILED"
#   exit 1
# fi


exit 0