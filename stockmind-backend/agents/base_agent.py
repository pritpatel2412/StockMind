"""
Base Agent Class
Abstract foundation for all agent types with personality, memory, and async methods
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
import asyncio
import uuid

from models.schemas import (
    AgentPersonality, AgentState, AgentActionType, AgentAction,
    SentimentType
)
from models.simulation_state import WorldState


class BaseAgent(ABC):
    """
    Abstract base class for all agent types.
    Implements personality, memory, portfolio tracking, and async decision methods.
    """
    
    def __init__(
        self,
        agent_type: str,
        personality: AgentPersonality,
        initial_cash: float = 1_000_000.0,
    ):
        """
        Initialize agent with personality and portfolio.
        
        Args:
            agent_type: Type of agent (hedge_fund, retail, etc.)
            personality: AgentPersonality configuration
            initial_cash: Starting cash balance
        """
        self.agent_id = str(uuid.uuid4())
        self.agent_type = agent_type
        self.personality = personality
        
        # Portfolio
        self.shares_held = 0
        self.cash_balance = initial_cash
        self.entry_prices: List[float] = []
        self.trades: List[AgentAction] = []
        
        # Statistics
        self.realized_pnl = 0.0
        self.winning_trades = 0
        self.total_trades = 0
        self.observation_memory: List[str] = []
        self.sentiment: float = 0.0  # -1.0 to 1.0 (bearish to bullish)
    
    def _update_pnl(self, current_price: float) -> None:
        """Update realized and unrealized P&L."""
        if self.shares_held > 0 and self.entry_prices:
            avg_entry = sum(self.entry_prices) / len(self.entry_prices)
            unrealized = (current_price - avg_entry) * self.shares_held
            return unrealized
        return 0.0
    
    def get_portfolio_value(self, current_price: float) -> float:
        """Get total portfolio value."""
        unrealized_pnl = self._update_pnl(current_price)
        return self.cash_balance + (self.shares_held * current_price) + unrealized_pnl
    
    def get_win_rate(self) -> float:
        """Get trading win rate."""
        if self.total_trades == 0:
            return 0.0
        return self.winning_trades / self.total_trades
    
    def to_state(self, current_price: float) -> AgentState:
        """Convert to AgentState for API serialization."""
        portfolio_value = self.get_portfolio_value(current_price)
        unrealized_pnl = self._update_pnl(current_price)
        
        return AgentState(
            agent_id=self.agent_id,
            agent_type=self.agent_type,
            personality=self.personality,
            current_price=current_price,
            shares_held=self.shares_held,
            cash_balance=self.cash_balance,
            total_portfolio_value=portfolio_value,
            realized_pnl=self.realized_pnl,
            unrealized_pnl=unrealized_pnl or 0.0,
            win_rate=self.get_win_rate(),
            total_trades=self.total_trades,
            last_action=self.trades[-1].action if self.trades else None,
            last_action_size=self.trades[-1].size if self.trades else 0,
        )
    
    def remember(self, observation: str) -> None:
        """Store observation in agent memory."""
        self.observation_memory.append(observation)
        # Keep only last 10 observations
        if len(self.observation_memory) > 10:
            self.observation_memory = self.observation_memory[-10:]
    
    async def execute_trade(
        self,
        action: AgentActionType,
        size: int,
        price: float,
        reasoning: str,
    ) -> Optional[AgentAction]:
        """
        Execute a trade and update portfolio.
        
        Args:
            action: BUY, SELL, or HOLD
            size: Number of shares
            price: Execution price
            reasoning: Trade reasoning
            
        Returns:
            AgentAction record or None if trade failed
        """
        trade_value = size * price
        
        if action == AgentActionType.BUY:
            if self.cash_balance < trade_value:
                return None  # Insufficient cash
            
            self.cash_balance -= trade_value
            self.shares_held += size
            self.entry_prices.append(price)
            self.entry_prices = self.entry_prices[-100:]  # Keep last 100
            
        elif action == AgentActionType.SELL:
            if self.shares_held < size:
                return None  # Insufficient shares
            
            self.cash_balance += trade_value
            self.shares_held -= size
            
            # Calculate P&L on sale
            if self.entry_prices:
                avg_entry = sum(self.entry_prices[-size:]) / min(size, len(self.entry_prices))
                pnl = (price - avg_entry) * size
                self.realized_pnl += pnl
                
                if pnl > 0:
                    self.winning_trades += 1
        
        elif action == AgentActionType.HOLD:
            return None  # No action taken
        
        self.total_trades += 1
        
        agent_action = AgentAction(
            agent_id=self.agent_id,
            action=action,
            size=size,
            price=price,
            reasoning=reasoning,
            timestamp=datetime.now(),
        )
        self.trades.append(agent_action)
        return agent_action
    
    @abstractmethod
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """
        Observe market state and generate observations.
        
        Args:
            world_state: Current WorldState
            
        Returns:
            Dictionary of observations (agent-specific)
        """
        pass
    
    @abstractmethod
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """
        Make trading decision based on observations.
        Uses LLM to generate decision with reasoning.
        
        Args:
            observations: Output from observe()
            world_state: Current WorldState
            
        Returns:
            Dictionary with action, size, and reasoning
        """
        pass
    
    @abstractmethod
    async def act(
        self,
        decision: Dict[str, Any],
        world_state: WorldState,
    ) -> Optional[AgentAction]:
        """
        Execute decision and return action record.
        
        Args:
            decision: Output from decide()
            world_state: Current WorldState
            
        Returns:
            AgentAction record or None
        """
        pass
    
    # Default no-op implementations for optional methods
    
    async def on_news(self, news_item: 'NewsItem') -> None:
        """React to news broadcast. Optional override."""
        pass
    
    async def on_price_update(self, new_price: float) -> None:
        """React to price update. Optional override."""
        pass
    
    async def on_halt(self, reason: str) -> None:
        """React to trading halt. Optional override."""
        pass
