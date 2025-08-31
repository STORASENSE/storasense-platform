import {AnalyticsSummaryResponse, AnalyticsTimeWindow, SensorType} from "@/redux/api/storaSenseApiSchemas";

export const COLORS = {
    min: "#a5b4fc",
    max: "#6366f1",
    ultrasonic: "#22c55e",
    fallback: "#64748b",
    byType: {
        TEMPERATURE_INSIDE: "#0ea5e9",
        TEMPERATURE_OUTSIDE: "#3b82f6",
        HUMIDITY: "#10b981",
        CO2: "#f59e0b",
        ULTRASONIC: "#ef4444",
    } as Record<SensorType, string>,
};

export const humanWindow: Record<AnalyticsTimeWindow, string> = {
    "7d": "7 days",
    "30d": "30 days",
    "365d": "365 days"
};

export function toNumber(val: number | string): number {
    if (typeof val === "number") {
        return val;
    }
    return Number(val);
}


export interface KbpiItem {
    count: number;
    sumAvg: number;
    min: number;
    max: number;
}

export interface KbpiAggregation {
    type: SensorType;
    avg: number;
    min: number;
    max: number;
}

export function aggregateAnalyticsSummary(summary: AnalyticsSummaryResponse): KbpiAggregation[] {
    const map = new Map<SensorType, KbpiItem>();
    summary.forEach(r => {
        const cur = map.get(r.type) ?? { count: 0, sumAvg: 0, min: Infinity, max: -Infinity };
        cur.count += 1;
        cur.sumAvg += r.avg_value;
        cur.min = Math.min(cur.min, r.min_value);
        cur.max = Math.max(cur.max, r.max_value);
        map.set(r.type, cur);
    });
    return Array.from(map, ([type, v]) => ({
        type,
        avg: v.count ? v.sumAvg / v.count : 0,
        min: v.min === Infinity ? 0 : v.min,
        max: v.max === -Infinity ? 0 : v.max
    }));
}
