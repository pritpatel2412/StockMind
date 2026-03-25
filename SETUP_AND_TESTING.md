# StockMind - Complete Setup & Testing Guide

## Backend Setup (Python)

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 12+ (or use Supabase)
- Redis (optional, for caching)
- API Keys: Groq, NVIDIA NIM, NewsAPI

### 2. Environment Setup

```bash
cd stockmind-backend
cp .env.example .env
```

Fill in your `.env` file with:
```
# Database (Supabase PostgreSQL)
DATABASE_URL=postgresql+asyncpg://[user]:[password]@[host]:[port]/[database]

# Authentication
JWT_SECRET=your_secure_jwt_secret_min_32_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Groq API
GROQ_API_KEY=your_groq_api_key

# NVIDIA NIM
NIM_API_KEY=your_nim_api_key
NIM_BASE_URL=http://localhost:8000/v1

# NewsAPI
NEWS_API_KEY=your_newsapi_key

# Redis
REDIS_URL=redis://localhost:6379

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python init_db.py
```

This creates all necessary tables:
- `users` - User accounts with bcrypt passwords
- `simulations` - Simulation configurations and metadata
- `simulation_ticks` - Per-tick market data
- `agent_actions` - Agent decisions and trades
- `market_data` - Historical price cache
- `news_feed` - Market news with sentiment
- `token_blacklist` - Logout tokens

### 5. Start Backend Server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

## Frontend Setup (Next.js)

### 1. Environment Configuration

Create `.env.local` in project root:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 2. Install Dependencies

```bash
pnpm install
```

### 3. Start Development Server

```bash
pnpm dev
```

Frontend will be available at: `http://localhost:3000`

---

## Authentication Flow Testing

### 1. Register New User

**Endpoint:** `POST /api/auth/register`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Frontend:** Navigate to `http://localhost:3000/register`

### 2. Login User

**Endpoint:** `POST /api/auth/login`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Frontend:** Navigate to `http://localhost:3000/login`

### 3. Get Current User

**Endpoint:** `GET /api/auth/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "user-123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

### 4. Refresh Token

**Endpoint:** `POST /api/auth/refresh`

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### 5. Logout User

**Endpoint:** `POST /api/auth/logout`

**Headers:**
```
Authorization: Bearer {access_token}
```

---

## Simulation API Testing

### 1. Start Simulation

**Endpoint:** `POST /api/simulation/start`

**Request:**
```json
{
  "ticker": "AAPL",
  "num_agents": 100,
  "agent_types": {
    "hedge_fund": 20,
    "retail": 50,
    "news": 10,
    "regulator": 5,
    "market_maker": 15
  },
  "time_horizon": "1d"
}
```

**Response:**
```json
{
  "simulation_id": "sim-123",
  "ticker": "AAPL",
  "status": "running",
  "current_price": 150.25,
  "current_tick": 0
}
```

### 2. Get Simulation Status

**Endpoint:** `GET /api/simulation/status/{simulation_id}`

**Response:**
```json
{
  "simulation_id": "sim-123",
  "status": "running",
  "current_price": 150.35,
  "current_tick": 42,
  "total_ticks": 100,
  "sentiment": {
    "bullish": 45,
    "bearish": 30,
    "neutral": 25
  }
}
```

### 3. Get Simulation Details

**Endpoint:** `GET /api/simulation/{simulation_id}`

**Response:**
```json
{
  "simulation_id": "sim-123",
  "ticker": "AAPL",
  "created_at": "2024-03-21T10:00:00Z",
  "current_price": 150.35,
  "price_history": [150.25, 150.28, 150.32, 150.35],
  "sentiment_history": [40, 42, 44, 45],
  "agent_count": 100,
  "total_actions": 256
}
```

---

## Troubleshooting

### Backend Issues

**Database Connection Error**
```
Error: could not translate host name "host" to address
```
- Verify DATABASE_URL is correct
- Check Supabase connection string format
- Ensure network access rules allow your IP

**JWT Token Error**
```
Error: Invalid token
```
- Verify JWT_SECRET matches between frontend and backend
- Check token hasn't expired (15 minutes default)
- Use refresh_token to get new access_token

**CORS Error**
```
Access to XMLHttpRequest blocked by CORS
```
- Backend CORS is enabled for all origins by default
- Verify NEXT_PUBLIC_API_URL is correct in frontend .env

### Frontend Issues

**Login Redirect Loop**
- Check browser localStorage for tokens
- Verify backend /auth/me endpoint works
- Check NEXT_PUBLIC_API_URL points to correct backend

**API Calls Failing**
- Open DevTools → Network tab
- Check request URL and Authorization header
- Verify backend is running on port 8000

---

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Database tables created successfully
- [ ] Frontend connects to backend API
- [ ] User can register with email/password
- [ ] User can login
- [ ] Access token stored in localStorage
- [ ] Authenticated requests include Authorization header
- [ ] Token refresh works after 15 minutes
- [ ] Logout clears tokens
- [ ] Simulation starts with real agents
- [ ] Price updates reflect agent actions
- [ ] News feed shows real market data
- [ ] Charts update in real-time

---

## Production Deployment

### Backend (Docker)
```bash
docker-compose up -d
```

### Frontend (Vercel)
```bash
pnpm build
vercel deploy
```

Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_URL` → Your backend URL

---

## Architecture Overview

```
┌─────────────────┐
│   Frontend      │
│  Next.js 16     │
│  React 19       │
└────────┬────────┘
         │ HTTP/REST
         │ JWT Auth
┌────────▼────────┐
│   Backend       │
│   FastAPI       │
│   LangGraph     │
└────────┬────────┘
         │ SQL
         │ Async
┌────────▼────────┐
│   Database      │
│  Supabase       │
│  PostgreSQL     │
└─────────────────┘
```

---

For issues or questions, check:
- `/stockmind-backend/README.md`
- `/stockmind-backend/AUTH_AND_DB.md`
- API Swagger docs at `/docs`
