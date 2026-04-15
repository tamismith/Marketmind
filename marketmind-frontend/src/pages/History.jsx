import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).catch(() => {});
}

function EvalSummary({ evaluation }) {
  if (!evaluation) return null;
  const { tone_label, tone, vad, explanation } = evaluation;
  const displayTone = tone_label || tone || "Unknown";
  return (
    <div style={{ fontSize: 12, marginTop: 6 }} className="muted">
      <div>Tone: <strong style={{ color: "#e2e8f0" }}>{displayTone}</strong></div>
      {vad ? (
        <div style={{ marginTop: 4, display: "flex", gap: 12 }}>
          <span>V: {vad.valence?.toFixed(2)}</span>
          <span>A: {vad.arousal?.toFixed(2)} ({vad.arousal_label})</span>
          <span>D: {vad.dominance?.toFixed(2)} ({vad.dominance_label})</span>
        </div>
      ) : null}
      {explanation?.tone_summary ? (
        <div style={{ marginTop: 4 }}>{explanation.tone_summary}</div>
      ) : null}
    </div>
  );
}

function VariantCard({ label, text, evaluation, isSelected, collapsed: initialCollapsed }) {
  const [collapsed, setCollapsed] = useState(initialCollapsed);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    copyToClipboard(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div style={{
      border: isSelected ? "1px solid #0ea5a3" : "1px solid #24314a",
      borderRadius: 8,
      padding: 12,
      background: isSelected ? "rgba(14,165,163,0.06)" : "transparent",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: collapsed ? 0 : 8 }}>
        <strong style={{ fontSize: 13 }}>{label}</strong>
        {isSelected && (
          <span style={{ fontSize: 11, background: "#0ea5a3", color: "#fff", borderRadius: 4, padding: "1px 6px" }}>
            Selected
          </span>
        )}
        <button
          className="btnGhost"
          style={{ marginLeft: "auto", fontSize: 11, padding: "2px 8px" }}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? "Show" : "Hide"}
        </button>
      </div>
      {!collapsed && (
        <>
          <p className="resultText" style={{ marginBottom: 6 }}>{text}</p>
          <button
            className="btnGhost btnInline"
            style={{ fontSize: 11 }}
            onClick={handleCopy}
          >
            {copied ? "Copied!" : "Copy"}
          </button>
          <EvalSummary evaluation={evaluation} />
        </>
      )}
    </div>
  );
}

export default function History() {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [adCopyItems, setAdCopyItems] = useState([]);
  const [activeTab, setActiveTab] = useState("text");
  const [previewImage, setPreviewImage] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");
  const [campaigns, setCampaigns] = useState([]);
  const [selectedCampaignFilter, setSelectedCampaignFilter] = useState("");

  const loadHistory = async () => {
    setErrorMessage("");
    setIsLoading(true);
    try {
      const [historyData, campaignData] = await Promise.all([
        api.get("/api/ai/history?limit=50"),
        api.get("/api/campaigns"),
      ]);
      setItems(historyData?.text_items || historyData?.items || []);
      setAdCopyItems(historyData?.ad_copy_items || []);
      setCampaigns(campaignData?.campaigns || []);
    } catch (error) {
      setErrorMessage(error.message || "Failed to load history.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const filterByCampaign = (list) => {
    if (!selectedCampaignFilter) return list;
    return list.filter((item) => String(item.campaign_id) === selectedCampaignFilter);
  };

  const filteredItems = filterByCampaign(items);
  const filteredAdItems = filterByCampaign(adCopyItems);

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h3 className="pageTitle">History</h3>
        <div className="actionRow">
          <button
            className={activeTab === "text" ? "btn btnInline" : "btnGhost btnInline"}
            onClick={() => setActiveTab("text")}
          >
            Text
          </button>
          <button
            className={activeTab === "ad_copy" ? "btn btnInline" : "btnGhost btnInline"}
            onClick={() => setActiveTab("ad_copy")}
          >
            Ad Copy
          </button>
          <button className="btnGhost" onClick={loadHistory}>Refresh</button>
        </div>
      </div>

      {/* Campaign filter */}
      {campaigns.length > 0 && (
        <div className="sectionCard" style={{ padding: "10px 14px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <label style={{ fontSize: 13 }} className="muted">Filter by campaign:</label>
            <select
              value={selectedCampaignFilter}
              onChange={(e) => setSelectedCampaignFilter(e.target.value)}
              style={{ fontSize: 13, padding: "4px 8px", borderRadius: 6, border: "1px solid #24314a", background: "var(--card, #111827)", color: "inherit" }}
            >
              <option value="">All campaigns</option>
              {campaigns.map((c) => (
                <option key={c.id} value={String(c.id)}>{c.name}</option>
              ))}
            </select>
            {selectedCampaignFilter && (
              <button className="btnGhost" style={{ fontSize: 12 }} onClick={() => setSelectedCampaignFilter("")}>
                Clear
              </button>
            )}
          </div>
        </div>
      )}

      {isLoading ? <p className="muted">Loading history...</p> : null}
      {errorMessage ? <p className="statusError">{errorMessage}</p> : null}

      {!isLoading && !errorMessage && activeTab === "text" && filteredItems.length === 0 ? (
        <div className="sectionCard">
          <p className="muted">
            {selectedCampaignFilter ? "No text history for this campaign." : "No history yet. Generate and select content first."}
          </p>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
              Generate Content
            </button>
          </div>
        </div>
      ) : null}

      {!isLoading && !errorMessage && activeTab === "ad_copy" && filteredAdItems.length === 0 ? (
        <div className="sectionCard">
          <p className="muted">
            {selectedCampaignFilter ? "No ad copy for this campaign." : "No ad copy history yet."}
          </p>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
              Generate Ad Copy
            </button>
          </div>
        </div>
      ) : null}

      {activeTab === "text" && filteredItems.map((item) => {
        const campaignName = campaigns.find((c) => c.id === item.campaign_id)?.name;
        return (
          <div key={item.content_id} className="sectionCard">
            <div className="metaRow">
              <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                {campaignName && (
                  <span className="pill" style={{ fontSize: 11 }}>{campaignName}</span>
                )}
                {item.selected_variant ? (
                  <span style={{ fontSize: 12 }} className="muted">Saved: Variant {item.selected_variant}</span>
                ) : (
                  <span style={{ fontSize: 12, color: "#6b7280" }}>Not saved</span>
                )}
              </div>
            </div>
            {item.description ? (
              <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 6 }}>{item.description}</p>
            ) : null}
            <div style={{ display: "grid", gap: 8, marginTop: 10 }}>
              <VariantCard
                label="Variant A"
                text={item.variant_a_text}
                evaluation={item.evaluation_a}
                isSelected={item.selected_variant === "A"}
                collapsed={item.selected_variant === "B"}
              />
              <VariantCard
                label="Variant B"
                text={item.variant_b_text}
                evaluation={item.evaluation_b}
                isSelected={item.selected_variant === "B"}
                collapsed={item.selected_variant === "A"}
              />
            </div>
          </div>
        );
      })}

      {activeTab === "ad_copy" && filteredAdItems.map((item) => {
        const campaignName = campaigns.find((c) => c.id === item.campaign_id)?.name;
        return (
          <div key={item.content_id} className="sectionCard">
            <div className="metaRow">
              <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
              {campaignName && (
                <span className="pill" style={{ fontSize: 11 }}>{campaignName}</span>
              )}
            </div>
            {item.description ? (
              <p style={{ fontSize: 13, color: "#94a3b8", marginTop: 6 }}>{item.description}</p>
            ) : null}
            <div style={{ marginTop: 10 }}>
              {item.selected_image_base64 ? (
                <button
                  type="button"
                  onClick={() => setPreviewImage(item.selected_image_base64)}
                  style={{ padding: 0, border: "none", background: "transparent", cursor: "zoom-in", marginBottom: 8 }}
                  title="Tap to enlarge"
                >
                  <img
                    src={`data:image/png;base64,${item.selected_image_base64}`}
                    alt="Selected ad image"
                    style={{ width: 160, height: 110, objectFit: "cover", borderRadius: 10, border: "1px solid #24314a", display: "block" }}
                  />
                </button>
              ) : (
                <p className="muted" style={{ marginBottom: 8 }}>No image selected yet.</p>
              )}
              <p className="resultText">{item.ad_copy_text || item.variant_a_text}</p>
              <button
                className="btnGhost btnInline"
                style={{ fontSize: 11, marginTop: 6 }}
                onClick={() => copyToClipboard(item.ad_copy_text || item.variant_a_text || "")}
              >
                Copy
              </button>
              <EvalSummary evaluation={item.evaluation || item.evaluation_a} />
            </div>
          </div>
        );
      })}

      {previewImage ? (
        <div
          onClick={() => setPreviewImage("")}
          style={{ position: "fixed", inset: 0, background: "rgba(8,12,20,0.85)", display: "grid", placeItems: "center", zIndex: 1000, padding: 20 }}
        >
          <div onClick={(e) => e.stopPropagation()} style={{ maxWidth: "92vw", maxHeight: "90vh", display: "grid", gap: 10 }}>
            <img
              src={`data:image/png;base64,${previewImage}`}
              alt="Ad image enlarged"
              style={{ maxWidth: "92vw", maxHeight: "82vh", borderRadius: 12, border: "1px solid #24314a" }}
            />
            <button className="btnGhost" onClick={() => setPreviewImage("")}>Close</button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
