"use client"

import {FC} from "react";
import useKeycloak from '@/auth/useKeycloak';
import ActiveStorageSelection from "./ActiveStorageSelection";
import {Button} from "@/components/ui/button";

const TopBar: FC = () => {
    const { keycloak, isLoading, isError } = useKeycloak();

    return (
        <div className="py-2 px-5 grow flex justify-between items-end">
            <div role="navigation" aria-label="search tools">
                <ActiveStorageSelection />
            </div>

            <div className="user-actions">
                {(!keycloak || isLoading || isError) ? (
                    <></>
                ) : keycloak.authenticated ? (
                    <Button onClick={() => keycloak.logout()}>
                        Logout
                    </Button>
                ) : (
                    <Button onClick={() => keycloak.login()}>
                        Login
                    </Button>
                )}
            </div>
        </div>
    );
}

export default TopBar;
