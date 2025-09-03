package org.storasense.models;

import lombok.Data;

@Data
public class SensorConfig {
    private String sensorId;
    private Double allowedMin;
    private Double allowedMax;
    private String email;
}
