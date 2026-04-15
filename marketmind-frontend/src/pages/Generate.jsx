import { useEffect, useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";

const initialForm = {
  tone: "",
  platform: "",
  description: "",
  goal: "",
  length: "",
  region: "",
};

const initialAdForm = {
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

function ScoreBar({ value, min = 0, max = 1, color = "#0ea5a3" }) {
  const pct = Math.round(((value - min) / (max - min)) * 100);
  return (
    <div style={{ background: "#1a2436", borderRadius: 4, height: 6, overflow: "hidden", marginTop: 4 }}>
      <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.4s ease" }} />
    </div>
  );
}

function EvalBlock({ evaluation }) {
  if (!evaluation) return null;
  const { tone_label, tone, vad, explanation, vad_alignment } = evaluation;
  const displayTone = tone_label || tone;

  return (
    <div className="evalBlock">

      {/* Tone / Valence */}
      <div style={{ marginBottom: 10 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <strong className="evalTitle">Overall feel</strong>
          <span className="muted" style={{ fontSize: 12 }}>{displayTone}</span>
        </div>
        {vad ? <ScoreBar value={vad.valence} min={-1} max={1} color="#0ea5a3" /> : null}
        {explanation?.tone_summary ? (
          <p className="muted" style={{ fontSize: 12, marginTop: 5 }}>{explanation.tone_summary}</p>
        ) : null}
      </div>

      {/* Energy / Arousal */}
      {vad ? (
        <div style={{ marginBottom: 10 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong className="evalTitle">Energy</strong>
            <span className="muted" style={{ fontSize: 12 }}>{vad.arousal_label}</span>
          </div>
          <ScoreBar value={vad.arousal} min={0} max={1} color="#f59e0b" />
          {explanation?.energy_summary ? (
            <p className="muted" style={{ fontSize: 12, marginTop: 5 }}>{explanation.energy_summary}</p>
          ) : null}
        </div>
      ) : null}

      {/* Voice / Dominance */}
      {vad ? (
        <div>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <strong className="evalTitle">Voice</strong>
            <span className="muted" style={{ fontSize: 12 }}>{vad.dominance_label}</span>
          </div>
          <ScoreBar value={vad.dominance} min={0} max={1} color="#8b5cf6" />
          {explanation?.voice_summary ? (
            <p className="muted" style={{ fontSize: 12, marginTop: 5 }}>{explanation.voice_summary}</p>
          ) : null}
        </div>
      ) : null}

      {/* Target Alignment */}
      {vad_alignment?.overall != null ? (
        <div style={{ marginTop: 10, paddingTop: 10, borderTop: "1px solid #1e2d45" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <strong className="evalTitle">Target Alignment</strong>
            <span style={{ color: "#0ea5a3", fontWeight: 600, fontSize: 13 }}>
              {Math.round(vad_alignment.overall * 100)}%
            </span>
          </div>
          {vad_alignment.valence != null ? (
            <div style={{ marginBottom: 4 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span className="muted" style={{ fontSize: 12 }}>Feel</span>
                <span className="muted" style={{ fontSize: 12 }}>{Math.round(vad_alignment.valence * 100)}%</span>
              </div>
              <ScoreBar value={vad_alignment.valence} min={0} max={1} color="#0ea5a3" />
            </div>
          ) : null}
          {vad_alignment.arousal != null ? (
            <div style={{ marginBottom: 4 }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span className="muted" style={{ fontSize: 12 }}>Energy</span>
                <span className="muted" style={{ fontSize: 12 }}>{Math.round(vad_alignment.arousal * 100)}%</span>
              </div>
              <ScoreBar value={vad_alignment.arousal} min={0} max={1} color="#f59e0b" />
            </div>
          ) : null}
          {vad_alignment.dominance != null ? (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span className="muted" style={{ fontSize: 12 }}>Voice</span>
                <span className="muted" style={{ fontSize: 12 }}>{Math.round(vad_alignment.dominance * 100)}%</span>
              </div>
              <ScoreBar value={vad_alignment.dominance} min={0} max={1} color="#8b5cf6" />
            </div>
          ) : null}
        </div>
      ) : null}

    </div>
  );
}

function EvalComparison({ evalA, evalB }) {
  if (!evalA || !evalB) return null;

  const THRESHOLD = 0.05;

  function compareRow(label, valA, valB, labelA, labelB) {
    const diff = valA - valB;
    let verdict;
    if (Math.abs(diff) < THRESHOLD) {
      verdict = "Similar";
    } else if (diff > 0) {
      verdict = "A scores higher";
    } else {
      verdict = "B scores higher";
    }
    return { label, labelA, labelB, verdict, valA, valB };
  }

  const rows = [
    compareRow(
      "Overall feel",
      evalA.score ?? 0,
      evalB.score ?? 0,
      evalA.tone_label || evalA.tone || "—",
      evalB.tone_label || evalB.tone || "—",
    ),
    compareRow(
      "Energy",
      evalA.vad?.arousal ?? 0,
      evalB.vad?.arousal ?? 0,
      evalA.vad?.arousal_label || "—",
      evalB.vad?.arousal_label || "—",
    ),
    compareRow(
      "Voice",
      evalA.vad?.dominance ?? 0,
      evalB.vad?.dominance ?? 0,
      evalA.vad?.dominance_label || "—",
      evalB.vad?.dominance_label || "—",
    ),
  ];

  const allSimilar = rows.every((r) => r.verdict === "Similar");

  return (
    <div className="sectionCard">
      <h4 style={{ marginTop: 0, marginBottom: 12 }}>A vs B Comparison</h4>
      {allSimilar ? (
        <p className="muted" style={{ fontSize: 13 }}>
          Both variants score similarly across all dimensions.
        </p>
      ) : (
        <div style={{ display: "grid", gap: 10 }}>
          {rows.map(({ label, labelA, labelB, verdict, valA, valB }) => (
            <div
              key={label}
              style={{
                display: "grid",
                gridTemplateColumns: "110px 1fr 1fr 1fr",
                alignItems: "center",
                gap: 8,
              }}
            >
              <strong className="evalTitle" style={{ fontSize: 12 }}>{label}</strong>
              <span className="muted" style={{ fontSize: 12 }}>
                A: {labelA}{" "}
                <span style={{ color: "#6b7280", fontSize: 11 }}>({valA.toFixed(2)})</span>
              </span>
              <span className="muted" style={{ fontSize: 12 }}>
                B: {labelB}{" "}
                <span style={{ color: "#6b7280", fontSize: 11 }}>({valB.toFixed(2)})</span>
              </span>
              <span
                style={{
                  fontSize: 12,
                  color: verdict === "Similar" ? "#6b7280" : "#0ea5a3",
                  fontWeight: verdict !== "Similar" ? 600 : 400,
                }}
              >
                {verdict === "Similar" ? "— Similar" : `→ ${verdict}`}
              </span>
            </div>
          ))}
        </div>
      )}
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
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAdGenerating, setIsAdGenerating] = useState(false);
  const [isSelecting, setIsSelecting] = useState(false);
  const [isSavingAdImage, setIsSavingAdImage] = useState(false);
  const [pendingTextSelection, setPendingTextSelection] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [adErrorMessage, setAdErrorMessage] = useState("");
  const [adSuccessMessage, setAdSuccessMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [showTextAdvanced, setShowTextAdvanced] = useState(false);
  const [showAdAdvanced, setShowAdAdvanced] = useState(false);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [isRegeneratingAd, setIsRegeneratingAd] = useState(false);
  const [regenInstruction, setRegenInstruction] = useState("");
  const [editedVariantA, setEditedVariantA] = useState("");
  const [editedVariantB, setEditedVariantB] = useState("");
  const [reEvalA, setReEvalA] = useState(null);
  const [reEvalB, setReEvalB] = useState(null);
  const [isReEvaluatingA, setIsReEvaluatingA] = useState(false);
  const [isReEvaluatingB, setIsReEvaluatingB] = useState(false);
  const [profile, setProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [campaigns, setCampaigns] = useState([]);
  const [selectedCampaignId, setSelectedCampaignId] = useState("");


  useEffect(() => {
    api.get("/api/business/profile")
      .then((data) => setProfile(data))
      .catch(() => setProfile(null))
      .finally(() => setProfileLoading(false));
    api.get("/api/campaigns")
      .then((data) => {
        const list = data.campaigns || [];
        setCampaigns(list);
        if (list.length > 0) setSelectedCampaignId(String(list[0].id));
      })
      .catch(() => setCampaigns([]));
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
      const payload = {
        ...form,
        business_name: profile?.business_name || "",
        industry: profile?.industry || "",
        target_audience: profile?.target_audience || "",
        region: form.region || profile?.region || "",
        campaign_id: selectedCampaignId ? parseInt(selectedCampaignId) : null,
      };
      const data = await api.post("/api/ai/generate/text", payload);
      setResult(data);
      setEditedVariantA(data.variant_a || "");
      setEditedVariantB(data.variant_b || "");
      setReEvalA(null);
      setReEvalB(null);
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
      const payload = {
        ...adForm,
        business_name: profile?.business_name || "",
        industry: profile?.industry || "",
        target_audience: profile?.target_audience || "",
        region: adForm.region || profile?.region || "",
        campaign_id: selectedCampaignId ? parseInt(selectedCampaignId) : null,
      };
      const data = await api.post("/api/ai/ad-copy", payload);
      setAdResult(data);
      const defaultId = data?.image_options?.[0]?.id || "";
      setSelectedAdImageId(defaultId);
      if ((!data?.image_options || data.image_options.length === 0) && data?.image_warnings?.length) {
        setAdErrorMessage("Image provider timed out. Ad copy was generated, but image options are temporarily unavailable. Please retry.");
      }
    } catch (error) {
      setAdErrorMessage(error.message || "Failed to generate ad copy.");
    } finally {
      setIsAdGenerating(false);
    }
  };

  const onRegenerate = async () => {
    if (!result?.content_id) return;
    setErrorMessage("");
    setSuccessMessage("");
    setIsRegenerating(true);
    try {
      const data = await api.post("/api/ai/regenerate/text", { content_id: result.content_id, instruction: regenInstruction });
      setResult((prev) => ({ ...prev, ...data }));
      setPendingTextSelection("");
    } catch (error) {
      setErrorMessage(error.message || "Failed to regenerate.");
    } finally {
      setIsRegenerating(false);
    }
  };

  const onRegenerateAd = async () => {
    if (!adResult?.content_id) return;
    setAdErrorMessage("");
    setAdSuccessMessage("");
    setIsRegeneratingAd(true);
    try {
      const data = await api.post("/api/ai/regenerate/ad-copy", { content_id: adResult.content_id });
      setAdResult((prev) => ({ ...prev, ad_copy: data.ad_copy, evaluation: data.evaluation }));
    } catch (error) {
      setAdErrorMessage(error.message || "Failed to regenerate ad copy.");
    } finally {
      setIsRegeneratingAd(false);
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

      {!profileLoading && (
        <div className="sectionCard">
          {profile?.business_name && profile?.industry && profile?.target_audience && profile?.region ? (
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span className="muted" style={{ fontSize: 13 }}>
                <strong className="evalTitle">{profile.business_name}</strong>
                {" · "}{profile.industry}
                {" · "}{profile.target_audience}
                {" · "}{profile.region}
              </span>
              <Link to="/app/brand" className="link" style={{ fontSize: 13, whiteSpace: "nowrap", marginLeft: 12 }}>
                Edit Profile →
              </Link>
            </div>
          ) : (
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span className="muted" style={{ fontSize: 13 }}>
                Complete your brand profile to speed up generation
              </span>
              <Link to="/app/brand" className="link" style={{ fontSize: 13, whiteSpace: "nowrap", marginLeft: 12 }}>
                Set up Brand Profile →
              </Link>
            </div>
          )}
        </div>
      )}

      {/* Campaign selector */}
      {campaigns.length > 0 && (() => {
        const selected = campaigns.find((c) => String(c.id) === String(selectedCampaignId));
        return (
          <div className="sectionCard">
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <label className="muted" style={{ fontSize: 13 }}>Campaign</label>
                <Link to="/app/campaigns" className="link" style={{ fontSize: 13 }}>Manage →</Link>
              </div>
              <select
                className="input"
                value={selectedCampaignId}
                onChange={(e) => setSelectedCampaignId(e.target.value)}
              >
                {campaigns.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              {selected && (
                <div className="muted" style={{ fontSize: 12, display: "flex", gap: 12 }}>
                  {selected.goal && <span>Goal: {selected.goal}</span>}
                  {selected.target_valence != null && (
                    <span>Feel {selected.target_valence?.toFixed(2)} · Energy {selected.target_arousal?.toFixed(2)} · Voice {selected.target_dominance?.toFixed(2)}</span>
                  )}
                  {selected.target_valence == null && <span>No emotional targets set</span>}
                </div>
              )}
            </div>
          </div>
        );
      })()}

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
            {/* Required fields */}
            <input className="input" name="description" placeholder="Description" value={form.description} onChange={onChange} required />

            <div className="formGrid4">
              <input className="input" name="tone" placeholder="Tone (optional if campaign VAD set)" value={form.tone} onChange={onChange} />
              <input className="input" name="platform" placeholder="Platform" value={form.platform} onChange={onChange} required />
            </div>

            {/* Advanced toggle */}
            <button
              type="button"
              className="btnGhost btnInline"
              style={{ fontSize: 13, marginTop: 4 }}
              onClick={() => setShowTextAdvanced((prev) => !prev)}
            >
              {showTextAdvanced ? "Advanced Settings ▴" : "Advanced Settings ▾"}
            </button>

            {/* Advanced fields */}
            {showTextAdvanced ? (
              <div className="formGrid4" style={{ marginTop: 8 }}>
                <input className="input" name="goal" placeholder="Goal (optional)" value={form.goal} onChange={onChange} />
                <input className="input" name="length" placeholder="Length" value={form.length} onChange={onChange} />
                <input className="input" name="region" placeholder="Region override" value={form.region} onChange={onChange} />
              </div>
            ) : null}

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


      {activeMode === "text" && result ? (
        <div className="gridCols2">
          <div className="sectionCard">
            <h4 style={{ marginTop: 0 }}>Variant A</h4>
            <textarea
              className="resultText"
              style={{ width: "100%", minHeight: 100, resize: "vertical", background: "var(--card, #111827)", color: "inherit", border: "1px solid #24314a", borderRadius: 6, padding: 8, fontFamily: "inherit", fontSize: "inherit" }}
              value={editedVariantA}
              onChange={(e) => setEditedVariantA(e.target.value)}
            />
            <button
              className="btnGhost btnInline"
              style={{ marginTop: 6, fontSize: 12 }}
              disabled={isReEvaluatingA}
              onClick={async () => {
                setIsReEvaluatingA(true);
                try {
                  const data = await api.post("/api/ai/evaluate", {
                    text: editedVariantA,
                    campaign_id: selectedCampaignId ? parseInt(selectedCampaignId) : null,
                  });
                  setReEvalA(data.evaluation);
                } finally {
                  setIsReEvaluatingA(false);
                }
              }}
            >
              {isReEvaluatingA ? "Evaluating..." : "Re-evaluate"}
            </button>
            <EvalBlock evaluation={reEvalA || result.evaluation_a} />
            {reEvalA && <p className="muted" style={{ fontSize: 11, marginTop: 4 }}>Showing re-evaluated scores</p>}
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
            <textarea
              className="resultText"
              style={{ width: "100%", minHeight: 100, resize: "vertical", background: "var(--card, #111827)", color: "inherit", border: "1px solid #24314a", borderRadius: 6, padding: 8, fontFamily: "inherit", fontSize: "inherit" }}
              value={editedVariantB}
              onChange={(e) => setEditedVariantB(e.target.value)}
            />
            <button
              className="btnGhost btnInline"
              style={{ marginTop: 6, fontSize: 12 }}
              disabled={isReEvaluatingB}
              onClick={async () => {
                setIsReEvaluatingB(true);
                try {
                  const data = await api.post("/api/ai/evaluate", {
                    text: editedVariantB,
                    campaign_id: selectedCampaignId ? parseInt(selectedCampaignId) : null,
                  });
                  setReEvalB(data.evaluation);
                } finally {
                  setIsReEvaluatingB(false);
                }
              }}
            >
              {isReEvaluatingB ? "Evaluating..." : "Re-evaluate"}
            </button>
            <EvalBlock evaluation={reEvalB || result.evaluation_b} />
            {reEvalB && <p className="muted" style={{ fontSize: 11, marginTop: 4 }}>Showing re-evaluated scores</p>}
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
        <EvalComparison evalA={result.evaluation_a} evalB={result.evaluation_b} />
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
          <div style={{ marginTop: 12 }}>
            <input
              type="text"
              className="input"
              placeholder='Regeneration instruction e.g. "make it more urgent"'
              value={regenInstruction}
              onChange={(e) => setRegenInstruction(e.target.value)}
              style={{ width: "100%" }}
            />
          </div>
          <div className="actionRow" style={{ marginTop: 10 }}>
            <button
              className="btn btnInline"
              onClick={onSaveSelectedVariant}
              disabled={!pendingTextSelection || isSelecting}
            >
              {isSelecting ? "Saving..." : "Save Selected Variant"}
            </button>
            <button
              className="btnGhost btnInline"
              onClick={onRegenerate}
              disabled={isRegenerating}
            >
              {isRegenerating ? "Regenerating..." : "Regenerate (1 credit)"}
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
            {/* Required fields */}
            <input className="input" name="description" placeholder="Description" value={adForm.description} onChange={onAdChange} required />

            <div className="formGrid4">
              <input className="input" name="tone" placeholder="Tone" value={adForm.tone} onChange={onAdChange} required />
              <input className="input" name="platform" placeholder="Platform" value={adForm.platform} onChange={onAdChange} required />
            </div>

            {/* Advanced toggle */}
            <button
              type="button"
              className="btnGhost btnInline"
              style={{ fontSize: 13, marginTop: 4 }}
              onClick={() => setShowAdAdvanced((prev) => !prev)}
            >
              {showAdAdvanced ? "Advanced Settings ▴" : "Advanced Settings ▾"}
            </button>

            {/* Advanced fields */}
            {showAdAdvanced ? (
              <>
                <div className="formGrid4" style={{ marginTop: 8 }}>
                  <input className="input" name="goal" placeholder="Goal (optional)" value={adForm.goal} onChange={onAdChange} />
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
                  <input className="input" name="color_palette" placeholder="Palette (earthy, pastel, vibrant...)" value={adForm.color_palette} onChange={onAdChange} />
                </div>

                <div className="gridCols2">
                  <input className="input" name="include_keywords" placeholder="Include keywords (comma-separated)" value={adForm.include_keywords} onChange={onAdChange} />
                  <input className="input" name="avoid_keywords" placeholder="Avoid keywords (comma-separated)" value={adForm.avoid_keywords} onChange={onAdChange} />
                </div>

                <label className="muted" style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <input type="checkbox" name="high_quality" checked={adForm.high_quality} onChange={onAdChange} />
                  High quality image mode (sharper, slower)
                </label>
              </>
            ) : null}

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
          {adResult ? (
            <div className="actionRow" style={{ marginTop: 10 }}>
              <button
                type="button"
                className="btnGhost btnInline"
                onClick={onRegenerateAd}
                disabled={isRegeneratingAd}
              >
                {isRegeneratingAd ? "Regenerating..." : "Regenerate Copy (1 credit)"}
              </button>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
