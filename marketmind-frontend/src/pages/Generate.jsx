import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
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

const initialAdForm = {
  business_name: "",
  industry: "",
  target_audience: "",
  tone: "",
  platform: "",
  description: "",
  goal: "",
  length: "",
  region: "",
  offer: "",
  cta: "",
  color_palette: "",
  high_quality: true,
  style_preset: "realistic",
  aspect_ratio: "1:1",
  shot_type: "medium",
  include_keywords: "",
  avoid_keywords: "",
};

function EvalBlock({ evaluation }) {
  if (!evaluation) return null;
  const explanation = evaluation.explanation;

  return (
    <div className="evalBlock">
      <div>
        <strong className="evalTitle">Overall feel:</strong> {evaluation.tone}
      </div>
      {typeof explanation === "string" && explanation ? (
        <div>
          <strong className="evalTitle">Why:</strong> {explanation}
        </div>
      ) : null}
      {explanation && typeof explanation === "object" ? (
        <div>
          <strong className="evalTitle">Why:</strong>
          {explanation.tone_summary ? <div>Tone: {explanation.tone_summary}</div> : null}
          {explanation.voice_summary ? <div>Voice: {explanation.voice_summary}</div> : null}
          {explanation.energy_summary ? <div>Energy: {explanation.energy_summary}</div> : null}
        </div>
      ) : null}
    </div>
  );
}

export default function Generate() {
  const navigate = useNavigate();
  const [activeMode, setActiveMode] = useState("text");
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [adForm, setAdForm] = useState(initialAdForm);
  const [adResult, setAdResult] = useState(null);
  const [selectedAdImageId, setSelectedAdImageId] = useState("");
  const [memoryPreview, setMemoryPreview] = useState(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAdGenerating, setIsAdGenerating] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);
  const [isSavingAdImage, setIsSavingAdImage] = useState(false);
  const [pendingTextSelection, setPendingTextSelection] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [adErrorMessage, setAdErrorMessage] = useState("");
  const [adSuccessMessage, setAdSuccessMessage] = useState("");
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

  const onAdChange = (e) => {
    const { name, value, type, checked } = e.target;
    setAdForm((prev) => ({ ...prev, [name]: type === "checkbox" ? checked : value }));
  };

  const onGenerate = async (e) => {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");
    setIsGenerating(true);

    try {
      const data = await api.post("/api/ai/generate/text", form);
      setResult(data);
      setPendingTextSelection("");
    } catch (error) {
      setErrorMessage(error.message || "Failed to generate text.");
    } finally {
      setIsGenerating(false);
    }
  };

  const onSaveSelectedVariant = async () => {
    if (!result?.content_id || !pendingTextSelection) return;

    setErrorMessage("");
    setSuccessMessage("");
    setIsSelecting(true);

    try {
      await api.post("/api/ai/select/text", {
        content_id: result.content_id,
        selected_variant: pendingTextSelection,
      });
      setSuccessMessage(
        `Variant ${pendingTextSelection} saved. You can now track it in History and Dashboard.`,
      );
      await loadMemoryPreview();
    } catch (error) {
      setErrorMessage(error.message || "Failed to save selection.");
    } finally {
      setIsSelecting(false);
    }
  };

  const onGenerateAdCopy = async (e) => {
    e.preventDefault();
    setAdErrorMessage("");
    setAdSuccessMessage("");
    setIsAdGenerating(true);

    try {
      const data = await api.post("/api/ai/ad-copy", adForm);
      setAdResult(data);
      const defaultId = data?.image_options?.[0]?.id || "";
      setSelectedAdImageId(defaultId);
    } catch (error) {
      setAdErrorMessage(error.message || "Failed to generate ad copy.");
    } finally {
      setIsAdGenerating(false);
    }
  };

  const onSaveAdImage = async (option) => {
    if (!adResult?.content_id || !option?.id || !option?.image_base64) {
      setAdErrorMessage("Missing image selection details. Please regenerate and try again.");
      return;
    }
    setAdErrorMessage("");
    setAdSuccessMessage("");
    setIsSavingAdImage(true);
    try {
      await api.post("/api/ai/select/ad-image", {
        content_id: adResult.content_id,
        image_option_id: option.id,
        image_base64: option.image_base64,
      });
      setSelectedAdImageId(option.id);
      setAdSuccessMessage(`Image option "${option.label}" saved. Check Dashboard or History.`);
    } catch (error) {
      setAdErrorMessage(error.message || "Failed to save selected image.");
    } finally {
      setIsSavingAdImage(false);
    }
  };

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h3 className="pageTitle">Generate Marketing Text</h3>
      </div>

      <div className="actionRow">
        <button
          className={activeMode === "text" ? "btn btnInline" : "btnGhost btnInline"}
          onClick={() => setActiveMode("text")}
        >
          Text Generation
        </button>
        <button
          className={activeMode === "ad" ? "btn btnInline" : "btnGhost btnInline"}
          onClick={() => setActiveMode("ad")}
        >
          Ad Copy + Image
        </button>
      </div>

      {activeMode === "text" ? (
        <div className="sectionCard">
          <form className="form" onSubmit={onGenerate}>
            <input className="input" name="business_name" placeholder="Business name" value={form.business_name} onChange={onChange} required />
            <input className="input" name="industry" placeholder="Industry" value={form.industry} onChange={onChange} required />
            <input className="input" name="target_audience" placeholder="Target audience" value={form.target_audience} onChange={onChange} required />
            <input className="input" name="description" placeholder="Description" value={form.description} onChange={onChange} required />
            <input className="input" name="goal" placeholder="Goal (optional)" value={form.goal} onChange={onChange} />

            <div className="formGrid4">
              <input className="input" name="tone" placeholder="Tone" value={form.tone} onChange={onChange} required />
              <input className="input" name="platform" placeholder="Platform" value={form.platform} onChange={onChange} required />
              <input className="input" name="length" placeholder="Length" value={form.length} onChange={onChange} />
              <input className="input" name="region" placeholder="Region" value={form.region} onChange={onChange} />
            </div>

            <button className="btn" type="submit" disabled={isGenerating}>
              {isGenerating ? "Generating..." : "Generate A/B Variants"}
            </button>
          </form>
        </div>
      ) : null}

      {activeMode === "text" && errorMessage ? (
        <p className="statusError">{errorMessage}</p>
      ) : null}
      {activeMode === "text" && successMessage ? (
        <div className="sectionCard">
          <p className="statusSuccess">{successMessage}</p>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button className="btnGhost btnInline" onClick={() => navigate("/app/history")}>
              Go to History
            </button>
            <button className="btnGhost btnInline" onClick={() => navigate("/app/analytics")}>
              Go to Analytics
            </button>
          </div>
        </div>
      ) : null}

      {activeMode === "text" ? (
        <div className="sectionCard">
          <h4 style={{ marginTop: 0, marginBottom: 8 }}>Brand Memory Preview</h4>
          {memoryPreview ? (
            <div style={{ display: "grid", gap: 6 }} className="muted">
              <div>
                Preferred voice so far:{" "}
                <strong className="evalTitle">
                  {memoryPreview.topTone || "Not enough data yet"}
                </strong>
              </div>
              <div>
                Most selected region style:{" "}
                <strong className="evalTitle">
                  {memoryPreview.topRegion || "Not enough data yet"}
                </strong>
              </div>
              <div>
                Selections learned from:{" "}
                <strong className="evalTitle">
                  {memoryPreview.selectedSamples}
                </strong>
              </div>
              {memoryPreview.latestWeek ? (
                <div>
                  Latest active week:{" "}
                  <strong className="evalTitle">
                    {memoryPreview.latestWeek.week_start_date} to {memoryPreview.latestWeek.week_end_date}
                  </strong>
                </div>
              ) : null}
            </div>
          ) : (
            <p className="muted">
              No memory insights yet. Select a few variants to build preferences.
            </p>
          )}
        </div>
      ) : null}

      {activeMode === "text" && result ? (
        <div className="gridCols2">
          <div className="sectionCard">
            <h4 style={{ marginTop: 0 }}>Variant A</h4>
            <p className="resultText">{result.variant_a}</p>
            <EvalBlock evaluation={result.evaluation_a} />
            <button
              className={pendingTextSelection === "A" ? "btn" : "btnGhost"}
              style={{ marginTop: 10, width: "100%" }}
              onClick={() => setPendingTextSelection("A")}
            >
              {pendingTextSelection === "A" ? "Chosen A" : "Choose A"}
            </button>
          </div>

          <div className="sectionCard">
            <h4 style={{ marginTop: 0 }}>Variant B</h4>
            <p className="resultText">{result.variant_b}</p>
            <EvalBlock evaluation={result.evaluation_b} />
            <button
              className={pendingTextSelection === "B" ? "btn" : "btnGhost"}
              style={{ marginTop: 10, width: "100%" }}
              onClick={() => setPendingTextSelection("B")}
            >
              {pendingTextSelection === "B" ? "Chosen B" : "Choose B"}
            </button>
          </div>
        </div>
      ) : null}

      {activeMode === "text" && result ? (
        <div className="sectionCard">
          <div className="metaRow">
            <span>
              Selected for save:{" "}
              <strong className="evalTitle">
                {pendingTextSelection ? `Variant ${pendingTextSelection}` : "None yet"}
              </strong>
            </span>
          </div>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button
              className="btn btnInline"
              onClick={onSaveSelectedVariant}
              disabled={!pendingTextSelection || isSelecting}
            >
              {isSelecting ? "Saving..." : "Save Selected Variant"}
            </button>
            <button className="btnGhost btnInline" onClick={() => navigate("/app/history")}>
              View Saved History
            </button>
          </div>
        </div>
      ) : null}

      {activeMode === "ad" ? (
        <div className="sectionCard">
          <h4 style={{ marginTop: 0, marginBottom: 6 }}>Generate Ad Copy + Image</h4>
          <p className="muted" style={{ marginBottom: 12 }}>
            Create conversion-focused ad copy with a matching image.
          </p>

          <form className="form" onSubmit={onGenerateAdCopy}>
            <input className="input" name="business_name" placeholder="Business name" value={adForm.business_name} onChange={onAdChange} required />
            <input className="input" name="industry" placeholder="Industry" value={adForm.industry} onChange={onAdChange} required />
            <input className="input" name="target_audience" placeholder="Target audience" value={adForm.target_audience} onChange={onAdChange} required />
            <input className="input" name="description" placeholder="Description" value={adForm.description} onChange={onAdChange} required />
            <input className="input" name="goal" placeholder="Goal (optional)" value={adForm.goal} onChange={onAdChange} />

            <div className="formGrid4">
              <input className="input" name="tone" placeholder="Tone" value={adForm.tone} onChange={onAdChange} required />
              <input className="input" name="platform" placeholder="Platform" value={adForm.platform} onChange={onAdChange} required />
              <input className="input" name="length" placeholder="Length" value={adForm.length} onChange={onAdChange} />
              <input className="input" name="region" placeholder="Region" value={adForm.region} onChange={onAdChange} />
            </div>

            <div className="gridCols2">
              <input className="input" name="offer" placeholder="Offer (optional)" value={adForm.offer} onChange={onAdChange} />
              <input className="input" name="cta" placeholder="CTA (optional)" value={adForm.cta} onChange={onAdChange} />
            </div>

            <div className="formGrid4">
              <select className="input" name="style_preset" value={adForm.style_preset} onChange={onAdChange}>
                <option value="realistic">Style: Realistic</option>
                <option value="bold">Style: Bold</option>
                <option value="minimal">Style: Minimal</option>
                <option value="warm">Style: Warm</option>
              </select>
              <select className="input" name="aspect_ratio" value={adForm.aspect_ratio} onChange={onAdChange}>
                <option value="1:1">Aspect: 1:1</option>
                <option value="4:5">Aspect: 4:5</option>
                <option value="16:9">Aspect: 16:9</option>
              </select>
              <select className="input" name="shot_type" value={adForm.shot_type} onChange={onAdChange}>
                <option value="close_up">Shot: Close-up</option>
                <option value="medium">Shot: Medium</option>
                <option value="wide">Shot: Wide</option>
              </select>
              <input
                className="input"
                name="color_palette"
                placeholder="Palette (earthy, pastel, vibrant...)"
                value={adForm.color_palette}
                onChange={onAdChange}
              />
            </div>

            <div className="gridCols2">
              <input
                className="input"
                name="include_keywords"
                placeholder="Include keywords (comma-separated)"
                value={adForm.include_keywords}
                onChange={onAdChange}
              />
              <input
                className="input"
                name="avoid_keywords"
                placeholder="Avoid keywords (comma-separated)"
                value={adForm.avoid_keywords}
                onChange={onAdChange}
              />
            </div>

            <label className="muted" style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <input
                type="checkbox"
                name="high_quality"
                checked={adForm.high_quality}
                onChange={onAdChange}
              />
              High quality image mode (sharper, slower)
            </label>

            <button className="btn" type="submit" disabled={isAdGenerating}>
              {isAdGenerating ? "Generating ad..." : "Generate Ad Copy"}
            </button>
          </form>

          {adErrorMessage ? <p className="statusError" style={{ marginTop: 12 }}>{adErrorMessage}</p> : null}
          {adSuccessMessage ? <p className="statusSuccess" style={{ marginTop: 12 }}>{adSuccessMessage}</p> : null}

          {adResult ? (
            <div className="gridCols2" style={{ marginTop: 14 }}>
              <div className="sectionCard">
                <h4 style={{ marginTop: 0 }}>Ad Copy</h4>
                <p className="resultText">{adResult.ad_copy}</p>
                <EvalBlock evaluation={adResult.evaluation} />
              </div>
              <div className="sectionCard">
                <h4 style={{ marginTop: 0, marginBottom: 8 }}>Image Options</h4>
                {adResult.image_options && adResult.image_options.length > 0 ? (
                  <div style={{ display: "grid", gap: 10 }}>
                    {adResult.image_options.map((option) => {
                      const isSelected = selectedAdImageId === option.id;
                      return (
                        <div
                          key={option.id}
                          className="sectionCard"
                          style={{
                            borderColor: isSelected ? "#0ea5a3" : undefined,
                            boxShadow: isSelected ? "0 0 0 2px rgba(14, 165, 163, 0.2)" : "none",
                          }}
                        >
                          <div className="metaRow">
                            <strong className="evalTitle">{option.label}</strong>
                            <span>{option.creativity_level}</span>
                          </div>
                          <img
                            src={`data:image/png;base64,${option.image_base64}`}
                            alt={`${option.label} ad visual option`}
                            style={{ width: "100%", borderRadius: 10, border: "1px solid #24314a", marginTop: 8 }}
                          />
                          <button
                            type="button"
                            className={isSelected ? "btn" : "btnGhost"}
                            style={{ marginTop: 10, width: "100%" }}
                            onClick={() => onSaveAdImage(option)}
                            disabled={isSavingAdImage}
                          >
                            {isSavingAdImage && isSelected ? "Saving..." : isSelected ? "Saved" : "Use This Image"}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                ) : adResult.image_base64 ? (
                  <div>
                    <p className="muted" style={{ marginBottom: 8 }}>Fallback image (single option).</p>
                    <img
                      src={`data:image/png;base64,${adResult.image_base64}`}
                      alt="Generated ad visual"
                      style={{ width: "100%", borderRadius: 10, border: "1px solid #24314a" }}
                    />
                  </div>
                ) : (
                  <p className="muted">No image returned for this request.</p>
                )}
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
