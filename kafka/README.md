This folder contains the Kafka-related resources for the project.

### It includes the following components:
- **connectors**: A folder containing the Kafka Connect resources, defined in JSON format.
- **kafka-connect-email-workshop**: A folder containing the setup for a Kafka Connect Plugin (sink) - used to send emails from Kafka topics. !!NOT SUPPORTED YET!!.
- **scripts**: Helper scripts to set up the MQTT connectors and Kafka topics (running within the Init container).
- **Dockerfile**: A Dockerfile to build the Kafka Connect instance (from the `confluentic/cp-kafka-connect` image), containing the MQTT-Connector plugin (from the `kafka-connect-mqtt` repository) and the Email-Connector plugin.

### Define connector resources within the `connectors` folder - see formats [here](connectors/README.md).
