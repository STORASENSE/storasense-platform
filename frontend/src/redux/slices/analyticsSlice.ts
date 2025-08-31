import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";


interface AnalyticsSliceState {
    timeWindow: AnalyticsTimeWindow;
}


const initialState: AnalyticsSliceState = {
    timeWindow: '7d'
}


const analyticsSlice = createSlice({
    name: "analyticsSlice",
    initialState,
    reducers: {

        setTimeWindow: (state, action: PayloadAction<AnalyticsTimeWindow>) => {
            state.timeWindow = action.payload;
        }

    }
});


export const { setTimeWindow } = analyticsSlice.actions;

export default analyticsSlice.reducer;
