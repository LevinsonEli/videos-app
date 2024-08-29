#!/bin/bash

docker build -t videos-app-unit-tests -f Dockerfile.unit_tests .

docker rm -f videos-app-unit-tests > /dev/null

docker run -d --name videos-app-unit-tests videos-app-unit-tests > /dev/null

docker wait videos-app-unit-tests > /dev/null

return_code=$(docker inspect -f '{{.State.ExitCode}}' videos-app-unit-tests)

summary_info=$(docker logs videos-app-unit-tests | sed -n '/short test summary info/,$p')

echo $return_code
echo $summary_info

docker rm -f videos-app-unit-tests > /dev/null
