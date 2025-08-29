package org.storasense.serialization;

import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.SchemaBuilder;
import org.apache.kafka.connect.data.Struct;
import org.apache.kafka.connect.data.Timestamp;
import org.storasense.models.Alarm;

import java.util.Date;

public class AlarmSchema {

    public static Schema buildSchema() {
        return SchemaBuilder.struct()
                .field("id", Schema.STRING_SCHEMA)
                .field("sensor_id", Schema.STRING_SCHEMA)
                .field("message",  Schema.STRING_SCHEMA)
                .field("created_at", Timestamp.SCHEMA)
                .build();
    }

    public static Struct buildStruct(Alarm alarm) {
        var schema = buildSchema();
        return new Struct(schema)
                .put("id", alarm.id().toString())
                .put("sensor_id", alarm.sensorId().toString())
                .put("message", alarm.message())
                .put("created_at", Date.from(alarm.createdAt().toInstant()));
    }

}
