import {configureStore} from "@reduxjs/toolkit/react";
import {setupListeners} from "@reduxjs/toolkit/query/react";
import {storaSenseApi} from "@/redux/api/storaSenseApi";


export const store = configureStore({
    reducer: {
        [storaSenseApi.reducerPath]: storaSenseApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(storaSenseApi.middleware),
});

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

setupListeners(store.dispatch)
