"use client";

import React, {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsByStorageIdQuery, useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";
import {Skeleton} from "@/components/ui/skeleton";

const humanWindow: Record<AnalyticsTimeWindow, string> = {
    "7d": "7 days",
    "30d": "30 days",
    "365d": "365 days",
};

type TopStats = { totalSensors: number; totalTypes: number; overallAvg: number };

const TopStatsSection: FC = () => {
    const timeWindow = useSelector((s: RootState) => s.analytics.timeWindow);
    const storageId = useSelector((s: RootState) => s.storage.activeStorage?.id) ?? undefined;

    const {data: sensors, isLoading: sensorsLoading} = useGetSensorsQuery(
        {storage_id: storageId as string},
        {skip: !storageId}
    );

    const {data: summary, isLoading: analyticsLoading, isError: analyticsError} =
        useGetAnalyticsByStorageIdQuery(
            {storage_id: storageId as string, window: timeWindow as AnalyticsTimeWindow},
            {skip: !storageId}
        );

    const topStats = useMemo<TopStats | undefined>(() => {
        if (!summary) return undefined;
        const totalSensors = summary.length;
        const totalTypes = new Set(summary.map(s => s.type)).size;
        const overallAvg = totalSensors
            ? summary.reduce((a, s) => a + s.avg_value, 0) / totalSensors
            : 0;
        return {totalSensors, totalTypes, overallAvg};
    }, [summary]);

    if (!storageId) return null;

    if (sensorsLoading || analyticsLoading) {
        return (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
                <Skeleton className="h-[100px]"/>
            </div>
        );
    }

    if (!sensors || sensors.length === 0) return null;
    if (analyticsError || !topStats || !summary || summary.length === 0) return null;

    return (
        <section>
            <ul className="w-full grid grid-cols-1 md:grid-cols-3 gap-4">
                <StatCard label="Total sensors" value={topStats.totalSensors}/>
                <StatCard label="Sensor types" value={topStats.totalTypes}/>
                <StatCard
                    label="Overall average"
                    value={topStats.overallAvg.toFixed(2)}
                    foot={`Window: ${humanWindow[timeWindow]}`}
                />
            </ul>
        </section>
    );
};

const StatCard: FC<{ label: string; value: string | number; foot?: string }> = ({
                                                                                    label,
                                                                                    value,
                                                                                    foot,
                                                                                }) => (
    <li>
        <article className="h-full rounded-2xl border bg-white p-4 shadow-sm">
            <header><h3 className="text-xs text-gray-500">{label}</h3></header>
            <div className="mt-1 text-2xl font-semibold">{value}</div>
            {foot && <footer className="mt-1 text-xs text-gray-400">{foot}</footer>}
        </article>
    </li>
);

export default TopStatsSection;
