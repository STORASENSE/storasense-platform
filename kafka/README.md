This folder contains the Kafka-related resources for the project.

### It includes the following components:
- **connectors**: A folder containing the Kafka Connect resources, defined in JSON format.
- **kafka-connect-mqtt**: A Kafka Connect source- and sink- connector plugin for MQTT.
- **scripts**: Helper scripts to set up the MQTT connectors and Kafka topics (running within the Init container).
- **Dockerfile**: A Dockerfile to build the Kafka Connect instance (from the `confluentic/cp-kafka-connect` image), containing the MQTT-Connector plugin (from the `kafka-connect-mqtt` repository).

### Define connector resources in the `connectors` folder in these formats:

**Source connector (MQTT Topic -> Kafka Topic)**:
```json
{
"name": "mqtt-source-s<number>",
"config": {
  "connector.class": "be.jovacon.kafka.connect.MQTTSourceConnector",
  "mqtt.broker": "tcp://<broker-adress>:<port>",
  "mqtt.clientID":"storasense-kafka-connect-mqtt-source-s<number>",
  "mqtt.username": "<username>",
  "mqtt.password": "<password>",
  "mqtt.topic": "<mqtt-topic>",
  "kafka.topic": "<kafka-topic>",
  "key.converter": "org.apache.kafka.connect.storage.StringConverter",
  "key.converter.schemas.enable": "false",
  "value.converter": "org.apache.kafka.connect.json.JsonConverter",
  "value.converter.schemas.enable": "false"
  }
}
```
