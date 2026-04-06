# Mindspeller Chatbot

This repository contains a full-stack chatbot built with a Next.js frontend and a Flask backend.
The main constraint behind this implementation is Python compatibility with older runtimes, especially Python 3.8.

The backend intentionally avoids the official `groq` SDK and uses `requests` to call Groq's OpenAI-compatible HTTP endpoint directly. This keeps the implementation compatible with older Python versions while still using modern LLM inference.

## Project Layout

```text
mindspeller/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
├── frontend/
│   ├── pages/
│   │   ├── _app.tsx
│   │   └── index.tsx
│   ├── styles/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   └── .env.local.example
└── .github/workflows/
    └── python-compatibility.yml
```

## Technical Decisions

1. Python compatibility first: backend code is written without Python 3.10+ syntax.
2. Groq integration via HTTP: uses `requests` against `https://api.groq.com/openai/v1/chat/completions`.
3. Separation of concerns: frontend handles chat UX, backend handles model calls and key security.
4. Deployment-safe config: frontend reads backend URL from environment variables.
5. Verifiable compatibility: CI workflow runs checks on Python 3.8 and Python 3.11.

## Backend API

### POST /api/chat

Request body:

```json
{
  "message": "user message",
  "history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi, how can I help?" }
  ]
}
```

Response body:

```json
{
  "reply": "assistant response",
  "history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi, how can I help?" },
    { "role": "user", "content": "user message" },
    { "role": "assistant", "content": "assistant response" }
  ]
}
```

### GET /api/health

Used for uptime/health checks.

## Local Setup

### Prerequisites

1. Node.js 16+
2. npm
3. Python runtime
4. Groq API key from https://console.groq.com

### Backend setup

Windows, Python 3.8 preferred:

```bash
cd backend
py -3.8 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` in `backend/`:

```env
GROQ_API_KEY=your_key_here
FRONTEND_URL=http://localhost:3000
```

Run backend:

```bash
python app.py
```

### Frontend setup

```bash
cd frontend
npm install
```

Create `.env.local` in `frontend/`:

```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

Run frontend:

```bash
npm run dev
```

Open `http://localhost:3000`.

## Deployment

### Backend deployment (Render, pinned to Python 3.8)

The backend includes a Dockerfile with `python:3.8-slim`, so production runtime stays on Python 3.8.

1. Create a new Render Web Service.
2. Connect this repository.
3. Set Root Directory to `backend`.
4. Render auto-detects Dockerfile.
5. Add env vars:
   - `GROQ_API_KEY=...`
   - `FRONTEND_URL=https://your-frontend-domain.vercel.app`
6. Deploy.

Health check URL:

```text
https://your-backend-service.onrender.com/api/health
```

### Frontend deployment (Vercel)

1. Import repository in Vercel.
2. Set Root Directory to `frontend`.
3. Add env var:

```env
NEXT_PUBLIC_BACKEND_URL=https://your-backend-service.onrender.com
```

4. Deploy.

## Python 3.8 Compatibility Proof

The workflow at `.github/workflows/python-compatibility.yml` validates backend checks on both Python 3.8 and Python 3.11.

This is useful when local machine does not have Python 3.8 installed, but compatibility must be demonstrated in evaluation.

## Common Issues

1. Backend starts but chat fails:
   - check `GROQ_API_KEY` in `backend/.env`
2. Frontend cannot reach backend:
   - check `NEXT_PUBLIC_BACKEND_URL`
   - ensure backend is running and reachable
3. CORS error in production:
   - set `FRONTEND_URL` to exact frontend domain in backend env

## Security Notes

1. Never commit `.env` or `.env.local`.
2. Keep API keys only in environment variables.
3. Restrict CORS origin in production using `FRONTEND_URL`.

## License

MIT