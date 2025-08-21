import {FC} from "react";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";


const Page: FC = () => {
    return (
        <AuthenticationRequired>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale mb-4">
                    Users
                </h1>
            </header>
            <section>

            </section>
        </AuthenticationRequired>
    );
}

export default Page;
