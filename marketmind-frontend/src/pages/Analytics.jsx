import { useEffect, useState } from "react";
import { api } from "../api/client";

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
            <p className="muted" style={{ fontSize: 12, marginBottom: 4 }}>System Trained On</p>
            <strong style={{ fontSize: 16 }}>{summary.selection_count || 0} selections</strong>
            {summary.learned_vad_label && (
              <p className="muted" style={{ fontSize: 12, marginTop: 4 }}>
                Tends toward: <strong style={{ color: "#e2e8f0" }}>{summary.learned_vad_label}</strong>
              </p>
            )}
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

          <StatRow label="Selection Rate" value={campaign.generation_count > 0 ? `${campaign.selection_rate}%` : "—"} />
          <StatRow
            label="Dominant Tone"
            value={campaign.dominant_tone ? campaign.dominant_tone.replace(/_/g, " ") : "Not enough data"}
          />

          <VadRow avg_vad={campaign.avg_vad} />
        </div>
      ))}
    </div>
  );
}
