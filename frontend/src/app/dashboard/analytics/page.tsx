import {FC} from "react";
import DashboardOverview from "@/components/dashboard/DashboardOverview";
import ProtectedPage from "@/components/ProtectedPage";

const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Analytics
                </h1>
            </header>
            <section>
            </section>
        </ProtectedPage>
    );
}

export default Page;
