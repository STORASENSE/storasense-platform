import {FC} from "react";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";
import UsersTable from "@/components/dashboard/users/UsersTable";


const Page: FC = () => {
    return (
        <AuthenticationRequired>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale mb-4">
                    Users
                </h1>
            </header>
            <ActiveStorageRequired>
                <UsersTable />
            </ActiveStorageRequired>
        </AuthenticationRequired>
    );
}

export default Page;
