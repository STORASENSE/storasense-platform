package org.storasense;

import lombok.extern.log4j.Log4j2;
import org.apache.kafka.streams.kstream.KTable;
import org.apache.kafka.streams.kstream.Repartitioned;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.connect.json.JsonConverter;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.errors.StreamsUncaughtExceptionHandler;
import org.apache.kafka.streams.kstream.Consumed;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.Produced;
import org.storasense.models.Measurement;
import org.storasense.models.SensorConfig;
import org.storasense.processing.MeasurementEvaluator;
import org.storasense.processing.MeasurementTimestampExtractor;
import org.storasense.serialization.AlarmSchema;
import org.storasense.serialization.JsonSerializationFactory;

import java.util.Map;
import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;


@Log4j2
public class Main {
    public record MeasurementWithSensorId(UUID sensorId, Measurement measurement) {}
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
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // builder for the streams
        final StreamsBuilder builder = new StreamsBuilder();

        // build JSON schema for alarms
        final var jsonConverter = new JsonConverter();
        jsonConverter.configure(Map.of("schemas.enable", "true"), false);
        final var alarmSchema = AlarmSchema.buildSchema();

        // Serdes for serialization
        log.info("Building Serdes for JSON Serialization...");
        final var serdeFactory = new JsonSerializationFactory();
        final var measurementSerde = serdeFactory.buildSerde(Measurement.class);
        final var sensorConfigSerde = serdeFactory.buildSerde(SensorConfig.class);
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

        KTable<String, SensorConfig> sensorConfigTable = builder.table(
        "sensor_values",
                Consumed.with(Serdes.String(), sensorConfigSerde)
        );

        sensorConfigTable.toStream()
            .peek((k, v) -> log.debug("CONF: k='{}' v={}", k, v));

         // Rekey, Repartition on sensorId (extracted from the original topic-key)
        final KStream<String, Measurement> rekeyed = measurementStream
                .selectKey((key, value) -> extractSensorIdFromKey(key).toString())
                .repartition(Repartitioned.with(Serdes.String(), measurementSerde).withNumberOfPartitions(5).withName("rekeyed-iot-sensordata"))
                .peek((k, v) -> log.info("MEAS REKEYED (post-repartition): k='{}' v={}", k, v));


        final var evaluator = new MeasurementEvaluator();

        final KStream<String, byte[]> alarmStream = rekeyed
                    .leftJoin(
                        sensorConfigTable,
                        (readOnlyKey, measurement, cfg) -> {
                            final boolean ok = cfg != null && cfg.getAllowedMin() != null && cfg.getAllowedMax() != null;
                            log.info("JOIN: k='{}' hasCfg={} min={} max={}", readOnlyKey, ok,
                                    ok ? cfg.getAllowedMin() : null, ok ? cfg.getAllowedMax() : null);
                            if (!ok) return null;
                            try {
                            UUID sensorId = UUID.fromString(readOnlyKey);
                            return evaluator.evaluate(
                                    UUID.fromString(readOnlyKey),
                                    measurement,
                                    cfg.getAllowedMin(),
                                    cfg.getAllowedMax()
                            );
                            } catch (IllegalArgumentException ex) {
                                log.error("JOIN: key is not a valid UUID: '{}'", readOnlyKey);
                                return null;
                            }

                        }
                )
                .filter((k, alarm) -> alarm != null)
                .peek((k, alarm) -> log.info("ALARM OBJ: k='{}' v={}", k, alarm))
                .mapValues((k, alarm) -> {
                    var struct = AlarmSchema.buildStruct(alarm);
                    return jsonConverter.fromConnectData(outputTopic, alarmSchema, struct);
                });

        // stream all alarms to the alarm topic
        alarmStream.to(
                outputTopic,
                Produced.with(Serdes.String(), Serdes.ByteArray())
        );

        log.info("Building the Kafka Streams application with the configured properties...");
        final KafkaStreams streams = new KafkaStreams(builder.build(), props);
        final CountDownLatch latch = new CountDownLatch(1);

        streams.setStateListener((newState, oldState) -> {
            log.debug("Kafka Streams app transitioned from '{}' to '{}'", oldState, newState);
        });
        streams.setUncaughtExceptionHandler(e -> {
            log.fatal("An unexpected exception was thrown in Kafka Streams app.", e);
            return StreamsUncaughtExceptionHandler.StreamThreadExceptionResponse.REPLACE_THREAD;
        });

        // attach shutdown handler to catch control-c
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            streams.close();
            latch.countDown();
        }));

        // execute app and wait for streams to close
        try {
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
