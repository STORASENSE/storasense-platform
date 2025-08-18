import Keycloak, { KeycloakConfig } from "keycloak-js";
import { createContext, useContext, useEffect, useRef, useState } from "react";


const keycloakConfig: KeycloakConfig = {
    url: "https://auth.storasense.de",
    realm: "storasense-realm",
    clientId: "frontend-client",
};


function buildKeycloak(): Keycloak {
    return new Keycloak(keycloakConfig);
}

///////////////////////////////////////////////////////////////////////////////////

export interface KeycloakContextState {
    keycloak?: Keycloak;
    isLoading: boolean;
    isError: boolean;
    error?: any;
}

export const KeycloakContext = createContext<KeycloakContextState>({
    isLoading: false,
    isError: false
});

///////////////////////////////////////////////////////////////////////////////////

export function useKeycloak(): KeycloakContextState {
    return useContext(KeycloakContext);
}

///////////////////////////////////////////////////////////////////////////////////

export function useKeycloakBuilder(): KeycloakContextState {
    const isRun = useRef<boolean>(false);

    const [keycloak, setKeycloak] = useState<Keycloak | undefined>(undefined);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [isError, setIsError] = useState<boolean>(false);
    const [error, setError] = useState<any>(undefined);

    useEffect(() => {
        if (isRun.current) {
            return;
        }

        isRun.current = true;
        setIsLoading(true);

        const keycloakInstance = buildKeycloak();
        setKeycloak(keycloak);

        keycloakInstance
            .init({
                onLoad: 'check-sso',
            })
            .then(() => {
                setIsError(false);
                setError(false);
            })
            .catch((error) => {
                setIsError(true);
                setError(error);
            })
            .finally(() => {
                setKeycloak(keycloakInstance);
                setIsLoading(false);
            });
    }, []);

    return { keycloak, isLoading, isError, error };
}
