import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {StoraSenseStorge} from "@/redux/api/storaSenseApiSchemas";


interface StorageSliceState {
    activeStorage?: StoraSenseStorge;
    availableStorages: StoraSenseStorge[];
}

const initialState: StorageSliceState = {
    activeStorage: {
        id: "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        name: "MyStorage"
    },
    availableStorages: [],
}


const storageSlice = createSlice({
    name: "storageSlice",
    initialState,
    reducers: {

        setActiveStorage: (state: StorageSliceState, action: PayloadAction<StoraSenseStorge>) => {
            return {
                ...state,
                activeStorage: action.payload,
            }
        }

    }
});


export const {setActiveStorage} = storageSlice.actions;

export default storageSlice.reducer;
