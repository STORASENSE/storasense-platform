package org.storasense.models;


import java.util.UUID;


public record Alarm(
        UUID sensorId,
        AlarmSeverity severity,
        String message,
        long timestamp
) {}
