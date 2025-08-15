"use client";
import * as React from "react";
import { FC, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { X } from "lucide-react";
import { AddSensorRequest, SensorType } from "@/redux/api/storaSenseApiSchemas";
import { useAddSensorMutation } from "@/redux/api/storaSenseApi";

interface FormData {
  id: string;
  name: string;
  type: SensorType;
  storage_id: string;
  allowed_min: number;
  allowed_max: number;
}

const SENSOR_TYPE_OPTIONS = [
  { value: "ULTRASONIC", label: "Ultrasonic" },
  { value: "TEMPERATURE_INSIDE", label: "Temperature (Inside)" },
  { value: "TEMPERATURE_OUTSIDE", label: "Temperature (Outside)" },
  { value: "HUMIDITY", label: "Humidity" },
  { value: "GAS", label: "Gas" },
] as const;

function mapFormDataToAddSensorRequest(formData: FormData): AddSensorRequest {
  return {
    sensor_id: formData.id,
    sensor: {
      name: formData.name,
      type: formData.type,
      storage_id: formData.storage_id,
      allowed_min: formData.allowed_min,
      allowed_max: formData.allowed_max,
    },
  };
}

interface AddSensorModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const AddSensorModal: FC<AddSensorModalProps> = ({ isOpen, onClose }) => {
  const [addSensor] = useAddSensorMutation();
  const [formData, setFormData] = useState<Partial<FormData>>({
    allowed_min: 0,
    allowed_max: 100,
  });
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const isFormValid = (data: Partial<FormData>): data is FormData => {
    return !!(
      data.id &&
      data.name &&
      data.type &&
      data.storage_id &&
      data.allowed_min !== undefined &&
      data.allowed_max !== undefined
    );
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!isFormValid(formData)) {
      setErrorMessage("Bitte füllen Sie alle Pflichtfelder aus.");
      return;
    }

    const request = mapFormDataToAddSensorRequest(formData);

    addSensor(request)
      .unwrap()
      .then(() => {
        onClose();
        setFormData({ allowed_min: 0, allowed_max: 100 });
      })
      .catch((error) => {
        console.error("Failed to add sensor:", error);

        // If Backend returns a specific error message
        if (error?.data?.detail) {
          setErrorMessage(
            typeof error.data.detail === "string"
              ? error.data.detail
              : JSON.stringify(error.data.detail)
          );
        } else {
          setErrorMessage("An error occurred when trying to add the new sensor.");
        }
      });
  };

  const handleInputChange =
    (field: keyof FormData) =>
    (
      e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
    ) => {
      const value =
        e.target.type === "number"
          ? parseFloat(e.target.value)
          : e.target.value;
      setFormData((prev) => ({ ...prev, [field]: value }));
    };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />

      <div className="relative bg-white rounded-lg shadow-lg w-full max-w-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">
            Add New Sensor
          </h2>
          <button
            type="button"
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {errorMessage && (
            <div className="p-3 text-sm text-red-700 bg-red-100 rounded-md">
              {errorMessage}
            </div>
          )}

          <div className="space-y-2">
            <label htmlFor="id" className="block text-sm font-medium text-gray-700">
              Sensor ID
            </label>
            <Input
              id="id"
              value={formData.id || ""}
              onChange={handleInputChange("id")}
              placeholder="e.g. ad5b8443-aef7-39a8-a530-75282ecb075f"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="name" className="block text-sm font-medium text-gray-700">
              Sensor Name
            </label>
            <Input
              id="name"
              value={formData.name || ""}
              onChange={handleInputChange("name")}
              placeholder="e.g. Ultrasonic Sensor A"
              required
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="type" className="block text-sm font-medium text-gray-700">
              Sensor Type
            </label>
            <select
              id="type"
              value={formData.type || ""}
              onChange={handleInputChange("type")}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            >
              <option value="">Select Sensor Type</option>
              {SENSOR_TYPE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label htmlFor="storage_id" className="block text-sm font-medium text-gray-700">
              Storage ID
            </label>
            <Input
              id="storage_id"
              value={formData.storage_id || ""}
              onChange={handleInputChange("storage_id")}
              placeholder="e.g. a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label htmlFor="min" className="block text-sm font-medium text-gray-700">
                Min. Value
              </label>
              <Input
                id="min"
                type="number"
                step="0.1"
                value={formData.allowed_min ?? ""}
                onChange={handleInputChange("allowed_min")}
                required
              />
            </div>
            <div className="space-y-2">
              <label htmlFor="max" className="block text-sm font-medium text-gray-700">
                Max. Value
              </label>
              <Input
                id="max"
                type="number"
                step="0.1"
                value={formData.allowed_max ?? ""}
                onChange={handleInputChange("allowed_max")}
                required
              />
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <Button type="button" variant="outline" onClick={onClose} className="flex-1">
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
              disabled={!isFormValid(formData)}
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
