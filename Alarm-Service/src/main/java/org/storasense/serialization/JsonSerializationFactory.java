package org.storasense.serialization;


import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.errors.SerializationException;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.common.serialization.Serializer;

import java.io.IOException;


public class JsonSerializationFactory {

    public <T> Serializer<T> buildSerializer(Class<T> targetType) {
        final ObjectMapper mapper = new ObjectMapper();
        return (topic, data) -> {
            if (data == null) {
                return null;
            }
            try {
                return mapper.writeValueAsBytes(data);
            } catch (final Exception e) {
                throw new SerializationException("Error serializing object to JSON", e);
            }
        };
    }

    public <T> Deserializer<T> buildDeserializer(Class<T> targetType) {
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

    public <T> Serde<T> buildSerde(Class<T> targetType) {
        var serializer = buildSerializer(targetType);
        var deserializer = buildDeserializer(targetType);
        return Serdes.serdeFrom(serializer, deserializer);
    }

}
