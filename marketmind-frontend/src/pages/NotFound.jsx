import { useNavigate } from "react-router-dom";

export default function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="page-center">
      <div className="card">
        <h2>Page not found</h2>
        <p>You can return to the dashboard, start generating, or go back to the landing page.</p>
        <div className="actionRow" style={{ marginTop: 16 }}>
          <button className="btn btnInline" onClick={() => navigate("/app")}>
            Go to Dashboard
          </button>
          <button className="btnGhost btnInline" onClick={() => navigate("/app/generate")}>
            Generate Content
          </button>
          <button className="btnGhost btnInline" onClick={() => navigate("/")}>
            Landing Page
          </button>
        </div>
      </div>
    </div>
  );
}
