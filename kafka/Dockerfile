FROM maven:3.9.6-eclipse-temurin-17 AS build

WORKDIR /src

# Get the MQTT Connector-Plugin
COPY ./kafka/kafka-connect-mqtt /src
RUN mvn -q -DskipTests clean package

# Use the Confluent Kafka Connect image
FROM confluentinc/cp-kafka-connect:latest
ENV CONNECT_PLUGIN_PATH=/usr/share/confluent-hub-components,/usr/share/java
# Copies the built MQTT Connector-Plugin into the Kafka Connect image
COPY --from=build /src/target/*-package/share/kafka-connect-mqtt /usr/share/java/kafka-connect-mqtt

# Non-root user is used by default in the Confluent Kafka Connect image
