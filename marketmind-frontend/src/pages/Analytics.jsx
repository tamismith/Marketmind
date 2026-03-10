import { useEffect, useMemo, useState } from "react";
import { api } from "../api/client";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const CHART_COLORS = {
  positive: "#22c55e",
  neutral: "#94a3b8",
  negative: "#ef4444",
  safe: "#0ea5a3",
  balanced: "#38bdf8",
  bold: "#f59e0b",
  experimental: "#a78bfa",
};

export default function Analytics() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const loadAnalytics = async () => {
    setErrorMessage("");
    setIsLoading(true);
    try {
      const result = await api.get("/api/ai/analytics");
      setData(result);
    } catch (error) {
      setErrorMessage(error.message || "Failed to load analytics.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const imageUsage = data?.image_creativity_usage;
  const imageCounts = imageUsage?.counts || {};
  const imageSamples = imageUsage?.selected_samples ?? 0;

  const weeklyToneData = useMemo(() => {
    return (data?.weekly_tone_trend || []).map((w) => ({
      week: w.week_start_date || w.week,
      positive: w.positive || 0,
      neutral: w.neutral || 0,
      negative: w.negative || 0,
    }));
  }, [data]);

  const regionData = useMemo(() => {
    return (data?.regional_style_preference || []).map((r) => ({
      region: r.region,
      selected_count: r.selected_count || 0,
    }));
  }, [data]);

  const creativityData = useMemo(() => {
    return [
      { name: "safe", value: imageCounts.safe || 0 },
      { name: "balanced", value: imageCounts.balanced || 0 },
      { name: "bold", value: imageCounts.bold || 0 },
      { name: "experimental", value: imageCounts.experimental || 0 },
    ];
  }, [imageCounts]);

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h3 className="pageTitle">Analytics</h3>
        <button className="btnGhost" onClick={loadAnalytics}>Refresh</button>
      </div>

      {isLoading ? <p className="muted">Loading analytics...</p> : null}
      {errorMessage ? <p className="statusError">{errorMessage}</p> : null}

      {!isLoading && !errorMessage ? (
        <div className="sectionCard">
          <h4 style={{ marginTop: 0 }}>Weekly Tone Trend (Visual)</h4>
          {weeklyToneData.length > 0 ? (
            <div style={{ width: "100%", height: 300 }}>
              <ResponsiveContainer>
                <BarChart data={weeklyToneData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#24314a" />
                  <XAxis dataKey="week" stroke="#9fb0cc" />
                  <YAxis stroke="#9fb0cc" allowDecimals={false} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="positive" stackId="tone" fill={CHART_COLORS.positive} />
                  <Bar dataKey="neutral" stackId="tone" fill={CHART_COLORS.neutral} />
                  <Bar dataKey="negative" stackId="tone" fill={CHART_COLORS.negative} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="muted">No weekly tone chart data yet.</p>
          )}
        </div>
      ) : null}

      {!isLoading && !errorMessage ? (
        <div className="gridCols2">
          <div className="sectionCard">
            <h4 style={{ marginTop: 0 }}>Regional Preference (Visual)</h4>
            {regionData.length > 0 ? (
              <div style={{ width: "100%", height: 300 }}>
                <ResponsiveContainer>
                  <BarChart data={regionData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#24314a" />
                    <XAxis dataKey="region" stroke="#9fb0cc" />
                    <YAxis stroke="#9fb0cc" allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="selected_count" fill={CHART_COLORS.safe} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p className="muted">No regional chart data yet.</p>
            )}
          </div>

          <div className="sectionCard">
            <h4 style={{ marginTop: 0 }}>Image Creativity Usage (Visual)</h4>
            {imageSamples > 0 ? (
              <div style={{ width: "100%", height: 300 }}>
                <ResponsiveContainer>
                  <PieChart>
                    <Tooltip />
                    <Legend />
                    <Pie
                      data={creativityData}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={90}
                    >
                      {creativityData.map((entry) => (
                        <Cell key={entry.name} fill={CHART_COLORS[entry.name]} />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <p className="muted">No image creativity chart data yet.</p>
            )}
          </div>
        </div>
      ) : null}
    </div>
  );
}
