"use client";

import React, {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsByStorageIdQuery, useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {Skeleton} from "@/components/ui/skeleton";
import {aggregateAnalyticsSummary, humanWindow, KbpiAggregation} from "@/components/dashboard/analytics/analyticsUtils";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";

const KpiByTypeSection: FC = () => {
    const timeWindow = useSelector((s: RootState) => s.analytics.timeWindow);
    const activeStorage = useSelector((s: RootState) => s.storage.activeStorage);
    const storageId = activeStorage?.id ?? undefined;

    // Hooks ALWAYS at top; use skip to disable
    const {data: sensors, isLoading: sensorsLoading, isError: sensorsError} = useGetSensorsQuery(
        {storage_id: storageId as string},
        {skip: !storageId}
    );

    const {data: summaryRaw, isLoading: analyticsLoading, isError: analyticsError} = useGetAnalyticsByStorageIdQuery(
        {storage_id: storageId as string, window: timeWindow as AnalyticsTimeWindow},
        {skip: !storageId}
    );

    const summary = summaryRaw ?? [];
    const kpisByType = useMemo<KbpiAggregation[]>(() => aggregateAnalyticsSummary(summary), [summary]);

    if (!storageId) return null;

    if (sensorsLoading) return <Skeleton className="h-56 w-full"/>;

    return (
        <Card>
            <CardHeader>
                <CardTitle>KPIs by type</CardTitle>
                <CardDescription>Aggregated over {humanWindow[timeWindow]}</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4">
                    {analyticsLoading ? (
                        <>
                            <Skeleton className="h-[100px]"/>
                            <Skeleton className="h-[100px]"/>
                            <Skeleton className="h-[100px]"/>
                        </>
                    ) : kpisByType.length === 0 ? (
                        <div className="text-sm text-gray-500">No data in the last {humanWindow[timeWindow]}.</div>
                    ) : (
                        kpisByType.map(k => (
                            <div key={k.type} className="rounded-xl border p-4">
                                <div className="text-sm text-gray-500">{k.type}</div>
                                <div className="mt-2 grid grid-cols-3 gap-2 text-center">
                                    <div>
                                        <div className="text-xs text-gray-500">Avg</div>
                                        <div className="text-lg font-semibold">{k.avg.toFixed(2)}</div>
                                    </div>
                                    <div>
                                        <div className="text-xs text-gray-500">Min</div>
                                        <div className="text-lg font-semibold">{k.min.toFixed(2)}</div>
                                    </div>
                                    <div>
                                        <div className="text-xs text-gray-500">Max</div>
                                        <div className="text-lg font-semibold">{k.max.toFixed(2)}</div>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </CardContent>
        </Card>
    );
};

export default KpiByTypeSection;
