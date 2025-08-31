'use client';

import { useEffect, useMemo, useState } from "react";
import AuthenticationRequired from "@/components/context/AuthenticationRequired";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend,
  AreaChart, Area, Cell
} from "recharts";
import { useSelector } from "react-redux";
import type { RootState } from "@/redux/store";

type Window = "7d" | "30d" | "365d";
type SummaryItem = { type: string; sensor_id: string; avg_value: number; min_value: number; max_value: number; };
type DoorOpenItem = { day: string; sensor_id: string; open_seconds: number; };

const COLORS = {
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
  } as Record<string, string>,
};

function Card(props: React.PropsWithChildren<{ title?: string; subtitle?: string; className?: string }>) {
  const { title, subtitle, className, children } = props;
  return (
    <div className={`bg-white rounded-2xl border shadow-sm p-5 ${className ?? ""}`}>
      {title && <div className="font-semibold">{title}</div>}
      {subtitle && <div className="text-xs text-gray-500 mt-0.5">{subtitle}</div>}
      {children}
    </div>
  );
}

function StatCard({ label, value, foot }: { label: string; value: string | number; foot?: string }) {
  return (
    <div className="rounded-2xl border bg-white p-4 shadow-sm">
      <div className="text-xs text-gray-500">{label}</div>
      <div className="mt-1 text-2xl font-semibold">{value}</div>
      {foot && <div className="mt-1 text-xs text-gray-400">{foot}</div>}
    </div>
  );
}

export default function Page() {
  const [win, setWin] = useState<Window>("7d");
  const [summary, setSummary] = useState<SummaryItem[]>([]);
  const [door, setDoor] = useState<DoorOpenItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [errMsg, setErrMsg] = useState<string | null>(null);
  const token = useSelector((s: RootState) => s.auth.token);

  // 1) zuerst /api (Proxy), dann ENV oder Domain
  const BASES = useMemo(
    () => ["/api", process.env.NEXT_PUBLIC_API_BASE ?? "https://api.storasense.de"],
    []
  );

  useEffect(() => {
    (async () => {
      setErrMsg(null);
      if (!token) { setSummary([]); setDoor([]); setLoading(false); return; }

      setLoading(true);
      const headers: HeadersInit = { Authorization: `Bearer ${token}` };

      const load = async (base: string) => {
        const [sRes, dRes] = await Promise.all([
          fetch(`${base}/analytics/summary?window=${win}`, { credentials: "include", headers }),
          fetch(`${base}/analytics/door-open-duration?window=${win}`, { credentials: "include", headers }),
        ]);
        if (!sRes.ok || !dRes.ok) throw new Error(`HTTP ${sRes.status}/${dRes.status} @ ${base}`);
        const sJson: unknown = await sRes.json();
        const dJson: unknown = await dRes.json();
        return {
          sArr: Array.isArray(sJson) ? (sJson as SummaryItem[]) : [],
          dArr: Array.isArray(dJson) ? (dJson as DoorOpenItem[]) : [],
        };
      };

      try {
        let ok = false;
        for (const base of BASES) {
          try {
            const { sArr, dArr } = await load(base);
            setSummary(sArr); setDoor(dArr); ok = true; break;
          } catch { /* nächster Kandidat */ }
        }
        if (!ok) { setSummary([]); setDoor([]); setErrMsg("Konnte keine Analytics-Daten laden."); }
      } catch (e) {
        setErrMsg(e instanceof Error ? e.message : "Unbekannter Fehler");
        setSummary([]); setDoor([]);
      } finally { setLoading(false); }
    })();
  }, [win, token, BASES]);

  // Aggregationen
  const kpisByType = useMemo(() => {
    const map = new Map<string, { count: number; sumAvg: number; min: number; max: number }>();
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
  }, [summary]);

  const topStats = useMemo(() => {
    const totalSensors = summary.length;
    const totalTypes = new Set(summary.map(s => s.type)).size;
    const overallAvg = totalSensors ? summary.reduce((a, s) => a + s.avg_value, 0) / totalSensors : 0;
    return { totalSensors, totalTypes, overallAvg };
  }, [summary]);

  const avgByTypeData = useMemo(
    () => kpisByType.map(k => ({ type: k.type, avg: +k.avg.toFixed(2), min: +k.min.toFixed(2), max: +k.max.toFixed(2) })),
    [kpisByType]
  );

  const barData = useMemo(
    () => summary.map(r => ({ name: `${r.type}-${r.sensor_id}`, min: r.min_value, max: r.max_value })),
    [summary]
  );

  const doorData = useMemo(
    () => door.map(r => ({ day: r.day, hours: Math.round((r.open_seconds / 3600) * 100) / 100 })),
    [door]
  );

  const humanWindow: Record<Window, string> = { "7d": "7 days", "30d": "30 days", "365d": "365 days" };
  const toNum = (v: number | string) => (typeof v === "number" ? v : Number(v));

  return (
    <AuthenticationRequired>
      <header className="mb-5">
        <h1 className="text-3xl font-semibold text-blue-whale">Analytics</h1>
        {errMsg && <div className="mt-2 text-sm text-red-600">Fehler: {errMsg}</div>}
      </header>

      <section className="space-y-6">
        {/* Window Switcher */}
        <div className="rounded-xl border bg-white/60 p-2 w-fit">
          {(["7d", "30d", "365d"] as Window[]).map(w => (
            <button
              key={w}
              onClick={() => setWin(w)}
              className={`px-4 py-2 rounded-lg border transition ${w === win ? "bg-blue-whale text-white border-blue-whale" : "bg-white hover:bg-gray-50"} ${w !== "7d" ? "ml-2" : ""}`}
            >
              {w}
            </button>
          ))}
        </div>

        {/* Top stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <StatCard label="Total sensors" value={topStats.totalSensors} />
          <StatCard label="Sensor types" value={topStats.totalTypes} />
          <StatCard label="Overall average" value={topStats.overallAvg.toFixed(2)} foot={`Window: ${humanWindow[win]}`} />
        </div>

        {/* KPI Cards by type */}
        <Card title="KPIs by type" subtitle={`Aggregated over ${humanWindow[win]}`}>
          <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-4">
            {kpisByType.map(k => (
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
            ))}
            {!loading && kpisByType.length === 0 && (
              <div className="text-sm text-gray-500">No data in the last {humanWindow[win]}.</div>
            )}
          </div>
        </Card>

        {/* Min/Max per sensor */}
        <Card title="Min/Max per sensor" subtitle="Each bar group shows min and max per sensor">
          <div className="w-full h-64 mt-3">
            <ResponsiveContainer>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" hide />
                <YAxis />
                <Tooltip
                  formatter={(value: number | string, name: string): [string | number, string] => [toNum(value).toFixed(2), name]}
                  contentStyle={{ borderRadius: 12 }}
                />
                <Legend />
                <Bar dataKey="min" name="Min" barSize={14} fill={COLORS.min} radius={[6, 6, 0, 0]} />
                <Bar dataKey="max" name="Max" barSize={14} fill={COLORS.max} radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Door-open area */}
        <Card title="Door open per day (hours)" subtitle={`Sum of open time per day • ${humanWindow[win]}`}>
          <div className="w-full h-64 mt-3">
            <ResponsiveContainer>
              <AreaChart data={doorData}>
                <defs>
                  <linearGradient id="doorArea" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={COLORS.ultrasonic} stopOpacity={0.35}/>
                    <stop offset="100%" stopColor={COLORS.ultrasonic} stopOpacity={0.06}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip
                  formatter={(value: number | string): [string, string] => [`${toNum(value).toFixed(2)} h`, "Hours"]}
                  contentStyle={{ borderRadius: 12 }}
                />
                <Area type="monotone" dataKey="hours" name="Hours" stroke={COLORS.ultrasonic} fill="url(#doorArea)" strokeWidth={2} animationDuration={600} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Averages by sensor type */}
        <Card title="Averages by sensor type" subtitle="Horizontal bars by type">
          <div className="w-full h-64 mt-3">
            <ResponsiveContainer>
              <BarChart data={avgByTypeData} layout="vertical" margin={{ left: 12, right: 16 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="type" type="category" width={160} />
                <Tooltip
                  formatter={(value: number | string): [string | number, string] => [toNum(value).toFixed(2), "Avg"]}
                  contentStyle={{ borderRadius: 12 }}
                />
                <Legend />
                <Bar dataKey="avg" name="Avg" barSize={16} radius={[0, 8, 8, 0]}>
                  {avgByTypeData.map((row, i) => (
                    <Cell key={i} fill={COLORS.byType[row.type] ?? COLORS.fallback} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {loading && <div className="animate-pulse text-xs text-gray-400">Loading data…</div>}
      </section>
    </AuthenticationRequired>
  );
}
