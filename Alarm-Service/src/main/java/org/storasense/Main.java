package org.storasense;


import lombok.extern.log4j.Log4j2;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.storasense.models.Alarm;
import org.storasense.models.Measurement;
import org.storasense.processing.MeasurementEvaluator;
import org.storasense.processing.MeasurementTimestampExtractor;
import org.storasense.serialization.JsonSerializationFactory;

import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;


@Log4j2
public class Main {

    public static void main(String[] args) {
        log.info("Starting alarm service!");

        // get environment variables
        log.info("Extracting all necessary environment variables...");
        final String appId = System.getenv("APPLICATION_ID");
        final String bootstrapServers = System.getenv("BOOTSTRAP_SERVERS");
        final String inputTopic = System.getenv("INPUT_TOPIC");
        final String outputTopic = System.getenv("OUTPUT_TOPIC");

        if (appId == null || bootstrapServers == null || inputTopic == null || outputTopic == null) {
            log.fatal("Shutting down application because some environment variables were missing.");
            System.exit(1);
        } else {
            log.info("All environment variables were extracted successfully!");
        }

        // configure Kafka properties
        final Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, appId);
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        // builder for the streams
        final StreamsBuilder builder = new StreamsBuilder();

        // Serdes for serialization
        log.info("Building Serdes for JSON Serialization...");
        final var serdeFactory = new JsonSerializationFactory();
        final var measurementSerde = serdeFactory.buildSerde(Measurement.class);
        final var alarmSerde = serdeFactory.buildSerde(Alarm.class);
        log.info("Serdes built successfully!");


        // stream for reading recorded measurements
        final KStream<String, Measurement> measurementStream = builder.stream(
                inputTopic,
                Consumed.with(Serdes.String(), measurementSerde)
                        .withTimestampExtractor(new MeasurementTimestampExtractor())
        );

        // log collected measurements
        measurementStream.peek((key, value) -> {
            log.debug("Reading measurement at '{}': {}", key, value);
        });

        // map all critical measurements to alarms
        final var evaluator = new MeasurementEvaluator();
        final KStream<String, Alarm> alarmStream =
                measurementStream
                .mapValues((key, value) -> {
                    var sensorId = extractSensorIdFromKey(key);
                    return evaluator.evaluate(sensorId, value);
                })
                .filter((key, value) -> value != null);

        // log generated alarms
        alarmStream.peek((key, value) -> {
            log.debug("Generating alarm: {}", value);
        });

        // stream all alarms to the alarm topic
        alarmStream.to(
                outputTopic,
                Produced.with(Serdes.String(), alarmSerde)
        );

        log.info("Building the Kafka Streams application with the configured properties...");
        final KafkaStreams streams = new KafkaStreams(builder.build(), props);
        final CountDownLatch latch = new CountDownLatch(1);

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            streams.close();
            latch.countDown();
        }));

        // execute app and wait for streams to close
        try {
            log.info("Initiated Kafka Streams application startup.");
            streams.start();
            latch.await();
        } catch (Throwable e) {
            log.error("An unexpected error occurred during Kafka Streams execution", e);
            throw new RuntimeException("An exception occurred during execution", e);
        }
    }

    private static UUID extractSensorIdFromKey(String key) {
        // key is always structured as "dhbw/ai/si2023/4/{SensorType}/{SensorId}"
        var splitString = key.split("/");
        var sensorId = splitString[splitString.length - 1];
        return UUID.fromString(sensorId);
    }

}
