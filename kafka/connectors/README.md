**Source connector (MQTT Source -> Kafka Topic)** => *mqtt-source-s\<number>.json*:
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
  "kafka.topic": "iot-sensordata",
  "key.converter": "org.apache.kafka.connect.storage.StringConverter",
  "key.converter.schemas.enable": "false",
  "value.converter": "org.apache.kafka.connect.json.JsonConverter",
  "value.converter.schemas.enable": "false"
  }
}
```

**Sink connector (Kafka Topic -> MQTT Sink)** => *mqtt-sink.json*:
```json
{
  "name": "mqtt-sink",
  "config": {
    "connector.class":"be.jovacon.kafka.connect.MQTTSinkConnector",
    "mqtt.topic":"<mqtt-topic>",
    "topics":"alarms",
    "mqtt.clientID":"storasense-kafka-connect-mqtt-sink",
    "mqtt.username":"<username>",
    "mqtt.password":"<password>",
    "mqtt.broker":"<broker-adress>:<port>",
    "key.converter":"org.apache.kafka.connect.storage.StringConverter",
    "key.converter.schemas.enable":"false",
    "value.converter":"org.apache.kafka.connect.storage.StringConverter",
    "value.converter.schemas.enable":"false"
  }
}
```

**Sink connector (Kafka Topic -> Postgres Sink)** => *alarms-postgres-sink.json*:
```json
{
"name": "alarms-postgres-sink",
"config": {
  "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
  "tasks.max": "1",
  "topics": "alarms",
  "connection.url": "jdbc:postgresql://<hostname>:<port>/<db>",
  "connection.user": "<user>",
  "connection.password": "<password>",
  "auto.create": "false",
  "auto.evolve": "false",
  "table.name.format": "Alarm",
  "insert.mode": "upsert",
  "pk.mode": "record_value",
  "pk.fields": "id",
  "key.converter": "org.apache.kafka.connect.storage.StringConverter",
  "value.converter": "org.apache.kafka.connect.json.JsonConverter",
  "value.converter.schemas.enable": "false",
  "batch.size": "300",
  "max.retries": "10",
  "retry.backoff.ms": "3000"
  }
}
```
