import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {
    GetMeasurementsRequest,
    GetMeasurementsResponse,
    GetSensorsByStorageIdRequest,
    GetSensorsByStorageIdResponse,
    GetStoragesByUserIdRequest,
    GetStoragesByUserIdResponse
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

        getStoragesByUserId: build.query<GetStoragesByUserIdResponse, GetStoragesByUserIdRequest>({
            query: ({ user_id }) => ({
                url: `/storages/byUserId/${user_id}`
            })
        }),

        getSensors: build.query<GetSensorsByStorageIdResponse, GetSensorsByStorageIdRequest>({
            query: ({ storage_id }) => ({
                url: `/sensors/byStorageId/${storage_id}`
            })
        }),

        getMeasurements: build.query<GetMeasurementsResponse, GetMeasurementsRequest>({
            query: ({ sensor_id, max_date }) => ({
                url: `/measurements/${sensor_id}/filter`,
                params: { max_date }
            }),
        }),

    })
});

export const {
    useGetStoragesByUserIdQuery,
    useGetSensorsQuery,
    useGetMeasurementsQuery,
} = storaSenseApi;
