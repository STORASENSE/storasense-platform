package org.storasense.serialization;

import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.SchemaBuilder;
import org.apache.kafka.connect.data.Struct;
import org.storasense.models.Alarm;

import java.time.format.DateTimeFormatter;

public class AlarmSchema {

    public static Schema buildSchema() {
        return SchemaBuilder.struct()
                .field("id", Schema.STRING_SCHEMA)
                .field("sensor_id", Schema.STRING_SCHEMA)
                .field("severity", Schema.STRING_SCHEMA)
                .field("message",  Schema.STRING_SCHEMA)
                .field("created_at", Schema.STRING_SCHEMA);
    }

    public static Struct buildStruct(Alarm alarm) {
        var schema = buildSchema();
        return new Struct(schema)
                .put("id", alarm.id())
                .put("sensor_id", alarm.sensorId())
                .put("severity", alarm.severity())
                .put("message", alarm.message())
                .put("created_at", alarm.createdAt().format(DateTimeFormatter.ISO_INSTANT));
    }

}
