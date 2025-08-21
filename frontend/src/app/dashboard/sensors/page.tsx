import {FC} from "react";
import SensorsOverview from "@/components/dashboard/sensors/SensorsOverview";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";

const Page: FC = () => {
    return (
        <AuthenticationRequired>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Sensors
                </h1>
            </header>
            <section>
                <ActiveStorageRequired>
                    <SensorsOverview />
                </ActiveStorageRequired>
            </section>
        </AuthenticationRequired>
    );
}

export default Page;
