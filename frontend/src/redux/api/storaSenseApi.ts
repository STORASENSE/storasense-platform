import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {GetMeasurementsRequest, GetMeasurementsResponse} from "@/redux/api/storaSenseApiSchemas";


export const storaSenseApi = createApi({
    reducerPath: 'storaSenseApi',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://localhost:8002',
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
