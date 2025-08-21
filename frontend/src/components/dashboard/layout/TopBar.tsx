"use client"

import {FC} from "react";
import useKeycloak from '@/auth/useKeycloak';
import ActiveStorageSelection from "./ActiveStorageSelection";

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
                    <button
                        onClick={() => keycloak.logout()}
                        className="px-4 py-2 bg-red-500 text-white rounded"
                    >
                        Logout
                    </button>
                ) : (
                    <button
                        onClick={() => keycloak.login()}
                        className="px-4 py-2 bg-blue-whale text-white border-blue-whale"
                    >
                        Login
                    </button>
                )}
            </div>
        </div>
    );
}

export default TopBar;
