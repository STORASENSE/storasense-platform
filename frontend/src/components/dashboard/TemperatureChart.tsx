"use client"

import {FC, useCallback, useEffect, useMemo, useState} from "react";
import {useGetMeasurementsQuery} from "@/redux/api/storaSenseApi";
import {ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent} from "@/components/ui/chart";
import {Area, AreaChart, CartesianGrid, XAxis} from "recharts";


const chartConfig = {
    inside: {
        label: "Inside",
        color: "#066DDC"
    }
} satisfies ChartConfig;


const TemperatureChart: FC = () => {
    /*
    const [maxDate, setMaxDate] = useState<Date>();
    const getMaxDate = useCallback(() => {
        const now = new Date();
        now.setFullYear(2030)
        now.setMinutes(now.getMinutes() - 30);
        return now;
    }, []);
    */
    const {data} = useGetMeasurementsQuery({
        sensor_id: '3a46e98b-b358-4763-9017-7238787b30b5',
        max_date: '2030-08-05 12:58:13.585000+00:00'
    });

    const transformedData = useMemo(() => {
        if (!data)
            return undefined;
        return data.measurements.map(measurement => ({
            date: measurement.created_at,
            inside: measurement.value
        }));
    }, [data]);

    if (!data) {
        return <></>;
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
