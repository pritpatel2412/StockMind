"""
StockMind Backend - README

AI-Powered Market Sentiment Simulation Engine
"""

# StockMind Backend

An advanced multi-agent market simulation engine powered by LLMs, featuring AI-driven agents with distinct personalities and trading strategies.

## Features

- **5 Agent Types**: Hedge funds, retail traders, news broadcasters, regulators, and market makers
- **LLM-Powered Decisions**: Uses Groq's llama-3.3-70b for agent reasoning
- **Real-time Market Data**: Integrates yfinance for historical price data
- **News Integration**: NewsAPI for sentiment-driven market movements
- **Vector RAG**: Historical event similarity search for context-aware decisions
- **Circuit Breaker**: Automatic trading halts on excessive volatility
- **Async-First**: Full async/await architecture for performance
- **WebSocket Streaming**: Real-time tick updates to frontend

## Quick Start

### Prerequisites

- Python 3.11+
- pip or uv
- API Keys:
  - Groq (free tier available): https://console.groq.com
  - NewsAPI (free tier): https://newsapi.org
  - NVIDIA NIM (optional): https://build.nvidia.com

### Installation

1. **Clone and Setup**
```bash
cd stockmind-backend
cp .env.example .env
# Edit .env with your API keys
```

2. **Install Dependencies**
```bash
# Using pip
pip install -r requirements.txt

# Or using uv (faster)
uv sync
```

3. **Run Server**
```bash
# Direct run
python main.py

# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access APIs**
```
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- WebSocket: ws://localhost:8000/ws/{simulation_id}
```

## API Endpoints

### Simulation Management

```
POST   /api/simulation/start          Start new simulation
GET    /api/simulation/status/{id}    Get simulation status
GET    /api/simulation/details/{id}   Get detailed state with all agents
POST   /api/simulation/pause/{id}     Pause simulation
POST   /api/simulation/resume/{id}    Resume simulation
GET    /api/simulation/history/{id}   Get price history
```

### Agents

```
GET    /api/agents/{sim_id}           List all agents
GET    /api/agents/{sim_id}/{agent_id} Get agent details
GET    /api/agents/{sim_id}/portfolio/summary  Portfolio metrics
```

### News

```
GET    /api/news/{sim_id}             Get news feed
GET    /api/news/{sim_id}/sentiment   Get sentiment summary
```

## Simulation Scenarios

### 1. Normal Market
- Calm, efficient market with stable volatility
- Balanced agent distribution
- Good for testing baseline behavior

### 2. Bull Run
- Sustained uptrend with strong momentum
- More retail agents (herd buying)
- Higher sentiment positivity

### 3. Bear Crash
- Extreme volatility, panic selling
- All agent types active
- Tests circuit breaker logic

### 4. Meme Stock Frenzy
- Reddit-coordinated retail buying
- Heavy retail agent presence
- Low market efficiency

### 5. Flash Crash
- Sudden market dislocation and recovery
- Tests liquidity crisis response
- Maximum market maker participation

## Agent Types

### Hedge Fund Agent
- **Strategy**: Quantitative, options-focused
- **Risk Tolerance**: High (0.8)
- **Decision Style**: Analytical
- **Capital**: $10M

### Retail Agent
- **Strategy**: Emotional, herding behavior
- **Risk Tolerance**: Low (0.3)
- **Decision Style**: Emotional (FOMO/panic)
- **Capital**: $50K

### News Agent
- **Strategy**: Sentiment classification and broadcast
- **Risk Tolerance**: None (no trading)
- **Function**: Market information

### Regulator Agent
- **Strategy**: Circuit breaker enforcement
- **Risk Tolerance**: None
- **Function**: Market protection

### Market Maker Agent
- **Strategy**: Liquidity provision, bid/ask spreads
- **Risk Tolerance**: Low-medium (0.2)
- **Decision Style**: Mechanical
- **Capital**: $5M

## Example Usage

### Start a Simulation

```python
import httpx
import asyncio

async def run_simulation():
    async with httpx.AsyncClient() as client:
        # Start simulation
        response = await client.post(
            "http://localhost:8000/api/simulation/start",
            json={
                "scenario": "bull_run",
                "agent_count": 100,
            }
        )
        sim_id = response.json()["simulation_id"]
        print(f"Started simulation: {sim_id}")
        
        # Get status
        await asyncio.sleep(5)
        response = await client.get(
            f"http://localhost:8000/api/simulation/status/{sim_id}"
        )
        print(response.json())

asyncio.run(run_simulation())
```

### WebSocket Real-time Updates

```javascript
// Connect to WebSocket for real-time ticks
const ws = new WebSocket("ws://localhost:8000/ws/simulation-id-here");

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Tick update:", data);
};
```

## Architecture

```
stockmind-backend/
├── agents/              # 5 agent implementations
├── simulation/          # Core simulation engine
├── data/               # Data fetchers & embeddings
├── utils/              # Groq client, rate limiting
├── models/             # Pydantic schemas
├── api/                # FastAPI routes
├── config.py           # Configuration & constants
├── main.py             # FastAPI app entry point
└── requirements.txt    # Dependencies
```

## Advanced Configuration

### Rate Limiting
- Groq free tier: 30 req/min (automatically throttled)
- Batch requests where possible
- Token bucket algorithm implemented

### Async Performance
- All I/O operations are async
- Parallel agent decisions via `asyncio.gather()`
- Redis integration ready (commented out)

### Vector RAG
- Pre-populated with 8 historical market events
- Semantic similarity search for context
- Improves decision quality with historical patterns

### Circuit Breaker
- Triggers at 20% price move
- 5-tick trading halt
- Configurable thresholds in RegulatorAgent

## Environment Variables

See `.env.example` for all options:

```
GROQ_API_KEY=xxx           # Groq LLM API key
NIM_API_KEY=xxx            # NVIDIA NIM (optional)
NEWS_API_KEY=xxx           # NewsAPI key
REDIS_URL=redis://...      # Redis (future use)
API_HOST=0.0.0.0           # Server host
API_PORT=8000              # Server port
DEBUG=False                # Debug mode
```

## Performance Notes

- Typical tick processing: 100-500ms (depends on LLM latency)
- Can run 1000 ticks per simulation
- Scales to 500+ agents per simulation
- Memory: ~500MB baseline + ~1MB per agent

## Troubleshooting

### "Engine not initialized"
- Ensure server startup completed
- Check health endpoint: `GET /health`

### Groq API errors
- Verify API key in `.env`
- Check rate limit (30 req/min free tier)
- Use mock mode by setting empty API key

### High latency
- LLM inference is async, some blocking time normal
- Consider reducing agent count
- Check Groq API status

## Future Improvements

- [ ] Redis caching for embeddings
- [ ] Multi-simulation orchestration
- [ ] Advanced portfolio analytics
- [ ] Risk management features
- [ ] Custom agent implementations
- [ ] Backtesting engine

## License

MIT
