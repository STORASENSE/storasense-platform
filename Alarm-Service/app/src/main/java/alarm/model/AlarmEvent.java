package main.java.alarm.model;

public class AlarmEvent {
    public String sensorId;
    public String state; // RAISED | CLEARED
    public long startedAt;
    public long currentTs;
    public double currentValue;
    public double min;
    public double max;
    public long durationMs;

    public AlarmEvent() {}

    public static AlarmEvent raised(String sensorId, long startedAt, long currentTs, double value, double min, double max, long durationMs) {
        AlarmEvent e = new AlarmEvent();
        e.sensorId = sensorId;
        e.state = "RAISED";
        e.startedAt = startedAt;
        e.currentTs = currentTs;
        e.currentValue = value;
        e.min = min;
        e.max = max;
        e.durationMs = durationMs;
        return e;
    }

    public static AlarmEvent cleared(String sensorId, long startedAt, long currentTs, double value, double min, double max, long durationMs) {
        AlarmEvent e = new AlarmEvent();
        e.sensorId = sensorId;
        e.state = "CLEARED";
        e.startedAt = startedAt;
        e.currentTs = currentTs;
        e.currentValue = value;
        e.min = min;
        e.max = max;
        e.durationMs = durationMs;
        return e;
    }


}
