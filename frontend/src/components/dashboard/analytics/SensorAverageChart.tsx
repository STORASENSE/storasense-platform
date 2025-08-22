"use client"

import React, {FC, useMemo} from "react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Bar, BarChart, CartesianGrid, Cell, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis} from "recharts";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsSummaryQuery} from "@/redux/api/storaSenseApi";
import {
    aggregateAnalyticsSummary,
    COLORS,
    KbpiAggregation,
    toNumber
} from "@/components/dashboard/analytics/analyticsUtils";
import {Skeleton} from "@/components/ui/skeleton";


const SensorAverageChart: FC = () => {
    const timeWindow = useSelector((state: RootState) => state.analytics.timeWindow);

    const {data: summary, isLoading, isError} = useGetAnalyticsSummaryQuery({
        window: timeWindow
    });

    const kpisByType = useMemo<KbpiAggregation[] | undefined>(() => {
        if (!summary) {
            return undefined;
        }
        return aggregateAnalyticsSummary(summary);
    }, [summary]);

    const avgByTypeData = useMemo(() => {
        if (!kpisByType) {
            return undefined;
        }
            return kpisByType.map(k => ({
                type: k.type,
                avg: +k.avg.toFixed(2),
                min: +k.min.toFixed(2),
                max: +k.max.toFixed(2)
            }))
        },
        [kpisByType]
    );

    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    Averages By Sensor Type
                </CardTitle>
                <CardDescription>
                    Horizontal bars by type
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="w-full h-64 mt-3">
                    {
                        isLoading ? (
                            <Skeleton className="w-full h-[200px]" />
                        ) : isError ? (
                            <></>
                        ) : (
                            <ResponsiveContainer>
                                <BarChart data={avgByTypeData} layout="vertical" margin={{ left: 12, right: 16 }}>
                                    <CartesianGrid strokeDasharray="3 3" />
                                    <XAxis type="number" />
                                    <YAxis dataKey="type" type="category" width={160} />
                                    <Tooltip
                                        formatter={(value: number | string): [string | number, string] => [toNumber(value).toFixed(2), "Avg"]}
                                        contentStyle={{ borderRadius: 12 }}
                                    />
                                    <Legend />
                                    <Bar dataKey="avg" name="Avg" barSize={16} radius={[0, 8, 8, 0]}>
                                        {avgByTypeData!.map((row, i) => (
                                            <Cell key={i} fill={COLORS.byType[row.type] ?? COLORS.fallback} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        )
                    }
                </div>
            </CardContent>
        </Card>
    );
}

export default SensorAverageChart;
