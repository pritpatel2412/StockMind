# StockMind - Complete End-to-End Setup

AI-powered market sentiment simulation engine with agent swarm dynamics, real market data integration, and JWT authentication.

## Project Structure

```
stockmind/
├── app/                          # Next.js frontend (React 19)
│   ├── login/                    # Login page
│   ├── register/                 # Registration page
│   ├── page.tsx                  # Main dashboard
│   └── layout.tsx                # App layout with AuthProvider
│
├── components/                   # React components
│   ├── WarRoomLayout.tsx         # Main 4-zone dashboard
│   ├── TopBar.tsx                # Simulation controls
│   ├── LeftPanel.tsx             # Config + sentiment chart
│   ├── CenterPanel.tsx           # Price chart + volume
│   ├── RightPanel.tsx            # News feed + cascade map
│   ├── BottomStatusBar.tsx       # Agent actions ticker
│   └── [other components...]
│
├── lib/                          # Utilities
│   ├── use-auth.tsx              # Auth context hook
│   ├── auth-client.ts            # API client
│   └── [other utilities...]
│
├── stockmind-backend/            # Python FastAPI backend
│   ├── config.py                 # Environment config
│   ├── database.py               # SQLAlchemy setup
│   ├── main.py                   # FastAPI app
│   ├── init_db.py                # Database initialization
│   ├── test_integration.py       # Full integration tests
│   │
│   ├── models/                   # Data models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── simulation_state.py   # Simulation state
│   │   └── database_models.py    # SQLAlchemy ORM models
│   │
│   ├── agents/                   # Agent implementations
│   │   ├── base_agent.py         # Abstract agent
│   │   ├── hedge_fund_agent.py   # Quant trader
│   │   ├── retail_agent.py       # Emotional trader
│   │   ├── news_agent.py         # News broadcaster
│   │   ├── regulator_agent.py    # Circuit breaker
│   │   └── market_maker_agent.py # Liquidity provider
│   │
│   ├── simulation/               # Engine & orchestration
│   │   ├── engine.py             # Main simulation engine
│   │   └── tick_processor.py     # Per-tick orchestration
│   │
│   ├── data/                     # Data integration
│   │   ├── market_fetcher.py     # yfinance integration
│   │   ├── news_fetcher.py       # NewsAPI integration
│   │   └── nim_embedder.py       # NVIDIA NIM embeddings
│   │
│   ├── utils/                    # Utilities
│   │   ├── auth_jwt.py           # JWT token handling
│   │   ├── auth_service.py       # Auth business logic
│   │   ├── groq_client.py        # Groq LLM client
│   │   ├── nim_client.py         # NVIDIA NIM client
│   │   └── simulation_data_service.py  # Data persistence
│   │
│   ├── api/                      # FastAPI routes
│   │   ├── routes/
│   │   │   ├── auth.py           # Auth endpoints
│   │   │   ├── simulation.py     # Simulation endpoints
│   │   │   ├── agents.py         # Agent endpoints
│   │   │   └── news.py           # News endpoints
│   │
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment template
│   ├── Dockerfile                # Docker config
│   ├── docker-compose.yml        # Docker Compose
│   └── README.md                 # Backend docs
│
├── SETUP_AND_TESTING.md          # Complete setup guide
├── VERIFICATION_CHECKLIST.md     # Testing checklist
├── API_REFERENCE.md              # API documentation
├── .env.local.example            # Frontend env template
└── package.json                  # Dependencies
```

## Quick Start (10 minutes)

### 1. Backend Setup

```bash
cd stockmind-backend
cp .env.example .env

# Edit .env with your API keys and database URL
# Minimum required:
# - DATABASE_URL (Supabase PostgreSQL)
# - GROQ_API_KEY
# - JWT_SECRET

pip install -r requirements.txt
python init_db.py
python -m uvicorn main:app --reload
```

Backend runs on: `http://localhost:8000`

### 2. Frontend Setup

```bash
cp .env.local.example .env.local
# Verify: NEXT_PUBLIC_API_URL=http://localhost:8000/api

pnpm install
pnpm dev
```

Frontend runs on: `http://localhost:3000`

### 3. Test the System

```bash
# In new terminal, from stockmind-backend:
python test_integration.py
```

Should see: ✓ PASSED for all tests

---

## Key Features

### 🔐 Authentication
- JWT tokens (15-min access, 7-day refresh)
- Bcrypt password hashing
- User registration and login
- Token blacklist on logout
- Automatic token refresh

### 📊 Simulation Engine
- 5 agent types with unique behaviors
- Real market data integration (yfinance)
- Real news sentiment (NewsAPI)
- LLM-powered agent decisions (Groq)
- Atomic state updates with async locks

### 💾 Data Persistence
- PostgreSQL via Supabase
- Full simulation history
- Agent action tracking
- User account management
- Market data caching

### 🎨 Dashboard
- Real-time war room visualization
- 6 interactive charts (Recharts)
- Smooth animations (Framer Motion)
- Responsive design
- Dark theme with neon accents

### 🚀 Performance
- Async-first backend (FastAPI)
- Rate limiting (30 req/min Groq)
- Optimized WebSocket ready
- Database connection pooling
- Frontend token caching

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - Logout

### Simulation
- `POST /api/simulation/start` - Start simulation
- `GET /api/simulation/status/{id}` - Get status
- `GET /api/simulation/{id}` - Get details
- `POST /api/simulation/{id}/pause` - Pause simulation
- `POST /api/simulation/{id}/resume` - Resume

### Agents & Data
- `GET /api/agents?simulation_id={id}` - List agents
- `GET /api/agents/{agent_id}` - Agent details
- `GET /api/news?ticker={symbol}` - Market news

See `API_REFERENCE.md` for full documentation.

---

## Technology Stack

### Frontend
- **Framework:** Next.js 16
- **UI:** React 19, shadcn/ui, Tailwind CSS v4
- **Visualization:** Recharts, Framer Motion
- **Auth:** JWT + localStorage
- **HTTP:** fetch API

### Backend
- **Framework:** FastAPI + Uvicorn
- **ORM:** SQLAlchemy 2.0 (async)
- **Database:** PostgreSQL (Supabase)
- **Auth:** JWT + bcrypt
- **LLM:** Groq (llama-3.3-70b)
- **Embeddings:** NVIDIA NIM
- **Data:** yfinance, NewsAPI
- **Orchestration:** LangGraph

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Deployment:** Vercel (frontend), Heroku/Railway (backend)
- **Database:** Supabase (managed PostgreSQL)
- **Monitoring:** Sentry (optional)

---

## Environment Variables

### Backend (.env)
```
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host/db

# API Keys
GROQ_API_KEY=
NIM_API_KEY=
NEWS_API_KEY=

# JWT
JWT_SECRET=min_32_character_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## Testing

### Unit Tests
```bash
# Backend
cd stockmind-backend
python -m pytest tests/

# Frontend
pnpm test
```

### Integration Tests
```bash
cd stockmind-backend
python test_integration.py
```

### Manual Testing
See `VERIFICATION_CHECKLIST.md` for step-by-step testing guide.

---

## Deployment

### Backend (Docker)
```bash
cd stockmind-backend
docker-compose up -d
```

### Frontend (Vercel)
```bash
pnpm build
vercel deploy
```

Set environment variables in Vercel dashboard.

---

## Documentation

- **Setup Guide:** `SETUP_AND_TESTING.md`
- **Testing Checklist:** `VERIFICATION_CHECKLIST.md`
- **API Reference:** `API_REFERENCE.md`
- **Backend README:** `stockmind-backend/README.md`
- **Auth & DB:** `stockmind-backend/AUTH_AND_DB.md`
- **Swagger UI:** `http://localhost:8000/docs`

---

## Support

For issues:
1. Check documentation above
2. Review error logs
3. Check Swagger UI for endpoint details
4. File issue on GitHub
5. Contact support@stockmind.ai

---

## License

MIT License - See LICENSE file for details

---

**Built with ❤️ using modern AI and web technologies**
