import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {GetMeasurementsRequest, GetMeasurementsResponse} from "@/redux/api/storaSenseApiSchemas";


function getBaseUrl(): string {
    switch (process.env.NODE_ENV) {
        case "test":
        case "development":
            return "http://localhost:8000";
        case "production":
            return "http://localhost:8000";
        default:
            throw new Error("Environment variable NODE_ENV was not set by node environment!");
    }
}


export const storaSenseApi = createApi({
    reducerPath: 'storaSenseApi',
    baseQuery: fetchBaseQuery({
        baseUrl: getBaseUrl(),
    }),
    endpoints: (build) => ({

        getMeasurements: build.query<GetMeasurementsResponse, GetMeasurementsRequest>({
            query: ({ sensor_id, max_date }) => ({
                url: `/measurements/${sensor_id}/filter`,
                params: { max_date }
            }),
        }),

    })
});

export const { useGetMeasurementsQuery } = storaSenseApi;
