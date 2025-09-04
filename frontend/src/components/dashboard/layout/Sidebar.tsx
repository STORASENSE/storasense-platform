"use client"

import { FC, ReactNode, useMemo } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { MdSpaceDashboard as DashboardIcon } from "react-icons/md";
import { FaBoxArchive as StorageIcon } from "react-icons/fa6";
import { SiGoogleanalytics as AnalyticsIcon } from "react-icons/si";
import { FaThermometer as SensorsIcon } from "react-icons/fa6";
import { FaUserPlus as UsersIcon } from "react-icons/fa6";
import { IoAlarm as AlarmIcon } from "react-icons/io5";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import HealthCheckCard from "@/components/dashboard/layout/HealthCheckCard";

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
    return (
        <nav className="h-full w-[300px] p-3 border-r-2 border-athens-gray flex flex-col">
            <div
                role="navigation"
                aria-label="external links"
                className="flex flex-col gap-3 flex-grow mt-6">
                <ul className="list-none flex flex-col gap-4">
                    <SidebarLink href="/dashboard" icon={<DashboardIcon />}>
                        Overview
                    </SidebarLink>
                    <SidebarLink href="/dashboard/analytics" icon={<AnalyticsIcon />}>
                        Analytics
                    </SidebarLink>
                    <SidebarLink href="/dashboard/alarms" icon={<AlarmIcon />}>
                        Alarms
                    </SidebarLink>
                    <SidebarLink href="/dashboard/storages" icon={<StorageIcon />}>
                        Storages
                    </SidebarLink>
                    <SidebarLink href="/dashboard/sensors" icon={<SensorsIcon />}>
                        Sensors
                    </SidebarLink>
                    <SidebarLink href="/dashboard/users" icon={<UsersIcon />}>
                        Users
                    </SidebarLink>
                </ul>
            </div>

            <AuthenticationRequired noMessage>
                <HealthCheckCard />
            </AuthenticationRequired>
        </nav>
    );
}

export default Sidebar;
