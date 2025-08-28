"use client"

import React, {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsSummaryQuery, useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";
import {
    aggregateAnalyticsSummary,
    COLORS,
    KbpiAggregation,
    toNumber
} from "@/components/dashboard/analytics/analyticsUtils";
import {Skeleton} from "@/components/ui/skeleton";
import {Bar, BarChart, CartesianGrid, Cell, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";

const SensorAverageChart: FC = () => {
    const timeWindow = useSelector((state: RootState) => state.analytics.timeWindow);
    const activeStorage = useSelector((state: RootState) => state.storage.activeStorage);

    const {data: sensors, isLoading: sensorsLoading} = useGetSensorsQuery(
        activeStorage ? {storage_id: activeStorage.id} : ({} as any),
        {skip: !activeStorage}
    );

    const sensorId = sensors?.[0]?.id;

    const {data: summaryRaw, isLoading} = useGetAnalyticsSummaryQuery(
        {sensor_id: sensorId ?? "", window: timeWindow as AnalyticsTimeWindow},
        {skip: !sensorId}
    );

    const summary = summaryRaw ?? [];

    const kpisByType = useMemo<KbpiAggregation[]>(() => {
        return aggregateAnalyticsSummary(summary);
    }, [summary]);

    const avgByTypeData = useMemo(() => {
        return kpisByType.map(k => ({
            type: k.type,
            avg: +k.avg.toFixed(2),
            min: +k.min.toFixed(2),
            max: +k.max.toFixed(2)
        }));
    }, [kpisByType]);

    if (sensorsLoading || !sensorId) return <Skeleton className="h-40 w-full"/>;

    return (
        <Card>
            <CardHeader>
                <CardTitle>Averages By Sensor Type</CardTitle>
                <CardDescription>Horizontal bars by type</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="w-full h-64 mt-3">
                    {isLoading ? (
                        <Skeleton className="w-full h-[200px]"/>
                    ) : (
                        <ResponsiveContainer>
                            <BarChart data={avgByTypeData} layout="vertical" margin={{left: 12, right: 16}}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis type="number"/>
                                <YAxis dataKey="type" type="category" width={160}/>
                                <Tooltip
                                    formatter={(value: number | string): [string | number, string] => [toNumber(value).toFixed(2), "Avg"]}
                                    contentStyle={{borderRadius: 12}}
                                />
                                <Legend/>
                                <Bar dataKey="avg" name="Avg" barSize={16} radius={[0, 8, 8, 0]}>
                                    {avgByTypeData.map((row, i) => (
                                        <Cell key={i} fill={COLORS.byType[row.type] ?? COLORS.fallback}/>
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </CardContent>
        </Card>
    );
}

export default SensorAverageChart;
