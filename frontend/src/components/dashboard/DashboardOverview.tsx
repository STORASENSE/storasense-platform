"use client"

import {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {Sensor, SensorType} from "@/redux/api/storaSenseApiSchemas";
import {Skeleton} from "@/components/ui/skeleton";
import SensorTelemetryFactory from "@/components/dashboard/telemetry/SensorTelemetryFactory";


const MONITORING_ORDER: Record<SensorType, number> = {
    TEMPERATURE_INSIDE: 1,
    TEMPERATURE_OUTSIDE: 2,
    HUMIDITY: 3,
    GAS: 4,
    ULTRASONIC: 5,
}

/////////////////////////////////////////////////////////////////////////////////////////

interface StorageMonitoringProps {
    storageId: string;
}

const StorageMonitoring: FC<StorageMonitoringProps> = ({ storageId }) => {
    const {data, isLoading, isError} = useGetSensorsQuery({
        storage_id: storageId,
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

    if (isLoading) {
        return (
            <Skeleton className="w-full h-[200px]"/>
        );
    }

    if (isError) {
        return <>Error!</>
    }

    console.log(data)

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

/////////////////////////////////////////////////////////////////////////////////////////

const SensorsOverview: FC = () => {
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);

    if (!activeStorage) {
        return <></>;
    }

    return (
        <StorageMonitoring storageId={activeStorage.id} />
    );
}

export default SensorsOverview;
