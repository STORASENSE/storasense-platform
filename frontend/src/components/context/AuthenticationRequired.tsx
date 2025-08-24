// Universal React component to protect pages with Keycloak authentication

'use client';

import { FC, ReactNode } from "react";
import useKeycloak from '../../auth/useKeycloak';
import { FaLock as LockIcon } from "react-icons/fa6";


interface AuthenticationRequiredProps {
    children: ReactNode;
}

const AuthenticationRequired: FC<AuthenticationRequiredProps> = ({ children }) => {
    const { keycloak, isLoading, isError } = useKeycloak();
    if (isLoading || isError || !keycloak?.authenticated) {
        return (
            <header className="mt-5 flex flex-col items-center">
                <h1 className="flex items-center gap-2 text-blue-whale text-xl font-semibold">
                    <LockIcon aria-hidden />
                    <span>
                        Content Locked
                    </span>
                </h1>
                <p className="mt-2">
                    You need to log in to view this content.
                </p>
            </header>
        );
    }
    return <>{children}</>;
};

export default AuthenticationRequired;
