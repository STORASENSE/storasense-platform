import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { useRouter } from 'next/navigation';
import useKeycloak from './useKeycloak';
import { useGetMeQuery } from '@/redux/api/storaSenseApi';
import { setToken } from '@/redux/slices/authSlice';

export function useAuthenticatedUser() {
    const { keycloak, authenticated } = useKeycloak();
    const dispatch = useDispatch();
    const router = useRouter();
    const [keycloakReady, setKeycloakReady] = useState(false);
    const [authFlowComplete, setAuthFlowComplete] = useState(false);

    // Keycloak ready check
    useEffect(() => {
        if (keycloak && keycloak.authenticated !== undefined) {
            setKeycloakReady(true);
        }
    }, [keycloak]);

    // Token management
    useEffect(() => {
        if (keycloakReady) {
            if (authenticated && keycloak?.token) {
                dispatch(setToken(keycloak.token));
                setAuthFlowComplete(true);
            } else if (!authenticated) {
                dispatch(setToken(null));
                setAuthFlowComplete(false);
            }
        }
    }, [keycloakReady, authenticated, keycloak?.token, dispatch]);

    // /me call - after Auth-Flow
    const {
        data: user,
        error,
        isLoading,
        isSuccess
    } = useGetMeQuery(undefined, {
        skip: !authFlowComplete || !keycloak?.token
    });

    // Auto redirect after successful user initialization
    useEffect(() => {
        if (isSuccess && user) {
            console.log('User initialized:', user.username);
            router.push('/dashboard');
        }
    }, [isSuccess, user, router]);

    // Error handling
    useEffect(() => {
        if (error && 'status' in error && error.status === 401) {
            console.log('Session expired, redirecting to login');
            dispatch(setToken(null));
            setAuthFlowComplete(false);
            keycloak?.login();
        }
    }, [error, keycloak, dispatch]);

    return {
        keycloak,
        authenticated,
        keycloakReady,
        authFlowComplete,
        user,
        isLoading,
        error,
        isSuccess
    };
}
