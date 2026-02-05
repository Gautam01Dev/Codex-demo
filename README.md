# SmartInvest AI (Full-Stack Web + Mobile-Ready)

SmartInvest AI is a full-stack investment intelligence platform for stocks and cryptocurrencies. It includes an ML prediction engine, recommendation module, AI insights, real-time dashboard, user authentication, watchlists, and alerts.

## Architecture

- **Frontend (Web):** React + Vite dashboard with dark/light mode and interactive charts.
- **Backend API:** FastAPI with JWT auth, rate limiting, and validated request schemas.
- **AI Layer:** Time-series forecasting using historical OHLCV (Yahoo Finance) + indicators (RSI, MACD, SMA).
- **Data Layer:** SQLAlchemy models for users, watchlists, alerts (Postgres or SQLite fallback).
- **Caching/Realtime-ready:** Redis configured for stream/cache expansion.
- **Mobile-ready:** documented API contract for React Native/Flutter client.
- **Deployability:** Dockerfiles + docker-compose for local/cloud setup.

## Core Features Implemented

1. **Market Prediction Engine**
   - Supports stocks and crypto assets.
   - Forecast outputs:
     - short-term (7 days)
     - mid-term (90 days)
     - confidence score (%)
   - Uses historical prices + indicators: volume, RSI, MACD, SMA20, SMA50.

2. **Investment Recommendation Module**
   - Buy/Hold/Sell recommendation from projected upside/downside.
   - Risk level (Low/Medium/High) via volatility proxy.
   - Suggested duration + allocation percentage.

3. **Pros & Cons Analyzer (AI Insights)**
   - Generates pro/con bullets based on model output and indicator state.
   - Integrates headline sentiment scoring (News API optional, fallback mode included).

4. **Real-Time Dashboard (Web UI Scaffold)**
   - Prediction chart overlay
   - Recommendation summary
   - Insights panel
   - Gainers/losers + Fear/Greed placeholder

5. **User Features**
   - Register/login (JWT)
   - Watchlist CRUD (add/list)
   - Alert creation endpoint
   - Personalized recommendation endpoint pattern available per symbol

## Security Controls

- JWT authentication for protected routes.
- Password hashing (`bcrypt` via passlib).
- Input validation with Pydantic constraints.
- Rate-limiter middleware enabled (SlowAPI).
- API key usage via environment variables (`.env`, never hard-coded).

## API Routes (selected)

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/market/predict`
- `POST /api/market/recommend`
- `POST /api/market/insights`
- `POST /api/market/watchlist`
- `GET /api/market/watchlist`
- `POST /api/market/alerts`
- `GET /api/dashboard/overview`

## Local Run

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
cp .env.example .env
docker compose up --build
```


## Deployment

See `DEPLOYMENT.md` for production deployment patterns (Docker, split frontend/backend, AWS reference architecture, and hardening checklist).

## Notes

- For crypto symbols, use pairs like `BTC` or `ETH` (auto-normalized to `-USD`).
- Replace default `SECRET_KEY` before production.
- Consider replacing linear baseline forecaster with LSTM/Prophet/Transformer for higher-quality predictions.
