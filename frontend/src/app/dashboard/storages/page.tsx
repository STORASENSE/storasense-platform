import {FC} from "react";
import ProtectedPage from "@/components/ProtectedPage";
import StorageOverview from "@/components/dashboard/storages/StorageOverview";
// import Link from "next/link";
// import { FaCartShopping as ShoppingIcon } from "react-icons/fa6";
// import StorageCreationForm from "@/components/dashboard/storages/purchase/StorageCreationForm";


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
            {/*<section className="mt-[100px] flex flex-col items-center">*/}
            {/*    /!*<h2 className="mb-3 flex gap-2 items-center text-xl font-semibold text-blue-whale">*!/*/}
            {/*    /!*    <ShoppingIcon aria-hidden />*!/*/}
            {/*    /!*    Purchase New Storage*!/*/}
            {/*    /!*</h2>*!/*/}
            {/*    /!*<p className="max-w-[600px] text-center">*!/*/}
            {/*    /!*    You may contact us to purchase a new monitoring device, which will be mailed to you in due time.*!/*/}
            {/*    /!*    You can find the form <Link className="underline" href="/dashboard/storages/purchase">here</Link>.*!/*/}
            {/*    /!*</p>*!/*/}
            {/*</section>*/}
        </ProtectedPage>
    );
}

export default Page;
