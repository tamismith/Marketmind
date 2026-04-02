import { useEffect, useState } from "react";
import { api } from "../api/client";

function ScoreBar({ value, min = -1, max = 1, color = "#0ea5a3" }) {
  const pct = Math.round(((value - min) / (max - min)) * 100);
  return (
    <div style={{ background: "#1a2436", borderRadius: 4, height: 6, overflow: "hidden", marginTop: 4 }}>
      <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 4, transition: "width 0.4s ease" }} />
    </div>
  );
}

function VadSliders({ valence, arousal, dominance, onChange }) {
  return (
    <div style={{ display: "grid", gap: 10 }}>
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
          <span className="muted" style={{ fontSize: 12 }}>Overall Feel (Valence)</span>
          <span className="muted" style={{ fontSize: 12 }}>{valence.toFixed(2)}</span>
        </div>
        <input type="range" min={-1} max={1} step={0.05} value={valence}
          onChange={(e) => onChange("target_valence", parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: "#0ea5a3" }} />
      </div>
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
          <span className="muted" style={{ fontSize: 12 }}>Energy (Arousal)</span>
          <span className="muted" style={{ fontSize: 12 }}>{arousal.toFixed(2)}</span>
        </div>
        <input type="range" min={0} max={1} step={0.05} value={arousal}
          onChange={(e) => onChange("target_arousal", parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: "#f59e0b" }} />
      </div>
      <div>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
          <span className="muted" style={{ fontSize: 12 }}>Voice (Dominance)</span>
          <span className="muted" style={{ fontSize: 12 }}>{dominance.toFixed(2)}</span>
        </div>
        <input type="range" min={0} max={1} step={0.05} value={dominance}
          onChange={(e) => onChange("target_dominance", parseFloat(e.target.value))}
          style={{ width: "100%", accentColor: "#8b5cf6" }} />
      </div>
    </div>
  );
}

const EMPTY_FORM = {
  name: "",
  goal: "",
  target_valence: 0,
  target_arousal: 0.5,
  target_dominance: 0.5,
  vadEnabled: false,
};

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [createForm, setCreateForm] = useState(EMPTY_FORM);
  const [isCreating, setIsCreating] = useState(false);
  const [createError, setCreateError] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [isSaving, setIsSaving] = useState(false);
  const [editError, setEditError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    fetchCampaigns();
  }, []);

  async function fetchCampaigns() {
    try {
      const data = await api.get("/api/campaigns");
      setCampaigns(data.campaigns || []);
    } catch {
      setCampaigns([]);
    } finally {
      setLoading(false);
    }
  }

  function handleCreateChange(field, value) {
    setCreateForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleCreate(e) {
    e.preventDefault();
    setCreateError("");
    setIsCreating(true);
    try {
      const payload = {
        name: createForm.name,
        goal: createForm.goal,
        ...(createForm.vadEnabled ? {
          target_valence: createForm.target_valence,
          target_arousal: createForm.target_arousal,
          target_dominance: createForm.target_dominance,
        } : {}),
      };
      const newCampaign = await api.post("/api/campaigns", payload);
      setCampaigns((prev) => [...prev, newCampaign]);
      setCreateForm(EMPTY_FORM);
      setShowCreate(false);
    } catch (err) {
      setCreateError(err.message || "Failed to create campaign.");
    } finally {
      setIsCreating(false);
    }
  }

  function startEdit(campaign) {
    setEditingId(campaign.id);
    setEditForm({
      name: campaign.name,
      goal: campaign.goal || "",
      target_valence: campaign.target_valence ?? 0,
      target_arousal: campaign.target_arousal ?? 0.5,
      target_dominance: campaign.target_dominance ?? 0.5,
      vadEnabled: campaign.target_valence != null,
    });
    setEditError("");
  }

  function handleEditChange(field, value) {
    setEditForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSave(id) {
    setEditError("");
    setIsSaving(true);
    try {
      const payload = {
        name: editForm.name,
        goal: editForm.goal,
        target_valence: editForm.vadEnabled ? editForm.target_valence : null,
        target_arousal: editForm.vadEnabled ? editForm.target_arousal : null,
        target_dominance: editForm.vadEnabled ? editForm.target_dominance : null,
      };
      const updated = await api.put(`/api/campaigns/${id}`, payload);
      setCampaigns((prev) => prev.map((c) => (c.id === id ? updated : c)));
      setEditingId(null);
    } catch (err) {
      setEditError(err.message || "Failed to save campaign.");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleDelete(id) {
    setDeletingId(id);
    try {
      await api.delete(`/api/campaigns/${id}`);
      setCampaigns((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      console.error("Failed to delete campaign:", err.message);
    } finally {
      setDeletingId(null);
    }
  }

  function vadSummary(c) {
    if (c.target_valence == null) return "No emotional targets set";
    return `Feel ${c.target_valence?.toFixed(2)} · Energy ${c.target_arousal?.toFixed(2)} · Voice ${c.target_dominance?.toFixed(2)}`;
  }

  if (loading) return <div className="pageStack"><p className="muted">Loading campaigns…</p></div>;

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h2 className="pageTitle">Campaigns</h2>
        <button className="btn btnInline" onClick={() => setShowCreate((prev) => !prev)}>
          {showCreate ? "Cancel" : "+ New Campaign"}
        </button>
      </div>

      <p className="muted" style={{ marginTop: 0 }}>
        Campaigns let you set a goal and emotional targets that are applied automatically when you generate content.
      </p>

      {/* Create form */}
      {showCreate && (
        <div className="sectionCard">
          <h4 style={{ marginTop: 0, marginBottom: 12 }}>New Campaign</h4>
          <form className="pageStack" onSubmit={handleCreate}>
            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>Campaign name</label>
              <input className="input" value={createForm.name} onChange={(e) => handleCreateChange("name", e.target.value)} placeholder="e.g. Summer Sale 2026" required />
            </div>
            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>Goal (optional)</label>
              <input className="input" value={createForm.goal} onChange={(e) => handleCreateChange("goal", e.target.value)} placeholder="e.g. Increase conversions" />
            </div>

            <label className="muted" style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
              <input type="checkbox" checked={createForm.vadEnabled} onChange={(e) => handleCreateChange("vadEnabled", e.target.checked)} />
              Set emotional targets
            </label>

            {createForm.vadEnabled && (
              <VadSliders
                valence={createForm.target_valence}
                arousal={createForm.target_arousal}
                dominance={createForm.target_dominance}
                onChange={handleCreateChange}
              />
            )}

            {createError && <p className="statusError">{createError}</p>}

            <div className="actionRow">
              <button type="submit" className="btn btnInline" disabled={isCreating}>
                {isCreating ? "Creating…" : "Create Campaign"}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Campaign list */}
      {campaigns.map((c) => (
        <div key={c.id} className="sectionCard">
          {editingId === c.id ? (
            /* Edit mode */
            <div className="pageStack">
              <div>
                <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>Campaign name</label>
                <input className="input" value={editForm.name} onChange={(e) => handleEditChange("name", e.target.value)} />
              </div>
              <div>
                <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>Goal</label>
                <input className="input" value={editForm.goal} onChange={(e) => handleEditChange("goal", e.target.value)} placeholder="e.g. Increase conversions" />
              </div>

              <label className="muted" style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
                <input type="checkbox" checked={editForm.vadEnabled} onChange={(e) => handleEditChange("vadEnabled", e.target.checked)} />
                Set emotional targets
              </label>

              {editForm.vadEnabled && (
                <VadSliders
                  valence={editForm.target_valence}
                  arousal={editForm.target_arousal}
                  dominance={editForm.target_dominance}
                  onChange={handleEditChange}
                />
              )}

              {editError && <p className="statusError">{editError}</p>}

              <div className="actionRow">
                <button className="btn btnInline" onClick={() => handleSave(c.id)} disabled={isSaving}>
                  {isSaving ? "Saving…" : "Save"}
                </button>
                <button className="btnGhost btnInline" onClick={() => setEditingId(null)}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            /* View mode */
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 12 }}>
              <div style={{ display: "grid", gap: 4 }}>
                <strong className="evalTitle">{c.name}</strong>
                <span className="muted" style={{ fontSize: 13 }}>
                  {c.goal ? `Goal: ${c.goal}` : "No goal set"}
                </span>
                <span className="muted" style={{ fontSize: 12 }}>{vadSummary(c)}</span>
              </div>
              <div className="actionRow" style={{ flexShrink: 0 }}>
                <button className="btnGhost btnInline" style={{ minWidth: "auto", padding: "6px 12px" }} onClick={() => startEdit(c)}>
                  Edit
                </button>
                {c.name !== "General" && (
                  <button
                    className="btnGhost btnInline"
                    style={{ minWidth: "auto", padding: "6px 12px", color: "#ffb4b4", borderColor: "rgba(255,100,100,0.3)" }}
                    onClick={() => handleDelete(c.id)}
                    disabled={deletingId === c.id}
                  >
                    {deletingId === c.id ? "…" : "Delete"}
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      ))}

      {campaigns.length === 0 && (
        <div className="sectionCardDashed" style={{ textAlign: "center", padding: 24 }}>
          <p className="muted">No campaigns yet. Create one to get started.</p>
        </div>
      )}
    </div>
  );
}
