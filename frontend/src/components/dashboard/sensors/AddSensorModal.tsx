"use client"

import {FC, useState} from "react";
import {Button} from "@/components/ui/button";
import {Input} from "@/components/ui/input";
import {X} from "lucide-react";

interface AddSensorModalProps {
    isOpen: boolean;
    onClose: () => void;
    onAdd: (sensor: {
        id: string;
        name: string;
        type: "ULTRASONIC" | "TEMPERATURE-INSIDE" | "TEMPERATURE-OUTSIDE" | "HUMIDITY" | "GAS";
        storage_id: string;
        allowed_min: number;
        allowed_max: number;
        status?: "online" | "offline" | "warning";
        unit?: string;
        location?: string;
        lastUpdate?: string;
    }) => void;
}

const AddSensorModal: FC<AddSensorModalProps> = ({ isOpen, onClose, onAdd }) => {
    const [formData, setFormData] = useState({
        id: "",
        name: "",
        type: "" as "ULTRASONIC" | "TEMPERATURE-INSIDE" | "TEMPERATURE-OUTSIDE" | "HUMIDITY" | "GAS" | "",
        storage_id: "",
        allowed_min: 0,
        allowed_max: 100,
        location: "",
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!formData.id || !formData.name || !formData.type || !formData.storage_id) return;

        const newSensor = {
            id: formData.id,
            name: formData.name,
            type: formData.type as "ULTRASONIC" | "TEMPERATURE-INSIDE" | "TEMPERATURE-OUTSIDE" | "HUMIDITY" | "GAS",
            storage_id: formData.storage_id,
            allowed_min: formData.allowed_min,
            allowed_max: formData.allowed_max,
            status: "online" as const,
            unit: getUnitForType(formData.type),
            location: formData.location,
            lastUpdate: "recently added"
        };

        onAdd(newSensor);
        setFormData({
            id: "",
            name: "",
            type: "",
            storage_id: "",
            allowed_min: 0,
            allowed_max: 100,
            location: ""
        });
        onClose();
    };

    const getUnitForType = (type: string) => {
        switch (type) {
            case "ULTRASONIC": return "cm";
            case "TEMPERATURE-INSIDE": return "°C";
            case "TEMPERATURE-OUTSIDE": return "°C";
            case "HUMIDITY": return "%";
            case "GAS": return "ppm";
            default: return "";
        }
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/50"
                onClick={onClose}
            />

            {/* Modal */}
            <div className="relative bg-white rounded-lg shadow-lg w-full max-w-md p-6">
                {/* Header */}
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-lg font-semibold text-gray-900">
                        Neuen Sensor hinzufügen
                    </h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="space-y-2">
                        <label htmlFor="id" className="block text-sm font-medium text-gray-700">
                            Sensor ID
                        </label>
                        <Input
                            id="id"
                            value={formData.id}
                            onChange={(e) => setFormData(prev => ({ ...prev, id: e.target.value }))}
                            placeholder="z.B. ad5b8443-aef7-39a8-a530-75282ecb075f"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                            Sensor Name
                        </label>
                        <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                            placeholder="z.B. Ultrasonic Sensor A"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label htmlFor="type" className="block text-sm font-medium text-gray-700">
                            Sensor Typ
                        </label>
                        <select
                            id="type"
                            value={formData.type}
                            onChange={(e) => setFormData(prev => ({ ...prev, type: e.target.value as any }))}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                            required
                        >
                            <option value="">Select Sensor Type</option>
                            <option value="ULTRASONIC">Ultrasonic</option>
                            <option value="TEMPERATURE_INSIDE">Temperature (Inside)</option>
                            <option value="TEMPERATURE_OUTSIDE">Temperature (Outside)</option>
                            <option value="HUMIDITY">Humidity</option>
                            <option value="GAS">Gas</option>
                        </select>
                    </div>

                    <div className="space-y-2">
                        <label htmlFor="storage_id" className="block text-sm font-medium text-gray-700">
                            Storage ID
                        </label>
                        <Input
                            id="storage_id"
                            value={formData.storage_id}
                            onChange={(e) => setFormData(prev => ({ ...prev, storage_id: e.target.value }))}
                            placeholder="e.g. storage-1"
                            required
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label htmlFor="min" className="block text-sm font-medium text-gray-700">
                                Min. Wert
                            </label>
                            <Input
                                id="min"
                                type="number"
                                step="0.1"
                                value={formData.allowed_min}
                                onChange={(e) => setFormData(prev => ({ ...prev, allowed_min: parseFloat(e.target.value) }))}
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <label htmlFor="max" className="block text-sm font-medium text-gray-700">
                                Max. Wert
                            </label>
                            <Input
                                id="max"
                                type="number"
                                step="0.1"
                                value={formData.allowed_max}
                                onChange={(e) => setFormData(prev => ({ ...prev, allowed_max: parseFloat(e.target.value) }))}
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                            Standort (optional)
                        </label>
                        <Input
                            id="location"
                            value={formData.location}
                            onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                            placeholder="z.B. Lager A - Regal 1"
                        />
                    </div>

                    <div className="flex gap-3 pt-4">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={onClose}
                            className="flex-1"
                        >
                            Abbrechen
                        </Button>
                        <Button
                            type="submit"
                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            Add Sensor
                        </Button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default AddSensorModal;
