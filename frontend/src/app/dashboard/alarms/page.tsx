import {FC} from "react";
import AlarmOverview from "@/components/dashboard/alarms/AlarmOverview";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";

// const Page: FC = () => {
//     return (
//         <AuthenticationRequired>
//             <header className="mb-5">
//                 <h1 className="text-3xl font-semibold text-blue-whale">
//                     Alarms
//                 </h1>
//             </header>
//             <section>
//                 <ActiveStorageRequired>
//                     <SensorsOverview />
//                 </ActiveStorageRequired> TODO add
//             </section>
//         </AuthenticationRequired>
//     );
// }

const Page: FC = () => {
    return (
        <>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Alarms
                </h1>
            </header>
            <section>
                <AlarmOverview />
            </section>
        </>
    );
}

export default Page;
