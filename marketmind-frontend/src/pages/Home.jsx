import { Link, useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const handleStart = () => {
    // for now: always go to login
    navigate("/login");
  };

  return (
    <div className="page-center">
      <div className="card">
        <h2>MarketMind</h2>
        <p>
          AI-powered marketing assistant for SMEs — generate content, track tone, manage credits,
          and review history.
        </p>

        <div style={{ display: "grid", gap: 10, marginTop: 16 }}>
          <button className="btn" onClick={handleStart}>
            Start generating
          </button>

          <div className="helper-row">
            <span>Already have an account?</span>
            <Link className="link" to="/login">Log in</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
