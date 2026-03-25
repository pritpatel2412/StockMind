"""
Retail Agent
Emotional, herding behavior, FOMO/panic trading
"""

from typing import Dict, Any, Optional
import random

from agents.base_agent import BaseAgent
from models.schemas import AgentPersonality, AgentActionType, AgentAction
from models.simulation_state import WorldState
from utils.groq_client import GroqClient
from data.nim_embedder import NIMEmbedder
from config import DEFAULT_PERSONALITIES


class RetailAgent(BaseAgent):
    """Retail agent: emotional, herd follower, panic/FOMO trader."""
    
    def __init__(
        self,
        groq_client: GroqClient,
        embedder: NIMEmbedder,
        initial_cash: float = 50_000.0,
    ):
        """Initialize retail agent."""
        personality = DEFAULT_PERSONALITIES["retail"]
        super().__init__(
            agent_type="retail",
            personality=AgentPersonality(**personality),
            initial_cash=initial_cash,
        )
        self.groq_client = groq_client
        self.embedder = embedder
        self.emotion_state = "neutral"  # neutral, fomo, panic
    
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """Observe market emotionally: price momentum, sentiment."""
        self.remember(f"Sentiment: {world_state.sentiment}, News: {len(world_state.recent_news)}")
        
        return {
            "current_price": world_state.current_price,
            "sentiment": world_state.sentiment.value,
            "news_count": len(world_state.recent_news),
            "portfolio_value": self.get_portfolio_value(world_state.current_price),
            "cash_available": self.cash_balance,
            "position_size": self.shares_held,
        }
    
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """Make emotional trading decision."""
        query = f"Market sentiment {observations['sentiment']}, panic/fomo indicators"
        rag_context = await self.embedder.format_rag_context(query)
        
        recent_news_context = "\n".join([
            f"- {news.title} ({news.sentiment.value})"
            for news in world_state.recent_news[:3]
        ]) or "No recent news"
        
        decision = await self.groq_client.make_trading_decision(
            agent_type="retail",
            price=observations["current_price"],
            volatility=world_state.volatility,
            bid=world_state.bid,
            ask=world_state.ask,
            recent_volume=world_state.current_tick_volume,
            sentiment=observations["sentiment"],
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
        """Execute emotional decision."""
        try:
            action_str = decision.get("action", "hold").lower()
            size = min(int(decision.get("size", 0)), 50_000)
            reasoning = decision.get("reasoning", "Emotional reaction")
            
            if action_str not in ["buy", "sell", "hold"]:
                return None
            
            action = AgentActionType(action_str)
            execution_price = (world_state.bid + world_state.ask) / 2
            
            return await self.execute_trade(
                action=action,
                size=size,
                price=execution_price,
                reasoning=reasoning,
            )
        except Exception as e:
            print(f"[RetailAgent] Error: {e}")
            return None
