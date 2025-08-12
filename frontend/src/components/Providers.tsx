"use client"

import {FC, ReactNode} from "react";
import {Provider as ReduxProvider} from "react-redux";
import {store} from "@/redux/store";
import {KeycloakProvider} from "@/components/KeycloakProvider";

const Providers: FC<{ children: ReactNode }> = ({ children}) => {
    return (
        <ReduxProvider store={store}>
            <KeycloakProvider>
                {children}
            </KeycloakProvider>
        </ReduxProvider>
    );
}

export default Providers;
