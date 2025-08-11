"use client"

import {FC} from "react";
import {Input} from "@/components/ui/input";
import useKeycloak from '../../app/(main)/useKeycloak';

const TopBar: FC = () => {
    const { keycloak, authenticated } = useKeycloak();

    return (
        <div className="py-2 px-5 grow flex justify-between items-end">
            <div role="navigation" aria-label="search tools">
                <Input placeholder="Search..."/>
            </div>

            <div className="user-actions">
                {authenticated ? (
                    <button
                        onClick={() => keycloak?.logout()}
                        className="px-4 py-2 bg-red-500 text-white rounded"
                    >
                        Logout
                    </button>
                ) : (
                    <button
                        onClick={() => keycloak?.login()}
                        className="px-4 py-2 bg-blue-500 text-white rounded"
                    >
                        Login
                    </button>
                )}
            </div>
        </div>
    );
}

export default TopBar;
