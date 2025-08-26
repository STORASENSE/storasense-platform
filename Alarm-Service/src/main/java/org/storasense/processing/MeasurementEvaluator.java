package org.storasense.processing;


import lombok.NonNull;
import org.storasense.models.Alarm;
import org.storasense.models.AlarmSeverity;
import org.storasense.models.Measurement;

import java.util.UUID;


public class MeasurementEvaluator {

    private static final double ALLOWED_MIN = -5.0;
    private static final double ALLOWED_MAX = 5.0;

    public Alarm evaluate(@NonNull UUID sensorId, @NonNull Measurement measurement) {
        double value = measurement.value()[0];
        Alarm alarm = null;
        if (value < ALLOWED_MIN) {
            var message = "Measured value %f is below the allowed minimum of %f".formatted(value, ALLOWED_MIN);
            alarm = new Alarm(sensorId, AlarmSeverity.MEDIUM, message, measurement.timestamp());
        } else if (value > ALLOWED_MAX) {
            var message = "Measured value %f is above the allowed maximum of %f".formatted(value, ALLOWED_MAX);
            alarm = new Alarm(sensorId, AlarmSeverity.MEDIUM, message, measurement.timestamp());
        }
        return alarm;
    }

}
