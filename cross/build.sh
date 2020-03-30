#!/bin/bash
set -e
cd $(dirname ${BASH_SOURCE[0]})/..

DOCKER_FILE_DIR="cross/docker/manylinux2014_s2geometry"
DOCKER_TAG="manylinux2014_s2geometry"
SOURCE_DIR="/s2geometry"

docker build ${DOCKER_FILE_DIR} -t ${DOCKER_TAG}
docker run --rm \
  -v $(pwd):${SOURCE_DIR}\
  --entrypoint bash \
  ${DOCKER_TAG} \
  -c "cd ${SOURCE_DIR}; cross/bdist_wheel_helper.sh"
