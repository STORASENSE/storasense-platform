import {FC} from "react";
import Link from "next/link";
import {Input} from "@/components/ui/input";


const TopBar: FC = () => {
    return (
        <div className="py-2 px-5 grow flex justify-between items-center">

            <div role="navigation" aria-label="search tools">
                <Input placeholder="Search..."/>
            </div>

            <div className="user links">
                <Link href="/login">
                    Login
                </Link>
            </div>

        </div>
    );
}

export default TopBar;
