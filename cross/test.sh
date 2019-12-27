#!/bin/bash
set -e
cd $(dirname ${BASH_SOURCE[0]})/..

for whl in ${1:-dist}/*-cp3*.whl; do
  ver=$(expr ${whl##*/} : '.*-cp3\(.\)-.*')
  docker run --rm \
    -v $(pwd)/${whl%/*}:/dist:ro \
    -v $(pwd)/src/python/pywraps2_test.py:/test.py:ro \
    --entrypoint bash python:3.${ver}-slim -c "\
      pip install --no-index /dist/${whl##*/} && \
      python <(sed 's/pywraps2/s2geometry/g' test.py)"
done
