import { useEffect, useState } from "react";
import { api } from "../api/client";

const initialForm = {
  business_name: "",
  industry: "",
  target_audience: "",
  tone: "",
  platform: "",
  description: "",
  goal: "",
  length: "",
  region: "",
};

function EvalBlock({ evaluation }) {
  if (!evaluation) return null;
  const explanation = evaluation.explanation;

  return (
    <div style={{ marginTop: 10, fontSize: 14, color: "#a9b0bf" }}>
      <div>
        <strong style={{ color: "#eef1f6" }}>Overall feel:</strong> {evaluation.tone}
      </div>
      {typeof explanation === "string" && explanation ? (
        <div>
          <strong style={{ color: "#eef1f6" }}>Why:</strong> {explanation}
        </div>
      ) : null}
      {explanation && typeof explanation === "object" ? (
        <div style={{ marginTop: 6 }}>
          <strong style={{ color: "#eef1f6" }}>Why:</strong>
          {explanation.tone_summary ? <div>Tone: {explanation.tone_summary}</div> : null}
          {explanation.voice_summary ? <div>Voice: {explanation.voice_summary}</div> : null}
          {explanation.energy_summary ? <div>Energy: {explanation.energy_summary}</div> : null}
        </div>
      ) : null}
    </div>
  );
}

export default function Generate() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [memoryPreview, setMemoryPreview] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const loadMemoryPreview = async () => {
    try {
      const analytics = await api.get("/api/ai/analytics");
      const topTone = analytics?.best_brand_voice?.top_tone;
      const selectedSamples = analytics?.best_brand_voice?.selected_samples ?? 0;
      const topRegion = analytics?.regional_style_preference?.[0]?.region || null;
      const latestWeek = analytics?.weekly_tone_trend?.length
        ? analytics.weekly_tone_trend[analytics.weekly_tone_trend.length - 1]
        : null;

      setMemoryPreview({
        topTone,
        selectedSamples,
        topRegion,
        latestWeek,
      });
    } catch {
      setMemoryPreview(null);
    }
  };

  useEffect(() => {
    loadMemoryPreview();
  }, []);

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const onGenerate = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");
    setIsGenerating(true);

    try {
      const data = await api.post("/api/ai/generate/text", form);
      setResult(data);
    } catch (error) {
      setErrorMessage(error.message || "Failed to generate text.");
    } finally {
      setIsGenerating(false);
    }
  };

  const onSelectVariant = async (selectedVariant) => {
    if (!result?.content_id) return;

    setErrorMessage("");
    setSuccessMessage("");
    setIsSelecting(true);

    try {
      await api.post("/api/ai/select/text", {
        content_id: result.content_id,
        selected_variant: selectedVariant,
      });
      setSuccessMessage(
        `Variant ${selectedVariant} selected. Preference saved for future generations.`,
      );
      await loadMemoryPreview();
    } catch (error) {
      setErrorMessage(error.message || "Failed to save selection.");
    } finally {
      setIsSelecting(false);
    }
  };

  return (
    <div style={{ display: "grid", gap: 18 }}>
      <h3 style={{ margin: 0 }}>Generate Marketing Text</h3>

      <form className="form" onSubmit={onGenerate}>
        <input className="input" name="business_name" placeholder="Business name" value={form.business_name} onChange={onChange} required />
        <input className="input" name="industry" placeholder="Industry" value={form.industry} onChange={onChange} required />
        <input className="input" name="target_audience" placeholder="Target audience" value={form.target_audience} onChange={onChange} required />
        <input className="input" name="description" placeholder="Description" value={form.description} onChange={onChange} required />
        <input className="input" name="goal" placeholder="Goal (optional)" value={form.goal} onChange={onChange} />

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 10 }}>
          <input className="input" name="tone" placeholder="Tone" value={form.tone} onChange={onChange} required />
          <input className="input" name="platform" placeholder="Platform" value={form.platform} onChange={onChange} required />
          <input className="input" name="length" placeholder="Length" value={form.length} onChange={onChange} />
          <input className="input" name="region" placeholder="Region" value={form.region} onChange={onChange} />
        </div>

        <button className="btn" type="submit" disabled={isGenerating}>
          {isGenerating ? "Generating..." : "Generate A/B Variants"}
        </button>
      </form>

      {errorMessage ? (
        <p style={{ margin: 0, color: "#ffb4b4" }}>{errorMessage}</p>
      ) : null}
      {successMessage ? (
        <p style={{ margin: 0, color: "#9ee6b7" }}>{successMessage}</p>
      ) : null}

      <div style={{ border: "1px solid #2a2f3c", borderRadius: 12, padding: 14, background: "#11131a" }}>
        <h4 style={{ marginTop: 0, marginBottom: 8 }}>Brand Memory Preview</h4>
        {memoryPreview ? (
          <div style={{ color: "#a9b0bf", fontSize: 14, display: "grid", gap: 6 }}>
            <div>
              Preferred voice so far:{" "}
              <strong style={{ color: "#eef1f6" }}>
                {memoryPreview.topTone || "Not enough data yet"}
              </strong>
            </div>
            <div>
              Most selected region style:{" "}
              <strong style={{ color: "#eef1f6" }}>
                {memoryPreview.topRegion || "Not enough data yet"}
              </strong>
            </div>
            <div>
              Selections learned from:{" "}
              <strong style={{ color: "#eef1f6" }}>
                {memoryPreview.selectedSamples}
              </strong>
            </div>
            {memoryPreview.latestWeek ? (
              <div>
                Latest active week:{" "}
                <strong style={{ color: "#eef1f6" }}>
                  {memoryPreview.latestWeek.week_start_date} to {memoryPreview.latestWeek.week_end_date}
                </strong>
              </div>
            ) : null}
          </div>
        ) : (
          <p style={{ margin: 0, color: "#a9b0bf" }}>
            No memory insights yet. Select a few variants to build preferences.
          </p>
        )}
      </div>

      {result ? (
        <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(2, minmax(0, 1fr))" }}>
          <div style={{ border: "1px solid #2a2f3c", borderRadius: 12, padding: 14, background: "#11131a" }}>
            <h4 style={{ marginTop: 0 }}>Variant A</h4>
            <p style={{ whiteSpace: "pre-wrap" }}>{result.variant_a}</p>
            <EvalBlock evaluation={result.evaluation_a} />
            <button className="btn" style={{ marginTop: 10 }} onClick={() => onSelectVariant("A")} disabled={isSelecting}>
              {isSelecting ? "Saving..." : "Select A"}
            </button>
          </div>

          <div style={{ border: "1px solid #2a2f3c", borderRadius: 12, padding: 14, background: "#11131a" }}>
            <h4 style={{ marginTop: 0 }}>Variant B</h4>
            <p style={{ whiteSpace: "pre-wrap" }}>{result.variant_b}</p>
            <EvalBlock evaluation={result.evaluation_b} />
            <button className="btn" style={{ marginTop: 10 }} onClick={() => onSelectVariant("B")} disabled={isSelecting}>
              {isSelecting ? "Saving..." : "Select B"}
            </button>
          </div>
        </div>
      ) : null}

      <div style={{ border: "1px dashed #2a2f3c", borderRadius: 12, padding: 14 }}>
        <h4 style={{ marginTop: 0, marginBottom: 6 }}>Ad Copy (Placeholder)</h4>
        <p style={{ margin: 0, color: "#a9b0bf" }}>
          Ad copy and image generation UI will be added next. Backend endpoint exists at
          <code> /api/ai/ad-copy</code>.
        </p>
      </div>
    </div>
  );
}
