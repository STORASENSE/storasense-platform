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

            </header>
            {/*<section>*/}
            {/*    <StorageCreationForm />*/}
            {/*</section>*/}
        </ProtectedPage>
    );
}

export default Page;
