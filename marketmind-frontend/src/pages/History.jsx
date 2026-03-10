import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";

function EvalSummary({ evaluation }) {
  if (!evaluation) return <span>No evaluation</span>;
  const explanation = evaluation.explanation || {};
  return (
    <div style={{ fontSize: 13 }} className="muted">
      <div>Feel: {evaluation.tone || "unknown"}</div>
      {explanation.tone_summary ? <div>{explanation.tone_summary}</div> : null}
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

  const loadHistory = async () => {
    setErrorMessage("");
    setIsLoading(true);
    try {
      const data = await api.get("/api/ai/history?limit=20");
      setItems(data?.text_items || data?.items || []);
      setAdCopyItems(data?.ad_copy_items || []);
    } catch (error) {
      setErrorMessage(error.message || "Failed to load history.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

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

      {isLoading ? <p className="muted">Loading history...</p> : null}
      {errorMessage ? <p className="statusError">{errorMessage}</p> : null}
      {!isLoading && !errorMessage && activeTab === "text" && items.length === 0 ? (
        <div className="sectionCard">
          <p className="muted">No history yet. Generate and select content first.</p>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
              Generate Content
            </button>
            <button className="btnGhost btnInline" onClick={() => navigate("/app/analytics")}>
              Open Analytics
            </button>
          </div>
        </div>
      ) : null}

      {!isLoading && !errorMessage && activeTab === "ad_copy" && adCopyItems.length === 0 ? (
        <div className="sectionCard">
          <p className="muted">No ad copy history yet. Generate ad copy first.</p>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
              Generate Ad Copy
            </button>
          </div>
        </div>
      ) : null}

      {activeTab === "text" && items.map((item) => (
        <div key={item.content_id} className="sectionCard">
          <div className="metaRow">
            <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
            <span>Selected: {item.selected_variant || "Not selected"}</span>
          </div>

          <div className="gridCols2">
            <div>
              <h4 style={{ marginTop: 0, marginBottom: 6 }}>Variant A</h4>
              <p className="resultText">{item.variant_a_text}</p>
              <EvalSummary evaluation={item.evaluation_a} />
            </div>
            <div>
              <h4 style={{ marginTop: 0, marginBottom: 6 }}>Variant B</h4>
              <p className="resultText">{item.variant_b_text}</p>
              <EvalSummary evaluation={item.evaluation_b} />
            </div>
          </div>
        </div>
      ))}

      {activeTab === "ad_copy" && adCopyItems.map((item) => (
        <div key={item.content_id} className="sectionCard">
          <div className="metaRow">
            <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
            <span>Type: Ad Copy</span>
          </div>

          <div>
            <h4 style={{ marginTop: 0, marginBottom: 6 }}>Ad Copy</h4>
            {item.selected_image_base64 ? (
              <button
                type="button"
                onClick={() => setPreviewImage(item.selected_image_base64)}
                style={{
                  padding: 0,
                  border: "none",
                  background: "transparent",
                  cursor: "zoom-in",
                  marginBottom: 8,
                }}
                title="Tap to enlarge"
              >
                <img
                  src={`data:image/png;base64,${item.selected_image_base64}`}
                  alt="Selected ad image preview"
                  style={{
                    width: 160,
                    height: 110,
                    objectFit: "cover",
                    borderRadius: 10,
                    border: "1px solid #24314a",
                    display: "block",
                  }}
                />
              </button>
            ) : (
              <p className="muted" style={{ marginBottom: 8 }}>
                No image selected yet.
              </p>
            )}
            <p className="resultText">{item.ad_copy_text || item.variant_a_text}</p>
            <EvalSummary evaluation={item.evaluation || item.evaluation_a} />
          </div>
        </div>
      ))}

      {previewImage ? (
        <div
          onClick={() => setPreviewImage("")}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(8, 12, 20, 0.85)",
            display: "grid",
            placeItems: "center",
            zIndex: 1000,
            padding: 20,
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              maxWidth: "92vw",
              maxHeight: "90vh",
              display: "grid",
              gap: 10,
            }}
          >
            <img
              src={`data:image/png;base64,${previewImage}`}
              alt="Selected ad image enlarged"
              style={{
                maxWidth: "92vw",
                maxHeight: "82vh",
                borderRadius: 12,
                border: "1px solid #24314a",
              }}
            />
            <button className="btnGhost" onClick={() => setPreviewImage("")}>
              Close
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
