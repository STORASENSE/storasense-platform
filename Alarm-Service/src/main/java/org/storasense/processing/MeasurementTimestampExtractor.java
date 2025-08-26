package org.storasense.processing;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.streams.processor.TimestampExtractor;
import org.storasense.models.Measurement;


public class MeasurementTimestampExtractor implements TimestampExtractor {

    @Override
    public long extract(ConsumerRecord<Object, Object> record, long partitionTime) {
        if (record.value() instanceof Measurement measurement) {
            return measurement.timestamp();
        }
        return record.timestamp();
    }

}
