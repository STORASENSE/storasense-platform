import {FC} from "react";
import AlarmOverview from "@/components/dashboard/alarms/AlarmOverview";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";

const Page: FC = () => {
    return (
        <AuthenticationRequired>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Alarms
                </h1>
            </header>
            <section>
                <ActiveStorageRequired>
                    <AlarmOverview />
                </ActiveStorageRequired>
            </section>
        </AuthenticationRequired>
    );
}

export default Page;
