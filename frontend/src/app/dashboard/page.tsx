import {FC} from "react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import TemperatureChart from "@/components/dashboard/TemperatureChart";

const Page: FC = () => {
    return (
        <>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Dashboard
                </h1>
            </header>
            <section>
                <Card>
                    <CardHeader>
                        <CardTitle className="text-blue-whale">
                            Temperature Overview
                        </CardTitle>
                        <CardDescription>
                            Last updated: 30s ago
                        </CardDescription>
                        <CardContent>
                            <TemperatureChart />
                        </CardContent>
                    </CardHeader>
                </Card>
            </section>
        </>
    );
}

export default Page;
