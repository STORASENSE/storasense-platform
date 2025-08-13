"use client"

import {FC, ReactNode, useMemo} from "react";
import Link from "next/link";
import {usePathname} from "next/navigation";
import {Button} from "@/components/ui/button";
import { MdSpaceDashboard as DashboardIcon } from "react-icons/md";
import { FaHouseUser as StorageIcon } from "react-icons/fa";
import { FaChartBar as AnalyticsIcon } from "react-icons/fa6";
import useKeycloak from "@/app/(main)/useKeycloak";

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
                w-full shadow-none text-base px-4 py-3`}>
                <Link href={props.href}>
                    <span aria-hidden className="text-xl mr-2">
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
    const { keycloak, authenticated } = useKeycloak();
    const username = authenticated ? keycloak?.idTokenParsed?.preferred_username || "[User]" : "[User]";

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
                </ul>
            </div>

            <div className="mt-auto pt-4 border-t border-athens-gray">
                <p className="text-base font-medium text-blue-whale text-left">
                    Welcome {username}
                </p>
            </div>
        </nav>
    );
}

export default Sidebar;
