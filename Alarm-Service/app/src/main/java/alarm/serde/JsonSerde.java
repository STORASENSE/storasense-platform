package main.java.alarm.serde;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.common.serialization.Deserializer;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serializer;

public class JsonSerde<T> implements Serde<T> {
    private final Class<T> cls;
    private final ObjectMapper objectMapper = new ObjectMapper();

    public JsonSerde(Class<T> cls) {
        this.cls = cls;
    }

    @Override
    public Serializer<T> serializer() {
        return (topic, data) -> {
            try {
                return objectMapper.writeValueAsBytes(data);
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        };
    }

   @Override
   public Deserializer<T> deserializer() {
       return (topic, data) -> {
           try {
               if (data == null) return null;
               return objectMapper.readValue(data, cls);
           } catch (Exception e) {
               throw new RuntimeException(e);
           }
       };
   }
}
