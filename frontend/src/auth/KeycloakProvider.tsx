import React, {
    useEffect,
    ReactNode, useRef,
} from 'react';
import { useDispatch } from 'react-redux';
import { setToken } from '@/redux/slices/authSlice';
import { KeycloakContext, useKeycloakBuilder } from './keycloakConfigurer';
import { useCreateMeMutation } from '@/redux/api/storaSenseApi';


interface KeycloakProviderProps {
    children: ReactNode;
}

export const KeycloakProvider: React.FC<KeycloakProviderProps> = ({ children }) => {
    const { keycloak, isLoading, isError, error } = useKeycloakBuilder({
        //onLoad: 'check-sso', TODO add
        checkLoginIframe: false
    });
    const createMeCalled = useRef(false);
    const [createMe] = useCreateMeMutation();
    const dispatch = useDispatch();

    useEffect(() => {
        if (isError) {
            dispatch(setToken(undefined));
        } else if (keycloak && !isLoading) {
            console.log('Successfully authenticated with keycloak');
            dispatch(setToken(keycloak.token));
            // set function for refreshing token
            keycloak.onTokenExpired = () => {
                console.log("Keycloak token expired. Attempting to refresh...");
                keycloak.updateToken(30) // Try to refresh the token 30 seconds before it expires
                    .then((refreshed) => {
                    if (refreshed) {
                        console.log("Token refreshed successfully.");
                        dispatch(setToken(keycloak.token));
                    } else {
                        console.warn('Token could not be refreshed, session may have expired.');
                    }
                    }).catch(() => {
                    console.error('Failed to refresh token.');
                    });
            }
            // create user if user doesn't already exist
            //createMe();
            if (!createMeCalled.current) {
                createMe();
                createMeCalled.current = true;
            }
        }
    }, [keycloak, isLoading, isError]);

    // log any errors if authentication fails
    useEffect(() => {
        if (error) {
            console.error('Failed to authenticate with keycloak', error);
        }
    }, [error]);

    return (
        <KeycloakContext.Provider value={{ keycloak, isLoading, isError, error }}>
            {children}
        </KeycloakContext.Provider>
    );
};

export { KeycloakContext };
