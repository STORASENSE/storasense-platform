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
    AnalyticsSummaryResponse,
    AnalyticsSummaryRequest,
    GetUsersByStorageIdResponse,
    GetUsersByStorageIdRequest,
    AddUserToStorageRequest,
    RemoveUserFromStorageRequest,
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

    tagTypes: ['Me', 'MyStorages', 'UsersInStorage'],

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

        getUsersByStorageId: build.query<GetUsersByStorageIdResponse, GetUsersByStorageIdRequest>({
            query: ({ storage_id }) => ({
                url: `/users/byStorageId/${storage_id}`,
            }),
            providesTags: ['UsersInStorage']
        }),

        addUserToStorage: build.mutation<void, AddUserToStorageRequest>({
            query: ({ username, storage_id }) => ({
                url: `/users/${username}/addToStorage`,
                params: { storage_id },
                method: 'POST'
            }),
            invalidatesTags: ['UsersInStorage']
        }),

        removeUserFromStorage: build.mutation<void, RemoveUserFromStorageRequest>({
            query: ({ username, storage_id }) => ({
                url: `/users/${username}/removeFromStorage`,
                params: { storage_id },
                method: 'DELETE'
            }),
            invalidatesTags: ['UsersInStorage']
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
            })
        }),

        getSensorStatus: build.query<SensorStatusResponse, { sensor_id: string }>({
            query: ({ sensor_id }) => ({
                url: `/sensors/status/${sensor_id}`,
                method: 'GET',
            }),
        }),

        deleteSensor: build.mutation<void, DeleteSensorRequest>({
            query: ({ sensor_id, sensor }) => ({
                url: `/sensors/${sensor_id}`,
                method: 'DELETE',
                body: sensor
            })
        }),

        getMeasurements: build.query<GetMeasurementsResponse, GetMeasurementsRequest>({
            query: ({ sensor_id, max_date }) => ({
                url: `/measurements/${sensor_id}/filter`,
                params: { max_date }
            }),
        }),

        getMeasurementsFromPastHour: build.query<GetMeasurementsResponse, Omit<GetMeasurementsRequest, "max_date">>({
            query: ({ sensor_id }) => {
                const max_date = new Date();
                max_date.setHours(max_date.getHours() - 1);
                return {
                    url: `/measurements/${sensor_id}/filter`,
                    params: {
                        max_date: max_date.toISOString()
                    }
                };
            }
        }),

        getAnalyticsSummary: build.query<AnalyticsSummaryResponse, AnalyticsSummaryRequest>({
          query: ({ sensor_id, window }) => ({
            url: `/analytics/summaryBySensorId/${sensor_id}`,
            method: "GET",
            params: { window },
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
                url: '/health',
                method: 'GET'
            })
        }),

    })
});

export const {
    useGetMeQuery,
    useCreateMeMutation,
    useGetMyStoragesQuery,
    useGetUsersByStorageIdQuery,
    useAddUserToStorageMutation,
    useRemoveUserFromStorageMutation,
    useGetStoragesByUserIdQuery,
    useCreateStorageMutation,
    useDeleteStorageMutation,
    useGetSensorsQuery,
    useGetMeasurementsQuery,
    useGetMeasurementsFromPastHourQuery,
    useGetHealthQuery,
    useAddSensorMutation,
    useDeleteSensorMutation,
    useGetSensorStatusQuery,
    useGetAnalyticsSummaryQuery,
    useGetAlarmsByStorageIdQuery,
    useDeleteAlarmMutation,
} = storaSenseApi;
