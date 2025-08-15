'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import useKeycloak from '../app/(main)/useKeycloak';
import AuthenticationMessage from "@/components/AuthenticationMessage";

function HomePageComponent() {
    const { keycloak, authenticated } = useKeycloak();
    const router = useRouter();

    useEffect(() => {
        if (authenticated) {
            router.push('/dashboard');
        }
    }, [authenticated, router]);

    if (!authenticated || !keycloak) {
        return(
            <div className="space-y-6">
                <AuthenticationMessage/>
                <div className="text-center -mt-16">
                    <button
                        onClick={() => keycloak?.login()}
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
                    >
                        Login
                    </button>
                </div>
            </div>
        );
    }

    // Fallback if useEffect hasn't been triggered yet
    return null;
}

export default HomePageComponent;
