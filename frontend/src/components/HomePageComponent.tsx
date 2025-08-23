'use client';

import useKeycloak from "@/auth/useKeycloak";
import AuthenticationMessage from "@/components/AuthenticationMessage";
import { useRouter } from "next/navigation";
import { useEffect } from "react";


function HomePageComponent() {
    const router = useRouter();
    const {keycloak, isLoading, isError} = useKeycloak();

    useEffect(() => {
        if (isLoading || isError) {
            return;
        }
        if (keycloak?.authenticated) {
            router.replace("/dashboard");
        }
    }, [keycloak, isLoading, isError]);

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-whale mx-auto mb-4"></div>
                    <p>Loading Auth...</p>
                </div>
            </div>
        );
    }

    if (isError) {
        return <></>;
    }

    // Show login page if not authenticated
    if (!keycloak?.authenticated) {
        return(
            <div className="space-y-6">
                <AuthenticationMessage/>
                <div className="text-center -mt-16">
                    <button id={ "login-button" }
                        onClick={() => keycloak?.login()}
                        className="px-4 py-2 bg-blue-whale text-white border-blue-whale"
                    >
                        Login
                    </button>
                </div>
            </div>
        );
    }

    return null;
}

export default HomePageComponent;
