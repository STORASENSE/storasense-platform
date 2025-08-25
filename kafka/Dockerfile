FROM maven:3.9.6-eclipse-temurin-17 AS build

WORKDIR /src

# Get the MQTT Connector-Plugin and build it using Maven
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/johanvandevenne/kafka-connect-mqtt /src
RUN mvn -q -DskipTests clean install

# Use the Confluent Kafka Connect image as the base image
FROM confluentinc/cp-kafka-connect:7.4.10

ENV CONNECT_PLUGIN_PATH=/usr/share/confluent-hub-components,/usr/share/java

# Copies the MQTT Connector-Plugin (built within build-stage) into the final Kafka Connect image
COPY --from=build /src/target/kafka-connect-mqtt-1.1.0-package/kafka-connect-mqtt /usr/share/java/kafka-connect-mqtt

# Installs the PostgreSQL JDBC driver
USER root
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.7.5
RUN mkdir -p /usr/share/java/postgresql && curl -fsSL -o /usr/share/java/postgresql/postgresql-jdbc.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar && chown -R appuser:appuser /usr/share/java/postgresql

USER appuser
