"use client"

import { FC, useState, useMemo } from "react";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import SensorCard from "./SensorCard";
import AddSensorModal from "./AddSensorModal";
import {
    useGetSensorsQuery,
    useDeleteSensorMutation,
    useGetSensorStatusQuery
} from "@/redux/api/storaSenseApi";
import { Sensor } from "@/redux/api/storaSenseApiSchemas";

interface SensorsOverviewProps {
    storageId: string;
    userId: string;
}

interface EnrichedSensor extends Sensor {
    status: "online" | "offline" | "warning";
    lastUpdate?: string;
}

// Custom hook to enrich sensor data with status
const useSensorWithStatus = (sensor: Sensor): EnrichedSensor => {
    const { data: statusData } = useGetSensorStatusQuery(
        { sensor_id: sensor.id },
        {
            pollingInterval: 60000,
            skip: !sensor.id
        }
    );

    return useMemo(() => ({
        ...sensor,
        status: statusData?.is_online ? "online" : "offline" as "online" | "offline" | "warning",
        lastUpdate: statusData?.last_measurement || undefined
    }), [sensor, statusData]);
};

const SensorsOverview: FC<SensorsOverviewProps> = ({ storageId, userId }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Query for Storage-Sensors
    const { data: sensorsData, refetch } = useGetSensorsQuery({
        storage_id: storageId
    });

    // Delete mutation
    const [deleteSensor] = useDeleteSensorMutation();

    const sensors = sensorsData || [];

    const handleModalClose = () => {
        setIsModalOpen(false);
        refetch();
    };

    const handleDeleteSensor = async (sensorId: string) => {
        try {
            await deleteSensor({ sensor_id: sensorId }).unwrap();
            refetch();
        } catch (error) {
            console.error('Failed to delete sensor:', error);
        }
    };

    return (
        <div className="space-y-6">
            <header className="flex justify-between items-center">
                <SensorStats sensors={sensors} />

                <Button
                    onClick={() => setIsModalOpen(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Sensor
                </Button>
            </header>

            <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sensors.map((sensor) => (
                    <SensorCardWithStatus
                        key={sensor.id}
                        sensor={sensor}
                        onDelete={handleDeleteSensor}
                    />
                ))}
            </main>

            {sensors.length === 0 && (
                <section className="text-center py-12">
                    <p className="text-gray-500 mb-4">
                        No sensors found for this storage.
                    </p>
                    <Button
                        onClick={() => setIsModalOpen(true)}
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Add first Sensor
                    </Button>
                </section>
            )}

            <AddSensorModal
                isOpen={isModalOpen}
                onClose={handleModalClose}
            />
        </div>
    );
};

// Component for Sensor Card with Status
const SensorCardWithStatus: FC<{ sensor: Sensor; onDelete: (id: string) => void }> = ({ sensor, onDelete }) => {
    const enrichedSensor = useSensorWithStatus(sensor);
    return <SensorCard sensor={enrichedSensor} onDelete={onDelete} />;
};

// SensorStats Component
const SensorStats: FC<{ sensors: Sensor[] }> = ({ sensors }) => {
    return (
        <div className="flex items-center gap-4">
            <div className="text-sm text-gray-600">
                {sensors.length} Sensors
            </div>
        </div>
    );
};

export default SensorsOverview;
