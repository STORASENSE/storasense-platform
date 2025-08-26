package org.storasense.models;


import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import org.storasense.serialization.ZonedDateTimeSerializer;

import java.time.ZonedDateTime;
import java.util.UUID;


public record Alarm(
        UUID id,
        @JsonProperty("sensor_id")
        UUID sensorId,
        AlarmSeverity severity,
        String message,
        @JsonProperty("created_at")
        @JsonSerialize(using=ZonedDateTimeSerializer.class)
        ZonedDateTime createdAt
) {}
