// Universal React component to protect pages with Keycloak authentication

'use client';

import { FC, ReactNode } from "react";
import useKeycloak from '../app/(main)/useKeycloak';
import AuthenticationMessage from "@/components/AuthenticationMessage";

interface ProtectedPageProps {
    children: ReactNode;
}

const ProtectedPage: FC<ProtectedPageProps> = ({ children }) => {
    const { keycloak, authenticated } = useKeycloak();
    if (!authenticated || !keycloak) {
        return (
            <>
                <AuthenticationMessage/>
            </>
        );
    }
    return <>{children}</>;
};

export default ProtectedPage;
