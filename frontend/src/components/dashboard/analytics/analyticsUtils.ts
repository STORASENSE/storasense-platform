// src/components/dashboard/analytics/analyticsUtils.ts
import {AnalyticsSummaryResponse, AnalyticsTimeWindow} from "@/redux/api/storaSenseApiSchemas";

export const COLORS = {
    min: "#a5b4fc",
    max: "#6366f1",
    ultrasonic: "#22c55e",
    fallback: "#64748b",
    byType: {
        TEMPERATURE_INSIDE: "#0ea5e9",
        TEMPERATURE_OUTSIDE: "#3b82f6",
        HUMIDITY: "#10b981",
        GAS: "#f59e0b",
        CO2: "#f59e0b",
        ULTRASONIC: "#ef4444",
    } as Record<string, string>,
};

export const humanWindow: Record<AnalyticsTimeWindow, string> = {
    "7d": "7 days",
    "30d": "30 days",
    "365d": "365 days",
};

export function toNumber(val: number | string): number {
    return typeof val === "number" ? val : Number(val);
}

export interface KbpiItem {
    count: number;
    sumAvg: number;
    min: number;
    max: number;
}

export interface KbpiAggregation {
    type: string;
    avg: number;
    min: number;
    max: number;
}

export function aggregateAnalyticsSummary(summary: AnalyticsSummaryResponse): KbpiAggregation[] {
    const map = new Map<string, KbpiItem>();

    summary.forEach((r: any) => {
        const key = String(r.type);
        const cur = map.get(key) ?? {count: 0, sumAvg: 0, min: Infinity, max: -Infinity};
        cur.count += 1;
        cur.sumAvg += r.avg_value ?? 0;
        cur.min = Math.min(cur.min, r.min_value ?? Number.POSITIVE_INFINITY);
        cur.max = Math.max(cur.max, r.max_value ?? Number.NEGATIVE_INFINITY);
        map.set(key, cur);
    });

    return Array.from(map, ([type, v]) => ({
        type,
        avg: v.count ? v.sumAvg / v.count : 0,
        min: isFinite(v.min) ? v.min : 0,
        max: isFinite(v.max) ? v.max : 0,
    }));
}
