import {FC, ReactNode} from "react";
import Sidebar from "@/components/dashboard/Sidebar";
import TopBar from "@/components/dashboard/TopBar";


const Layout: FC<{ children: ReactNode }> = ({ children }) => (
    <div className="w-screen h-screen flex flex-col">

        <nav className="w-full h-[75px] flex border-b-2 border-athens-gray">
            <div className="w-[300px] p-3 flex justify-start items-center border-r-2 border-athens-gray">
                StoraSense
            </div>
            <TopBar />
        </nav>

        <div className="w-full h-[calc(100%-75px)] flex">
            <Sidebar />
            <main className="h-full p-5 grow bg-alabaster overflow-y-auto">
                {children}
            </main>
        </div>

    </div>
);

export default Layout;
