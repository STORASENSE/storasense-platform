#!/usr/bin/env bash
set -euo pipefail
URL="${1:-http://kafka-connect:8083/connector-plugins}"
RETRIES="${2:-60}"
SLEEP="${3:-2}"
for i in $(seq 1 "$RETRIES"); do
code=$(curl -s -o /dev/null -w '%{http_code}' "$URL" || true)
if [ "$code" = "200" ]; then
echo "Kafka Connect REST ready"
exit 0
fi
echo "Waiting for Kafka Connect REST ($i/$RETRIES)…"
sleep "$SLEEP"
done
echo "ERROR: Kafka Connect REST not ready" >&2
exit 1
