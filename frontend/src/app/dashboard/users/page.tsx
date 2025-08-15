import {FC} from "react";
import ProtectedPage from "@/components/ProtectedPage";


const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale mb-4">
                    Users
                </h1>
            </header>
            <section>

            </section>
        </ProtectedPage>
    );
}

export default Page;
