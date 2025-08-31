package org.storasense.processing;


import lombok.NonNull;
import org.storasense.models.Alarm;
import org.storasense.models.Measurement;

import java.time.ZonedDateTime;
import java.util.UUID;


public class MeasurementEvaluator {

    public Alarm evaluate(@NonNull UUID sensorId, @NonNull Measurement measurement, double allowedMin, double allowedMax) {
        double value = measurement.value()[0];
        String message;
        if (value < allowedMin) {
            message = "Measured value %f is below the allowed minimum of %f".formatted(value, allowedMin);
        } else if (value > allowedMax) {
            message = "Measured value %f is above the allowed maximum of %f".formatted(value, allowedMax);
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
