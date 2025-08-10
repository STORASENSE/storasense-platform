import {FC, SVGProps} from "react";
import {Area, AreaChart, CartesianGrid, XAxis, YAxis} from "recharts";
import {ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent} from "@/components/ui/chart";
import {Measurement} from "@/redux/api/storaSenseApiSchemas";


const defaultGradient: SVGProps<SVGStopElement>[] = [
    { offset: "5%", stopColor: "#066DDC", stopOpacity: 0.8 },
    { offset: "95%", stopColor: "#7FBDFF", stopOpacity: 0.1 }
];


interface SensorTelemetryChartProps {
    id: string;
    config?: ChartConfig;
    data: Measurement[];
    valueUnit?: string;
    valueName?: string;
    gradient?: SVGProps<SVGStopElement>[];
}

const SensorTelemetryChart: FC<SensorTelemetryChartProps> = (props) => {
    return (
        <ChartContainer config={props.config || {}} className="h-[200px] w-full">
            <AreaChart data={props.data}>
                <defs>
                    <linearGradient id={`${props.id}-gradient`} x1="0" y1="0" x2="0" y2="1">
                        {(props.gradient || defaultGradient).map(stopProps => (
                            <stop key={JSON.stringify(stopProps)} {...stopProps} />
                        ))}
                    </linearGradient>
                </defs>
                <CartesianGrid vertical={false} />
                <XAxis
                    dataKey="created_at"
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
                <YAxis
                    tickLine={false}
                    axisLine={false}
                    tickFormatter={(temp: string) => {
                        return `${temp}${props.valueUnit}`;
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
                            formatter={(value, name) => (
                                <div className="min-w-[150px] flex justify-between">
                                    <span className="text-muted-foreground">
                                        {props.valueName || name}
                                    </span>
                                    <div>
                                        <span>
                                            {Math.round((value as number)*100)/100}
                                        </span>
                                        <span className="ml-1 text-muted-foreground">
                                            {props.valueUnit}
                                        </span>
                                    </div>
                                </div>
                            )}
                            indicator="dot"
                        />
                    }
                />
                <Area
                    dataKey="value"
                    type="bump"
                    fill={`url(#${props.id}-gradient)`}
                    stackId="a"
                />
            </AreaChart>
        </ChartContainer>
    );
}

export default SensorTelemetryChart;
