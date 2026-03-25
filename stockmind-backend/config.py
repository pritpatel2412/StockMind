"""
StockMind Backend Configuration
Complete environment setup, constants, and default configurations
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# ENVIRONMENT VARIABLES
# ============================================================================

# API Keys & Endpoints
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NIM_API_KEY = os.getenv("NIM_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./stockmind.db")

# JWT & Auth Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-super-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ============================================================================
# SIMULATION CONSTANTS
# ============================================================================

# Tick Configuration
TICK_DURATION_MS = 1000  # 1 second per tick
MAX_TICKS = 1000  # Max 1000 ticks per simulation
INITIAL_PRICE = 100.0
INITIAL_VOLUME = 1_000_000

# Agent Configuration
DEFAULT_AGENT_COUNT = 100
MAX_AGENTS_PER_TYPE = 500
AGENT_TYPES = ["hedge_fund", "retail", "news", "regulator", "market_maker"]

# Order Book
MAX_ORDER_BOOK_DEPTH = 100
MAX_ORDER_SIZE = 100_000
MIN_PRICE_STEP = 0.01

# Volatility & Market Parameters
MIN_VOLATILITY = 0.001
MAX_VOLATILITY = 0.50
VOLATILITY_MEAN_REVERSION = 0.05  # How fast vol reverts to mean
BASE_VOLATILITY = 0.02  # 2% daily vol baseline

# ============================================================================
# RATE LIMITING (Groq Free Tier: 30 req/min)
# ============================================================================

GROQ_RATE_LIMIT = 30  # requests per minute
GROQ_RATE_WINDOW = 60  # seconds

# ============================================================================
# NIM CONFIGURATION
# ============================================================================

NIM_EMBEDDINGS_MODEL = "nvidia/nv-embed-qa-4"
NIM_BASE_URL = os.getenv("NIM_BASE_URL", "http://localhost:8000/v1")

# ============================================================================
# VECTOR STORE - HISTORICAL EVENTS FOR RAG
# ============================================================================

HISTORICAL_EVENTS = [
    {
        "title": "2008 Financial Crisis",
        "description": "Lehman Brothers collapse, credit freeze, VIX spike to 80",
        "impact": "extreme_bearish",
        "volatility_spike": 0.8,
    },
    {
        "title": "COVID-19 Market Crash",
        "description": "Global pandemic announcement, lockdowns, 30% S&P decline in weeks",
        "impact": "extreme_bearish",
        "volatility_spike": 0.6,
    },
    {
        "title": "GameStop Meme Stock Rally",
        "description": "Reddit-coordinated retail buying, squeeze short sellers, 1000% gains",
        "impact": "extreme_bullish",
        "volatility_spike": 0.5,
    },
    {
        "title": "Fed Rate Hike Announcement",
        "description": "FOMC announces interest rate increase, inflation concerns",
        "impact": "bearish",
        "volatility_spike": 0.3,
    },
    {
        "title": "Apple Earnings Beat",
        "description": "Strong quarterly earnings, revenue growth, positive guidance",
        "impact": "bullish",
        "volatility_spike": 0.15,
    },
    {
        "title": "Trade War Escalation",
        "description": "New tariffs announced, market uncertainty, retaliatory measures",
        "impact": "bearish",
        "volatility_spike": 0.25,
    },
    {
        "title": "Tech IPO Boom",
        "description": "Multiple successful IPOs, venture funding surge, speculation peak",
        "impact": "bullish",
        "volatility_spike": 0.2,
    },
    {
        "title": "Crypto Crash",
        "description": "Bitcoin plunge, stablecoin depegging, contagion fears",
        "impact": "extreme_bearish",
        "volatility_spike": 0.7,
    },
]

# ============================================================================
# DEFAULT AGENT PERSONALITIES
# ============================================================================

DEFAULT_PERSONALITIES: Dict[str, Dict[str, Any]] = {
    "hedge_fund": {
        "name": "Quantitative Hedge Fund",
        "description": "Data-driven, options-focused, SEC filings analyst",
        "risk_tolerance": 0.8,
        "trade_frequency": 0.4,  # Acts 40% of ticks
        "position_size_multiplier": 2.0,
        "decision_style": "analytical",
        "prompt_suffix": "Analyze technical indicators, implied volatility, and macroeconomic data. Focus on probability-weighted returns and risk-adjusted positions.",
    },
    "retail": {
        "name": "Retail Investor",
        "description": "Emotional, herding behavior, FOMO/panic trader",
        "risk_tolerance": 0.3,
        "trade_frequency": 0.6,  # Acts 60% of ticks
        "position_size_multiplier": 0.5,
        "decision_style": "emotional",
        "prompt_suffix": "React to market sentiment and news. Follow trends, respond to peer behavior, and manage fear/greed emotions.",
    },
    "news": {
        "name": "News Broadcaster",
        "description": "Sentiment classifier, news distributor",
        "risk_tolerance": 0.1,
        "trade_frequency": 0.3,
        "position_size_multiplier": 0.0,
        "decision_style": "informational",
        "prompt_suffix": "Classify news sentiment and broadcast to market. No direct trading.",
    },
    "regulator": {
        "name": "Market Regulator",
        "description": "Circuit breaker, halt enforcement, rule enforcer",
        "risk_tolerance": 0.0,
        "trade_frequency": 0.1,
        "position_size_multiplier": 0.0,
        "decision_style": "regulatory",
        "prompt_suffix": "Monitor for circuit breaker conditions, sudden price moves, and manipulation. Enforce trading halts if needed.",
    },
    "market_maker": {
        "name": "Market Maker",
        "description": "Liquidity provider, bid/ask spreads, quote provider",
        "risk_tolerance": 0.2,
        "trade_frequency": 0.9,  # Acts 90% of ticks
        "position_size_multiplier": 1.0,
        "decision_style": "mechanical",
        "prompt_suffix": "Provide liquidity with tight spreads. Adjust for volatility and inventory. Focus on volume and consistency.",
    },
}

# ============================================================================
# PRESET SCENARIOS
# ============================================================================

PRESET_SCENARIOS = {
    "normal_market": {
        "name": "Normal Market Conditions",
        "description": "Calm, efficient market with stable volatility",
        "agents": {
            "hedge_fund": 20,
            "retail": 30,
            "news": 5,
            "regulator": 2,
            "market_maker": 10,
        },
        "initial_volatility": 0.02,
        "market_efficiency": 0.8,
    },
    "bull_run": {
        "name": "Bull Market Rally",
        "description": "Sustained uptrend with strong momentum",
        "agents": {
            "hedge_fund": 15,
            "retail": 50,
            "news": 5,
            "regulator": 2,
            "market_maker": 8,
        },
        "initial_volatility": 0.025,
        "market_efficiency": 0.6,
    },
    "bear_crash": {
        "name": "Market Crash",
        "description": "Extreme volatility, panic selling, circuit breaker testing",
        "agents": {
            "hedge_fund": 30,
            "retail": 40,
            "news": 10,
            "regulator": 5,
            "market_maker": 15,
        },
        "initial_volatility": 0.4,
        "market_efficiency": 0.2,
    },
    "meme_frenzy": {
        "name": "Meme Stock Frenzy",
        "description": "Reddit-coordinated retail buying, sentiment-driven bubbles",
        "agents": {
            "hedge_fund": 10,
            "retail": 80,
            "news": 8,
            "regulator": 3,
            "market_maker": 5,
        },
        "initial_volatility": 0.35,
        "market_efficiency": 0.1,
    },
    "flash_crash": {
        "name": "Flash Crash",
        "description": "Sudden market dislocation, rapid recovery, liquidity crisis",
        "agents": {
            "hedge_fund": 25,
            "retail": 20,
            "news": 8,
            "regulator": 8,
            "market_maker": 20,
        },
        "initial_volatility": 0.5,
        "market_efficiency": 0.05,
    },
}

# ============================================================================
# PROMPT TEMPLATES
# ============================================================================

SENTIMENT_ANALYSIS_PROMPT = """Analyze the sentiment of the following news headline and classify it as:
- bullish: positive outlook for asset price
- bearish: negative outlook for asset price
- neutral: no clear directional bias

Headline: {headline}

Respond with JSON: {{"sentiment": "bullish|bearish|neutral", "confidence": 0.0-1.0}}"""

DECISION_PROMPT_TEMPLATE = """You are a {agent_type} in a financial market simulation.

Current Market State:
- Price: ${price}
- Volatility: {volatility:.2%}
- Order Spread: ${bid} - ${ask}
- Recent Volume: {volume}
- Overall Sentiment: {sentiment}

Your Agent Profile:
- Risk Tolerance: {risk_tolerance}
- Position Size Preference: {position_multiplier}x

Recent Market Events:
{recent_events}

Historical Similar Events:
{historical_context}

Based on this information, should you:
1. BUY (specify size 0-100k shares)
2. SELL (specify size 0-100k shares)
3. HOLD (maintain current position)

{agent_suffix}

Respond with JSON: {{"action": "buy|sell|hold", "size": 0-100000, "reasoning": "brief explanation"}}"""

# ============================================================================
# LOGGING
# ============================================================================

LOG_LEVEL = "INFO" if not DEBUG else "DEBUG"

# ============================================================================
# EXPORT CONSTANTS FOR EASY IMPORT
# ============================================================================

__all__ = [
    "GROQ_API_KEY",
    "NIM_API_KEY",
    "NEWS_API_KEY",
    "REDIS_URL",
    "API_HOST",
    "API_PORT",
    "DEBUG",
    "TICK_DURATION_MS",
    "MAX_TICKS",
    "INITIAL_PRICE",
    "INITIAL_VOLUME",
    "DEFAULT_AGENT_COUNT",
    "AGENT_TYPES",
    "DEFAULT_PERSONALITIES",
    "PRESET_SCENARIOS",
    "HISTORICAL_EVENTS",
    "SENTIMENT_ANALYSIS_PROMPT",
    "DECISION_PROMPT_TEMPLATE",
    "GROQ_RATE_LIMIT",
    "GROQ_RATE_WINDOW",
    "NIM_EMBEDDINGS_MODEL",
    "NIM_BASE_URL",
]
