import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
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
    StoraSenseStorge,
    GetAlarmsByStorageIdRequest,
    DeleteAlarmRequest,
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

    tagTypes: ['Me', 'MyStorages'],

    endpoints: (build) => ({

        getMe: build.query<StoraSenseUser | undefined, void>({
            query: () => '/users/me',
            providesTags: ['Me']
        }),

        // same as getMe, but used for signing up ad-hoc
        createMe: build.mutation<StoraSenseUser | undefined, void>({
            query: () => '/users/me',
            invalidatesTags: ['Me', 'MyStorages']
        }),

        getMyStorages: build.query<StoraSenseStorge[], void>({
            query: () => '/storages/myStorages',
            providesTags: ['MyStorages']
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
            }),
            invalidatesTags: ['MyStorages']
        }),

        deleteStorage: build.mutation<void, string>({
            query: (storageId) => ({
                url: `/storages/${storageId}`,
                method: 'DELETE'
            }),
            invalidatesTags: ['MyStorages']
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

        getAlarmsByStorageId: build.query<void, GetAlarmsByStorageIdRequest>({
            query: ({ storage_id }) => ({
                url: `/alarms/byStorageId/${storage_id}`,
                method: 'GET',
            }),
        }),

        deleteAlarm: build.mutation<void, DeleteAlarmRequest>({
            query: ({ alarm_id }) => ({
                url: `/alarms/${alarm_id}`,
                method: 'DELETE'
            })
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
    useCreateMeMutation,
    useGetMyStoragesQuery,
    useGetStoragesByUserIdQuery,
    useCreateStorageMutation,
    useDeleteStorageMutation,
    useGetSensorsQuery,
    useGetMeasurementsQuery,
    useGetHealthQuery,
    useAddSensorMutation,
    useDeleteSensorMutation,
    useGetSensorStatusQuery,
    useGetAlarmsByStorageIdQuery,
    useDeleteAlarmMutation,
} = storaSenseApi;
