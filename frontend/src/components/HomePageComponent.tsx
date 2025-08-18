'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useDispatch } from 'react-redux';
import useKeycloak from '../app/(main)/useKeycloak';
import AuthenticationMessage from "@/components/AuthenticationMessage";
import { useGetMeQuery } from '@/redux/api/storaSenseApi';
import { setToken } from '@/redux/slices/authSlice';

function HomePageComponent() {
    const { keycloak, authenticated } = useKeycloak();
    const router = useRouter();
    const dispatch = useDispatch();
    const [keycloakReady, setKeycloakReady] = useState(false);

    // Store the Keycloak token in Redux when Keycloak is ready and authenticated
    useEffect(() => {
        if (keycloak && authenticated && keycloak.token) {
            dispatch(setToken(keycloak.token));
        } else if (!authenticated) {
            dispatch(setToken(null));
        }
    }, [keycloak, authenticated, dispatch]);

    // /me call
    const {
        data: user,
        error,
        isLoading,
        isSuccess
    } = useGetMeQuery(undefined, {
        skip: !keycloakReady || !authenticated || !keycloak?.token
    });

    // Set Keycloak ready state when Keycloak is initialized
    useEffect(() => {
        if (keycloak && keycloak.authenticated !== undefined) {
            setKeycloakReady(true);
        }
    }, [keycloak]);

    // Redirect to dashboard when user is successfully loaded
    useEffect(() => {
        if (isSuccess && user) {
            console.log('User initialized:', user.username);
            router.push('/dashboard');
        }
    }, [isSuccess, user, router]);

    // Handle errors
    useEffect(() => {
        if (error && 'status' in error && error.status === 401) {
            console.log('Session expired, redirecting to login');
            dispatch(setToken(null));
            keycloak?.login();
        }
    }, [error, keycloak, dispatch]);

    // Wait for Keycloak to be ready
    if (!keycloakReady) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-whale mx-auto mb-4"></div>
                    <p>Loading Auth...</p>
                </div>
            </div>
        );
    }

    if (!authenticated || !keycloak) {
        return(
            <div className="space-y-6">
                <AuthenticationMessage/>
                <div className="text-center -mt-16">
                    <button
                        onClick={() => keycloak?.login()}
                        className="px-4 py-2 bg-blue-whale text-white border-blue-whale"
                    >
                        Login
                    </button>
                </div>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-whale mx-auto mb-4"></div>
                    <p>Loading User...</p>
                </div>
            </div>
        );
    }

    return null;
}

export default HomePageComponent;
