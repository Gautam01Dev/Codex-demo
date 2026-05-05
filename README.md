# Three-Tier Blog Application

This project is a **3-tier web blog application**:

1. **Presentation tier**: React + Vite frontend (`frontend/`)
2. **Application tier**: FastAPI backend (`backend/`)
3. **Data tier**: PostgreSQL (via Docker) or SQLite fallback through SQLAlchemy

## Features

- Create blog posts
- View all posts ordered by newest first
- View full post details
- REST API with validation using Pydantic

## API Endpoints

- `GET /api/blog/posts`
- `POST /api/blog/posts`
- `GET /api/blog/posts/{post_id}`

## Run with Docker

```bash
docker compose up --build
```

Frontend: `http://localhost:5173`  
Backend API: `http://localhost:8000`

## Local development

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
