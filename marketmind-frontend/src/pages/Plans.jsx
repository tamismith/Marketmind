import { useEffect, useState } from "react";
import { api } from "../api/client";

const TIERS = [
  {
    key: "free",
    label: "Free",
    price: "£0",
    period: "",
    credits: 50,
    description: "Perfect for trying out MarketMind.",
    features: ["50 credits", "Text A/B generation", "Ad copy + image generation", "Brand memory"],
    package: null,
  },
  {
    key: "starter",
    label: "Starter",
    price: "£9.99",
    period: "/mo",
    credits: 200,
    description: "For solo entrepreneurs getting started.",
    features: ["200 credits", "All Free features", "Campaign management", "Priority support"],
    package: "starter_monthly",
    highlight: false,
  },
  {
    key: "pro",
    label: "Pro",
    price: "£24.99",
    period: "/mo",
    credits: 600,
    description: "For growing small businesses.",
    features: ["600 credits", "All Starter features", "Advanced analytics", "Logo generation"],
    package: "pro_monthly",
    highlight: true,
  },
  {
    key: "enterprise",
    label: "Enterprise",
    price: "£49.99",
    period: "/mo",
    credits: 2000,
    description: "For agencies managing multiple brands.",
    features: ["2,000 credits", "All Pro features", "Multiple business profiles", "Dedicated support"],
    package: "enterprise_monthly",
    highlight: false,
  },
];

const TOPUP = {
  key: "topup_100",
  label: "Top-up Pack",
  price: "£4.99",
  credits: 100,
  description: "One-off credit boost — no subscription needed.",
  package: "topup_100",
};

export default function Plans() {
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const loadUser = async () => {
    try {
      const data = await api.get("/auth/me");
      setUserInfo(data);
    } catch {
      setUserInfo(null);
    } finally {
      setLoading(false);
    }
  };

  const loadTransactions = async () => {
    try {
      const data = await api.get("/auth/transactions");
      setTransactions(data.transactions || []);
    } catch {
      setTransactions([]);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const handlePurchase = async (packageKey, label) => {
    setSuccessMsg("");
    setErrorMsg("");
    setPurchasing(packageKey);
    try {
      const result = await api.post("/auth/purchase", { package: packageKey });
      setSuccessMsg(
        `Purchase simulated: ${label}. ${result.credits_added} credits added. Balance: ${result.credits} credits.`
      );
      setUserInfo((prev) => ({
        ...prev,
        credits: result.credits,
        subscription_tier: result.subscription_tier,
      }));
      if (showHistory) loadTransactions();
    } catch (err) {
      setErrorMsg(err.message || "Purchase failed.");
    } finally {
      setPurchasing("");
    }
  };

  const handleShowHistory = () => {
    if (!showHistory) loadTransactions();
    setShowHistory((v) => !v);
  };

  if (loading) {
    return (
      <div className="pageStack">
        <p className="muted">Loading...</p>
      </div>
    );
  }

  return (
    <div className="pageStack">
      <div className="sectionCard">
        <div className="pageHeader">
          <div>
            <h3 style={{ margin: 0 }}>Plans &amp; Credits</h3>
            <p className="muted" style={{ marginTop: 4, marginBottom: 0 }}>
              This is a simulated purchase flow — no real payment is processed.
            </p>
          </div>
          {userInfo && (
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 13, color: "#94a3b8" }}>Current balance</div>
              <div style={{ fontSize: 22, fontWeight: 700, color: "#0ea5a3" }}>
                {userInfo.credits} credits
              </div>
              <div style={{ fontSize: 12, color: "#94a3b8", textTransform: "capitalize" }}>
                {userInfo.subscription_tier} plan
              </div>
            </div>
          )}
        </div>
      </div>

      {successMsg && (
        <div className="sectionCard">
          <p className="statusSuccess" style={{ margin: 0 }}>{successMsg}</p>
        </div>
      )}
      {errorMsg && (
        <div className="sectionCard">
          <p className="statusError" style={{ margin: 0 }}>{errorMsg}</p>
        </div>
      )}

      {/* Subscription tiers */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 14 }}>
        {TIERS.map((tier) => {
          const isCurrent = userInfo?.subscription_tier === tier.key;
          return (
            <div
              key={tier.key}
              className="sectionCard"
              style={{
                borderColor: tier.highlight ? "#0ea5a3" : isCurrent ? "#4ade80" : undefined,
                boxShadow: tier.highlight ? "0 0 0 2px rgba(14,165,163,0.25)" : undefined,
                position: "relative",
              }}
            >
              {tier.highlight && (
                <div
                  style={{
                    position: "absolute",
                    top: -10,
                    left: "50%",
                    transform: "translateX(-50%)",
                    background: "#0ea5a3",
                    color: "#fff",
                    fontSize: 11,
                    fontWeight: 700,
                    padding: "2px 10px",
                    borderRadius: 20,
                    letterSpacing: 1,
                  }}
                >
                  MOST POPULAR
                </div>
              )}
              {isCurrent && (
                <div className="pill" style={{ marginBottom: 8, fontSize: 11 }}>Current plan</div>
              )}
              <h4 style={{ margin: "0 0 4px" }}>{tier.label}</h4>
              <div style={{ fontSize: 24, fontWeight: 700, color: "#0ea5a3" }}>
                {tier.price}
                <span style={{ fontSize: 13, fontWeight: 400, color: "#94a3b8" }}>{tier.period}</span>
              </div>
              <p className="muted" style={{ fontSize: 13, marginTop: 4 }}>{tier.description}</p>
              <ul style={{ paddingLeft: 16, margin: "10px 0", fontSize: 13, color: "#cbd5e1" }}>
                {tier.features.map((f) => (
                  <li key={f} style={{ marginBottom: 4 }}>{f}</li>
                ))}
              </ul>
              {tier.package ? (
                <button
                  className={tier.highlight ? "btn" : "btnGhost"}
                  style={{ width: "100%", marginTop: 8 }}
                  onClick={() => handlePurchase(tier.package, tier.label)}
                  disabled={!!purchasing || isCurrent}
                >
                  {purchasing === tier.package
                    ? "Processing..."
                    : isCurrent
                    ? "Current plan"
                    : `Simulate Purchase`}
                </button>
              ) : (
                <div
                  className="muted"
                  style={{ textAlign: "center", marginTop: 10, fontSize: 13 }}
                >
                  Your current free tier
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* One-off top-up */}
      <div className="sectionCard">
        <div className="pageHeader">
          <div>
            <h4 style={{ margin: 0 }}>{TOPUP.label}</h4>
            <p className="muted" style={{ margin: "4px 0 0" }}>{TOPUP.description}</p>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <span style={{ fontSize: 20, fontWeight: 700, color: "#0ea5a3" }}>
              {TOPUP.price}
            </span>
            <span className="muted" style={{ fontSize: 13 }}>+{TOPUP.credits} credits</span>
            <button
              className="btn btnInline"
              onClick={() => handlePurchase(TOPUP.package, TOPUP.label)}
              disabled={!!purchasing}
            >
              {purchasing === TOPUP.package ? "Processing..." : "Buy Top-up"}
            </button>
          </div>
        </div>
      </div>

      {/* Credit cost reference */}
      <div className="sectionCard">
        <h4 style={{ marginTop: 0, marginBottom: 10 }}>Credit costs</h4>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
          <thead>
            <tr style={{ color: "#94a3b8", textAlign: "left" }}>
              <th style={{ paddingBottom: 6 }}>Action</th>
              <th style={{ paddingBottom: 6, textAlign: "right" }}>Credits</th>
            </tr>
          </thead>
          <tbody>
            {[
              ["Text A/B generation", 2],
              ["Ad copy + image generation", 5],
              ["Regenerate with modification", 1],
              ["Logo generation", 1],
            ].map(([action, cost]) => (
              <tr key={action} style={{ borderTop: "1px solid #1e2d45" }}>
                <td style={{ padding: "7px 0", color: "#cbd5e1" }}>{action}</td>
                <td style={{ padding: "7px 0", textAlign: "right", color: "#0ea5a3", fontWeight: 600 }}>
                  {cost}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Transaction history */}
      <div className="sectionCard">
        <div className="pageHeader">
          <h4 style={{ margin: 0 }}>Transaction History</h4>
          <button className="btnGhost" onClick={handleShowHistory}>
            {showHistory ? "Hide" : "Show"}
          </button>
        </div>

        {showHistory && (
          <div style={{ marginTop: 10 }}>
            {transactions.length === 0 ? (
              <p className="muted">No transactions yet.</p>
            ) : (
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
                <thead>
                  <tr style={{ color: "#94a3b8", textAlign: "left" }}>
                    <th style={{ paddingBottom: 6 }}>Date</th>
                    <th style={{ paddingBottom: 6 }}>Description</th>
                    <th style={{ paddingBottom: 6, textAlign: "right" }}>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((t) => (
                    <tr key={t.id} style={{ borderTop: "1px solid #1e2d45" }}>
                      <td style={{ padding: "6px 0", color: "#94a3b8" }}>
                        {t.created_at ? new Date(t.created_at).toLocaleDateString() : "—"}
                      </td>
                      <td style={{ padding: "6px 0", color: "#cbd5e1" }}>{t.description}</td>
                      <td
                        style={{
                          padding: "6px 0",
                          textAlign: "right",
                          fontWeight: 600,
                          color: t.amount > 0 ? "#4ade80" : "#f87171",
                        }}
                      >
                        {t.amount > 0 ? `+${t.amount}` : t.amount}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
