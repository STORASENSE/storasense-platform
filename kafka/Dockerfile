# ---------- Stage 1: Build MQTT Connector (Maven) ----------
FROM maven:3.9.6-eclipse-temurin-17 AS mqttbuild

WORKDIR /src/mqtt
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/johanvandevenne/kafka-connect-mqtt . \
 && mvn -q -DskipTests clean install

# ---------- Stage 2: Build Email Connector (SBT) ----------
FROM eclipse-temurin:17-jdk AS emailbuild

# Install SBT
RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://repo.scala-sbt.org/scalasbt/debian/sbt-1.9.9.deb -o /tmp/sbt.deb \
 && apt-get update && apt-get install -y /tmp/sbt.deb \
 && rm -f /tmp/sbt.deb

# Copy Source email-connector-plugin
WORKDIR /src/email
COPY ./kafka/kafka-connect-email-workshop/ .
RUN sbt -no-colors -batch clean assembly

# ---------- Stage 3: Final Kafka Connect Image ----------
FROM confluentinc/cp-kafka-connect:7.4.10

# Plugin-Paths
ENV CONNECT_PLUGIN_PATH=/usr/share/confluent-hub-components,/usr/share/java

# Install MQTT Plugin
COPY --from=mqttbuild /src/mqtt/target/kafka-connect-mqtt-1.1.0-package/kafka-connect-mqtt /usr/share/java/kafka-connect-mqtt

# Install Email Plugin
RUN mkdir -p /usr/share/java/kafka-connect-email
COPY --from=emailbuild /src/email/target/scala-*/kafka-connect-email-assembly-*.jar /usr/share/java/kafka-connect-email/

COPY ./kafka /kafka

USER root
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-jdbc:10.7.5
RUN mkdir -p /usr/share/java/postgresql \
 && curl -fsSL -o /usr/share/java/postgresql/postgresql-jdbc.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar \
 && chown -R appuser:appuser /usr/share/java/postgresql
USER appuser
