"""
Pydantic v2 Response Models and Schemas
API request/response types and data validation
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# ============================================================================
# ENUMS
# ============================================================================

class SentimentType(str, Enum):
    """Market sentiment classification"""
    EXTREME_BULLISH = "extreme_bullish"
    BULLISH = "bullish"
    NEUTRAL = "neutral"
    BEARISH = "bearish"
    EXTREME_BEARISH = "extreme_bearish"


class AgentActionType(str, Enum):
    """Agent action types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class SimulationStatus(str, Enum):
    """Simulation state"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


# ============================================================================
# AGENT SCHEMAS
# ============================================================================

class AgentPersonality(BaseModel):
    """Agent personality configuration"""
    name: str
    description: str
    risk_tolerance: float = Field(ge=0.0, le=1.0)
    trade_frequency: float = Field(ge=0.0, le=1.0)
    position_size_multiplier: float = Field(ge=0.0, le=10.0)
    decision_style: str


class AgentState(BaseModel):
    """Agent state snapshot"""
    agent_id: str
    agent_type: str
    personality: AgentPersonality
    current_price: float
    shares_held: int
    cash_balance: float
    total_portfolio_value: float
    realized_pnl: float
    unrealized_pnl: float
    win_rate: float
    total_trades: int
    last_action: Optional[AgentActionType] = None
    last_action_size: int = 0


class AgentAction(BaseModel):
    """Agent decision output"""
    agent_id: str
    action: AgentActionType
    size: int = Field(ge=0, le=100_000)
    price: float
    reasoning: str
    timestamp: datetime


# ============================================================================
# ORDER & PRICE SCHEMAS
# ============================================================================

class OrderBook(BaseModel):
    """Order book state"""
    bids: List[tuple[float, int]]  # [(price, quantity), ...]
    asks: List[tuple[float, int]]
    spread: float
    mid_price: float


class PriceLevel(BaseModel):
    """Single price level in order book"""
    price: float
    quantity: int
    side: str  # "bid" or "ask"


# ============================================================================
# NEWS & SENTIMENT SCHEMAS
# ============================================================================

class NewsItem(BaseModel):
    """News headline with sentiment"""
    title: str
    source: str
    url: str
    sentiment: SentimentType
    confidence: float = Field(ge=0.0, le=1.0)
    impact_score: float = Field(ge=0.0, le=1.0)
    published_at: datetime
    summary: Optional[str] = None


class SentimentBreakdown(BaseModel):
    """Market sentiment aggregation"""
    overall_sentiment: SentimentType
    bullish_score: float = Field(ge=0.0, le=1.0)
    bearish_score: float = Field(ge=0.0, le=1.0)
    neutral_score: float = Field(ge=0.0, le=1.0)
    news_count: int
    dominant_themes: List[str] = []


# ============================================================================
# TICK & PRICE HISTORY
# ============================================================================

class TickUpdate(BaseModel):
    """Single tick/candle data"""
    tick: int
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    vwap: float
    volatility: float


class PriceHistory(BaseModel):
    """Price history with multiple scenarios"""
    base_price: List[TickUpdate]  # Actual price
    bull_scenario: List[TickUpdate]  # If all agents bullish
    bear_scenario: List[TickUpdate]  # If all agents bearish


# ============================================================================
# SIMULATION STATE SCHEMAS
# ============================================================================

class SimulationConfig(BaseModel):
    """Simulation configuration"""
    scenario: str
    ticker: str = "AAPL"
    agent_count: int
    agent_distribution: Optional[Dict[str, int]] = None
    initial_price: float = 100.0
    initial_volume: int = 1_000_000
    max_ticks: int = 1000
    custom_volatility: Optional[float] = None


class SimulationSnapshot(BaseModel):
    """Current simulation state"""
    simulation_id: str
    status: SimulationStatus
    current_tick: int
    max_ticks: int
    current_price: float
    volatility: float
    sentiment: SentimentType
    total_agents: int
    active_agents: int
    total_volume_this_tick: int
    cumulative_volume: int
    price_change_percent: float
    order_book: OrderBook
    timestamp: datetime


# ============================================================================
# DETAILED SIMULATION STATE
# ============================================================================

class DetailedSimulationState(BaseModel):
    """Full simulation state with all details"""
    simulation_id: str
    status: SimulationStatus
    config: SimulationConfig
    current_tick: int
    current_price: float
    volatility: float
    sentiment: SentimentBreakdown
    agents: List[AgentState]
    recent_news: List[NewsItem]
    price_history: PriceHistory
    recent_actions: List[AgentAction]
    metrics: Dict[str, Any]
    error_message: Optional[str] = None


# ============================================================================
# API REQUEST/RESPONSE
# ============================================================================

class StartSimulationRequest(BaseModel):
    """Start simulation request"""
    scenario: str = "normal_market"
    ticker: str = "AAPL"
    agent_count: Optional[int] = None
    agent_distribution: Optional[Dict[str, int]] = None
    custom_volatility: Optional[float] = None


class SimulationStatusResponse(BaseModel):
    """Simulation status response"""
    simulation_id: str
    status: SimulationStatus
    current_tick: int
    current_price: float
    volatility: float
    error_message: Optional[str] = None


class TickUpdateMessage(BaseModel):
    """WebSocket tick update message"""
    message_type: str = "tick_update"
    simulation_id: str
    tick: int
    price: float
    volatility: float
    volume: int
    sentiment: SentimentType


class AgentActionMessage(BaseModel):
    """WebSocket agent action message"""
    message_type: str = "agent_action"
    simulation_id: str
    tick: int
    agent_action: AgentAction


class NewsBroadcastMessage(BaseModel):
    """WebSocket news broadcast message"""
    message_type: str = "news_broadcast"
    simulation_id: str
    tick: int
    news: NewsItem


class CircuitBreakerMessage(BaseModel):
    """WebSocket circuit breaker alert"""
    message_type: str = "circuit_breaker"
    simulation_id: str
    tick: int
    reason: str
    halt_duration: int  # ticks
