package main.java.alarm.transform;

import main.java.alarm.model.AlarmEvent;
import main.java.alarm.model.SensorReading;
import main.java.alarm.model.Threshold;
import org.apache.kafka.streams.kstream.ValueTransformerWithKey;
import org.apache.kafka.streams.processor.ProcessorContext;
import org.apache.kafka.streams.state.KeyValueStore;

import java.util.Map;

public class AlarmEvaluator implements ValueTransformerWithKey<String, SensorReading, AlarmEvent> {
    public static class SensorState {
    public Long lastOutsideStartTs; // null if in range
    public boolean alarmActive;
}

private final String storeName;
private final Map<String, Threshold> thresholds;
private final double defaultMin;
private final double defaultMax;
private final long windowMs;

private KeyValueStore<String, SensorState> store;

public AlarmEvaluator(String storeName,
                      Map<String, Threshold> thresholds,
                      double defaultMin,
                      double defaultMax,
                      long windowMs) {
    this.storeName = storeName;
    this.thresholds = thresholds;
    this.defaultMin = defaultMin;
    this.defaultMax = defaultMax;
    this.windowMs = windowMs;
}

@Override
@SuppressWarnings("unchecked")
public void init(ProcessorContext context) {
    this.store = (KeyValueStore<String, SensorState>) context.getStateStore(storeName);
}

@Override
public AlarmEvent transform(String sensorId, SensorReading reading) {
    if (sensorId == null || reading == null) return null;

    Threshold t = thresholds.get(sensorId);
    double min = t != null ? t.min : defaultMin;
    double max = t != null ? t.max : defaultMax;

    boolean out = reading.value < min || reading.value > max;

    SensorState s = store.get(sensorId);
    if (s == null) {
        s = new SensorState();
        s.lastOutsideStartTs = null;
        s.alarmActive = false;
    }

    if (out) {
        if (s.lastOutsideStartTs == null) {
            s.lastOutsideStartTs = reading.ts;
            store.put(sensorId, s);
            return null;
        } else {
            long duration = reading.ts - s.lastOutsideStartTs;
            if (!s.alarmActive && duration >= windowMs) {
                s.alarmActive = true;
                store.put(sensorId, s);
                return AlarmEvent.raised(sensorId, s.lastOutsideStartTs, reading.ts, reading.value, min, max, duration);
            } else {
                store.put(sensorId, s);
                return null;
            }
        }
    } else {
        AlarmEvent cleared = null;
        if (s.alarmActive && s.lastOutsideStartTs != null) {
            long duration = reading.ts - s.lastOutsideStartTs;
            cleared = AlarmEvent.cleared(sensorId, s.lastOutsideStartTs, reading.ts, reading.value, min, max, duration);
        }
        s.lastOutsideStartTs = null;
        s.alarmActive = false;
        store.put(sensorId, s);
        return cleared;
    }
}

@Override
public void close() {}

}
