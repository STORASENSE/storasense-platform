import {BaseQueryError, BaseQueryMeta, createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {
    CreateStorageRequest,
    GetMeasurementsRequest,
    GetMeasurementsResponse,
    GetSensorsByStorageIdRequest,
    GetSensorsByStorageIdResponse,
    GetStoragesByUserIdRequest,
    GetStoragesByUserIdResponse,
    StoraSenseUser,
    AddSensorRequest,
    AddSensorResponse,
    DeleteSensorRequest,
    SensorStatusResponse,
} from "@/redux/api/storaSenseApiSchemas";
import type { RootState } from '../store';

function getBaseUrl(): string {
    switch (process.env.NODE_ENV) {
        case "test":
        case "development":
            return "https://api.storasense.de";
        case "production":
            return "https://api.storasense.de";
        default:
            throw new Error("Environment variable NODE_ENV was not set by node environment!");
    }
}

export const storaSenseApi = createApi({
    reducerPath: 'storaSenseApi',
    baseQuery: fetchBaseQuery({
        baseUrl: getBaseUrl(),
        prepareHeaders: (headers, {getState }) => {
            const token = (getState() as RootState).auth.token;
            if (token) {
                headers.set('Authorization', `Bearer ${token}`);
            }
            return headers;
        }
    }),
    endpoints: (build) => ({

        getMe: build.query<StoraSenseUser | undefined, void>({
            query: () => '/users/me'
        }),

        getStoragesByUserId: build.query<GetStoragesByUserIdResponse, GetStoragesByUserIdRequest>({
            query: ({ user_id }) => ({
                url: `/storages/byUserId/${user_id}`
            })
        }),

        createStorage: build.mutation<void, CreateStorageRequest>({
            query: (request) => ({
                url: '/storages',
                body: request,
                method: 'POST'
            })
        }),

        getSensors: build.query<GetSensorsByStorageIdResponse, GetSensorsByStorageIdRequest>({
            query: ({ storage_id }) => ({
                url: `/sensors/byStorageId/${storage_id}`,
                method: 'GET',
            })
        }),

        addSensor: build.mutation<AddSensorResponse, AddSensorRequest>({
            query: ({sensor_id, sensor}) => ({
                url: `/sensors/${sensor_id}`,
                method: 'POST',
                body: sensor,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        }),

        getSensorStatus: build.query<SensorStatusResponse, { sensor_id: string }>({
            query: ({ sensor_id }) => ({
                url: `/sensors/status/${sensor_id}`,
                method: 'GET',
            }),
        }),

        deleteSensor: build.mutation<void, DeleteSensorRequest>({
            query: ({ sensor_id }) => ({
                url: `/sensors/${sensor_id}`,
                method: 'DELETE'
            })
        }),

        getMeasurements: build.query<GetMeasurementsResponse, GetMeasurementsRequest>({
            query: ({ sensor_id, max_date }) => ({
                url: `/measurements/${sensor_id}/filter`,
                params: { max_date }
            }),
        }),

        getHealth: build.query<{ status: string }, void>({
            query: () => ({
                url: '/health'
            })
        }),

    })
});

export const {
    useGetMeQuery,
    useGetStoragesByUserIdQuery,
    useCreateStorageMutation,
    useGetSensorsQuery,
    useGetMeasurementsQuery,
    useGetHealthQuery,
    useAddSensorMutation,
    useDeleteSensorMutation,
    useGetSensorStatusQuery
} = storaSenseApi;
