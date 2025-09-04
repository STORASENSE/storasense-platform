"use client";

import React, {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsByStorageIdQuery, useGetSensorsQuery} from "@/redux/api/storaSenseApi";
import {AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {COLORS, toNumber} from "@/components/dashboard/analytics/analyticsUtils";
import {Skeleton} from "@/components/ui/skeleton";

const SensorMinMaxChart: FC = () => {
    const timeWindow = useSelector((s: RootState) => s.analytics.timeWindow);
    const activeStorage = useSelector((s: RootState) => s.storage.activeStorage);
    const storageId = activeStorage?.id ?? undefined;

    const {data: sensors, isLoading: sensorsLoading, isError: sensorsError} = useGetSensorsQuery(
        {storage_id: storageId as string},
        {skip: !storageId}
    );

    const {data: summaryRaw, isLoading: analyticsLoading, isError: analyticsError} = useGetAnalyticsByStorageIdQuery(
        {storage_id: storageId as string, window: timeWindow as AnalyticsTimeWindow},
        {skip: !storageId}
    );

    const summary = summaryRaw ?? [];
    const barData = useMemo(
        () => summary.map(r => ({name: `${r.type}-${r.sensor_id}`, min: r.min_value, max: r.max_value})),
        [summary]
    );

    if (!storageId) return null;

    if (sensorsLoading) {
        return (
            <Card>
                <CardContent>
                    <div className="p-4"><Skeleton className="h-40 w-full"/></div>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card>
            <CardHeader>
                <CardTitle>Min/Max Per Sensor</CardTitle>
                <CardDescription>Each bar group shows min and max per sensor</CardDescription>
            </CardHeader>
            <CardContent>
                <div className="w-full h-64 mt-3">
                    {analyticsLoading ? (
                        <Skeleton className="w-full h-[250px]"/>
                    ) : (
                        <ResponsiveContainer>
                            <BarChart data={barData}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="name" hide/>
                                <YAxis/>
                                <Tooltip
                                    formatter={(value: number | string, name: string): [string | number, string] => [toNumber(value).toFixed(2), name]}
                                    contentStyle={{borderRadius: 12}}
                                />
                                <Legend/>
                                <Bar dataKey="min" name="Min" barSize={14} fill={COLORS.min} radius={[6, 6, 0, 0]}/>
                                <Bar dataKey="max" name="Max" barSize={14} fill={COLORS.max} radius={[6, 6, 0, 0]}/>
                            </BarChart>
                        </ResponsiveContainer>
                    )}
                </div>
            </CardContent>
        </Card>
    );
};

export default SensorMinMaxChart;
