import {FC, ReactNode} from "react";
import {Sensor} from "@/redux/api/storaSenseApiSchemas";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";


interface SensorTelemetryCardProps {
    sensor: Sensor;
    title: string;
    description?: ReactNode;
    children?: ReactNode;
}

const SensorTelemetryCard: FC<SensorTelemetryCardProps> = (props) => {
    return (
        <Card>
            <CardHeader>
                <CardTitle className="text-blue-whale">
                    {props.title}
                </CardTitle>
                <CardDescription>
                    {props.description}
                </CardDescription>
                <CardContent>
                    {props.children}
                </CardContent>
            </CardHeader>
        </Card>
    );
}

export default SensorTelemetryCard;
