This folder contains the Kafka-related resources for the project.

### It includes the following components:
- **connectors**: A folder containing the Kafka Connect resources, defined in JSON format.
- **kafka-connect-mqtt**: A Kafka Connect source- and sink- connector plugin for MQTT.
- **scripts**: Helper scripts to set up the MQTT connectors and Kafka topics (running within the Init container).
- **Dockerfile**: A Dockerfile to build the Kafka Connect instance (from the `confluentic/cp-kafka-connect` image), containing the MQTT-Connector plugin (from the `kafka-connect-mqtt` repository).

### Define connector resources within the `connectors` folder - see formats [here](connectors/README.md).
