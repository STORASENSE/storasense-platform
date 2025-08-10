"use client"

import {FC, useEffect, useState} from "react";
import {Sensor, SensorType} from "@/redux/api/storaSenseApiSchemas";
import SensorTelemetryCard from "@/components/dashboard/telemetry/SensorTelemetryCard";
import SensorTelemetryChart from "@/components/dashboard/telemetry/SensorTelemetryChart";
import {useGetMeasurementsQuery} from "@/redux/api/storaSenseApi";
import {Skeleton} from "@/components/ui/skeleton";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import {AlertCircleIcon} from "lucide-react";


interface SensorTelemetryFactoryProps {
    sensor: Sensor;
}

const SensorTelemetryFactory: FC<SensorTelemetryFactoryProps> = ({ sensor }) => {
    const [maxDate, setMaxDate] = useState<Date>(new Date());

    useEffect(() => {
        const counter = setTimeout(() => {
            const now = new Date();
            now.setMinutes(now.getMinutes() - 30);
            setMaxDate(now);
        }, 30000);

        return () => {
            clearTimeout(counter);
        }
    }, []);

    const {data, isLoading, isError} = useGetMeasurementsQuery({
        sensor_id: sensor.id,
        max_date: maxDate.toISOString()
    });

    if (isLoading) {
        return (
            <>
                <Skeleton className="mt-2 mb-3 w-full h-[100px]"/>
                <Skeleton className="mb-3 w-full h-[40px]"/>
                <Skeleton className="w-full h-[40px]"/>
            </>
        );
    }

    if (isError) {
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <AlertCircleIcon />
                <AlertTitle>
                    Error while fetching temperature data.
                </AlertTitle>
                <AlertDescription>
                    An error occurred while contacting the server.
                </AlertDescription>
            </Alert>
        );
    }

    switch (sensor.type) {
        case SensorType.TEMPERATURE_INSIDE:
            return (
                <SensorTelemetryCard
                    sensor={sensor}
                    title="Temperature"
                    description={
                        <>
                            The temperature inside the storage. Should be between {sensor.allowed_min}°C
                            and {sensor.allowed_max}°C.
                        </>
                    }>
                    <SensorTelemetryChart
                        id={`tempInside-${sensor.id}`}
                        data={data!.measurements}
                        valueName="Temperature"
                        valueUnit="°C"
                    />
                </SensorTelemetryCard>
            );
        case SensorType.TEMPERATURE_OUTSIDE:
            return (
                <SensorTelemetryCard
                    sensor={sensor}
                    title="External Temperature"
                    description={
                        <>
                            The temperature outside the storage. Should be between {sensor.allowed_min}°C
                            and {sensor.allowed_max}°C.
                        </>
                    }>
                    <SensorTelemetryChart
                        id={`tempOutside-${sensor.id}`}
                        data={data!.measurements}
                        valueName="Temperature"
                        valueUnit="°C"
                    />
                </SensorTelemetryCard>
            );
        case SensorType.HUMIDITY:
            return (
                <SensorTelemetryCard
                    sensor={sensor}
                    title="Humidity"
                    description={
                        <>
                            The humidity inside the storage. Should be between {sensor.allowed_min}%
                            and {sensor.allowed_max}%.
                        </>
                    }>
                    <SensorTelemetryChart
                        id={`tempInside-${sensor.id}`}
                        data={data!.measurements}
                        valueName="Humidity"
                        valueUnit="%"
                    />
                </SensorTelemetryCard>
            );
        case SensorType.GAS:
            return (
                <SensorTelemetryCard
                    sensor={sensor}
                    title="Apparent Diffusion Coefficient"
                    description={
                        <>
                            How freely water molecules can move inside the storage. High values may
                            indicate spoilage. Should be between {sensor.allowed_min}mm<sup>2</sup>/s
                            and {sensor.allowed_max}mm<sup>2</sup>/s.
                        </>
                    }>
                    <SensorTelemetryChart
                        id={`tempInside-${sensor.id}`}
                        data={data!.measurements}
                        valueUnit={"mm\u00B2/s"}
                    />
                </SensorTelemetryCard>
            );
        case SensorType.ULTRASONIC:
            return (
                <SensorTelemetryCard
                    sensor={sensor}
                    title="Door Status"
                    description={
                        <>
                            Whether the storage's door is open.
                        </>
                    }>
                    <SensorTelemetryChart
                        id={`tempInside-${sensor.id}`}
                        data={data!.measurements}
                        valueUnit="%"
                    />
                </SensorTelemetryCard>
            );
    }
}

export default SensorTelemetryFactory;
