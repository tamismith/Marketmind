import { useEffect, useState } from "react";
import { api } from "../api/client";

const EMPTY = {
  business_name: "",
  industry: "",
  target_audience: "",
  region: "",
  logo_base64: "",
};

export default function Brand() {
  const [form, setForm] = useState(EMPTY);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState(null); // { type: "success" | "error", message }

  // Load existing profile on mount
  useEffect(() => {
    api
      .get("/api/business/profile")
      .then((data) => {
        setForm({
          business_name: data.business_name || "",
          industry: data.industry || "",
          target_audience: data.target_audience || "",
          region: data.region || "",
          logo_base64: data.logo_base64 || "",
        });
      })
      .catch(() => setStatus({ type: "error", message: "Failed to load profile." }))
      .finally(() => setLoading(false));
  }, []);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
    setStatus(null);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setStatus(null);
    try {
      await api.put("/api/business/profile", form);
      setStatus({ type: "success", message: "Profile saved." });
    } catch (err) {
      setStatus({ type: "error", message: err.message || "Failed to save profile." });
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="pageStack">
        <p className="muted">Loading profile…</p>
      </div>
    );
  }

  return (
    <div className="pageStack">
      <div className="pageHeader">
        <h2 className="pageTitle">Brand Profile</h2>
      </div>

      <p className="muted" style={{ marginTop: 0 }}>
        This information is used to pre-fill your generation forms so you don't have to repeat
        yourself every time.
      </p>

      <form className="pageStack" onSubmit={handleSubmit}>
        <div className="sectionCard">
          <div className="pageStack">

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Business name
              </label>
              <input
                className="input"
                name="business_name"
                value={form.business_name}
                onChange={handleChange}
                placeholder="e.g. Acme Co"
              />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Industry
              </label>
              <input
                className="input"
                name="industry"
                value={form.industry}
                onChange={handleChange}
                placeholder="e.g. Fashion, SaaS, Food & Drink"
              />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Target audience
              </label>
              <input
                className="input"
                name="target_audience"
                value={form.target_audience}
                onChange={handleChange}
                placeholder="e.g. Women 25–40 interested in sustainable fashion"
              />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Region
              </label>
              <input
                className="input"
                name="region"
                value={form.region}
                onChange={handleChange}
                placeholder="e.g. United Kingdom"
              />
            </div>

          </div>
        </div>

        <div className="actionRow">
          <button
            type="submit"
            className="btn btnInline"
            disabled={saving}
          >
            {saving ? "Saving…" : "Save Profile"}
          </button>

          {status && (
            <p
              className={status.type === "success" ? "statusSuccess" : "statusError"}
              style={{ alignSelf: "center", margin: 0 }}
            >
              {status.message}
            </p>
          )}
        </div>
      </form>
    </div>
  );
}
