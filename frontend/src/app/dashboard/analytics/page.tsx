'use client';

import React from "react";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import TopStatsSection from "@/components/dashboard/analytics/TopStatsSection";
import KpiByTypeSection from "@/components/dashboard/analytics/KpiByTypeSection";
import SensorMinMaxChart from "@/components/dashboard/analytics/SensorMinMaxChart";
import SensorAverageChart from "@/components/dashboard/analytics/SensorAverageChart";
import TimeWindowSelection from "@/components/dashboard/analytics/TimeWindowSelection";
import ActiveStorageRequired from "@/components/context/ActiveStorageRequired";


export default function Page() {
    return (
        <AuthenticationRequired>
            <header className="mb-5">
                <h1 className="text-3xl font-semibold text-blue-whale">
                    Analytics
                </h1>
            </header>
            <ActiveStorageRequired>
                <section className="space-y-6">
                    {/* Window Switcher */}
                    <TimeWindowSelection />´
                    {/* Top stats */}
                    <TopStatsSection />´
                    {/* KPI Cards by type */}
                    <KpiByTypeSection />´
                    {/* Min/Max per sensor */}
                    <SensorMinMaxChart />
                    {/* Averages by sensor type */}
                    <SensorAverageChart />
                </section>
            </ActiveStorageRequired>
        </AuthenticationRequired>
    );
}
