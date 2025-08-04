"use client"

import {FC, ReactNode, useMemo} from "react";

import Link from "next/link";
import {usePathname} from "next/navigation";
import {Button} from "@/components/ui/button";
import { MdSpaceDashboard as DashboardIcon } from "react-icons/md";
import { FaHouseUser as StorageIcon } from "react-icons/fa";


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
                w-full shadow-none`}>
                <Link href={props.href}>
                    <span aria-hidden>
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
        <nav className="h-full w-[300px] p-3 border-r-2 border-athens-gray">

            <div
                role="navigation"
                aria-label="external links"
                className="flex flex-col gap-3">
                <ul className="list-none flex flex-col gap-2">
                    <SidebarLink href="/dashboard" icon={<DashboardIcon />}>
                        Dashboard
                    </SidebarLink>
                    <SidebarLink href="/dashboard/storage" icon={<StorageIcon />}>
                        Storage
                    </SidebarLink>
                </ul>
            </div>

        </nav>
    );
}

export default Sidebar;
