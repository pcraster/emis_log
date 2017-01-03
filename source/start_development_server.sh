#!/usr/bin/env bash
set -e
docker build -t test/log .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/log:/log test/log
