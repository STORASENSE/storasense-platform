"use client"

import React, {FC, useMemo} from "react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {useSelector} from "react-redux";
import {RootState} from "@/redux/store";
import {useGetAnalyticsSummaryQuery} from "@/redux/api/storaSenseApi";
import {Skeleton} from "@/components/ui/skeleton";
import {aggregateAnalyticsSummary, humanWindow, KbpiAggregation} from "@/components/dashboard/analytics/analyticsUtils";


const KpiByTypeSection: FC = () => {
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

    return (
        <Card>
            <CardHeader>
                <CardTitle>
                    KPIs by type
                </CardTitle>
                <CardDescription>
                    Aggregated over {humanWindow[timeWindow]}
                </CardDescription>
            </CardHeader>
            <CardContent>
                <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4">
                    {
                        isLoading ? (
                            <>
                                <Skeleton  className="h-[100px]" />
                                <Skeleton  className="h-[100px]" />
                                <Skeleton  className="h-[100px]" />
                                <Skeleton  className="h-[100px]" />
                                <Skeleton  className="h-[100px]" />
                                <Skeleton  className="h-[100px]" />
                            </>
                        ) : isError ? (
                            <></>
                        ) : (kpisByType!.length === 0) ? (
                            <div className="text-sm text-gray-500">
                                No data in the last {humanWindow[timeWindow]}.
                            </div>
                        ) : kpisByType!.map(k => (
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
                    }
                </div>
            </CardContent>
        </Card>
    );
}

export default KpiByTypeSection;
