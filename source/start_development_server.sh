#!/usr/bin/env bash
set -e


docker build -t test/emis_log .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis_log:/emis_log \
    test/emis_log
