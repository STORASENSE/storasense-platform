package org.storasense.models;


public record Measurement(
        long timestamp,
        double[] value,
        long sequence,
        Meta meta
) {

    public record Meta(long startup, MeasurementUnit unit) {}

}
