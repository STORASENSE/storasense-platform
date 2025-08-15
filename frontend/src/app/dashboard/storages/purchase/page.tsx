import StorageCreationForm from "@/components/dashboard/storages/purchase/StorageCreationForm";
import ProtectedPage from "@/components/ProtectedPage";
import { FC } from "react";


const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Purchase New Storage
                </h1>
                <p>
                    The purchase of a new storage is merely simulated, as this is a university
                    project. Submitting the below form will not result in any charges whatsoever,
                    and will simply create a new storage for you right away. Note that because of this,
                    sensors need to be added manually.
                </p>
            </header>
            <section>
                <StorageCreationForm />
            </section>
        </ProtectedPage>
    );
}

export default Page;
