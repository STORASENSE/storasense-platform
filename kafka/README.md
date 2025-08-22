This folder contains the Kafka-related code for the project - included via our Docker-Compose setup.

It includes the following components:
- **kafka-connect-mqtt**: A Kafka Connect source- and sink- connector for MQTT.
- **scripts**: Scripts to run the Kafka Connect MQTT connector.
- **Dockerfile**: A Dockerfile to build the Kafka Connect instance (from the `confluentic/cp-kafka-connect` image) and the MQTT connectors (from the `kafka-connect-mqtt` repository).
