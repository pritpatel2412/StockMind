"""
Simulation World State Model
Central state container for all market and agent data
"""

from typing import List, Dict, Optional, Set, Any
from datetime import datetime
from pydantic import BaseModel, Field
import asyncio

from models.schemas import (
    SentimentType, AgentState, NewsItem, OrderBook, TickUpdate
)


class WorldState(BaseModel):
    """
    Central immutable state representation of the entire simulation.
    Protected by asyncio.Lock for thread-safe atomic updates.
    """
    
    # Simulation metadata
    simulation_id: str
    current_tick: int = 0
    start_time: datetime
    
    # Price and market data
    initial_price: float
    current_price: float
    price_history: List[TickUpdate] = Field(default_factory=list)
    real_price_history: List[Dict[str, Any]] = Field(default_factory=list)
    volatility: float
    bid: float
    ask: float
    
    # Volume and liquidity
    current_tick_volume: int = 0
    cumulative_volume: int = 0
    order_book: OrderBook
    
    # Agent states
    agents: Dict[str, AgentState] = Field(default_factory=dict)
    active_agents: Set[str] = Field(default_factory=set)
    
    # News and sentiment
    recent_news: List[NewsItem] = Field(default_factory=list)
    sentiment: SentimentType = SentimentType.NEUTRAL
    sentiment_scores: Dict[str, float] = Field(
        default_factory=lambda: {
            "bullish": 0.0,
            "bearish": 0.0,
            "neutral": 1.0,
        }
    )
    
    # Simulation control
    is_halted: bool = False
    halt_reason: Optional[str] = None
    halt_end_tick: Optional[int] = None
    
    # Metrics
    total_trades: int = 0
    
    class Config:
        """Pydantic configuration"""
        arbitrary_types_allowed = True
    
    def update_price(self, new_price: float, volume: int) -> None:
        """Update price and track volatility."""
        if self.current_price > 0:
            price_change = (new_price - self.current_price) / self.current_price
            # Update volatility with exponential moving average
            self.volatility = (
                0.9 * self.volatility + 
                0.1 * abs(price_change)
            )
        
        # Capture history before updating current price
        tick_update = TickUpdate(
            tick=self.current_tick,
            timestamp=datetime.now(),
            open_price=self.current_price,
            high_price=max(self.current_price, new_price),
            low_price=min(self.current_price, new_price),
            close_price=new_price,
            volume=volume,
            vwap=new_price,
            volatility=self.volatility
        )
        self.price_history.append(tick_update)
        
        self.current_price = new_price
        self.current_tick_volume += volume
        self.cumulative_volume += volume
        
        # Update bid/ask spread
        spread = max(0.01, self.volatility * self.current_price)
        self.bid = self.current_price - spread / 2
        self.ask = self.current_price + spread / 2
    
    def add_news(self, news: NewsItem, max_history: int = 50) -> None:
        """Add news item and maintain history."""
        self.recent_news.insert(0, news)
        if len(self.recent_news) > max_history:
            self.recent_news = self.recent_news[:max_history]
    
    def update_sentiment(self) -> None:
        """Calculate sentiment from recent news."""
        if not self.recent_news:
            self.sentiment = SentimentType.NEUTRAL
            self.sentiment_scores = {"bullish": 0.0, "bearish": 0.0, "neutral": 1.0}
            return
        
        bullish = 0.0
        bearish = 0.0
        
        # Weight recent news more heavily
        for i, news in enumerate(self.recent_news[:20]):
            weight = 1.0 / (i + 1)  # Inverse weight by recency
            
            if news.sentiment in ["extreme_bullish", "bullish"]:
                bullish += weight * news.confidence
            elif news.sentiment in ["extreme_bearish", "bearish"]:
                bearish += weight * news.confidence
        
        # Normalize
        total = bullish + bearish
        if total > 0:
            bullish /= total
            bearish /= total
        else:
            bullish = bearish = 0.5
        
        neutral = 1.0 - bullish - bearish
        
        self.sentiment_scores = {
            "bullish": bullish,
            "bearish": bearish,
            "neutral": neutral,
        }
        
        # Determine overall sentiment
        if bullish > 0.6:
            self.sentiment = SentimentType.EXTREME_BULLISH if bullish > 0.8 else SentimentType.BULLISH
        elif bearish > 0.6:
            self.sentiment = SentimentType.EXTREME_BEARISH if bearish > 0.8 else SentimentType.BEARISH
        else:
            self.sentiment = SentimentType.NEUTRAL
    
    def is_circuit_breaker_triggered(self, price_change_threshold: float = 0.20) -> bool:
        """Check if circuit breaker should activate (20% move)."""
        if len(self.price_history) < 2:
            return False
        
        prev_price = self.price_history[-1].close_price
        current_price = self.current_price
        
        price_change = abs((current_price - prev_price) / prev_price)
        return price_change > price_change_threshold
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return self.model_dump(mode='json')


# ============================================================================
# THREAD-SAFE STATE MANAGER
# ============================================================================

class StateManager:
    """Thread-safe wrapper around WorldState with locking."""
    
    def __init__(self, world_state: WorldState):
        self.state = world_state
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> WorldState:
        """Get lock and return state."""
        await self._lock.acquire()
        return self.state
    
    def release(self) -> None:
        """Release lock."""
        self._lock.release()
    
    async def update_atomic(self, update_func) -> None:
        """Execute update function atomically."""
        await self._lock.acquire()
        try:
            update_func(self.state)
        finally:
            self._lock.release()
