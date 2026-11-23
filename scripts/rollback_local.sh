#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "Starting rollback to v1"

docker image inspect elpriset:v1 > /dev/null

docker rm -f elpriset-version 2>/dev/null || true

docker run -d \
  --name elpriset-version \
  -p 127.0.0.1:8000:8000 \
  elpriset:v1

curl --fail --silent --show-error \
  --retry 10 --retry-all-errors --retry-delay 1 \
  --retry-max-time 30 --max-time 5 \
  http://127.0.0.1:8000/health

python3 scripts/verify_version.py \
  82c37061c50e4d3e41876feb66d138bfbb845022

docker inspect --format '{{.Config.Image}}' elpriset-version

echo "Rollback completed"
