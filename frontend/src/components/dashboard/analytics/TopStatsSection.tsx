"use client"

import React, {FC, useMemo} from "react";
import {useGetAnalyticsSummaryQuery} from "@/redux/api/storaSenseApi";
import {Skeleton} from "@/components/ui/skeleton";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";


interface StatCardProps {
    label: string;
    value: string | number;
    foot?: string;
}

const StatCard: FC<StatCardProps> = ({ label, value, foot }) => {
    return (
        <li>
            <article className="h-full rounded-2xl border bg-white p-4 shadow-sm">
                <header>
                    <h3 className="text-xs text-gray-500">
                        {label}
                    </h3>
                </header>
                <div className="mt-1 text-2xl font-semibold">
                    {value}
                </div>
                {foot && (
                    <footer className="mt-1 text-xs text-gray-400">
                        {foot}
                    </footer>
                )}
            </article>
        </li>
    );
}

///////////////////////////////////////////////////////////////////////////////////

const humanWindow: Record<AnalyticsTimeWindow, string> = {
    "7d": "7 days",
    "30d": "30 days",
    "365d": "365 days"
};

interface TopStats {
    totalSensors: number;
    totalTypes: number;
    overallAvg: number;
}


const TopStatsSection: FC = () => {
    const timeWindow = useSelector((state: RootState) => state.analytics.timeWindow);

    const {data: summary, isLoading, isError, error} = useGetAnalyticsSummaryQuery({
        window: timeWindow
    });

    const topStats = useMemo<TopStats | undefined>(() => {
        if (!summary) {
            return undefined;
        }
        const totalSensors = summary.length;
        const totalTypes = new Set(summary.map(s => s.type)).size;
        const overallAvg = totalSensors ? summary.reduce((a, s) => a + s.avg_value, 0) / totalSensors : 0;
        return { totalSensors, totalTypes, overallAvg };
    }, [summary]);

    if (isLoading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
            </div>
        );
    }

    if (isError) {
        console.error(error);
        return <></>;
    }

    return (
        <section>
            <ul className="w-full grid grid-cols-1 md:grid-cols-3 gap-4">
                <StatCard
                    label="Total sensors"
                    value={topStats!.totalSensors}
                />
                <StatCard
                    label="Sensor types"
                    value={topStats!.totalTypes}
                />
                <StatCard
                    label="Overall average"
                    value={topStats!.overallAvg.toFixed(2)}
                    foot={`Window: ${humanWindow[timeWindow]}`}
                />
            </ul>
        </section>
    );
}

export default TopStatsSection;
