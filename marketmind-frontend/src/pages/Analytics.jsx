import { useEffect, useState } from "react";
import { api } from "../api/client";

function cardStyle() {
  return {
    border: "1px solid #2a2f3c",
    borderRadius: 12,
    padding: 14,
    background: "#11131a",
    display: "grid",
    gap: 8,
  };
}

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

  const topTone = data?.best_brand_voice?.top_tone || "Not enough data yet";
  const selectedSamples = data?.best_brand_voice?.selected_samples ?? 0;
  const topRegion = data?.regional_style_preference?.[0]?.region || "Not enough data yet";
  const latestWeek = data?.weekly_tone_trend?.length
    ? data.weekly_tone_trend[data.weekly_tone_trend.length - 1]
    : null;

  return (
    <div style={{ display: "grid", gap: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3 style={{ margin: 0 }}>Analytics</h3>
        <button className="logout" onClick={loadAnalytics}>Refresh</button>
      </div>

      {isLoading ? <p style={{ margin: 0, color: "#a9b0bf" }}>Loading analytics...</p> : null}
      {errorMessage ? <p style={{ margin: 0, color: "#ffb4b4" }}>{errorMessage}</p> : null}

      {!isLoading && !errorMessage ? (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 12 }}>
          <div style={cardStyle()}>
            <h4 style={{ margin: 0 }}>Preferred Voice</h4>
            <div style={{ color: "#a9b0bf" }}>
              Your selected content is mostly <strong style={{ color: "#eef1f6" }}>{topTone}</strong>.
            </div>
          </div>

          <div style={cardStyle()}>
            <h4 style={{ margin: 0 }}>Top Region Style</h4>
            <div style={{ color: "#a9b0bf" }}>
              Most selected regional style: <strong style={{ color: "#eef1f6" }}>{topRegion}</strong>.
            </div>
          </div>

          <div style={cardStyle()}>
            <h4 style={{ margin: 0 }}>Learning Progress</h4>
            <div style={{ color: "#a9b0bf" }}>
              Preferences learned from <strong style={{ color: "#eef1f6" }}>{selectedSamples}</strong> selections.
            </div>
          </div>
        </div>
      ) : null}

      {!isLoading && !errorMessage ? (
        <div style={cardStyle()}>
          <h4 style={{ margin: 0 }}>Latest Weekly Trend</h4>
          {latestWeek ? (
            <div style={{ color: "#a9b0bf", display: "grid", gap: 6 }}>
              <div>
                Week: <strong style={{ color: "#eef1f6" }}>{latestWeek.week_start_date} to {latestWeek.week_end_date}</strong>
              </div>
              <div>
                Tone mix: <strong style={{ color: "#eef1f6" }}>
                  Positive {latestWeek.positive}, Neutral {latestWeek.neutral}, Negative {latestWeek.negative}
                </strong>
              </div>
            </div>
          ) : (
            <p style={{ margin: 0, color: "#a9b0bf" }}>No weekly trend yet. Select more variants first.</p>
          )}
        </div>
      ) : null}
    </div>
  );
}
