import {FC} from "react";
import {Card, CardContent, CardHeader} from "@/components/ui/card";
import {Waves, Thermometer, Droplets, Eye, Sun, MapPin, Clock, Settings} from "lucide-react";

interface Sensor {
    id: string;
    name: string;
    type: "ULTRASONIC" | "TEMPERATURE_INSIDE" | "TEMPERATURE_OUTSIDE" | "GAS" | "HUMIDITY";
    storage_id: string;
    allowed_min: number;
    allowed_max: number;
    status?: "online" | "offline" | "warning";
    value?: string;
    unit?: string;
    location?: string;
    lastUpdate?: string;
}

interface SensorCardProps {
    sensor: Sensor;
}

const SensorCard: FC<SensorCardProps> = ({ sensor }) => {
    const getIcon = () => {
        switch (sensor.type) {
            case "ULTRASONIC": return <Waves className="w-5 h-5" />;
            case "TEMPERATURE_INSIDE": return <Thermometer className="w-5 h-5" />;
            case "TEMPERATURE_OUTSIDE": return <Thermometer className="w-5 h-5" />;
            case "HUMIDITY": return <Droplets className="w-5 h-5" />;
            case "GAS": return <Eye className="w-5 h-5" />;
            default: return <Settings className="w-5 h-5" />;
        }
    };

    const getStatusColor = () => {
        switch (sensor.status) {
            case "online": return "bg-green-100 text-green-800 border-green-200";
            case "warning": return "bg-yellow-100 text-yellow-800 border-yellow-200";
            case "offline": return "bg-red-100 text-red-800 border-red-200";
            default: return "bg-gray-100 text-gray-800 border-gray-200";
        }
    };

    const getTypeDisplayName = (type: string) => {
        switch (type) {
            case "ULTRASONIC": return "Ultrasonic";
            case "TEMPERATURE_INSIDE": return "Temperature (Inside)";
            case "TEMPERATURE_OUTSIDE": return "Temperature (Outside)";
            case "HUMIDITY": return "Humidity";
            case "GAS": return "Gas";
            default: return type;
        }
    };

    return (
        <Card className="hover:shadow-lg transition-shadow duration-200 border-l-4 border-l-blue-500">
            <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
                            {getIcon()}
                        </div>
                        <div>
                            <h3 className="font-semibold text-gray-900 text-sm leading-tight">
                                {sensor.name}
                            </h3>
                            <div className="flex items-center gap-1 mt-1">
                                <MapPin className="w-3 h-3 text-gray-400" />
                                <span className="text-xs text-gray-500">
                                    {sensor.location || `Storage: ${sensor.storage_id}`}
                                </span>
                            </div>
                            <div className="text-xs text-gray-500 mt-1">
                                {getTypeDisplayName(sensor.type)}
                            </div>
                        </div>
                    </div>
                    <div className={`text-xs px-2 py-1 rounded-full ${getStatusColor()}`}>
                        {sensor.status || "unknown"}
                    </div>
                </div>
            </CardHeader>
            <CardContent className="pt-0">
                <div className="space-y-3">
                    {/* Messwert */}
                    <div className="bg-gray-50 rounded-lg p-3">
                        <div className="text-2xl font-bold text-gray-900">
                            {sensor.value || "N/A"}{sensor.unit || ""}
                        </div>
                        <div className="text-xs text-gray-500 uppercase tracking-wide">
                            Last value
                        </div>
                    </div>

                    {/* Grenzwerte */}
                    <div className="bg-blue-50 rounded-lg p-3">
                        <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Min:</span>
                            <span className="font-medium">{sensor.allowed_min}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Max:</span>
                            <span className="font-medium">{sensor.allowed_max}</span>
                        </div>
                    </div>

                    {/* Zusatzinfo */}
                    <div className="flex items-center justify-between text-xs text-gray-500">
                        <div className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            <span>{sensor.lastUpdate || "Unknown"}</span>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};

export default SensorCard;
