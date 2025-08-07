"use client"

import {FC, useEffect, useMemo, useState} from "react";
import {useGetMeasurementsQuery} from "@/redux/api/storaSenseApi";
import {ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent} from "@/components/ui/chart";
import {Area, AreaChart, CartesianGrid, XAxis} from "recharts";
import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert";
import {AlertCircleIcon} from "lucide-react";
import {Skeleton} from "@/components/ui/skeleton";


const chartConfig = {
    inside: {
        label: "Inside",
        color: "#066DDC"
    }
} satisfies ChartConfig;


const TemperatureChart: FC = () => {
    const [maxDate, setMaxDate] = useState<Date>(new Date());

    useEffect(() => {
        const counter = setTimeout(() => {
            const now = new Date();
            now.setMinutes(now.getMinutes() + 30);
            setMaxDate(now);
        }, 30000);

        return () => {
            clearTimeout(counter);
        }
    }, []);

    const {data, isLoading, isError} = useGetMeasurementsQuery({
        sensor_id: '3f8f788a-a6d0-34ee-9cc0-2a762338cfda',
        max_date: maxDate.toISOString()
    });

    const transformedData = useMemo(() => {
        if (!data)
            return undefined;
        return data.measurements.map(measurement => ({
            date: measurement.created_at,
            inside: measurement.value
        }));
    }, [data]);

    if (isLoading) {
        return (
            <>
                <Skeleton className="mt-2 mb-3 w-full h-[100px]"/>
                <Skeleton className="mb-3 w-full h-[40px]"/>
                <Skeleton className="w-full h-[40px]"/>
            </>
        );
    }

    if (isError) {
        return (
            <Alert variant="destructive" className="mt-2 p-2">
                <AlertCircleIcon />
                <AlertTitle>
                    Error while fetching temperature data.
                </AlertTitle>
                <AlertDescription>
                    An error occurred while contacting the server.
                </AlertDescription>
            </Alert>
        );
    }

    return (
        <>
            <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
                <AreaChart data={transformedData}>
                    <defs>
                        <linearGradient id="fillTempInside" x1="0" y1="0" x2="0" y2="1">
                            <stop
                                offset="5%"
                                stopColor="#066DDC"
                                stopOpacity={0.8}
                            />
                            <stop
                                offset="95%"
                                stopColor="#7FBDFF"
                                stopOpacity={0.1}
                            />
                        </linearGradient>
                    </defs>
                    <CartesianGrid vertical={false} />
                    <XAxis
                        dataKey="date"
                        tickLine={false}
                        axisLine={false}
                        tickMargin={8}
                        minTickGap={32}
                        tickFormatter={(dateStr: string) => {
                            const date = new Date(dateStr);
                            return date.toLocaleDateString("en-US", {
                                month: "short",
                                day: "numeric",
                            });
                        }}
                    />
                    <ChartTooltip
                        cursor={false}
                        content={
                            <ChartTooltipContent
                                labelFormatter={(value: string) => {
                                    return new Date(value).toLocaleDateString("en-US", {
                                        month: "short",
                                        day: "numeric",
                                    });
                                }}
                                indicator="dot"
                            />
                        }
                    />
                    <Area
                        dataKey="inside"
                        type="natural"
                        fill="url(#fillTempInside)"
                        stroke="#066DDC"
                        stackId="a"
                    />
                </AreaChart>
            </ChartContainer>
        </>
    );
}

export default TemperatureChart;
