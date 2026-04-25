# MarketMind

**AI-powered marketing content generation for SMEs**

MarketMind is developed as a dissertation artefact for CO3202 Entrepreneurial Project, University of Leicester (April 2026).

The system generates dual A/B marketing variants guided by VAD (Valence/Arousal/Dominance) emotional targeting, learns from user selections over time, and adapts its generation style to each brand's personality through a Human-in-the-Loop feedback mechanism.

The full source code is hosted on the University of Leicester GitLab. The backend artefacts are located in `marketmind-backend/` and the frontend artefacts in `marketmind-frontend/`.

---

## Tech Stack

**Backend:** Flask, SQLAlchemy, PostgreSQL, Flask-JWT-Extended, Flask-Migrate, VADER Sentiment, python-dotenv

**Frontend:** React, React Router

**AI:** OpenAI GPT-4o-mini (text generation), Stability AI SDXL (logo/image generation)

---

## Key Features

- A/B content generation with VAD emotional targeting
- Automated evaluation — tone scoring, sentiment analysis, VAD alignment, CTA quality
- Brand memory that learns from user selections and adapts future outputs
- History-driven generation mode using learned VAD profile
- Logo and ad image generation
- Campaign management and analytics dashboard
- Credit-based subscription model with simulated purchase

---

## Environment Variables

Create a `.env` file in `marketmind-backend/` with the following:

```
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=postgresql://user:password@localhost/marketmind
```

---

## Software Artefacts

### Backend — `marketmind-backend/`

| File / Folder | Description |
|---|---|
| `run.py` | Flask application entry point |
| `requirements.txt` | Python dependencies |
| `seed.py` | Demo seed script — creates GlowSkin and FinTrust evaluation profiles |
| `marketmind/models/` | SQLAlchemy models: User, Campaign, GeneratedContent, BrandMemory, BusinessProfile, CreditTransaction |
| `marketmind/controllers/` | Business logic — AI generation, logo generation, campaign management, business profile |
| `marketmind/services/` | Core services — AI provider, evaluation, feedback/brand memory |
| `marketmind/routes/` | Flask route definitions — auth, AI, logo, campaigns, business |
| `marketmind/config/` | Application settings |
| `marketmind/migrations/` | Alembic database migrations |

**Key files:**
- `marketmind/controllers/ai_controller.py` — VAD-driven and history-driven generation modes, parameter mapping, alignment scoring
- `marketmind/services/feedback_service.py` — Brand memory aggregation and learned VAD from selection history
- `marketmind/services/evaluation_service.py` — VAD evaluation of generated content
- `marketmind/services/ai_provider.py` — Isolated OpenAI and Stability AI API communication

### Frontend — `marketmind-frontend/src/`

| File / Folder | Description |
|---|---|
| `pages/Home.jsx` | Public landing page |
| `pages/Register.jsx` | Account registration |
| `pages/Login.jsx` | Authentication |
| `pages/DashboardHome.jsx` | Main dashboard |
| `pages/Generate.jsx` | Content generation interface (VAD-driven / history-driven mode toggle) |
| `pages/Analytics.jsx` | Campaign analytics — dominant tone, avg VAD, selection count, learned brand tendency |
| `pages/History.jsx` | Generation history with descriptions and feedback |
| `pages/Campaigns.jsx` | Campaign management |
| `pages/Brand.jsx` | Brand memory and business profile settings |
| `pages/Plans.jsx` | Credit purchase and subscription tiers |
| `components/ProtectedRoute.jsx` | JWT-gated route wrapper |
| `components/PublicOnlyRoute.jsx` | Redirect authenticated users away from public pages |
| `layouts/DashboardLayout.jsx` | Shared dashboard layout |
| `api/client.js` | API client with JWT handling |

---

## Running the Project

### Backend
```bash
cd marketmind-backend
pip install -r requirements.txt
FLASK_APP=run.py flask run
```

### Frontend
```bash
cd marketmind-frontend
npm install
npm run dev
```

### Seed Demo Profiles
```bash
cd marketmind-backend
FLASK_APP=run.py python seed.py
```

Demo accounts:
- `glowskin@demo.com` / `Demo1234!`
- `fintrust@demo.com` / `Demo1234!`

---

## Known Limitations

- Image generation latency averages 8–24 seconds due to synchronous Stability AI API calls
- VAD arousal and dominance scoring uses a rule-based lexicon which produces a floor effect on professional marketing content
- History-driven mode requires a minimum number of selections before activating

---

