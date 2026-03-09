import { useEffect, useState } from "react";
import { api } from "../api/client";

function EvalSummary({ evaluation }) {
  if (!evaluation) return <span>No evaluation</span>;
  const explanation = evaluation.explanation || {};
  return (
    <div style={{ color: "#a9b0bf", fontSize: 13 }}>
      <div>Feel: {evaluation.tone || "unknown"}</div>
      {explanation.tone_summary ? <div>{explanation.tone_summary}</div> : null}
    </div>
  );
}

export default function History() {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  const loadHistory = async () => {
    setErrorMessage("");
    setIsLoading(true);
    try {
      const data = await api.get("/api/ai/history?limit=20");
      setItems(data?.items || []);
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
    <div style={{ display: "grid", gap: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h3 style={{ margin: 0 }}>History</h3>
        <button className="logout" onClick={loadHistory}>Refresh</button>
      </div>

      {isLoading ? <p style={{ margin: 0, color: "#a9b0bf" }}>Loading history...</p> : null}
      {errorMessage ? <p style={{ margin: 0, color: "#ffb4b4" }}>{errorMessage}</p> : null}
      {!isLoading && !errorMessage && items.length === 0 ? (
        <p style={{ margin: 0, color: "#a9b0bf" }}>No history yet. Generate and select content first.</p>
      ) : null}

      {items.map((item) => (
        <div
          key={item.content_id}
          style={{
            border: "1px solid #2a2f3c",
            borderRadius: 12,
            padding: 14,
            background: "#11131a",
            display: "grid",
            gap: 10,
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", color: "#a9b0bf", fontSize: 13 }}>
            <span>{item.created_at ? new Date(item.created_at).toLocaleString() : "Unknown date"}</span>
            <span>Selected: {item.selected_variant || "Not selected"}</span>
          </div>

          <div style={{ display: "grid", gap: 10, gridTemplateColumns: "repeat(2, minmax(0, 1fr))" }}>
            <div>
              <h4 style={{ marginTop: 0, marginBottom: 6 }}>Variant A</h4>
              <p style={{ marginTop: 0, whiteSpace: "pre-wrap" }}>{item.variant_a_text}</p>
              <EvalSummary evaluation={item.evaluation_a} />
            </div>
            <div>
              <h4 style={{ marginTop: 0, marginBottom: 6 }}>Variant B</h4>
              <p style={{ marginTop: 0, whiteSpace: "pre-wrap" }}>{item.variant_b_text}</p>
              <EvalSummary evaluation={item.evaluation_b} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
