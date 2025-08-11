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
            <>
                <AuthenticationMessage/>
                <div className="text-center">
                    <button
                        onClick={() => keycloak?.login()}
                        className="px-4 py-2 bg-blue-500 text-white rounded"
                    >
                        Login
                    </button>
                </div>
            </>
        );
    }

    // Fallback if useEffect hasnt been triggered yet
    return null;
}

export default HomePageComponent;
