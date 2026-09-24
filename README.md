# PocketSmart AI

PocketSmart AI is a FastAPI + Jinja2 + SQLite GenAI budget-planning assistant based on the supplied 39-page project PDF.

## PDF-aligned scope

The project covers:

- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner
- Gemini text recommendations
- Optional outfit-image analysis for Jewelry
- User registration, login, logout and session-based personalization
- JWT token endpoint
- Recommendation history and detail pages
- Responsive HTML/CSS/JavaScript frontend
- FastAPI backend and modular services
- Local catalog plus platform search links
- Validation, tests and fallback recommendations

The PDF uses Flask in its early architecture description, then defines a FastAPI backend in Milestone 3 and the conclusion describes FastAPI + Jinja2. This implementation follows that later/final architecture.

## Important: Gemini model

The default model is the current stable `gemini-3.8-flash`. It is configurable through `.env`.

If Gemini is temporarily unavailable, the app retries transient failures and then uses its local fallback recommendation engine. Therefore the web application does not crash just because Gemini is unavailable.

## Quick Windows setup

### Option A - easiest

Double-click `setup_windows.bat`.

Then edit `.env` and add your NEW Gemini API key:

```env
GEMINI_API_KEY=YOUR_NEW_KEY_HERE
GEMINI_MODEL=gemini-3.8-flash
```

Then double-click `run_windows.bat`.

### Option B - VS Code terminal

```powershell
cd pocketsmart-ai
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python run.py
```

Open `http://127.0.0.1:8000`.

## First test

1. Register.
2. Login.
3. Open Home Planner.
4. Enter a normal budget such as `50000`.
5. Generate recommendations.
6. Repeat for Party.
7. Repeat for Jewelry.
8. Upload a JPEG/PNG/WebP outfit image in Jewelry.
9. Open History.
10. Open a saved recommendation.

## Useful URLs

- `/` - landing page
- `/register` - registration
- `/login` - login
- `/dashboard` - user dashboard
- `/planner/home` - Home planner
- `/planner/party` - Party planner
- `/planner/jewelry` - Jewelry planner
- `/history` - recommendation history
- `/docs` - FastAPI Swagger docs
- `/health` - health check
- `/startup` - configuration status

## API routes

- `POST /register`
- `POST /token`
- `POST /logout`
- `GET /api/session-info`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/history`
- `GET /api/recommendations/{id}`

## Security

- Do not put the Gemini key in Python source code.
- Do not commit `.env` to Git.
- If an API key has ever been exposed in a screenshot/chat, revoke it and create a new one.
- Use a long random `SECRET_KEY` for real deployment.

## Data-source note

The PDF mentions Amazon, Flipkart, IKEA, Swiggy, Zomato, OYO and other platforms. This implementation deliberately uses a local mock catalog and search URLs instead of pretending to have live prices, ratings or stock. Live partner/API integrations are a separate production phase.

## Tests

```powershell
pytest -q
```

The test suite covers health, public pages, authentication/session behavior and fallback planner generation.

## Project structure

```text
pocketsmart-ai/
├── app/
│   ├── ai/
│   │   ├── gemini_client.py
│   │   └── prompts.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── planners.py
│   ├── services/
│   │   ├── catalog_service.py
│   │   └── recommendation_service.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── data/catalog.json
├── static/css/styles.css
├── static/js/app.js
├── templates/
├── tests/
├── uploads/
├── .env.example
├── PROJECT_ROADMAP.md
├── START_HERE.txt
├── setup_windows.bat
├── run_windows.bat
├── requirements.txt
└── run.py
```
