# Alarm-Feature mit Apache Kafka

Kafka (Broker, KRaft-Modus)
* Zentrale Event-/Daten-Drehscheibe für Streams.
* Speichert Nachrichten in Topics (z.B. iot-sensordata, alarme).
* Ermöglicht horizontale Skalierung über Partitionen.
* Garantiert Reihenfolge pro Partition und Consumer-Group-Offsets.

Kafka Connect (Laufzeit für Connectoren)
* Standardisierte Integrations-Laufzeit, um externe Systeme anzubinden.
* Führt den MQTT Source Connector aus (und optional einen MQTT Sink).
* Verwaltet Connector-Tasks, Status, Offsets und Wiederanläufe.
* Deklarative Konfiguration (per JSON/REST)

MQTT Source Connector (innerhalb von Connect)
* Intialisiert und konfiguriert via INIT-Container (one-shot).
* Verbindet sich als MQTT-Client an deinen externen Mosquitto-Broker.
* Abonniert MQTT-Topics (z.B. sensor/+) und schreibt Nachrichten in Kafka (iot-sensordata).
* Setzt idealerweise die Sensor-ID als Kafka-Key (SMTs), damit pro Sensor deterministisch partitioniert wird.
* Ermöglicht saubere Entkopplung zwischen MQTT-Welt und Kafka.

MQTT Sink Connector (innerhalb von Connect)
* Konsumiert aus Kafka (z.B. alarme) und publiziert daraus abgeleitete Befehle/Events zurück in MQTT.
* Ermöglicht einen Rückkanal an Geräte/Aktoren (z.B. devices/${key}/commands).
* Ebenfalls deklarativ konfigurierbar und skalierbar.

Kafka-Init (One‑Shot Init-Container)
* Wartet automatisch, bis Kafka erreichbar ist.
* Legt die benötigten Topics idempotent an (iot-sensordata, alarme) mit gewünschter Partitionierung.
* Beendet sich nach erfolgreicher Initialisierung (keine dauerhafte Last).

Kafka UI (Redpanda Console)
* Web-Oberfläche zur Einsicht in Cluster, Topics, Partitionen, Nachrichten und Consumer-Lags.
* Hilfreich für Debugging, Monitoring und manuelle Checks.
* Über Traefik nach außen erreichbar.

Alarmservice (Kafka Streams)
* Konsumiert iot-sensordata keyed by sensor_id.
* Führt Schwellwertlogik pro individueller Sensor-Messwertaufzeichnung aus.
* Produziert strukturierte Alarme (Json) in das Topic alarme.
* Lässt sich horizontal skalieren entsprechend der Partitionen.
