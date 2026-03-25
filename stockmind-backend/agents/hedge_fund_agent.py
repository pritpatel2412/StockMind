"""
Hedge Fund Agent
Quantitative, data-driven, options-focused trading strategy
"""

from typing import Dict, Any, Optional
import random

from agents.base_agent import BaseAgent
from models.schemas import AgentPersonality, AgentActionType, AgentAction
from models.simulation_state import WorldState
from utils.groq_client import GroqClient
from data.nim_embedder import NIMEmbedder
from config import DEFAULT_PERSONALITIES


class HedgeFundAgent(BaseAgent):
    """
    Hedge fund agent: Quantitative, analyzes technical indicators,
    implied volatility, macroeconomic data, and SEC filings.
    """
    
    def __init__(
        self,
        groq_client: GroqClient,
        embedder: NIMEmbedder,
        initial_cash: float = 10_000_000.0,
    ):
        """
        Initialize hedge fund agent.
        
        Args:
            groq_client: Groq LLM client
            embedder: NIM embedder for RAG
            initial_cash: Starting capital
        """
        personality = DEFAULT_PERSONALITIES["hedge_fund"]
        super().__init__(
            agent_type="hedge_fund",
            personality=AgentPersonality(**personality),
            initial_cash=initial_cash,
        )
        self.groq_client = groq_client
        self.embedder = embedder
        self.volatility_threshold = 0.15
        self.position_target = 50000  # Target position size
    
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """
        Observe market conditions: volatility, technical indicators, sentiment.
        
        Args:
            world_state: Current market state
            
        Returns:
            Observations dictionary
        """
        self.remember(f"Price: ${world_state.current_price:.2f}, Vol: {world_state.volatility:.2%}")
        
        return {
            "current_price": world_state.current_price,
            "volatility": world_state.volatility,
            "bid": world_state.bid,
            "ask": world_state.ask,
            "sentiment": world_state.sentiment.value,
            "portfolio_value": self.get_portfolio_value(world_state.current_price),
            "cash_available": self.cash_balance,
            "position_size": self.shares_held,
            "recent_news_count": len(world_state.recent_news),
        }
    
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """
        Make trading decision based on quantitative analysis.
        
        Args:
            observations: Market observations
            world_state: Current state
            
        Returns:
            Decision dict with action, size, reasoning
        """
        # Get historical context for RAG
        query = f"Market volatility {observations['volatility']:.2%}, sentiment {observations['sentiment']}"
        rag_context = await self.embedder.format_rag_context(query)
        
        # Format recent news
        recent_news_context = "\n".join([
            f"- {news.title} ({news.sentiment.value})"
            for news in world_state.recent_news[:5]
        ]) or "No recent news"
        
        # Call LLM for decision
        decision = await self.groq_client.make_trading_decision(
            agent_type="hedge_fund",
            price=observations["current_price"],
            volatility=observations["volatility"],
            bid=observations["bid"],
            ask=observations["ask"],
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
        """
        Execute decision and update portfolio.
        
        Args:
            decision: LLM decision output
            world_state: Current state
            
        Returns:
            AgentAction or None
        """
        try:
            action_str = decision.get("action", "hold").lower()
            size = min(int(decision.get("size", 0)), 100_000)
            reasoning = decision.get("reasoning", "Quantitative analysis")
            
            if action_str not in ["buy", "sell", "hold"]:
                return None
            
            action = AgentActionType(action_str)
            
            # Use mid-price for execution
            execution_price = (world_state.bid + world_state.ask) / 2
            
            return await self.execute_trade(
                action=action,
                size=size,
                price=execution_price,
                reasoning=reasoning,
            )
        
        except Exception as e:
            print(f"[HedgeFundAgent] Error acting on decision: {e}")
            return None
