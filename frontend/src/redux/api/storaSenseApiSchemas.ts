/////////////////////////////////////////////////////////////////////////
/// Pagination
/////////////////////////////////////////////////////////////////////////

export interface NumberedPageRequest {
    page_number: number;
    page_size: number;
}

export interface CursorBasedPageRequest {
    page_number: number;
    cursor: number;
}

export interface Page<T> {
    page_number: number;
    total_pages: number;
    items: T[];
}

export interface NumberedPage<T> extends Page<T> {
    page_size: number;
}

export interface CursorBasedPage<T> extends Page<T> {
    cursor: number
}

/////////////////////////////////////////////////////////////////////////
/// Enums
/////////////////////////////////////////////////////////////////////////

export enum MeasurementUnit {
    CELSIUS,
    FAHRENHEIT,
    PERCENT,
}

export enum SensorType {
    TEMPERATURE_INSIDE = 'TEMPERATURE_INSIDE',
    TEMPERATURE_OUTSIDE = 'TEMPERATURE_OUTSIDE',
    HUMIDITY = 'HUMIDITY',
    ULTRASONIC = 'ULTRASONIC',
    GAS = 'GAS',
}

/////////////////////////////////////////////////////////////////////////
/// Model Types
/////////////////////////////////////////////////////////////////////////

export interface StoraSenseUser {
    id: string;
    keycloak_id: string;
    username: string;
    email?: string;
    name?: string;
}

export interface StoraSenseStorge {
    id: string;
    name: string;
}

export interface Sensor {
    id: string;
    name: string;
    type: SensorType;
    storage_id: string;
    allowed_min: number;
    allowed_max: number;
}

export interface Measurement {
    id: string;
    value: number;
    unit: MeasurementUnit;
    created_at: Date;
}

/////////////////////////////////////////////////////////////////////////
/// Requests & Responses
/////////////////////////////////////////////////////////////////////////

export interface GetStoragesByUserIdRequest {
    user_id: string;
}

export type GetStoragesByUserIdResponse = StoraSenseStorge[];

/////////////////////////////////////////////////////////////////////////

export interface GetSensorsByStorageIdRequest {
    storage_id: string;
}

export type GetSensorsByStorageIdResponse = Sensor[];

/////////////////////////////////////////////////////////////////////////

export interface AddSensorRequest {
    sensor_id: string;
    sensor: {
        name: string;
        type: SensorType;
        storage_id: string;
        allowed_min: number;
        allowed_max: number;
    };
}

export interface AddSensorResponse {
    sensor_id: string;
    name: string;
    type: SensorType;
    storage_id: string;
    allowed_min: number;
    allowed_max: number;
    location?: string;
}

export interface DeleteSensorRequest {
    sensor_id: string;
}

export interface SensorStatusResponse {
  sensor_id: string;
  is_online: boolean;
  last_measurement: string | null;
}

/////////////////////////////////////////////////////////////////////////

export interface GetMeasurementsRequest {
    sensor_id: string;
    page_request: CursorBasedPageRequest;
}

export interface GetMeasurementsResponse {
    measurements: Measurement[];
}

/////////////////////////////////////////////////////////////////////////

export interface CreateStorageRequest {
    name: string;
}
