"use client"

import {FC, useState, useMemo} from "react";
import {Button} from "@/components/ui/button";
import {Plus} from "lucide-react";
import SensorCard from "./SensorCard";
import AddSensorModal from "./AddSensorModal";
import {useGetSensorsQuery, useDeleteSensorMutation, useGetSensorStatusQuery, useAddSensorMutation} from "@/redux/api/storaSenseApi";
import {Sensor} from "@/redux/api/storaSenseApiSchemas";

interface SensorsOverviewProps {
    storageId: string;
    userId: string;
}

// Custom hook to enrich sensor data with status
const useSensorWithStatus = (sensor: Sensor) => {
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
    const [viewMode, setViewMode] = useState<"storage" | "user">("storage");

    // Query for Storage-Sensors
    const { data: storageSensorsData, refetch: refetchStorage } = useGetSensorsQuery(
        { storage_id: storageId },
        { skip: viewMode !== "storage" }
    );
    // Add mutation
    const [addSensor] = useAddSensorMutation();
    // Delete mutation
    const [deleteSensor] = useDeleteSensorMutation();

    // Get backend sensors based on view mode
    const backendSensors = viewMode === "storage"
        ? (storageSensorsData || [])
        : [];

    const handleAddSensor = async (newSensor: Sensor) => {
        try {
            await addSensor({ sensor: newSensor }).unwrap();
            refetchStorage();
        } catch {
            console.error('Failed to add sensor:');
        }
    };

    const handleDeleteSensor = async (sensorId: string) => {
        try {
            await deleteSensor({ sensor_id: sensorId }).unwrap();
            refetchStorage();
        } catch (error) {
            console.error('Failed to delete sensor:', error);
        }
    };

    return (
        <div className="space-y-6">
            {/* Header with Switch and Add Button */}
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-6">
                    {/* View Mode Switch */}
                    <div className="flex items-center gap-3 bg-gray-100 rounded-lg p-1">
                        <button
                            onClick={() => setViewMode("storage")}
                            className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                                viewMode === "storage"
                                    ? "bg-white text-gray-900 shadow-sm"
                                    : "text-gray-600 hover:text-gray-900"
                            }`}
                        >
                            Storage Sensors
                        </button>
                        <button
                            onClick={() => setViewMode("user")}
                            className={`px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                                viewMode === "user"
                                    ? "bg-white text-gray-900 shadow-sm"
                                    : "text-gray-600 hover:text-gray-900"
                            }`}
                        >
                            My Sensors
                        </button>
                    </div>

                    <SensorStats sensors={backendSensors} />
                </div>

                <Button
                    onClick={() => setIsModalOpen(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Sensor
                </Button>
            </div>

            {/* Sensor Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {backendSensors.map((sensor) => (
                    <SensorCardWithStatus
                        key={sensor.id}
                        sensor={sensor}
                        onDelete={handleDeleteSensor}
                    />
                ))}
            </div>

            {/* Empty State */}
            {backendSensors.length === 0 && (
                <div className="text-center py-12">
                    <div className="text-gray-500 mb-4">
                        {viewMode === "storage"
                            ? "No sensors found for this storage."
                            : "You have no sensors added yet."
                        }
                    </div>
                    <Button
                        onClick={() => setIsModalOpen(true)}
                        className="bg-blue-600 hover:bg-blue-700 text-white"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        Add first Sensor
                    </Button>
                </div>
            )}

            {/* Add Sensor Modal */}
            <AddSensorModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onAdd={() => handleAddSensor()}
            />
        </div>
    );
};

// Component for Sensor Card with Status
const SensorCardWithStatus: FC<{ sensor: Sensor; onDelete: (id: string) => void }> = ({ sensor, onDelete }) => {
    const enrichedSensor = useSensorWithStatus(sensor);
    return <SensorCard sensor={enrichedSensor} onDelete={onDelete} />;
};

// SensorStats Component to display sensor statistics
const SensorStats: FC<{ sensors: Sensor[] }> = ({ sensors }) => {
    const stats = useMemo(() => {
        const online = sensors.filter(s => s.status === "online").length;
        const warning = sensors.filter(s => s.status === "warning").length;
        const offline = sensors.filter(s => s.status === "offline").length;

        return { online, warning, offline, total: sensors.length };
    }, [sensors]);

    return (
        <div className="flex items-center gap-4">
            <div className="text-sm text-gray-600">
                {stats.total} Sensors active
            </div>
            <div className="flex gap-2">
                <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-xs text-gray-600">
                        {stats.online} Online
                    </span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                    <span className="text-xs text-gray-600">
                        {stats.warning} Warning
                    </span>
                </div>
                <div className="flex items-center gap-1">
                    <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                    <span className="text-xs text-gray-600">
                        {stats.offline} Offline
                    </span>
                </div>
            </div>
        </div>
    );
};

export default SensorsOverview;
