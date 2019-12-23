#!/bin/bash
set -e
cd $(dirname ${BASH_SOURCE[0]})/../..

for whl in ${1:-dist}/*-cp3*.whl; do
  ver=$(expr ${whl##*/} : '.*-cp3\(.\)-.*')
  docker run --rm -v $(pwd)/${whl%/*}:/dist:ro --entrypoint bash python:3.${ver}-slim -c \
    "pip install --no-index /dist/${whl##*/} && \
     python -c 'from s2geometry import S2CellId, S2LatLng; \
                print(S2CellId(S2LatLng.FromDegrees(110, 66)).ToToken());'"
done
