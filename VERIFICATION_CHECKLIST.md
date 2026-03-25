# StockMind Complete Functionality Verification Guide

## Quick Start Checklist

### Backend Setup (5 minutes)
- [ ] Copy `.env.example` to `.env` in `stockmind-backend/`
- [ ] Fill in database URL (Supabase PostgreSQL)
- [ ] Fill in API keys (Groq, NIM, NewsAPI)
- [ ] Run `pip install -r requirements.txt`
- [ ] Run `python init_db.py` to create database tables
- [ ] Start server: `python -m uvicorn main:app --reload`
- [ ] Verify: http://localhost:8000/docs (Swagger UI visible)

### Frontend Setup (2 minutes)
- [ ] Copy `.env.local.example` to `.env.local`
- [ ] Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api`
- [ ] Run `pnpm install`
- [ ] Start dev server: `pnpm dev`
- [ ] Verify: http://localhost:3000 (app loads)

---

## End-to-End Testing Flow

### Phase 1: Database Connectivity
**Goal:** Verify backend can connect to Supabase

```bash
# In stockmind-backend directory
python -c "from database import init_db; import asyncio; asyncio.run(init_db())"
```

Expected output:
```
Database initialized successfully
Tables created: users, simulations, simulation_ticks, agent_actions, market_data, news_feed, token_blacklist
```

### Phase 2: Authentication System
**Goal:** Verify JWT auth works end-to-end

**Test 1: Register User**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }'
```

Expected response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

**Test 2: Login User**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

**Test 3: Get Current User**
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected response:
```json
{
  "id": "user-123",
  "email": "test@example.com",
  "full_name": "Test User",
  "is_active": true
}
```

### Phase 3: Frontend Authentication
**Goal:** Verify login/register pages work with backend

1. Navigate to http://localhost:3000/register
   - [ ] Page loads without errors
   - [ ] Form has email, password, name fields
   - [ ] Submit button works
   - [ ] Success redirects to homepage
   - [ ] Token stored in localStorage

2. Navigate to http://localhost:3000/login
   - [ ] Login form appears
   - [ ] Can login with credentials from registration
   - [ ] Token refreshes work
   - [ ] Can navigate to dashboard

### Phase 4: Simulation Engine
**Goal:** Verify agent swarm and price simulation work

**Test 1: Start Simulation**
```bash
curl -X POST http://localhost:8000/api/simulation/start \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
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
  }'
```

Expected response:
```json
{
  "simulation_id": "sim-abc123",
  "status": "running",
  "current_price": 150.25,
  "current_tick": 0
}
```

**Test 2: Get Simulation Status** (run multiple times to see price changes)
```bash
curl http://localhost:8000/api/simulation/status/sim-abc123 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Watch for:
- [ ] `current_tick` increases over time
- [ ] `current_price` fluctuates based on agent actions
- [ ] `sentiment` values reflect agent opinion distribution

**Test 3: Verify Real Market Data**
```bash
curl http://localhost:8000/api/news?ticker=AAPL \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected: Real news items with sentiment scores

### Phase 5: Data Persistence
**Goal:** Verify simulation data persists in database

1. Start a simulation
2. Let it run for 30 ticks
3. Restart backend server
4. Query the same simulation ID

```bash
curl http://localhost:8000/api/simulation/sim-abc123 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Expected: Simulation history preserved with all ticks and agent actions

### Phase 6: Real-Time Dashboard
**Goal:** Verify frontend displays real agent data

1. In browser, login and navigate to dashboard
2. View war room display:
   - [ ] Top bar shows simulation controls
   - [ ] Left panel shows agent configuration
   - [ ] Center panel shows price chart updating
   - [ ] Right panel shows news feed
   - [ ] Bottom bar shows agent actions

3. Run the integration test:
```bash
cd stockmind-backend
python test_integration.py
```

Expected output: All tests pass with real API data

---

## Verification Checklist

### API Endpoints
- [ ] POST /api/auth/register - Create new user
- [ ] POST /api/auth/login - Login user
- [ ] GET /api/auth/me - Get current user (requires auth)
- [ ] POST /api/auth/refresh - Refresh expired token
- [ ] POST /api/auth/logout - Logout (clears token)
- [ ] POST /api/simulation/start - Start simulation (requires auth)
- [ ] GET /api/simulation/status/{id} - Get current price/tick (requires auth)
- [ ] GET /api/simulation/{id} - Get full simulation data (requires auth)
- [ ] GET /api/agents?simulation_id={id} - List agents (requires auth)
- [ ] GET /api/news?ticker={symbol} - Get news feed (requires auth)

### Database Tables
- [ ] `users` - User accounts with bcrypt hashed passwords
- [ ] `simulations` - Simulation metadata and configuration
- [ ] `simulation_ticks` - Per-tick market data (price, volume, sentiment)
- [ ] `agent_actions` - Individual agent decisions and trades
- [ ] `market_data` - Historical price cache
- [ ] `news_feed` - Real news with sentiment scores
- [ ] `token_blacklist` - Logged-out tokens

### Frontend Components
- [ ] Login page - Works with backend auth
- [ ] Register page - Creates users in database
- [ ] War room dashboard - Shows real agent data
- [ ] Sentiment charts - Updates from simulation engine
- [ ] Agent status - Real agent metrics
- [ ] News feed - Real market news
- [ ] Price charts - Real price history
- [ ] Token management - Refresh and logout work

### Real Data Integration
- [ ] Market prices from yfinance API
- [ ] News from NewsAPI
- [ ] Agent decisions from Groq LLM
- [ ] Sentiment analysis from NVIDIA NIM
- [ ] User authentication with bcrypt hashing
- [ ] JWT token management

---

## Troubleshooting

### Backend won't start
```
Error: could not translate host name
```
→ Fix: Check DATABASE_URL format in .env

### Authentication fails
```
Error: Invalid credentials
```
→ Fix: Verify JWT_SECRET matches between requests
→ Check user exists in database

### Frontend can't connect to backend
```
Error: Failed to fetch
```
→ Fix: Verify NEXT_PUBLIC_API_URL in .env.local
→ Check backend is running on port 8000
→ Check CORS is enabled in main.py

### Simulations won't start
```
Error: User not found
```
→ Fix: Ensure you're logged in (valid access token)
→ Check token isn't expired (15 min default)

### Price not updating
```
Price remains static
```
→ Fix: Verify agents are running (check logs)
→ Check market data fetcher has API key (yfinance)
→ Verify Groq API key is set

---

## Performance Baselines

- **Auth endpoints:** < 100ms
- **Simulation start:** < 500ms
- **Status update:** < 50ms
- **Agent count:** 100-500 agents per simulation
- **Tick speed:** 1 second per tick (configurable)
- **Price update:** < 1% deviation per tick

---

## Next Steps

1. **Deploy backend to production:** Use Docker + Heroku/Railway
2. **Deploy frontend:** Use `vercel deploy`
3. **Setup monitoring:** Add Sentry error tracking
4. **Add more agents:** Increase MAX_AGENTS_PER_TYPE in config
5. **Extend market data:** Add more tickers and data sources
6. **Add real-time WebSocket:** Replace polling with SSE/WebSocket

---

## Support

For issues or questions:
1. Check backend logs: `tail -f /path/to/app.log`
2. Check frontend console: DevTools → Console tab
3. Review API docs: `http://localhost:8000/docs`
4. Check GitHub issues: [StockMind Issues]
5. Email support: support@stockmind.ai
