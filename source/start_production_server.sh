#!/usr/bin/env bash
set -e


docker build -t test/log .
docker run -p3031:3031 test/log
