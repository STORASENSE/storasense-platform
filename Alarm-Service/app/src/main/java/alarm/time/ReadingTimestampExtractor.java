package main.java.alarm.time;
import main.java.alarm.model.SensorReading;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.streams.processor.TimestampExtractor;

public class ReadingTimestampExtractor implements TimestampExtractor {
	@Override
	public long extract(ConsumerRecord<Object, Object> record, long partitionTime) {
		if (record.value() instanceof SensorReading r) {
			// Eventtime from payload
			return r.ts;
		}
		return record.timestamp(); // Fallback
	}
}
