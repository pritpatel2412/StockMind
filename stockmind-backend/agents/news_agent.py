"""
News Agent
Sentiment classifier and news broadcaster
"""

from typing import Dict, Any, Optional

from agents.base_agent import BaseAgent
from models.schemas import AgentPersonality, AgentActionType, AgentAction, NewsItem
from models.simulation_state import WorldState
from utils.groq_client import GroqClient
from data.nim_embedder import NIMEmbedder
from data.news_fetcher import NewsFetcher
from config import DEFAULT_PERSONALITIES


class NewsAgent(BaseAgent):
    """News agent: classifies sentiment, broadcasts news, doesn't trade."""
    
    def __init__(
        self,
        groq_client: GroqClient,
        embedder: NIMEmbedder,
        news_fetcher: NewsFetcher,
        initial_cash: float = 1_000_000.0,
    ):
        """Initialize news agent."""
        personality = DEFAULT_PERSONALITIES["news"]
        super().__init__(
            agent_type="news",
            personality=AgentPersonality(**personality),
            initial_cash=initial_cash,
        )
        self.groq_client = groq_client
        self.embedder = embedder
        self.news_fetcher = news_fetcher
        self.last_news_tick = 0
    
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """Fetch and observe news."""
        self.remember(f"News items in system: {len(world_state.recent_news)}")
        
        return {
            "tick": world_state.current_tick,
            "news_count": len(world_state.recent_news),
            "current_sentiment": world_state.sentiment.value,
        }
    
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """
        Decide whether to broadcast news.
        News agents don't trade, so return hold.
        """
        return {
            "action": "hold",
            "size": 0,
            "reasoning": "News agent - broadcasting only",
        }
    
    async def act(
        self,
        decision: Dict[str, Any],
        world_state: WorldState,
    ) -> Optional[AgentAction]:
        """No trading for news agents."""
        return None
    
    async def broadcast_news(self, world_state: WorldState) -> Optional[NewsItem]:
        """Fetch and broadcast news to market."""
        articles = await self.news_fetcher.fetch_news(limit=1)
        
        if not articles:
            return None
        
        news_items = await self.news_fetcher.create_news_items(articles)
        
        if news_items:
            news_item = news_items[0]
            world_state.add_news(news_item)
            world_state.update_sentiment()
            return news_item
        
        return None
