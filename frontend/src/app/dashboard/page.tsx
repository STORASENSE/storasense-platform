import {FC} from "react";
import {Card, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";

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
                    </CardHeader>
                </Card>
            </section>
        </>
    );
}

export default Page;
