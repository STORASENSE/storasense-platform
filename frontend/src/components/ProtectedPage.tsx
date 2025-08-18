// Universal React component to protect pages with Keycloak authentication

'use client';

import { FC, ReactNode } from "react";
import useKeycloak from '../auth/useKeycloak';
import AuthenticationMessage from "@/components/AuthenticationMessage";

interface ProtectedPageProps {
    children: ReactNode;
}

const ProtectedPage: FC<ProtectedPageProps> = ({ children }) => {
    const { keycloak, isLoading, isError } = useKeycloak();
    if (isLoading || isError || !keycloak?.authenticated) {
        return (
            <>
                <AuthenticationMessage/>
            </>
        );
    }
    return <>{children}</>;
};

export default ProtectedPage;
