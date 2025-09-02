"use client";

import { FC } from "react";
import { useSelector } from "react-redux";
import { RootState } from "@/redux/store";
import {
    useGetAlarmsByStorageIdQuery,
    useDeleteAlarmMutation
} from "@/redux/api/storaSenseApi";
import AlarmCard from "./AlarmCard";
import {Alarm} from "@/redux/api/storaSenseApiSchemas";

const AlarmOverview: FC = () => {
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage)!;

    // Alarme query
    const { data: alarmsData, refetch } = useGetAlarmsByStorageIdQuery({
        storage_id: activeStorage.id
    }, {pollingInterval: 30000}); // Polling all 30 Seconds

    const [deleteAlarm] = useDeleteAlarmMutation();

    const alarms = alarmsData || [];

    const handleDeleteAlarm = async (alarmId: string) => {
        try {
            await deleteAlarm({ alarm_id: alarmId }).unwrap();
            refetch();
        } catch (error) {
            console.error("Failed to delete alarm:", error);
        }
    };

    return (
        <div className="space-y-6">
            <header className="flex justify-between items-center">
                <AlarmStats alarms={alarms} />
            </header>

            <main className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {alarms.map((alarm: Alarm) => (
                    <AlarmCard
                        key={alarm.id}
                        alarm={alarm}
                        onDelete={handleDeleteAlarm}
                    />
                ))}
            </main>

            {alarms.length === 0 && (
                <section className="text-center py-12">
                    <p className="text-gray-500 mb-4">
                        There seems to be no alarms in the storage.
                    </p>
                </section>
            )}
        </div>
    );
};

const AlarmStats: FC<{ alarms: any[] }> = ({ alarms }) => (
    <div className="flex items-center gap-4">
        <div className="text-sm text-gray-600">
            {alarms.length} Alarm(s)
        </div>
    </div>
);

export default AlarmOverview;
