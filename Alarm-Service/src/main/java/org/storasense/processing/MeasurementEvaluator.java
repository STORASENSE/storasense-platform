package org.storasense.processing;


import lombok.NonNull;
import org.storasense.models.Alarm;
import org.storasense.models.Measurement;

import java.time.ZonedDateTime;
import java.util.UUID;


public class MeasurementEvaluator {

    // sample limits for demonstration purposes!
    private static final double ALLOWED_MIN = -5.0;
    private static final double ALLOWED_MAX = 5.0;

    public Alarm evaluate(@NonNull UUID sensorId, @NonNull Measurement measurement) {
        double value = measurement.value()[0];
        String message;
        if (value < ALLOWED_MIN) {
            message = "Measured value %f is below the allowed minimum of %f".formatted(value, ALLOWED_MIN);
        } else if (value > ALLOWED_MAX) {
            message = "Measured value %f is above the allowed maximum of %f".formatted(value, ALLOWED_MAX);
        } else {
            return null;
        }
        return new Alarm(
                UUID.randomUUID(),
                sensorId,
                message,
                ZonedDateTime.now()
        );
    }

}
