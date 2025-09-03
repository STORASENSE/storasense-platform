#!/usr/bin/env bash
set -euo pipefail

BOOTSTRAP="${BOOTSTRAP:-kafka:9092}"

create_topic() {
  local topic="$1"
  local partitions="$2"
  local rf="$3"
  echo "Ensuring topic '${topic}' (partitions=${partitions}, rf=${rf})"
  /opt/bitnami/kafka/bin/kafka-topics.sh \
    --bootstrap-server "${BOOTSTRAP}" \
    --create --if-not-exists \
    --topic "${topic}" \
    --partitions "${partitions}" \
    --replication-factor "${rf}"
}

create_topic "iot-sensordata" "${IOT_PARTITIONS:-5}" 1
create_topic "alarms" "${ALARM_PARTITIONS:-1}" 1
create_topic "sensor_values" 5 1
create_topic "alarms-notify" 3 1

echo "All topics ensured."