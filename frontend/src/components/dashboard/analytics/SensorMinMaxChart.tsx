"use client"

import React, {FC, useMemo} from "react";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsSummaryQuery} from "@/redux/api/storaSenseApi";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {COLORS, toNumber} from "@/components/dashboard/analytics/analyticsUtils";
import {Skeleton} from "@/components/ui/skeleton";


const SensorMinMaxChart: FC = () => {
    const timeWindow = useSelector((state: RootState) => state.analytics.timeWindow);

    const {data: summary, isLoading, isError} = useGetAnalyticsSummaryQuery({
        window: timeWindow
    });

    const barData = useMemo(() => {
        if (!summary) {
            return undefined;
        }
        return summary.map(r =>({
            name: `${r.type}-${r.sensor_id}`,
            min: r.min_value,
            max: r.max_value
        }))
    }, [summary]);

    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    Min/Max Per Sensor
                </CardTitle>
                <CardDescription>
                    Each bar group shows min and max per sensor
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="w-full h-64 mt-3">
                    {
                        isLoading ? (
                            <Skeleton className="w-full h-[250px]" />
                        ) : isError ? (
                            <></>
                        ) : (
                            <ResponsiveContainer>
                                <BarChart data={barData}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis dataKey="name" hide />
                                    <YAxis />
                                    <Tooltip
                                        formatter={(value: number | string, name: string): [string | number, string] => [toNumber(value).toFixed(2), name]}
                                        contentStyle={{ borderRadius: 12 }}
                                    />
                                    <Legend />
                                    <Bar dataKey="min" name="Min" barSize={14} fill={COLORS.min} radius={[6, 6, 0, 0]} />
                                    <Bar dataKey="max" name="Max" barSize={14} fill={COLORS.max} radius={[6, 6, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        )
                    }
                </div>
            </CardContent>
        </Card>
    );
}

export default SensorMinMaxChart;
