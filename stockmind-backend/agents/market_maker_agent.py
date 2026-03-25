"""
Market Maker Agent
Liquidity provider with bid/ask spreads
"""

from typing import Dict, Any, Optional
import random

from agents.base_agent import BaseAgent
from models.schemas import AgentPersonality, AgentActionType, AgentAction
from models.simulation_state import WorldState
from utils.groq_client import GroqClient
from data.nim_embedder import NIMEmbedder
from config import DEFAULT_PERSONALITIES


class MarketMakerAgent(BaseAgent):
    """Market maker: liquidity provider, quote provider, inventory management."""
    
    def __init__(
        self,
        groq_client: GroqClient,
        embedder: NIMEmbedder,
        initial_cash: float = 5_000_000.0,
    ):
        """Initialize market maker agent."""
        personality = DEFAULT_PERSONALITIES["market_maker"]
        super().__init__(
            agent_type="market_maker",
            personality=AgentPersonality(**personality),
            initial_cash=initial_cash,
        )
        self.groq_client = groq_client
        self.embedder = embedder
        self.target_inventory = 50000  # Shares to hold
        self.spread_multiplier = 1.0
    
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """Observe liquidity conditions and inventory."""
        self.remember(f"Spread: {world_state.ask - world_state.bid:.4f}, Inventory: {self.shares_held}")
        
        return {
            "current_price": world_state.current_price,
            "bid": world_state.bid,
            "ask": world_state.ask,
            "spread": world_state.ask - world_state.bid,
            "volatility": world_state.volatility,
            "current_inventory": self.shares_held,
            "order_book_depth": len(world_state.order_book.bids),
        }
    
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """Decide on quotes and inventory management."""
        query = f"Market making volatility {observations['volatility']:.2%}"
        rag_context = await self.embedder.format_rag_context(query)
        
        recent_news_context = "\n".join([
            f"- {news.title}"
            for news in world_state.recent_news[:2]
        ]) or "No recent news"
        
        decision = await self.groq_client.make_trading_decision(
            agent_type="market_maker",
            price=observations["current_price"],
            volatility=observations["volatility"],
            bid=observations["bid"],
            ask=observations["ask"],
            recent_volume=world_state.current_tick_volume,
            sentiment=world_state.sentiment.value,
            recent_news=recent_news_context,
            historical_context=rag_context,
            agent_suffix=self.personality.prompt_suffix,
        )
        
        return decision
    
    async def act(
        self,
        decision: Dict[str, Any],
        world_state: WorldState,
    ) -> Optional[AgentAction]:
        """Execute quote/inventory decision."""
        try:
            action_str = decision.get("action", "hold").lower()
            size = min(int(decision.get("size", 0)), 100_000)
            reasoning = decision.get("reasoning", "Market making")
            
            if action_str not in ["buy", "sell", "hold"]:
                return None
            
            action = AgentActionType(action_str)
            
            # Market makers trade at mid-price
            execution_price = (world_state.bid + world_state.ask) / 2
            
            return await self.execute_trade(
                action=action,
                size=size,
                price=execution_price,
                reasoning=reasoning,
            )
        except Exception as e:
            print(f"[MarketMakerAgent] Error: {e}")
            return None
