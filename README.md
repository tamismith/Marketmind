# MarketMind

## About This Project

MarketMind is an AI-powered marketing content generation platform developed as a dissertation artefact for CO3202 Entrepreneurial Project, University of Leicester (April 2026).

The system generates dual marketing variants (A/B) guided by VAD (Valence/Arousal/Dominance) emotional targeting, learns from user selections over time, and adapts its generation style to each brand's personality through a Human-in-the-Loop feedback mechanism.

## Software Artefacts

### Backend — `marketmind-backend/`
| File / Folder | Description |
|---|---|
| `run.py` | Flask application entry point |
| `requirements.txt` | Python dependencies |
| `seed.py` | Demo seed script — creates GlowSkin and FinTrust evaluation profiles |
| `marketmind/models/` | SQLAlchemy database models (User, Campaign, GeneratedContent, BrandMemory, BusinessProfile) |
| `marketmind/controllers/` | Business logic — AI generation, campaign management, auth, user profile |
| `marketmind/services/` | Core services — AI provider, evaluation, feedback/brand memory |
| `marketmind/routes/` | Flask route definitions |
| `marketmind/migrations/` | Alembic database migrations |

**Key files:**
- `marketmind/controllers/ai_controller.py` — VAD-driven and history-driven generation modes, parameter mapping, alignment scoring
- `marketmind/services/feedback_service.py` — Brand memory aggregation and learned VAD from selection history
- `marketmind/services/evaluation_service.py` — VAD evaluation of generated content

### Frontend — `marketmind-frontend/src/`
| File / Folder | Description |
|---|---|
| `pages/Generate.jsx` | Main content generation interface (VAD-driven / history-driven mode toggle) |
| `pages/Analytics.jsx` | Campaign analytics — dominant tone, avg VAD, selection count, learned brand tendency |
| `pages/History.jsx` | Generation history with descriptions and feedback |
| `pages/Campaigns.jsx` | Campaign management with VAD target settings |
| `pages/Settings.jsx` | Brand memory and business profile settings |
| `api/client.js` | Axios API client with JWT handling |

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
Demo accounts: `glowskin@demo.com` / `Demo1234!` and `fintrust@demo.com` / `Demo1234!`
