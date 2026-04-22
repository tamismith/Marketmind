import { Link, useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  const handleStart = () => {
    navigate("/login");
  };

  return (
    <div className="landingWrap">
      <section className="landingHero">
        <div className="landingBrand">MarketMind</div>
        <p className="landingTag">AI Marketing Platform for SMEs</p>
        <h1 className="landingTitle">
          Generate smarter marketing content that learns your brand over time
        </h1>
        <p className="landingSubtitle">
          MarketMind generates two ready-to-use marketing variants for your chosen platform,
          evaluates their tone and emotional style, and remembers the choices you make so
          every future generation feels more like you.
        </p>

        <div className="landingActions">
          <button className="btn landingBtn" onClick={handleStart}>
            Get Started
          </button>
          <Link className="btnGhost landingBtnGhost" to="/register">
            Create Account
          </Link>
        </div>
      </section>

      <section className="landingHow">
        <h2 style={{ textAlign: "center", marginBottom: 24 }}>How it works</h2>
        <div className="landingSteps">
          <div className="landingStep">
            <span className="stepNumber">1</span>
            <h3>Fill in your business details</h3>
            <p className="muted">
              Enter your business name, industry, target audience, and platform.
              Add optional details like tone, region, and campaign goal.
            </p>
          </div>
          <div className="landingStep">
            <span className="stepNumber">2</span>
            <h3>Get two AI-generated variants</h3>
            <p className="muted">
              MarketMind generates two versions of your copy — one more measured,
              one more expressive — so you always have a real choice rather than two
              versions of the same thing.
            </p>
          </div>
          <div className="landingStep">
            <span className="stepNumber">3</span>
            <h3>Pick your favourite and build your brand voice</h3>
            <p className="muted">
              Select the one that feels right. Every choice you make is saved, and
              the more you use MarketMind the more the output starts to sound like you.
            </p>
          </div>
        </div>

        <div className="landingModes">
          <h3 style={{ textAlign: "center", margin: "32px 0 8px" }}>Two generation modes — you choose</h3>
          <p className="muted" style={{ textAlign: "center", marginBottom: 20, fontSize: 14 }}>
            Before generating, you can pick how MarketMind decides what tone and style to aim for.
          </p>
          <div className="landingModesGrid">
            <div className="landingModeCard">
              <div className="modeTag">Mode 1</div>
              <h4>Target-driven</h4>
              <p className="muted">
                MarketMind uses your campaign goals and the emotional profile of your inputs
                to set a tone target. It then generates one variant on each side of that target
                so you get a genuine contrast — one more measured, one more expressive.
                Good for when you have a clear brief or a campaign with specific goals.
              </p>
            </div>
            <div className="landingModeCard">
              <div className="modeTag">Mode 2</div>
              <h4>History-driven</h4>
              <p className="muted">
                MarketMind looks at the variants you have previously selected and uses the
                tone and style patterns from those choices as the target instead.
                The more you have used it, the more it steers output towards what you have
                already shown you like. Good for when you want consistency with your past content.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="landingGrid landingGrid4">
        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>A/B Content Generation</h3>
          <p className="muted">
            Generate two platform-ready variants per request and compare style before publishing.
          </p>
        </article>

        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Campaigns</h3>
          <p className="muted">
            Group your generations under a campaign and set an emotional target — the tone,
            energy, and confidence level you want your content to hit. MarketMind uses that
            target to steer every generation within the campaign towards a consistent feel.
          </p>
        </article>

        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Brand Memory</h3>
          <p className="muted">
            Select preferred outputs and let your future prompts reflect those choices.
            The more you use it, the better it knows your brand.
          </p>
        </article>

        <article className="sectionCard">
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>History & Analytics</h3>
          <p className="muted">
            Review past generations and track tone and regional preference patterns over time.
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
