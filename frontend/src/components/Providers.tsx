"use client"

import {FC, ReactNode} from "react";
import {Provider as ReduxProvider} from "react-redux";
import {store} from "@/redux/store";


const Providers: FC<{ children: ReactNode }> = ({ children}) => {
    return (
        <ReduxProvider store={store}>
            {children}
        </ReduxProvider>
    );
}

export default Providers;
