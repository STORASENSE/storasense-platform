"use client"

import {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {Sensor, SensorType} from "@/redux/api/storaSenseApiSchemas";
import {Skeleton} from "@/components/ui/skeleton";
import SensorTelemetryFactory from "@/components/dashboard/telemetry/SensorTelemetryFactory";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { FaCircleInfo as InfoIcon } from "react-icons/fa6";


const MONITORING_ORDER: Record<SensorType, number> = {
    TEMPERATURE_INSIDE: 1,
    TEMPERATURE_OUTSIDE: 2,
    HUMIDITY: 3,
    GAS: 4,
    ULTRASONIC: 5,
}

/////////////////////////////////////////////////////////////////////////////////////////

const SensorsOverview: FC = () => {
    // never undefined because component is wrapped  in <ActiveStorageRequired>
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage)!;

    const {data, isLoading, isError, error} = useGetSensorsQuery({
        storage_id: activeStorage.id,
    });

    const sortedSensors = useMemo<Sensor[] | undefined>(() => {
        if (!data)
            return undefined;

        return data.toSorted((a, b) => {
            const orderA = MONITORING_ORDER[a.type];
            const orderB = MONITORING_ORDER[b.type];
            return orderA - orderB;
        });
    }, [data]);

    if (isError) {
        console.error('An error occurred while fetching sensors', error);
        let message = 'An unknown error occurred. Please try again later.';
        if ('status' in error) {
            switch (error.status) {
                case 401:
                    message = 'You do not have permission to view this content.';
                    break;
            }
        }
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <InfoIcon />
                <AlertTitle>
                    Error while loading sensor data.
                </AlertTitle>
                <AlertDescription>
                    {message}
                </AlertDescription>
            </Alert>
        );
    }

    if (isLoading) {
        return (
            <Skeleton className="w-full h-[200px]"/>
        );
    }

    if (sortedSensors!.length === 0) {
        return (
            <Alert className="mt-2 p-2">
                <InfoIcon />
                <AlertTitle>
                    Cannot display data.
                </AlertTitle>
                <AlertDescription>
                    There are no sensors in this storage!
                </AlertDescription>
            </Alert>
        );
    }

    return (
        <ul className="list-none flex flex-col gap-5">
            {
                sortedSensors!.map(sensor => (
                    <li key={sensor.id}>
                        <SensorTelemetryFactory sensor={sensor} />
                    </li>
                ))
            }
        </ul>
    );
}

export default SensorsOverview;
