import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface AuthState {
    token?: string;
}

const initialState: AuthState = {
    token: undefined,
};

export const authSlice = createSlice({
    name: 'authSlice',
    initialState,
    reducers: {
        setToken: (state, action: PayloadAction<string | undefined>) => {
            state.token = action.payload;
        },
    },
});

export const { setToken } = authSlice.actions;

export default authSlice.reducer;
