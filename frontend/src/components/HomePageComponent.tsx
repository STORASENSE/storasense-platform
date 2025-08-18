'use client';

import AuthenticationMessage from "@/components/AuthenticationMessage";
import { useAuthenticatedUser } from '@/app/(main)/useAuthenticatedUser';

function HomePageComponent() {
    const {
        keycloak,
        authenticated,
        keycloakReady,
        isLoading
    } = useAuthenticatedUser();

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

    // Show login page if not authenticated
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

    // Show loading state if user is authenticated but still loading
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
