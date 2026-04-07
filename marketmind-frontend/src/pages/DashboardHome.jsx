import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../api/client";

export default function DashboardHome() {
  const navigate = useNavigate();
  const [savedTextItems, setSavedTextItems] = useState([]);
  const [savedAdItems, setSavedAdItems] = useState([]);
  const [isLoadingSaved, setIsLoadingSaved] = useState(true);
  const [businessName, setBusinessName] = useState(null);

  useEffect(() => {
    api.get("/api/business/profile")
      .then((data) => setBusinessName(data.business_name || null))
      .catch(() => setBusinessName(null));
  }, []);

  const loadSavedItems = async () => {
    setIsLoadingSaved(true);
    try {
      const data = await api.get("/api/ai/history?limit=10");
      const textItems = data?.text_items || data?.items || [];
      const adItems = data?.ad_copy_items || [];
      const selectedOnly = textItems.filter((item) => item.selected_variant);
      setSavedTextItems(selectedOnly.slice(0, 5));
      setSavedAdItems(adItems.slice(0, 5));
    } catch {
      setSavedTextItems([]);
      setSavedAdItems([]);
    } finally {
      setIsLoadingSaved(false);
    }
  };

  useEffect(() => {
    loadSavedItems();
  }, []);

  return (
    <div className="pageStack">
      <div className="sectionCard">
        <h3 style={{ marginTop: 0, marginBottom: 8 }}>
          Welcome back{businessName ? `, ${businessName}` : ""} 👋
        </h3>
        <p className="muted" style={{ marginBottom: 14 }}>
          Start with generation, then use history and analytics to refine your brand voice.
        </p>
        <div className="actionRow">
          <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
            Begin Generation
          </button>
          <button className="btnGhost btnInline" onClick={() => navigate("/app/history")}>
            View History
          </button>
          <button className="btnGhost btnInline" onClick={() => navigate("/app/analytics")}>
            Open Analytics
          </button>
        </div>
      </div>

      <div className="sectionCard">
        <div className="pageHeader">
          <h4 style={{ margin: 0 }}>Saved Content</h4>
          <button className="btnGhost" onClick={loadSavedItems}>Refresh</button>
        </div>
        {isLoadingSaved ? <p className="muted">Loading saved content...</p> : null}

        {!isLoadingSaved ? (
          <div className="gridCols2">
            <div className="sectionCard">
              <h4 style={{ marginTop: 0, marginBottom: 8 }}>Saved Text Selections</h4>
              {savedTextItems.length === 0 ? (
                <div>
                  <p className="muted">No saved text selections yet.</p>
                  <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
                    Generate Text
                  </button>
                </div>
              ) : (
                <div style={{ display: "grid", gap: 10 }}>
                  {savedTextItems.map((item) => (
                    <div key={item.content_id} className="sectionCard">
                      <div className="metaRow">
                        <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
                        <span>Saved: Variant {item.selected_variant}</span>
                      </div>
                      <p className="resultText" style={{ marginTop: 8 }}>
                        {item.selected_text || (item.selected_variant === "A" ? item.variant_a_text : item.variant_b_text)}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="sectionCard">
              <h4 style={{ marginTop: 0, marginBottom: 8 }}>Saved Ad Copy</h4>
              {savedAdItems.length === 0 ? (
                <div>
                  <p className="muted">No saved ad copy yet.</p>
                  <button className="btn btnInline" onClick={() => navigate("/app/generate")}>
                    Generate Ad Copy
                  </button>
                </div>
              ) : (
                <div style={{ display: "grid", gap: 10 }}>
                  {savedAdItems.map((item) => (
                    <div key={item.content_id} className="sectionCard">
                      <div className="metaRow">
                        <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
                        <span>Type: Ad Copy</span>
                      </div>
                      {item.selected_image_base64 ? (
                        <img
                          src={`data:image/png;base64,${item.selected_image_base64}`}
                          alt="Saved ad selection"
                          style={{
                            width: 160,
                            height: 110,
                            objectFit: "cover",
                            borderRadius: 10,
                            border: "1px solid #24314a",
                            marginTop: 8,
                            display: "block",
                          }}
                        />
                      ) : (
                        <p className="muted" style={{ marginTop: 8, marginBottom: 0 }}>
                          No image saved yet for this ad copy.
                        </p>
                      )}
                      <p className="resultText" style={{ marginTop: 8 }}>
                        {item.ad_copy_text || item.variant_a_text}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : null}

        {!isLoadingSaved ? (
          <div className="actionRow" style={{ marginTop: 12 }}>
            <button className="btnGhost btnInline" onClick={() => navigate("/app/history")}>
              View Full History
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
}
