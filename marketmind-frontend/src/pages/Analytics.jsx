import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

export default function Analytics() {
  const navigate = useNavigate();
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
  const imageUsage = data?.image_creativity_usage;
  const topImageCreativity = imageUsage?.top_creativity_level || "Not enough data yet";
  const imageCounts = imageUsage?.counts || {};
  const imageSamples = imageUsage?.selected_samples ?? 0;
  const latestWeek = data?.weekly_tone_trend?.length
    ? data.weekly_tone_trend[data.weekly_tone_trend.length - 1]
    : null;

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h3 className="pageTitle">Analytics</h3>
        <button className="btnGhost" onClick={loadAnalytics}>Refresh</button>
      </div>

      {isLoading ? <p className="muted">Loading analytics...</p> : null}
      {errorMessage ? <p className="statusError">{errorMessage}</p> : null}

      {!isLoading && !errorMessage ? (
        <div className="gridCols3">
          <div className="sectionCard">
            <h4 style={{ margin: 0 }}>Preferred Voice</h4>
            <div className="muted">
              Your selected content is mostly <strong className="evalTitle">{topTone}</strong>.
            </div>
          </div>

          <div className="sectionCard">
            <h4 style={{ margin: 0 }}>Top Region Style</h4>
            <div className="muted">
              Most selected regional style: <strong className="evalTitle">{topRegion}</strong>.
            </div>
          </div>

          <div className="sectionCard">
            <h4 style={{ margin: 0 }}>Learning Progress</h4>
            <div className="muted">
              Preferences learned from <strong className="evalTitle">{selectedSamples}</strong> selections.
            </div>
          </div>

          <div className="sectionCard">
            <h4 style={{ margin: 0 }}>Most Used Image Creativity</h4>
            <div className="muted">
              Most selected image style: <strong className="evalTitle">{topImageCreativity}</strong>.
            </div>
            <div className="muted" style={{ marginTop: 6 }}>
              Safe {imageCounts.safe || 0}, Balanced {imageCounts.balanced || 0}, Bold {imageCounts.bold || 0}, Experimental {imageCounts.experimental || 0}
            </div>
            <div className="muted" style={{ marginTop: 6 }}>
              Based on <strong className="evalTitle">{imageSamples}</strong> saved image selections.
            </div>
          </div>
        </div>
      ) : null}

      {!isLoading && !errorMessage ? (
        <div className="sectionCard">
          <h4 style={{ margin: 0 }}>Latest Weekly Trend</h4>
          {latestWeek ? (
            <div style={{ display: "grid", gap: 6 }} className="muted">
              <div>
                Week: <strong className="evalTitle">{latestWeek.week_start_date} to {latestWeek.week_end_date}</strong>
              </div>
              <div>
                Tone mix: <strong className="evalTitle">
                  Positive {latestWeek.positive}, Neutral {latestWeek.neutral}, Negative {latestWeek.negative}
                </strong>
              </div>
            </div>
          ) : (
            <div>
              <p className="muted">No weekly trend yet. Select more variants first.</p>
              <div className="actionRow" style={{ marginTop: 10 }}>
                <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
                  Generate Variants
                </button>
                <button className="btnGhost btnInline" onClick={() => navigate("/app/history")}>
                  Check History
                </button>
              </div>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}
