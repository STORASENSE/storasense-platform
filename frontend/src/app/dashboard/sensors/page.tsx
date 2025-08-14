import {FC} from "react";
import SensorsOverview from "@/components/dashboard/sensors/SensorsOverview";
import ProtectedPage from "@/components/ProtectedPage";

const Page: FC = () => {
    return (
        <ProtectedPage>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Sensors
                </h1>
            </header>
            <section>
                <SensorsOverview storageId={""} userId={""} />
            </section>
        </ProtectedPage>
    );
}

export default Page;

// const Page: FC = () => {
//     return (
//         <>
//             <header className="mb-5">
//                 <h1 className="text-3xl font-semibold text-blue-whale">
//                     Sensors
//                 </h1>
//             </header>
//             <section>
//                 <SensorsOverview/>
//             </section>
//         </>
// );
// }

//export default Page;
