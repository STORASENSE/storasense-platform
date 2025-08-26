package org.storasense.models;


import java.util.UUID;


public record Alarm(
        UUID id,
        UUID sensor_id,
        AlarmSeverity severity,
        String message,
        String created_at
) {}
