'use client';
import {FC, useState, useEffect, useMemo} from "react";
import ProtectedPage from "@/components/ProtectedPage";
import {
  ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  AreaChart, Area
} from "recharts";

type Window = "7d" | "30d" | "365d";

/** Backend-Response-Typen */
type SummaryItem = {
  type: string;
  sensor_id: string;      // UUID als string
  avg_value: number;
  min_value: number;
  max_value: number;
};

type DoorOpenItem = {
  day: string;            // 'YYYY-MM-DD'
  sensor_id: string;      // UUID
  open_seconds: number;   // Sekunden
};

const Page: FC = () => {
  const [win, setWin] = useState<Window>("7d");
  const [summary, setSummary] = useState<SummaryItem[]>([]);
  const [door, setDoor] = useState<DoorOpenItem[]>([]);
  const [loading, setLoading] = useState(false);

  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "/api";

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const [sRes, dRes] = await Promise.all([
          fetch(`${apiBase}/analytics/summary?window=${win}`, { credentials: "include" }),
          fetch(`${apiBase}/analytics/door-open-duration?window=${win}`, { credentials: "include" })
        ]);
        const sJson: unknown = await sRes.json();
        const dJson: unknown = await dRes.json();
        setSummary(Array.isArray(sJson) ? (sJson as SummaryItem[]) : []);
        setDoor(Array.isArray(dJson) ? (dJson as DoorOpenItem[]) : []);
      } finally {
        setLoading(false);
      }
    })();
  }, [win, apiBase]);

  const kpisByType = useMemo(() => {
    const map = new Map<string, {count:number; sumAvg:number; min:number; max:number}>();
    summary.forEach((r) => {
      const cur = map.get(r.type) ?? {count:0, sumAvg:0, min:Infinity, max:-Infinity};
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

  const barData = useMemo(() => (
    summary.map((r) => ({
      name: `${r.type}-${r.sensor_id}`,
      min: r.min_value,
      max: r.max_value
    }))
  ), [summary]);

  const doorData = useMemo(() => (
    door.map((r) => ({
      day: r.day,
      hours: Math.round((r.open_seconds/3600)*100)/100
    }))
  ), [door]);

  return (
    <ProtectedPage>
      <header className="mb-5">
        <h1 className="text-3xl font-semibold text-blue-whale">Analytics</h1>
      </header>

      <section className="space-y-6">
        {/* Zeitraum-Auswahl */}
        <div className="flex items-center gap-2">
          {(["7d","30d","365d"] as Window[]).map(w => (
            <button
              key={w}
              onClick={() => setWin(w)}
              className={`px-4 py-2 rounded-lg border ${w===win ? "bg-blue-whale text-white" : "bg-white hover:bg-gray-100"}`}
            >
              {w}
            </button>
          ))}
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {kpisByType.map(k => (
            <div key={k.type} className="rounded-2xl border p-4 shadow-sm">
              <div className="text-sm text-gray-500">{k.type}</div>
              <div className="mt-2 grid grid-cols-3 gap-2 text-center">
                <div>
                  <div className="text-xs text-gray-500">Ø</div>
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
            <div className="col-span-3 text-sm text-gray-500">
              Keine Daten im Zeitraum {win}.
            </div>
          )}
        </div>

        {/* Min/Max je Sensor */}
        <div className="rounded-2xl border p-4 shadow-sm">
          <div className="mb-3 font-semibold">Min/Max je Sensor</div>
          <div className="w-full h-72">
            <ResponsiveContainer>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" hide />
                <YAxis />
                <Tooltip />
                <Bar dataKey="min" />
                <Bar dataKey="max" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Tür offen pro Tag */}
        <div className="rounded-2xl border p-4 shadow-sm">
          <div className="mb-3 font-semibold">Tür offen pro Tag (Stunden)</div>
          <div className="w-full h-72">
            <ResponsiveContainer>
              <AreaChart data={doorData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="hours" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </ProtectedPage>
  );
};

export default Page;
