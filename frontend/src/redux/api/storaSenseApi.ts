import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export const storaSenseApi = createApi({
    reducerPath: 'storaSenseApi',
    baseQuery: fetchBaseQuery({
        baseUrl: 'http://.../',
    }),
    endpoints: (build) => ({

    })
});
