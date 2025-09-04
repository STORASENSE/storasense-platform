import {FC} from "react";
import {Card, CardContent, CardHeader} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {FaBell as Bell, FaTrash as TrashIcon, FaClock as Clock, FaMapPin as MapPin, FaWarehouse as WarehouseIcon} from "react-icons/fa6";

interface Alarm {
    id: string;
    message?: string;
    sensor_id: string;
    created_at: Date | string;
    sensor_name?: string;
    storage_name?: string;
}

interface AlarmCardProps {
    alarm: Alarm,
    onDelete?: (alarmId: string) => void,
    key?: unknown
}

const AlarmCard: FC<AlarmCardProps> = ({alarm, onDelete}) => {
    const handleDelete = () => {
        if (onDelete && window.confirm("Do you really want to delete the alarm?")) {
            onDelete(alarm.id);
        }
    };

    return (
        <Card className="hover:shadow-lg transition-shadow duration-200 border-l-4 border-blue-whale bg-white">
            <CardHeader className="pb-2">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-red-100 rounded-lg text-red-600">
                            <Bell className="w-5 h-5"/>
                        </div>
                        <div>
                            <h3 className="font-semibold text-gray-900 text-base leading-tight">
                                {alarm.message || "Kein Alarm-Text"}
                            </h3>
                            <div className="flex items-center gap-2 mt-1">
                                <MapPin className="w-3 h-3 text-gray-400"/>
                                <span className="text-xs text-gray-500">
                                    Sensor: {alarm.sensor_name || alarm.sensor_id}
                                </span>
                                <WarehouseIcon className="w-3 h-3 text-gray-400 ml-2"/>
                                <span className="text-xs text-gray-500">
                                    Storage: {alarm.storage_name || "-"}
                                </span>
                            </div>
                        </div>
                    </div>
                    {onDelete && (
                        <Button
                            variant="ghost"
                            size="sm"
                            onClick={handleDelete}
                            className="text-red-500 hover:text-red-700 hover:bg-red-50 p-1 h-auto"
                        >
                            <TrashIcon className="w-4 h-4"/>
                        </Button>
                    )}
                </div>
            </CardHeader>
            <CardContent className="pt-0">
                <div className="flex items-center gap-1 text-xs text-gray-500">
                    <Clock className="w-3 h-3"/>
                    <span>{new Date(alarm.created_at).toLocaleString()}</span>
                </div>
            </CardContent>
        </Card>
    );
};

export default AlarmCard;
