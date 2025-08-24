#!/usr/bin/env bash
set -euo pipefail

HOST=${1:-kafka}
PORT=${2:-9092}
RETRIES=${3:-60}

echo "Waiting for Kafka at ${HOST}:${PORT} ..."
for i in $(seq 1 "${RETRIES}"); do
if bash -c "</dev/tcp/${HOST}/${PORT}" >/dev/null 2>&1; then
echo "Kafka is reachable"
exit 0
fi
echo "Retry ${i}/${RETRIES}..."
sleep 2
done

echo "Kafka not reachable after ${RETRIES} attempts" >&2
exit 1
