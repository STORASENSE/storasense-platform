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
