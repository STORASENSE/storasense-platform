#!/bin/bash
set -euo pipefail

CONNECT_URL="${1:-http://kafka-connect:8083}"
CONF_FILE="${2:?Usage: $0 <CONNECT_URL> <CONF_FILE>}"

curl -X POST \
  -H 'Content-Type: application/json' \
  --data @"${CONF_FILE}" \
  "${CONNECT_URL}/connectors"
