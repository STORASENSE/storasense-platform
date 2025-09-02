"use client"

import { FC, ReactNode, useMemo } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { MdSpaceDashboard as DashboardIcon } from "react-icons/md";
import { MdOutlineWarehouse as StorageIcon } from "react-icons/md";
import { MdOutlineQueryStats as AnalyticsIcon } from "react-icons/md";
import { MdOutlineDeviceThermostat as SensorsIcon } from "react-icons/md";
import { MdOutlinePeople as UsersIcon } from "react-icons/md";
import { MdAlarmOn as AlarmIcon } from "react-icons/md";
import useKeycloak from "@/auth/useKeycloak";
import { useGetHealthQuery } from "@/redux/api/storaSenseApi";

interface SidebarLinkProps {
    href: string;
    icon: ReactNode;
    children: string;
}

const SidebarLink: FC<SidebarLinkProps> = (props) => {
    const pathname = usePathname();

    const isActive = useMemo(() => {
        return pathname === props.href;
    }, [pathname]);

    return (
        <li>
            <Button asChild className={`
                ${isActive ? 'bg-black-haze font-semibold' : 'bg-white'}
                hover:bg-black-haze text-blue-whale justify-start
                w-full shadow-none text-base px-1 py-2`}>
                <Link href={props.href}>
                    <span aria-hidden className="text-3xl mr-2">
                        {props.icon}
                    </span>
                    <span>
                        {props.children}
                    </span>
                </Link>
            </Button>
        </li>
    );
};

const Sidebar: FC = () => {
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

    return (
        <nav className="h-full w-[300px] p-3 border-r-2 border-athens-gray flex flex-col">
            <div
                role="navigation"
                aria-label="external links"
                className="flex flex-col gap-3 flex-grow mt-6">
                <ul className="list-none flex flex-col gap-4">
                    <SidebarLink href="/dashboard/storages" icon={<StorageIcon />}>
                        Storages
                    </SidebarLink>
                    <SidebarLink href="/dashboard" icon={<DashboardIcon />}>
                        Overview
                    </SidebarLink>
                    <SidebarLink href="/dashboard/analytics" icon={<AnalyticsIcon />}>
                        Analytics
                    </SidebarLink>
                     <SidebarLink href="/dashboard/alarms" icon={<AlarmIcon />}>
                        Alarms
                    </SidebarLink>
                    <SidebarLink href="/dashboard/sensors" icon={<SensorsIcon />}>
                        Sensors
                    </SidebarLink>
                    <SidebarLink href="/dashboard/users" icon={<UsersIcon />}>
                        Users
                    </SidebarLink>
                </ul>
            </div>

            {(!isLoading && !isError && keycloak?.authenticated) && (
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
            )}
        </nav>
    );
}

export default Sidebar;
