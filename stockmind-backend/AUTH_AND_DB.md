# Authentication & Database Integration Guide

## Overview

The StockMind backend now includes comprehensive authentication with JWT tokens, role-based access control, and full database persistence with Supabase PostgreSQL. This guide covers setup, usage, and integration.

## Database Schema

### Tables

1. **users** - User accounts and authentication
   - `id` (PK): UUID
   - `email` (unique): User email
   - `password_hash`: bcrypt hashed password
   - `full_name`: Display name
   - `is_active`: Account status
   - `created_at`, `updated_at`: Timestamps

2. **simulations** - Simulation runs
   - `id` (PK): UUID
   - `user_id` (FK): Owner user
   - `name`: Simulation name
   - `ticker`: Stock ticker
   - `scenario`: bullish/bearish/neutral/crash
   - `agent_count`: Number of agents
   - `time_horizon`: 1d/1w/1m/3m
   - `status`: running/paused/completed/failed
   - `start_price`, `end_price`, `min_price`, `max_price`: Price data
   - `final_sentiment`: JSON sentiment breakdown
   - Timestamps and config

3. **simulation_ticks** - Tick-by-tick data
   - `id` (PK): UUID
   - `simulation_id` (FK): Parent simulation
   - `tick_number`: Sequence number
   - `price`: Tick price
   - `volume`: Trade volume
   - `sentiment_bullish/bearish/neutral`: Sentiment values
   - `timestamp`

4. **agent_actions** - Individual agent trades
   - `id` (PK): UUID
   - `simulation_id` (FK): Parent simulation
   - `tick_id` (FK): Parent tick
   - `agent_id`, `agent_type`: Agent identifier and type
   - `action`: buy/sell/hold/broadcast/regulate
   - `quantity`, `price`: Trade details
   - `reasoning`: LLM reasoning text
   - `sentiment_input`: JSON input sentiment
   - `timestamp`

5. **market_data** - Historical market cache
   - `id` (PK): UUID
   - `ticker`: Stock ticker
   - `date`: Trading date
   - `open_price`, `close_price`, `high_price`, `low_price`: OHLC
   - `volume`: Trade volume
   - `cached_at`: Cache timestamp

6. **news_feed** - News articles
   - `id` (PK): UUID
   - `ticker`: Stock ticker
   - `title`, `description`: Article content
   - `source`: News source
   - `sentiment`: positive/negative/neutral
   - `sentiment_score`: -1 to 1
   - `published_at`, `cached_at`: Timestamps
   - `url`: Article URL

7. **token_blacklist** - Revoked JWT tokens
   - `id` (PK): UUID
   - `user_id` (FK): Token owner
   - `token_jti`: JWT token ID
   - `blacklisted_at`, `expires_at`: Timestamps

## Authentication Flow

### Register
```
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "User Name"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "refresh_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "bearer"
}
```

### Login
```
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "secure_password"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "refresh_token": "eyJ0eXAiOiJKV1Q...",
  "token_type": "bearer"
}
```

### Refresh Token
```
POST /api/auth/refresh
{
  "refresh_token": "eyJ0eXAiOiJKV1Q..."
}

Response:
{
  "access_token": "new_access_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer"
}
```

### Logout
```
POST /api/auth/logout
Headers: Authorization: Bearer <access_token>

Response:
{
  "message": "Logged out successfully"
}
```

### Get Current User
```
GET /api/auth/me
Headers: Authorization: Bearer <access_token>

Response:
{
  "id": "user_id",
  "email": "user@example.com",
  "full_name": "User Name",
  "is_active": true
}
```

## Token Details

### Access Token (15 minutes)
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234568890,
  "type": "access",
  "jti": "token_id"
}
```

### Refresh Token (7 days)
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234912690,
  "type": "refresh",
  "jti": "token_id"
}
```

## Backend Setup

### 1. Environment Variables
Create `.env` file:
```
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/database
JWT_SECRET=your_super_secret_key_change_in_production_min_32_chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2. Initialize Database
```bash
python init_db.py
```

This creates:
- All tables with proper indexes
- Demo user: `demo@stockmind.ai` / `demo123456`
- Sample simulation data

### 3. Start Backend
```bash
python main.py
```

Server runs at `http://localhost:8000`

API docs at `http://localhost:8000/docs`

## Frontend Integration

### Setup
1. Set environment variable for API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

2. Wrap app with `AuthProvider`:
   ```tsx
   import { AuthProvider } from '@/lib/use-auth';

   export default function RootLayout({ children }) {
     return (
       <AuthProvider>
         {children}
       </AuthProvider>
     );
   }
   ```

### Authentication Hook
```tsx
import { useAuth } from '@/lib/use-auth';

export function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();

  return (
    <div>
      {isAuthenticated ? (
        <>
          <p>Welcome, {user?.email}</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <p>Please log in</p>
      )}
    </div>
  );
}
```

### Auth Client
```tsx
import { authClient } from '@/lib/auth-client';

// Manual API requests
const response = await authClient.request('/simulation/start', {
  method: 'POST',
  body: JSON.stringify({ /* ... */ })
});
```

## Security

- Passwords hashed with bcrypt (rounds: 12)
- JWT tokens signed with HS256
- Tokens stored in localStorage (consider using httpOnly cookies in production)
- Token refresh on 401 responses
- Blacklist on logout
- All database queries parameterized (SQLAlchemy)
- CORS configured for frontend access

## Data Persistence

All simulation data is now persisted:
- Simulation metadata and configuration
- Tick-by-tick market data
- Agent actions and reasoning
- Market data cache
- News feed

### Query Examples

```python
# Get user's simulations
simulations = await SimulationDataService.get_user_simulations(
    user_id=user.id,
    limit=20,
    session=session
)

# Get simulation history
ticks = await SimulationDataService.get_simulation_history(
    simulation_id=sim.id,
    user_id=user.id,
    limit=1000,
    session=session
)

# Get agent actions
actions = await SimulationDataService.get_agent_actions(
    simulation_id=sim.id,
    user_id=user.id,
    agent_type="hedge_fund",
    session=session
)
```

## Deployment

For production deployment:

1. Set strong JWT_SECRET (>32 characters)
2. Use production Supabase PostgreSQL instance
3. Enable SSL/TLS for database connections
4. Use environment-specific configuration
5. Configure CORS for production domain
6. Consider storing tokens in httpOnly cookies
7. Implement rate limiting on auth endpoints
8. Enable database backups

## Troubleshooting

### Database Connection Error
- Check DATABASE_URL format
- Verify network access to Supabase
- Confirm credentials

### JWT Issues
- Ensure JWT_SECRET is set consistently
- Check token expiration times
- Verify algorithm matches (HS256)

### CORS Errors
- Frontend and backend must be on same or allowed origin
- Check CORS middleware configuration

## Files Created

Backend:
- `database.py` - Database connection and session
- `models/database_models.py` - SQLAlchemy ORM models
- `utils/auth_jwt.py` - JWT token utilities
- `utils/auth_service.py` - Authentication service
- `utils/simulation_data_service.py` - Data persistence layer
- `api/routes/auth.py` - Authentication endpoints
- `init_db.py` - Database initialization script

Frontend:
- `lib/auth-client.ts` - API client for auth
- `lib/use-auth.tsx` - React context and hook
- `app/login/page.tsx` - Login page
- `app/register/page.tsx` - Register page

Configuration:
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies (updated)
