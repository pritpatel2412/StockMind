# StockMind API Quick Reference

Base URL: `http://localhost:8000/api` (or your deployed backend URL)

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

---

### Login User
**POST** `/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

Response (200): Same as register

---

### Get Current User
**GET** `/auth/me`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "id": "user-abc123",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}
```

---

### Refresh Token
**POST** `/auth/refresh`

Request:
```json
{
  "refresh_token": "eyJhbGc..."
}
```

Response (200): Same as login

---

### Logout
**POST** `/auth/logout`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "message": "Successfully logged out"
}
```

---

## Simulation Endpoints

### Start Simulation
**POST** `/simulation/start`

Headers: `Authorization: Bearer {access_token}`

Request:
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

Response (200):
```json
{
  "simulation_id": "sim-abc123def456",
  "ticker": "AAPL",
  "status": "running",
  "current_price": 150.25,
  "current_tick": 0,
  "total_ticks": 100
}
```

---

### Get Simulation Status
**GET** `/simulation/status/{simulation_id}`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "simulation_id": "sim-abc123def456",
  "status": "running",
  "current_price": 150.35,
  "price_change": 0.10,
  "price_change_pct": 0.067,
  "current_tick": 42,
  "total_ticks": 100,
  "sentiment": {
    "bullish": 45,
    "bearish": 30,
    "neutral": 25
  }
}
```

---

### Get Simulation Details
**GET** `/simulation/{simulation_id}`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "simulation_id": "sim-abc123def456",
  "user_id": "user-abc123",
  "ticker": "AAPL",
  "status": "running",
  "created_at": "2024-03-21T10:00:00Z",
  "current_price": 150.35,
  "initial_price": 150.25,
  "price_high": 151.50,
  "price_low": 149.80,
  "price_history": [150.25, 150.28, 150.32, 150.35],
  "sentiment_history": [40, 42, 44, 45],
  "volume_history": [1000000, 1050000, 1100000, 1150000],
  "total_agents": 100,
  "total_actions": 256,
  "agent_types": {
    "hedge_fund": 20,
    "retail": 50,
    "news": 10,
    "regulator": 5,
    "market_maker": 15
  }
}
```

---

### Pause Simulation
**POST** `/simulation/{simulation_id}/pause`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "message": "Simulation paused",
  "current_tick": 42
}
```

---

### Resume Simulation
**POST** `/simulation/{simulation_id}/resume`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "message": "Simulation resumed"
}
```

---

## Agent Endpoints

### List Agents
**GET** `/agents?simulation_id={simulation_id}`

Headers: `Authorization: Bearer {access_token}`

Query Parameters:
- `simulation_id` (required): Simulation ID
- `agent_type` (optional): Filter by type
- `limit` (optional): Max results (default: 50)

Response (200):
```json
[
  {
    "agent_id": "agent-001",
    "agent_type": "hedge_fund",
    "simulation_id": "sim-abc123def456",
    "sentiment": "bullish",
    "confidence": 0.85,
    "portfolio_value": 1000000,
    "cash": 50000,
    "holdings": {
      "AAPL": 6666.67
    },
    "last_action": "BUY",
    "action_count": 12
  },
  {
    "agent_id": "agent-002",
    "agent_type": "retail",
    "sentiment": "neutral",
    "confidence": 0.60,
    "portfolio_value": 50000,
    "cash": 5000,
    "holdings": {
      "AAPL": 300
    },
    "last_action": "HOLD",
    "action_count": 3
  }
]
```

---

### Get Agent Details
**GET** `/agents/{agent_id}`

Headers: `Authorization: Bearer {access_token}`

Response (200):
```json
{
  "agent_id": "agent-001",
  "agent_type": "hedge_fund",
  "simulation_id": "sim-abc123def456",
  "sentiment": "bullish",
  "confidence": 0.85,
  "portfolio_value": 1000000,
  "cash": 50000,
  "holdings": {
    "AAPL": 6666.67
  },
  "trade_history": [
    {
      "timestamp": "2024-03-21T10:05:00Z",
      "action": "BUY",
      "quantity": 6666.67,
      "price": 150.25,
      "reasoning": "Technical indicators show strong uptrend"
    }
  ],
  "decision_count": 12,
  "accuracy": 0.67
}
```

---

## News Endpoints

### Get News Feed
**GET** `/news?ticker={symbol}`

Headers: `Authorization: Bearer {access_token}`

Query Parameters:
- `ticker` (required): Stock symbol
- `limit` (optional): Max results (default: 10)
- `sentiment` (optional): Filter by sentiment (bullish/bearish/neutral)

Response (200):
```json
[
  {
    "id": "news-001",
    "title": "Apple Reports Record Earnings",
    "description": "Tech giant surpasses analyst expectations...",
    "source": "Reuters",
    "published_at": "2024-03-21T09:30:00Z",
    "url": "https://example.com/news",
    "sentiment": "bullish",
    "sentiment_score": 0.85,
    "keywords": ["apple", "earnings", "profit", "growth"],
    "impact_score": 0.75
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

- Auth endpoints: 10 requests/minute
- Simulation endpoints: 60 requests/minute
- Agent endpoints: 100 requests/minute
- News endpoints: 50 requests/minute

---

## Authentication

All protected endpoints require:

```
Authorization: Bearer {access_token}
```

Token expires in 15 minutes. Use refresh endpoint to get new token.

---

## WebSocket (Future)

```
ws://localhost:8000/ws/simulation/{simulation_id}?token={access_token}
```

Real-time simulation updates (price, sentiment, agent actions)
