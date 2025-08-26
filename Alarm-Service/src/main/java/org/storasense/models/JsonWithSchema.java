package org.storasense.models;

import com.fasterxml.jackson.module.jsonSchema.JsonSchema;


public record JsonWithSchema<T>(
        JsonSchema schema,
        T payload
) {}
