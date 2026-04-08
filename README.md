<p align="center">
  <h1 align="center">📈 StockMind</h1>
  <p align="center"><strong>AI-Powered Multi-Agent Market Simulation & Sentiment Analysis Platform</strong></p>
  <p align="center">A neo-brutalist "War Room" where thousands of LLM agents trade in real-time.</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js" />
  <img src="https://img.shields.io/badge/FastAPI-Python-green?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/NVIDIA-NIM_Embeddings-76B900?style=flat-square&logo=nvidia" />
  <img src="https://img.shields.io/badge/WebSockets-Real--time-blue?style=flat-square" />
</p>

---

## What is StockMind?

StockMind is a **multi-agent financial simulation system** that models hedge funds, retail traders, market makers, and regulators — each with distinct strategies, risk profiles, and AI-driven decision logic.

Watch thousands of agents trade in real-time. Trigger market scenarios. Observe emergent behavior. Understand how sentiment, news, and agent psychology shape market dynamics.

This is not a trading app. It's a **simulation engine** for market research, strategy testing, and AI behavior analysis.

---

## Agent Types

| Agent | Strategy | Risk Profile | Behavior |
|-------|----------|-------------|---------|
| 🏦 **Hedge Fund** | Quantitative / Arbitrage | High (0.8) | Maximize alpha via complex timing |
| 👤 **Retail Trader** | Emotional / Momentum | Low (0.3) | FOMO-driven herding behavior |
| 📰 **News Agent** | Information Broker | N/A | Classifies & broadcasts sentiment |
| 🏪 **Market Maker** | Delta Neutral / Spread | Med (0.2) | Provides liquidity, maintains spreads |
| ⚖️ **Regulator** | Market Stability | N/A | Enforces circuit breakers (20% halt) |

---

## Key Features

### ⚡ Real-Time Simulation Engine
- FastAPI + AsyncIO backend orchestrates thousands of concurrent agent decisions
- WebSocket streaming delivers live market dynamics to the dashboard
- Sub-second latency from agent decision → chart update

### 🧠 AI-Driven Sentiment Analysis
- Groq LLaMA 3.3 70B processes real-time news ingestion
- Sentiment scores directly influence agent behavior and price movements
- Heatmaps visualize sentiment distribution across market sectors

### 📚 RAG-Powered Decision Making
- NVIDIA NIM embeddings (`nv-embedqa-e5-v5`) index historical market events
- Agents query this knowledge base to inform decisions — e.g., "this pattern looks like 2008"
- Retrieval-augmented reasoning makes agent behavior more realistic

### 🎮 Scenario Testing
Pre-configured market scenarios:
- 🚀 Bull Run
- 🐻 Bear Crash
- 🐸 Meme Stock Frenzy
- ⚡ Flash Crash

### 🖥️ Neo-Brutalist War Room Dashboard
- High-contrast dark mode with electric lime, purple, and pink accents
- Live Recharts visualizations: price charts, volume bars, sentiment heatmaps
- Agent activity feed — see each agent's decision in real-time

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS, Recharts |
| Backend | FastAPI, Python, AsyncIO |
| Real-time | WebSockets |
| LLM | Groq LLaMA 3.3 70B |
| RAG | NVIDIA NIM Embeddings |
| Market Data | yfinance |
| News/Sentiment | NewsAPI |
| Database | Supabase PostgreSQL |
| Auth | JWT with token rotation |

---

## Architecture

```
                    ┌─────────────────────────────┐
                    │   Next.js War Room Dashboard  │
                    │  (Neo-brutalist real-time UI) │
                    └──────────────┬───────────────┘
                                   │ WebSocket
                    ┌──────────────▼───────────────┐
                    │      FastAPI Backend           │
                    │   Simulation Engine (AsyncIO)  │
                    └──┬──────────┬───────────┬─────┘
                       │          │           │
              ┌────────▼──┐  ┌───▼────┐  ┌──▼──────────┐
              │ Agent Swarm│  │  Groq  │  │  NVIDIA NIM  │
              │(1000s LLM) │  │  LLM   │  │  RAG Engine  │
              └────────────┘  └────────┘  └─────────────┘
                       │
              ┌────────▼──────────────┐
              │  yfinance + NewsAPI    │
              │  (Real market data)    │
              └───────────────────────┘
```

---

## Getting Started

```bash
git clone https://github.com/pritpatel2412/StockMind
cd StockMind

# Frontend
npm install
npm run dev

# Backend
cd stockmind-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Required env vars:** `GROQ_API_KEY`, `NVIDIA_NIM_API_KEY`, `NEWS_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`

---

## Built By

**Prit Patel** — B.Tech CSE @ CHARUSAT University
[GitHub](https://github.com/pritpatel2412) · [LinkedIn](https://linkedin.com/in/pritpatel2412)
