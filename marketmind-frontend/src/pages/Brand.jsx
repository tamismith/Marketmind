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
  const [status, setStatus] = useState(null);

  // Logo state
  const [logoDescription, setLogoDescription] = useState("");
  const [logoStyle, setLogoStyle] = useState("minimal");
  const [logoFeeling, setLogoFeeling] = useState("");
  const [logoShape, setLogoShape] = useState("");
  const [logoColours, setLogoColours] = useState("");
  const [showLogoContext, setShowLogoContext] = useState(false);
  const [generatedLogo, setGeneratedLogo] = useState("");
  const [isGeneratingLogo, setIsGeneratingLogo] = useState(false);
  const [isSavingLogo, setIsSavingLogo] = useState(false);
  const [logoStatus, setLogoStatus] = useState(null);

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

  async function handleGenerateLogo() {
    setLogoStatus(null);
    setIsGeneratingLogo(true);
    try {
      const data = await api.post("/api/logo/generate", {
        description: logoDescription,
        style: logoStyle,
        feeling: logoFeeling,
        shape: logoShape,
        colours: logoColours,
      });
      setGeneratedLogo(data.image_base64);
    } catch (err) {
      setLogoStatus({ type: "error", message: err.message || "Failed to generate logo." });
    } finally {
      setIsGeneratingLogo(false);
    }
  }

  async function handleSaveLogo() {
    setLogoStatus(null);
    setIsSavingLogo(true);
    try {
      await api.post("/api/logo/save", { image_base64: generatedLogo });
      setForm((prev) => ({ ...prev, logo_base64: generatedLogo }));
      setLogoStatus({ type: "success", message: "Logo saved to profile." });
    } catch (err) {
      setLogoStatus({ type: "error", message: err.message || "Failed to save logo." });
    } finally {
      setIsSavingLogo(false);
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
              <input className="input" name="business_name" value={form.business_name} onChange={handleChange} placeholder="e.g. Acme Co" />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Industry
              </label>
              <input className="input" name="industry" value={form.industry} onChange={handleChange} placeholder="e.g. Fashion, SaaS, Food & Drink" />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Target audience
              </label>
              <input className="input" name="target_audience" value={form.target_audience} onChange={handleChange} placeholder="e.g. Women 25–40 interested in sustainable fashion" />
            </div>

            <div>
              <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                Region
              </label>
              <input className="input" name="region" value={form.region} onChange={handleChange} placeholder="e.g. United Kingdom" />
            </div>

          </div>
        </div>

        <div className="actionRow">
          <button type="submit" className="btn btnInline" disabled={saving}>
            {saving ? "Saving…" : "Save Profile"}
          </button>
          {status && (
            <p className={status.type === "success" ? "statusSuccess" : "statusError"} style={{ alignSelf: "center", margin: 0 }}>
              {status.message}
            </p>
          )}
        </div>
      </form>

      {/* Logo section */}
      <div className="sectionCard">
        <h4 style={{ marginTop: 0, marginBottom: 4 }}>Logo</h4>
        <p className="muted" style={{ fontSize: 13, marginBottom: 14 }}>
          Generate a logo mark from a short brand description.
        </p>

        {form.logo_base64 && (
          <div style={{ marginBottom: 16 }}>
            <p className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Current logo</p>
            <img
              src={`data:image/png;base64,${form.logo_base64}`}
              alt="Saved brand logo"
              style={{ width: 140, height: 140, borderRadius: 10, border: "1px solid #24314a", objectFit: "contain", background: "#fff", display: "block" }}
            />
          </div>
        )}

        <div className="pageStack">
          <div>
            <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
              Describe your brand
            </label>
            <input
              className="input"
              value={logoDescription}
              onChange={(e) => setLogoDescription(e.target.value)}
              placeholder="e.g. sustainable fashion brand for young women"
            />
          </div>

          <div>
            <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
              Style
            </label>
            <select className="input" value={logoStyle} onChange={(e) => setLogoStyle(e.target.value)}>
              <option value="minimal">Minimal</option>
              <option value="modern">Modern</option>
              <option value="bold">Bold</option>
              <option value="classic">Classic</option>
            </select>
          </div>

          <button
            type="button"
            className="btnGhost btnInline"
            style={{ fontSize: 13 }}
            onClick={() => setShowLogoContext((prev) => !prev)}
          >
            {showLogoContext ? "Less options ▴" : "More options ▾"}
          </button>

          {showLogoContext && (
            <div className="pageStack">
              <div>
                <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                  Feeling
                </label>
                <select className="input" value={logoFeeling} onChange={(e) => setLogoFeeling(e.target.value)}>
                  <option value="">No preference</option>
                  <option value="premium">Premium</option>
                  <option value="playful">Playful</option>
                  <option value="trustworthy">Trustworthy</option>
                  <option value="bold">Bold</option>
                  <option value="calm">Calm</option>
                  <option value="energetic">Energetic</option>
                </select>
              </div>

              <div>
                <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                  Shape / Symbol
                </label>
                <select className="input" value={logoShape} onChange={(e) => setLogoShape(e.target.value)}>
                  <option value="">No preference</option>
                  <option value="abstract">Abstract mark</option>
                  <option value="monogram">Letter / Monogram</option>
                  <option value="geometric">Geometric shape</option>
                  <option value="nature">Nature / Organic</option>
                  <option value="badge">Badge / Emblem</option>
                  <option value="icon">Icon / Object</option>
                </select>
              </div>

              <div>
                <label className="muted" style={{ display: "block", marginBottom: 6, fontSize: 13 }}>
                  Colours
                </label>
                <select className="input" value={logoColours} onChange={(e) => setLogoColours(e.target.value)}>
                  <option value="">No preference</option>
                  <option value="teal_white">Teal &amp; White</option>
                  <option value="navy_gold">Navy &amp; Gold</option>
                  <option value="black_white">Black &amp; White</option>
                  <option value="earthy">Earthy Tones</option>
                  <option value="pastels">Pastels</option>
                  <option value="vibrant">Vibrant &amp; Bold</option>
                  <option value="monochrome">Monochrome</option>
                </select>
              </div>
            </div>
          )}

          <div className="actionRow">
            <button
              type="button"
              className="btn btnInline"
              onClick={handleGenerateLogo}
              disabled={isGeneratingLogo || !logoDescription.trim()}
            >
              {isGeneratingLogo ? "Generating…" : generatedLogo ? "Regenerate (3 credits)" : "Generate Logo (3 credits)"}
            </button>
            {logoStatus && (
              <p className={logoStatus.type === "success" ? "statusSuccess" : "statusError"} style={{ alignSelf: "center", margin: 0 }}>
                {logoStatus.message}
              </p>
            )}
          </div>

          {generatedLogo && (
            <div>
              <p className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Generated logo</p>
              <img
                src={`data:image/png;base64,${generatedLogo}`}
                alt="Generated logo"
                style={{ width: 140, height: 140, borderRadius: 10, border: "1px solid #24314a", objectFit: "contain", background: "#fff", display: "block", marginBottom: 12 }}
              />
              <button
                type="button"
                className="btn btnInline"
                onClick={handleSaveLogo}
                disabled={isSavingLogo}
              >
                {isSavingLogo ? "Saving…" : "Save to Profile"}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
