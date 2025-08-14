"use client"

import {FC, useState} from "react";
import {Button} from "@/components/ui/button";
import {Plus} from "lucide-react";
import SensorCard from "./SensorCard";
import AddSensorModal from "./AddSensorModal";

interface Sensor {
    id: string;
    name: string;
    type: "ULTRASONIC" | "TEMPERATURE" | "HUMIDITY" | "MOTION" | "LIGHT";
    storage_id: string;
    allowed_min: number;
    allowed_max: number;
    status?: "online" | "offline" | "warning";
    value?: string;
    unit?: string;
    location?: string;
    lastUpdate?: string;
}

const mockSensors: Sensor[] = [
    {
        id: "1",
        name: "Ultrasonic Sensor 1",
        type: "ULTRASONIC",
        storage_id: "storage-1",
        allowed_min: 0,
        allowed_max: 100,
        status: "online",
        value: "50",
        unit: "cm",
        location: "Warehouse A",
        lastUpdate: "2023-10-01T12:00:00Z"
    },
    {
        id: "2",
        name: "Temperature Sensor Inside",
        type: "TEMPERATURE",
        storage_id: "storage-2",
        allowed_min: -20,
        allowed_max: 50,
        status: "warning",
        value: "25",
        unit: "°C",
        location: "Office Room 1",
        lastUpdate: "2023-10-01T12:05:00Z"
    },
    {
        id: "3",
        name: "Humidity Sensor Outside",
        type: "HUMIDITY",
        storage_id: "storage-3",
        allowed_min: 0,
        allowed_max: 100,
        status: "offline",
        value: "2",
        unit: "%",
        location: "Garden Area",
        lastUpdate: "2"
    }
];

const SensorsOverview: FC = () => {
    const [sensors, setSensors] = useState<Sensor[]>(mockSensors);
    const [isModalOpen, setIsModalOpen] = useState(false);

    const handleAddSensor = (newSensor: Omit<Sensor, "id">) => {
        const sensor: Sensor = {
            ...newSensor,
            id: crypto.randomUUID()
        };
        setSensors(prev => [...prev, sensor]);
    };

    return (
        <div className="space-y-6">
            {/* Header mit Add Button */}
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <div className="text-sm text-gray-600">
                        {sensors.length} Sensors active
                    </div>
                    <div className="flex gap-2">
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                            <span className="text-xs text-gray-600">
                                {sensors.filter(s => s.status === "online").length} Online
                            </span>
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                            <span className="text-xs text-gray-600">
                                {sensors.filter(s => s.status === "warning").length} Warning
                            </span>
                        </div>
                        <div className="flex items-center gap-1">
                            <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                            <span className="text-xs text-gray-600">
                                {sensors.filter(s => s.status === "offline").length} Offline
                            </span>
                        </div>
                    </div>
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
                {sensors.map((sensor) => (
                    <SensorCard key={sensor.id} sensor={sensor} />
                ))}
            </div>

            {/* Add Sensor Modal */}
            <AddSensorModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                onAdd={handleAddSensor}
            />
        </div>
    );
};

export default SensorsOverview;
