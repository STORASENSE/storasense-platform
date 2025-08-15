import {FC} from "react";
import ProtectedPage from "@/components/ProtectedPage";


const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Users
                </h1>
                <p>
                    Below is al list of all users that have access to the active storage.
                </p>
            </header>
            <section>

            </section>
        </ProtectedPage>
    );
}

export default Page;
