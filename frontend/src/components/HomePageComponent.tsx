'use client';

import { useKeycloak } from '@/components/KeycloakProvider';

function HomePageComponent() {
    const { keycloak, isAuthenticated } = useKeycloak();

    if (!keycloak) {
        return <div className="text-center p-10">Page is loading...</div>;
    }

    if (isAuthenticated) {
        return (
            <div className="text-center p-10">
                <h1 className="text-2xl mb-4">Welcome, {keycloak.tokenParsed?.preferred_username}!</h1>
                <p>You're signed in.</p>
                <button
                    onClick={() => keycloak.logout()}
                    className="mt-4 px-4 py-2 bg-red-500 text-white rounded"
                >
                    Sign out
                </button>
            </div>
        );
    }

    return (
        <div className="text-center p-10">
            <h1 className="text-2xl mb-4">Please sign in</h1>
            <button
                onClick={() => keycloak.login()}
                className="px-4 py-2 bg-blue-500 text-white rounded"
            >
                Sign in
            </button>
        </div>
    );
}

export default HomePageComponent;
