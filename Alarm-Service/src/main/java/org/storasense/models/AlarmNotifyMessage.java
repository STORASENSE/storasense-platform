package org.storasense.models;

public record AlarmNotifyMessage(
    String email,
    Alarm alarm
) {}
