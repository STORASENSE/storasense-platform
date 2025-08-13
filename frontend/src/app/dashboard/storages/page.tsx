import {FC} from "react";
import ProtectedPage from "@/components/ProtectedPage";
import StorageOverview from "@/components/dashboard/storages/StorageOverview";

const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Storages
                </h1>
                <p>
                    In order to view data about your storage in the dashboard, activate it by clicking it.
                    Only one storage may be active at a time.
                </p>
            </header>
            <section>
                <StorageOverview />
            </section>
        </ProtectedPage>
    );
}

export default Page;
