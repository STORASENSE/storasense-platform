'use client';

import useKeycloak from "@/auth/useKeycloak";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import {Button} from "@/components/ui/button";
import {Skeleton} from "@/components/ui/skeleton";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";


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
            <Skeleton className="w-[80px] h-[40px]"/>
        );
    }

    if (isError) {
        return (
            <Alert variant="destructive">
                <AlertTitle>
                    An unknown error occurred.
                </AlertTitle>
                <AlertDescription>
                    Failed to load authentication provider.
                </AlertDescription>
            </Alert>
        );
    }

    // Show login page if not authenticated
    if (!keycloak?.authenticated) {
        return(
            <Button onClick={() => keycloak?.login()}>
                Login
            </Button>
        );
    }

    return null;
}

export default HomePageComponent;
