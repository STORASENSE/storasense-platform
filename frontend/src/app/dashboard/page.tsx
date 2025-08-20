import {FC} from "react";
import DashboardOverview from "@/components/dashboard/DashboardOverview";
import ProtectedPage from "@/components/ProtectedPage";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";

const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Dashboard
                </h1>
            </header>
            <section>
                <ActiveStorageRequired>
                    <DashboardOverview />
                </ActiveStorageRequired>
            </section>
        </ProtectedPage>
    );
}

export default Page;
