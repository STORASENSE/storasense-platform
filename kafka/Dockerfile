FROM maven:3.9.6-eclipse-temurin-17 AS build

WORKDIR /src

# Get the MQTT Connector-Plugin and build it using Maven
COPY ./kafka/kafka-connect-mqtt /src
RUN mvn -q -DskipTests clean install

# Use the Confluent Kafka Connect image as the base image
FROM confluentinc/cp-kafka-connect:7.4.10

ENV CONNECT_PLUGIN_PATH=/usr/share/confluent-hub-components,/usr/share/java
# Copies the MQTT Connector-Plugin (built within build-stage) into the final Kafka Connect image
COPY --from=build /src/target/kafka-connect-mqtt-1.1.0-package/kafka-connect-mqtt /usr/share/java/kafka-connect-mqtt

#Non-root user is used by default in the Confluent Kafka Connect image
#
