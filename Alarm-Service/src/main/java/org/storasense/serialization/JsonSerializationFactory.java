package org.storasense.serialization;


import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.module.jsonSchema.JsonSchema;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;
import org.storasense.models.JsonWithSchema;

import java.io.IOException;


public class JsonSerializationFactory {

    private final ObjectMapper mapper = new ObjectMapper();

    private byte[] serializeObject(String topic, Object obj) {
        if (obj == null) {
            return null;
        }
        try {
            return mapper.writeValueAsBytes(obj);
        } catch (final Exception e) {
            throw new SerializationException("Error serializing object to JSON", e);
        }
    }

    private <T> Serializer<T> buildSerializer(Class<T> targetType) {
        return this::serializeObject;
    }

    private <T> Serializer<JsonWithSchema<T>> buildSerializerWithSchema(Class<T> targetType) {
        return this::serializeObject;
    }

    private <T> Deserializer<T> buildDeserializer(Class<T> targetType) {
        final ObjectMapper mapper = new ObjectMapper();
        return (topic, data) -> {
            if (data == null) {
                return null;
            }
            try {
                // if data is a JSON object wrapped in string quotes:
                // unwrap data
                var node = mapper.readTree(data);
                if (node.isTextual()) {
                    return (T) mapper.readValue(node.textValue(), targetType);
                }
                // else, convert directly
                return (T) mapper.readValue(data, targetType);
            } catch (final IOException e) {
                throw new SerializationException(e);
            }
        };
    }

    private <T> Deserializer<JsonWithSchema<T>> buildDeserializerWithSchema(JsonSchema schema, Class<T> targetType) {
        var deserializer = buildDeserializer(targetType);
        return (topic, data) -> {
            var object = deserializer.deserialize(topic, data);
            if (object == null) {
                return null;
            }
            return new JsonWithSchema<>(schema, object);
        };
    }

    public <T> Serde<T> buildSerde(Class<T> targetType) {
        var serializer = buildSerializer(targetType);
        var deserializer = buildDeserializer(targetType);
        return Serdes.serdeFrom(serializer, deserializer);
    }

    public <T> Serde<JsonWithSchema<T>> buildSerdeWithSchema(JsonSchema schema, Class<T> targetType) {
        var serializer = buildSerializerWithSchema(targetType);
        var deserializer = buildDeserializerWithSchema(schema, targetType);
        return Serdes.serdeFrom(serializer, deserializer);
    }

}
