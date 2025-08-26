import {FC} from "react";
import {Card, CardContent, CardHeader} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {FaBell as Bell, FaTrash as TrashIcon, FaClock as Clock, FaMapPin as MapPin} from "react-icons/fa6";

interface Alarm {
    id: string;
    message?: string;
    sensor_id: string;
    created_at: Date;
}

interface AlarmCardProps {
    alarm: Alarm,
    sensorName?: string,
    onDelete?: (alarmId: string) => void,
    key?: unknown
}

const AlarmCard: FC<AlarmCardProps> = ({alarm, sensorName, onDelete, key}) => {
    const handleDelete = () => {
        if (onDelete && window.confirm("Do you really want to delete the alarm?")) {
            onDelete(alarm.id);
        }
    };

    return (
        <Card className="hover:shadow-lg transition-shadow duration-200 border-l-4 border-blue-whale">
            <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-red-100 rounded-lg text-red-600">
                            <Bell className="w-5 h-5"/>
                        </div>
                        <div>
                            <h3 className="font-semibold text-gray-900 text-sm leading-tight">
                                {alarm.message || "No Alarm-Message"}
                            </h3>
                            <div className="flex items-center gap-1 mt-1">
                                <MapPin className="w-3 h-3 text-gray-400"/>
                                <span className="text-xs text-gray-500">
                                    Sensor: {sensorName || alarm.sensor_id}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
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
