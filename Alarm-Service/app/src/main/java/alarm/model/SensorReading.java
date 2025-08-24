package main.java.alarm.model;

public class SensorReading {

    public String sensorId;
    public long ts; // epoch millis (Eventtime)
    public double value;

    public SensorReading() {}

    public SensorReading(String sensorId, long ts, double value) {
    this.sensorId = sensorId;
    this.ts = ts;
    this.value = value;
    }


}
