# StockMind: End-to-End Getting Started Guide 🚀

This guide will take you from a fresh clone to running your first AI-driven market simulation.

---

## 📋 Table of Contents
1. [Backend Setup](#1-backend-setup)
2. [Database Initialization](#2-database-initialization)
3. [Frontend Setup](#3-frontend-setup)
4. [Running Your First Simulation](#4-running-your-first-simulation)
5. [Common Troubleshooting](#5-common-troubleshooting)

---

## 1. Backend Setup

The backend is a FastAPI application that orchestrates the AI Agent Swarm.

### Required Software
- Python 3.11 or 3.12
- `pip` or `uv`

### installation Steps
```bash
# Navigate to backend directory
cd stockmind-backend

# Create virtual environment
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration
Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
```
**Essential Variables in `.env`:**
- `DATABASE_URL`: Your PostgreSQL connection string (e.g., from Supabase).
- `GROQ_API_KEY`: Get one from [console.groq.com](https://console.groq.com).
- `JWT_SECRET`: A long, random string (at least 32 characters).
- `NEWS_API_KEY`: Get one from [newsapi.org](https://newsapi.org).

---

## 2. Database Initialization

StockMind uses PostgreSQL with SQLAlchemy for persistent storage of simulations, agents, and user data.

```bash
# From stockmind-backend directory
python init_db.py
```
This script will create the tables: `users`, `simulations`, `simulation_ticks`, `agent_actions`, `market_data`, and `news_feed`.

---

## 3. Frontend Setup

The frontend is a modern Next.js 15 application using the App Router.

### Required Software
- Node.js 18+
- `pnpm` (recommended)

### Installation Steps
```bash
# From the root directory
pnpm install
```

### Environment Configuration
Create a `.env.local` file in the root directory:
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local
```

### Start Development Server
```bash
pnpm dev
```
The UI will be available at [http://localhost:3000](http://localhost:3000).

---

## 4. Running Your First Simulation

1. **Start the Backend**:
   ```bash
   # In one terminal
   cd stockmind-backend
   uvicorn main:app --reload --port 8000
   ```
2. **Start the Frontend**:
   ```bash
   # In another terminal
   pnpm dev
   ```
3. **Login/Register**:
   - Go to [http://localhost:3000/register](http://localhost:3000/register).
   - Create an account.
4. **Deploy War Room**:
   - Click **"Start New Simulation"**.
   - Select a ticker (e.g., `AAPL`, `TSLA`, `NVDA`).
   - Choose a scenario (e.g., *Bull Run*).
   - Watch the AI Agents (Hedge Funds, Retail, etc.) start trading in real-time.

---

## 5. Common Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"Engine not initialized"** | Ensure you ran `init_db.py` and the backend server started successfully. |
| **API Errors (401/403)** | Check your `JWT_SECRET` matches in `.env` and you are logged in. |
| **No Market Data** | Ensure you have an internet connection (yfinance) and your `NEWS_API_KEY` is valid. |
| **WebSocket Connection Failed** | Check if the backend is running on port 8000 and nothing is blocking port 8000. |

---

Need more help? Check the [API Reference](API_REFERENCE.md) or the [Full Technical Guide](SETUP_AND_TESTING.md).
