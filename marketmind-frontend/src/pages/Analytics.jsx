import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function AccuracyBar({ value }) {
  const color = value >= 70 ? "#22c55e" : value >= 40 ? "#f59e0b" : "#ef4444";
  return (
    <div style={{ marginTop: 6 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
        <span style={{ fontSize: 12 }} className="muted">Brand Language Accuracy</span>
        <strong style={{ fontSize: 13, color }}>{value}%</strong>
      </div>
      <div style={{ background: "#1a2436", borderRadius: 4, height: 8, overflow: "hidden" }}>
        <div style={{ width: `${value}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.4s ease" }} />
      </div>
    </div>
  );
}

function StatRow({ label, value }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "6px 0", borderBottom: "1px solid #1a2436" }}>
      <span className="muted" style={{ fontSize: 13 }}>{label}</span>
      <strong style={{ fontSize: 13 }}>{value ?? "—"}</strong>
    </div>
  );
}

function VadRow({ avg_vad }) {
  if (!avg_vad || (avg_vad.valence == null && avg_vad.arousal == null && avg_vad.dominance == null)) return null;
  return (
    <div style={{ marginTop: 8, fontSize: 12, display: "flex", gap: 14 }} className="muted">
      {avg_vad.valence != null && <span>Valence: <strong style={{ color: "#e2e8f0" }}>{avg_vad.valence}</strong></span>}
      {avg_vad.arousal != null && <span>Arousal: <strong style={{ color: "#e2e8f0" }}>{avg_vad.arousal}</strong></span>}
      {avg_vad.dominance != null && <span>Dominance: <strong style={{ color: "#e2e8f0" }}>{avg_vad.dominance}</strong></span>}
    </div>
  );
}

function AccuracyTrend({ trend }) {
  if (!trend || trend.length < 2) return null;
  const data = trend.map((point, i) => ({
    label: `#${i + 1}`,
    accuracy: point.accuracy,
  }));
  return (
    <div style={{ marginTop: 16 }}>
      <p className="muted" style={{ fontSize: 12, marginBottom: 6 }}>Brand Language Accuracy Trend</p>
      <ResponsiveContainer width="100%" height={120}>
        <LineChart data={data} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
          <XAxis dataKey="label" tick={{ fontSize: 10, fill: "#64748b" }} />
          <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: "#64748b" }} />
          <Tooltip
            contentStyle={{ background: "#111827", border: "1px solid #24314a", borderRadius: 6, fontSize: 12 }}
            formatter={(val) => [`${val}%`, "Accuracy"]}
          />
          <Line
            type="monotone"
            dataKey="accuracy"
            stroke="#0ea5a3"
            strokeWidth={2}
            dot={{ r: 3, fill: "#0ea5a3" }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default function Analytics() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const loadAnalytics = async () => {
    setErrorMessage("");
    setIsLoading(true);
    try {
      const result = await api.get("/api/campaigns/analytics");
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

  const summary = data?.summary;
  const campaigns = data?.campaigns || [];

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h3 className="pageTitle">Analytics</h3>
        <button className="btnGhost" onClick={loadAnalytics}>Refresh</button>
      </div>

      {isLoading ? <p className="muted">Loading analytics...</p> : null}
      {errorMessage ? <p className="statusError">{errorMessage}</p> : null}

      {!isLoading && !errorMessage && campaigns.length === 0 ? (
        <div className="sectionCard">
          <p className="muted">No campaign data yet. Generate some content first.</p>
          <button className="btn btnInline" style={{ marginTop: 10 }} onClick={() => navigate("/app/generate")}>
            Generate Content
          </button>
        </div>
      ) : null}

      {/* Summary cards */}
      {!isLoading && summary && (
        <div className="gridCols2">
          <div className="sectionCard">
            <p className="muted" style={{ fontSize: 12, marginBottom: 4 }}>Most Active Campaign</p>
            <strong style={{ fontSize: 16 }}>{summary.most_active_campaign || "—"}</strong>
          </div>
          <div className="sectionCard">
            <p className="muted" style={{ fontSize: 12, marginBottom: 4 }}>Highest Brand Language Accuracy</p>
            <strong style={{ fontSize: 16 }}>
              {summary.highest_accuracy_campaign
                ? `${summary.highest_accuracy_campaign} — ${summary.highest_accuracy_value}%`
                : "—"}
            </strong>
          </div>
        </div>
      )}

      {/* Per campaign cards */}
      {!isLoading && campaigns.map((campaign) => (
        <div key={campaign.id} className="sectionCard">
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
            <h4 style={{ margin: 0 }}>{campaign.name}</h4>
            {campaign.goal && (
              <span className="muted" style={{ fontSize: 12 }}>— {campaign.goal}</span>
            )}
          </div>

          <StatRow label="Generations" value={campaign.generation_count} />
          <StatRow label="Selection Rate" value={campaign.generation_count > 0 ? `${campaign.selection_rate}%` : "—"} />
          <StatRow
            label="Dominant Tone"
            value={campaign.dominant_tone ? campaign.dominant_tone.replace(/_/g, " ") : "Not enough data"}
          />

          <VadRow avg_vad={campaign.avg_vad} />

          {campaign.brand_language_accuracy != null ? (
            <>
              <AccuracyBar value={campaign.brand_language_accuracy} />
              <AccuracyTrend trend={campaign.accuracy_trend} />
            </>
          ) : (
            <p className="muted" style={{ fontSize: 12, marginTop: 8 }}>
              {campaign.target_valence == null && campaign.target_arousal == null && campaign.target_dominance == null
                ? "Set VAD targets on this campaign to see brand language accuracy."
                : "Select some variants to build accuracy data."}
            </p>
          )}
        </div>
      ))}
    </div>
  );
}
