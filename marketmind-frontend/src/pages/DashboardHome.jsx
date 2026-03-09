import { useNavigate } from "react-router-dom";

export default function DashboardHome() {
  const navigate = useNavigate();

  return (
    <div>
      <h3 style={{ marginTop: 0, marginBottom: 8 }}>Welcome to MarketMind</h3>
      <p style={{ marginTop: 0, marginBottom: 16, color: "#a9b0bf" }}>
        You are signed in. Start by generating A/B content variants for your
        campaign.
      </p>

      <button className="btn" style={{ maxWidth: 240 }} onClick={() => navigate("/app/generate")}>
        Begin Generation
      </button>
    </div>
  );
}
