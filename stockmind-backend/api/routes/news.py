"""
News API Routes
/api/news/* endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

# Reference to global engine
engine = None


def set_engine(sim_engine):
    """Set the simulation engine reference."""
    global engine
    engine = sim_engine


@router.get("/{simulation_id}")
async def get_news_feed(
    simulation_id: str,
    sentiment: Optional[str] = None,
    limit: int = 20,
):
    """
    Get news feed for simulation.
    
    Args:
        simulation_id: Simulation ID
        sentiment: Filter by sentiment (bullish, bearish, neutral)
        limit: Number of items to return
        
    Returns:
        List of news items
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    world_state = engine.simulations[simulation_id]["world_state"]
    
    news_items = world_state.recent_news
    
    # Filter by sentiment if specified
    if sentiment:
        news_items = [
            n for n in news_items
            if sentiment.lower() in n.sentiment.value
        ]
    
    return {
        "simulation_id": simulation_id,
        "total_items": len(news_items),
        "news": [
            n.model_dump()
            for n in news_items[:limit]
        ],
    }


@router.get("/{simulation_id}/sentiment")
async def get_sentiment_summary(simulation_id: str):
    """Get current market sentiment."""
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    world_state = engine.simulations[simulation_id]["world_state"]
    
    return {
        "simulation_id": simulation_id,
        "overall_sentiment": world_state.sentiment.value,
        "sentiment_scores": world_state.sentiment_scores,
        "news_count": len(world_state.recent_news),
        "dominant_themes": ["tech", "earnings", "fed", "inflation"][:3],
    }
