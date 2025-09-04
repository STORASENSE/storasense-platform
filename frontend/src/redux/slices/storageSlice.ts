import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {StoraSenseStorge} from "@/redux/api/storaSenseApiSchemas";


interface StorageSliceState {
    activeStorage?: StoraSenseStorge;
}

const initialState: StorageSliceState = {
    activeStorage: undefined
}

if (typeof window !== 'undefined' && localStorage.getItem('activeStorage')) {
    try {
        const storage = JSON.parse(localStorage.getItem('activeStorage')!);
        initialState.activeStorage = storage;
    } catch {
        localStorage.removeItem('activeStorage');
    }
}


const storageSlice = createSlice({
    name: "storageSlice",
    initialState,
    reducers: {

        setActiveStorage: (state: StorageSliceState, action: PayloadAction<StoraSenseStorge | undefined>) => {
            if (action.payload) {
                localStorage.setItem('activeStorage', JSON.stringify(action.payload));
            } else {
                localStorage.removeItem('activeStorage');
            }
            return {
                ...state,
                activeStorage: action.payload,
            }
        }

    }
});


export const {setActiveStorage} = storageSlice.actions;

export default storageSlice.reducer;
