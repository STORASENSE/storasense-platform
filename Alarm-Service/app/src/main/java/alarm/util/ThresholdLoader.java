package main.java.alarm.util;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import main.java.alarm.model.Threshold;

import java.io.File;
import java.util.Collections;
import java.util.Map;

public class ThresholdLoader {
public static Map<String, Threshold> load(String path) {
try {
ObjectMapper mapper = new ObjectMapper();
return mapper.readValue(new File(path), new TypeReference<Map<String, Threshold>>() {});
} catch (Exception e) {
System.err.println("WARN: thresholds file not found or invalid: " + e.getMessage());
return Collections.emptyMap();
}
}
}
