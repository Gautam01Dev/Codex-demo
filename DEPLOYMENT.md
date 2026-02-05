# Deployment Guide (Web + API)

This project is deployable in two common ways:

1. **Single-VM / ECS-style Docker deployment** (fastest path)
2. **Split deployment** (frontend static hosting + backend API service)

---

## 1) Docker Deployment (recommended to start)

### Prerequisites
- Docker + Docker Compose installed
- A server (EC2, Azure VM, GCP Compute Engine, DigitalOcean, etc.)
- Domain names (optional but recommended)

### Step 1: Configure environment
Create `.env` from the template:

```bash
cp .env.example .env
```

Set strong values:
- `SECRET_KEY` to a long random secret
- `DATABASE_URL` for Postgres
- `REDIS_URL` for Redis
- API keys (`ALPHA_VANTAGE_API_KEY`, `NEWS_API_KEY`) if used

### Step 2: Build and run

```bash
docker compose up --build -d
```

Services started:
- Backend API on `:8000`
- Frontend on `:5173`
- Postgres on `:5432`
- Redis on `:6379`

### Step 3: Add reverse proxy + TLS (production)
Use Nginx/Caddy/Traefik in front:
- Route `https://api.yourdomain.com` -> backend `:8000`
- Route `https://app.yourdomain.com` -> frontend `:5173`
- Enable HTTPS certificates (Let's Encrypt)

### Step 4: Hardening checklist
- Rotate `SECRET_KEY`
- Restrict CORS to your frontend domains only
- Close public DB/Redis ports in firewall/security groups
- Add request logging + monitoring (e.g., Grafana/CloudWatch)
- Set backup policy for Postgres volume

---

## 2) Split Deployment (scalable default)

### Frontend (Vite)
Deploy as static build to Vercel/Netlify/S3+CloudFront:

```bash
cd frontend
npm ci
npm run build
```

Set `VITE_API_BASE=https://api.yourdomain.com` in host env variables.

### Backend (FastAPI)
Deploy to ECS/Fargate, Render, Railway, Fly.io, or Kubernetes using `backend/Dockerfile`.

Container command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Attach managed services:
- Managed Postgres (RDS/Cloud SQL/Azure PG)
- Managed Redis (Elasticache/MemoryStore/Azure Cache)

---

## AWS Reference Setup

- **Frontend:** S3 + CloudFront
- **Backend:** ECS Fargate service
- **Database:** RDS Postgres
- **Cache:** ElastiCache Redis
- **Secrets:** AWS Secrets Manager / SSM Parameter Store
- **TLS + DNS:** ACM + Route53

Minimal flow:
1. Push Docker image to ECR
2. Create ECS task with environment variables/secrets
3. Place ECS behind ALB
4. Point `api.yourdomain.com` to ALB
5. Deploy frontend with `VITE_API_BASE` pointing to API domain

---

## Health Check and Smoke Test

After deploy:

```bash
curl https://api.yourdomain.com/
```

Expected response:

```json
{"message":"SmartInvest AI backend is running"}
```

Auth smoke test flow:
1. `POST /api/auth/register`
2. `POST /api/auth/login`
3. Call protected endpoints with `Authorization: Bearer <token>`

---

## Mobile App Deployment Notes

Mobile clients (React Native / Flutter) can target the same backend API.
- Store JWT securely (Keychain/Keystore)
- Use HTTPS-only endpoints
- Configure API base by environment (dev/staging/prod)
