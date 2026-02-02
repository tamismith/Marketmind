import { useState } from "react";

const defaultForm = {
  business_name: "Green Brew Cafe",
  industry: "Coffee shop",
  target_audience: "Students",
  tone: "Friendly",
  platform: "Instagram",
  description: "Affordable coffee and snacks near campus",
  goal: "Increase foot traffic",
  length: "short",
  region: "UK",
  offer: "10% off with student ID",
  cta: "Pop in today",
};

export default function App() {
  const [form, setForm] = useState(defaultForm);
  const [health, setHealth] = useState(null);
  const [caption, setCaption] = useState("");
  const [adCopy, setAdCopy] = useState("");
  const [imageBase64, setImageBase64] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const update = (key, value) => setForm((p) => ({ ...p, [key]: value }));

  async function checkHealth() {
    setError("");
    try {
      const res = await fetch("/api/ai/health");
      const data = await res.json();
      setHealth(data.status || "ok");
    } catch (e) {
      setHealth(null);
      setError("Health check failed. Is the backend running on port 5001?");
    }
  }

  async function generateCaption() {
    setLoading(true);
    setError("");
    setCaption("");
    try {
      const payload = {
        business_name: form.business_name,
        industry: form.industry,
        target_audience: form.target_audience,
        tone: form.tone,
        platform: form.platform,
        description: form.description,
        goal: form.goal,
        length: form.length,
        region: form.region,
      };

      const res = await fetch("/api/ai/caption", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.message || "Caption request failed");
      setCaption(data.caption || "");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function generateAd() {
    setLoading(true);
    setError("");
    setAdCopy("");
    setImageBase64("");
    try {
      const payload = {
        business_name: form.business_name,
        industry: form.industry,
        target_audience: form.target_audience,
        tone: form.tone,
        platform: form.platform,
        description: form.description,
        goal: form.goal,
        length: form.length,
        region: form.region,
        offer: form.offer,
        cta: form.cta,
      };

      const res = await fetch("/api/ai/ad-copy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.message || "Ad request failed");

      setAdCopy(data.ad_copy || "");
      setImageBase64(data.image_base64 || "");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ fontFamily: "system-ui", maxWidth: 900, margin: "40px auto", padding: 20 }}>
      <h1 style={{ marginBottom: 4 }}>MarketMind Demo</h1>
      <p style={{ marginTop: 0, opacity: 0.7 }}>Minimal frontend for interview demonstration</p>

      <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 20 }}>
        <button onClick={checkHealth}>Check API Health</button>
        <span>
          Status:{" "}
          <b style={{ color: health ? "green" : "gray" }}>
            {health ? health : "unknown"}
          </b>
        </span>
      </div>

      {error && (
        <div style={{ background: "#ffe5e5", border: "1px solid #ffb3b3", padding: 12, marginBottom: 20 }}>
          <b>Error:</b> {error}
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        {[
          ["business_name", "Business name"],
          ["industry", "Industry"],
          ["target_audience", "Target audience"],
          ["tone", "Tone"],
          ["platform", "Platform"],
          ["region", "Region"],
          ["goal", "Goal"],
          ["length", "Length (short/medium)"],
        ].map(([k, label]) => (
          <label key={k} style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            <span style={{ fontSize: 13, opacity: 0.8 }}>{label}</span>
            <input
              value={form[k]}
              onChange={(e) => update(k, e.target.value)}
              style={{ padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
            />
          </label>
        ))}

        <label style={{ gridColumn: "1 / -1", display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 13, opacity: 0.8 }}>Description</span>
          <textarea
            value={form.description}
            onChange={(e) => update("description", e.target.value)}
            rows={3}
            style={{ padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
          />
        </label>

        <label style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 13, opacity: 0.8 }}>Offer (ad only)</span>
          <input
            value={form.offer}
            onChange={(e) => update("offer", e.target.value)}
            style={{ padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
          />
        </label>

        <label style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          <span style={{ fontSize: 13, opacity: 0.8 }}>CTA (ad only)</span>
          <input
            value={form.cta}
            onChange={(e) => update("cta", e.target.value)}
            style={{ padding: 10, borderRadius: 8, border: "1px solid #ddd" }}
          />
        </label>
      </div>

      <div style={{ display: "flex", gap: 10, marginTop: 18 }}>
        <button onClick={generateCaption} disabled={loading}>
          {loading ? "Working..." : "Generate Caption"}
        </button>
        <button onClick={generateAd} disabled={loading}>
          {loading ? "Working..." : "Generate Ad Copy"}
        </button>
      </div>

      <div style={{ marginTop: 22, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        <div style={{ border: "1px solid #eee", borderRadius: 10, padding: 14 }}>
          <h3 style={{ marginTop: 0 }}>Caption Output</h3>
          <div style={{ whiteSpace: "pre-wrap", minHeight: 80 }}>{caption || "—"}</div>
        </div>

        <div style={{ border: "1px solid #eee", borderRadius: 10, padding: 14 }}>
          <h3 style={{ marginTop: 0 }}>Ad Copy Output</h3>
          <div style={{ whiteSpace: "pre-wrap", minHeight: 80 }}>{adCopy || "—"}</div>

          {imageBase64 ? (
            <div style={{ marginTop: 12 }}>
              <h4 style={{ margin: "10px 0" }}>Generated Image</h4>
              <img
                src={`data:image/png;base64,${imageBase64}`}
                alt="Generated ad"
                style={{ width: "100%", borderRadius: 10, border: "1px solid #ddd" }}
              />
            </div>
          ) : (
            <p style={{ opacity: 0.6, marginTop: 10 }}>No image returned (or generation failed).</p>
          )}
        </div>
      </div>
    </div>
  );
}
