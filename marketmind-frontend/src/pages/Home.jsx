import { Link, useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const handleStart = () => {
    // for now: always go to login
    navigate("/login");
  };

  return (
    <div className="landingWrap">
      <section className="landingHero">
        <div className="landingBrand">MarketMind</div>
        <p className="landingTag">AI Marketing Platform for SMEs</p>
        <h1 className="landingTitle">
          Generate better campaigns with feedback-driven brand learning
        </h1>
        <p className="landingSubtitle">
          MarketMind helps you generate A/B marketing content, evaluate tone, save winning
          choices, and build a stronger brand voice over time.
        </p>

        <div className="landingActions">
          <button className="btn landingBtn" onClick={handleStart}>
            Begin Generation
          </button>
          <Link className="btnGhost landingBtnGhost" to="/register">
            Create Account
          </Link>
        </div>
      </section>

      <section className="landingGrid">
        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>A/B Content Generation</h3>
          <p className="muted">
            Generate two platform-ready variants per request and compare style before publishing.
          </p>
        </article>

        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Brand Memory Loop</h3>
          <p className="muted">
            Select preferred outputs and let your future prompts reflect those choices.
          </p>
        </article>

        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>History & Analytics</h3>
          <p className="muted">
            Review generation history and track tone and regional preference patterns.
          </p>
        </article>
      </section>

      <div className="helper-row">
        <span>Already have an account?</span>
        <Link className="link" to="/login">
          Log in
        </Link>
      </div>
    </div>
  );
}
