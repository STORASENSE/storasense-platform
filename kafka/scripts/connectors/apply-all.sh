#!/usr/bin/env bash
set -euo pipefail
CONNECT_URL="${1:-http://kafka-connect:8083}"
CONF_DIR="${2:-/opt/connectors}"
shopt -s nullglob
for f in "$CONF_DIR"/*.json; do
echo "Processing $f"
/opt/scripts/loadConnector.sh "$CONNECT_URL" "$f"
done
echo "All connectors applied."
