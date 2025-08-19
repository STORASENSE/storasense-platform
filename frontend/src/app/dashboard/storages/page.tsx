import {FC} from "react";
import ProtectedPage from "@/components/ProtectedPage";
import StorageOverview from "@/components/dashboard/storages/StorageOverview";


const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale mb-4">
                    Storages
                </h1>
                 <p className="text-gray-500 mb-4">
                        In order to view data about your storage in the dashboard, activate it by selecting it.
                        <br />
                        Only one storage can be active at a time.
                 </p>
            </header>
            <section>
                <StorageOverview />
            </section>
        </ProtectedPage>
    );
}

export default Page;
