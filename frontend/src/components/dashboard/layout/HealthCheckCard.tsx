"use client"

import useKeycloak from "@/auth/useKeycloak";
import {useGetHealthQuery} from "@/redux/api/storaSenseApi";
import {useMemo} from "react";
import {Skeleton} from "@/components/ui/skeleton";


const HealthCheckCard: React.FC = () => {
    const { keycloak, isLoading, isError } = useKeycloak();

    const { data: healthData, isSuccess } = useGetHealthQuery(undefined, {
        skip: isLoading || isError || !keycloak?.authenticated,
        pollingInterval: 60000, // Poll every 60 seconds
    });

    const username = useMemo<string>(() => {
        const defaultUsername = "[User]";
        if (isLoading || isError || !keycloak?.authenticated) {
            return defaultUsername;
        }
        return keycloak?.idTokenParsed?.preferred_username || defaultUsername;
    }, [keycloak, isLoading, isError]);

    const isBackendOnline = useMemo<boolean>(() => {
        return isSuccess && healthData?.status !== undefined;
    }, [healthData, isSuccess]);

    if (isLoading) {
        return (
            <Skeleton className="w-full h-[120px]"/>
        );
    }

    if (isError || !healthData) {
        return <></>;
    }

    return (
        <div className="mt-auto pt-3 border-t border-athens-gray">
            <div className="bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 rounded-lg p-3 border border-slate-200 shadow-md">
                {isBackendOnline ? (
                    <div className="flex items-center space-x-2 mb-2">
                        <div className="relative">
                            <div className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></div>
                            <div className="absolute inset-0 w-2 h-2 bg-emerald-400 rounded-full animate-ping opacity-75"></div>
                        </div>
                        <span id = "Backend_Online" className="text-xs font-medium text-emerald-600 uppercase tracking-wide">
                            Online
                        </span>
                    </div>
                ) : (
                    <div className="flex items-center space-x-2 mb-2">
                        <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                        <span id ="Backend_Offline" className="text-xs font-medium text-red-600 uppercase tracking-wide">
                            Offline
                        </span>
                    </div>
                )}
                <div className="space-y-1">
                    <p className="text-xs text-slate-500 font-medium">Welcome back</p>
                    <p className="text-base font-bold text-slate-800 truncate">{username}</p>
                </div>
                <div className="mt-2 h-0.5 bg-gradient-to-r from-blue-200 via-indigo-300 to-purple-200 rounded-full"></div>
            </div>
        </div>
    );
}

export default HealthCheckCard;
