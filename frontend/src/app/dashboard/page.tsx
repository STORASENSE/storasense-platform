import {FC} from "react";
import DashboardOverview from "@/components/dashboard/DashboardOverview";

const Page: FC = () => {
    return (
        <>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Dashboard
                </h1>
            </header>
            <section>
                <DashboardOverview />
            </section>
        </>
    );
}

export default Page;
