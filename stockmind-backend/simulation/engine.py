"""
Simulation Engine
Main orchestrator for market simulation
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import asyncio

from models.schemas import SimulationStatus, SentimentType
from models.simulation_state import WorldState, StateManager
from agents.hedge_fund_agent import HedgeFundAgent
from agents.retail_agent import RetailAgent
from agents.news_agent import NewsAgent
from agents.regulator_agent import RegulatorAgent
from agents.market_maker_agent import MarketMakerAgent
from data.market_fetcher import MarketFetcher
from data.news_fetcher import NewsFetcher
from data.nim_embedder import NIMEmbedder
from utils.groq_client import GroqClient
from simulation.tick_processor import TickProcessor
from config import (
    INITIAL_PRICE, INITIAL_VOLUME, PRESET_SCENARIOS, DEFAULT_PERSONALITIES,
    BASE_VOLATILITY, MAX_TICKS
)


class SimulationEngine:
    """Core simulation orchestrator."""
    
    def __init__(self):
        """Initialize simulation engine."""
        self.simulations: Dict[str, Dict[str, Any]] = {}
        self.groq_client = GroqClient()
        self.embedder = NIMEmbedder()
        self.market_fetcher = MarketFetcher()
        self.news_fetcher = NewsFetcher()
        self.tick_processor = TickProcessor(self.market_fetcher)
    
    async def initialize(self) -> None:
        """Initialize async clients."""
        await self.groq_client.initialize()
        await self.news_fetcher.initialize()
    
    async def shutdown(self) -> None:
        """Cleanup resources."""
        await self.groq_client.close()
        await self.news_fetcher.close()
    
    async def create_simulation(
        self,
        scenario: str = "normal_market",
        ticker: str = "AAPL",
        agent_count: Optional[int] = None,
        agent_distribution: Optional[Dict[str, int]] = None,
        custom_volatility: Optional[float] = None,
    ) -> str:
        """
        Create and initialize simulation.
        
        Args:
            scenario: Preset scenario name
            agent_count: Total agent count
            agent_distribution: Custom agent type distribution
            custom_volatility: Override scenario volatility
            
        Returns:
            Simulation ID
        """
        sim_id = str(uuid.uuid4())
        
        # Load scenario
        scenario_config = PRESET_SCENARIOS.get(scenario, PRESET_SCENARIOS["normal_market"])
        
        # Initialize world state with real market data
        self.market_fetcher.ticker = ticker
        start_price = await self.market_fetcher.get_current_price()
        
        # Fetch actual historical data for the chart
        hist_df = await self.market_fetcher.fetch_historical_data(period="1d", interval="15m")
        real_history = []
        try:
            # yfinance download returns a dict with 'Close' when converted to dict
            if hist_df and 'Close' in hist_df:
                closes = hist_df['Close']
                # Sort by timestamp
                for ts in sorted(closes.keys()):
                    real_history.append({
                        "time": ts.strftime("%H:%M") if hasattr(ts, 'strftime') else str(ts),
                        "price": float(closes[ts])
                    })
        except Exception as e:
            print(f"[SimulationEngine] Error parsing history: {e}")

        volatility = custom_volatility or scenario_config.get("initial_volatility", BASE_VOLATILITY)
        
        world_state = WorldState(
            simulation_id=sim_id,
            current_tick=0,
            start_time=datetime.now(),
            initial_price=start_price,
            current_price=start_price,
            price_history=[],
            real_price_history=real_history,
            volatility=volatility,
            bid=start_price - 0.05,
            ask=start_price + 0.05,
            order_book=self.market_fetcher.create_order_book(
                start_price,
                0.10,
                depth=10,
            ),
        )
        
        # Create agents based on distribution
        agent_dist = agent_distribution or scenario_config.get("agents", {})
        agents = []
        
        # Hedge fund agents
        for _ in range(agent_dist.get("hedge_fund", 0)):
            agents.append(HedgeFundAgent(self.groq_client, self.embedder))
        
        # Retail agents
        for _ in range(agent_dist.get("retail", 0)):
            agents.append(RetailAgent(self.groq_client, self.embedder))
        
        # News agent
        for _ in range(agent_dist.get("news", 0)):
            agents.append(NewsAgent(self.groq_client, self.embedder, self.news_fetcher))
        
        # Market maker agents
        for _ in range(agent_dist.get("market_maker", 0)):
            agents.append(MarketMakerAgent(self.groq_client, self.embedder))
        
        # Regulator agent (singleton)
        regulator = None
        if agent_dist.get("regulator", 0) > 0:
            regulator = RegulatorAgent()
        
        # Initialize agent states in world state
        for agent in agents:
            world_state.agents[agent.agent_id] = agent.to_state(start_price)
        
        # Store simulation
        self.simulations[sim_id] = {
            "world_state": world_state,
            "state_manager": StateManager(world_state),
            "agents": agents,
            "regulator": regulator,
            "status": SimulationStatus.IDLE,
            "tick_results": [],
            "paused": False,
        }
        
        return sim_id
    
    async def start_simulation(
        self,
        sim_id: str,
        max_ticks: int = MAX_TICKS,
    ) -> None:
        """
        Start simulation main loop.
        
        Args:
            sim_id: Simulation ID
            max_ticks: Maximum ticks to run
        """
        if sim_id not in self.simulations:
            raise ValueError(f"Simulation {sim_id} not found")
        
        sim = self.simulations[sim_id]
        sim["status"] = SimulationStatus.RUNNING
        sim["max_ticks"] = max_ticks
        
        world_state = sim["world_state"]
        agents = sim["agents"]
        regulator = sim["regulator"]
        
        try:
            while world_state.current_tick < max_ticks:
                # Check if paused
                while sim["paused"]:
                    await asyncio.sleep(0.1)
                
                # Process tick
                tick_result = await self.tick_processor.process_tick(
                    world_state,
                    agents,
                    regulator,
                )
                
                sim["tick_results"].append(tick_result)
                
                # Update agent states
                for agent in agents:
                    world_state.agents[agent.agent_id] = agent.to_state(world_state.current_price)
                
                # Broadcast updates
                if hasattr(self, "broadcast_callback") and self.broadcast_callback:
                    payload = {
                        "id": sim_id,
                        "timestamp": int(datetime.now().timestamp() * 1000),
                        "status": "running",
                        "currentTick": world_state.current_tick,
                        "totalTicks": max_ticks,
                        "currentPrice": world_state.current_price,
                        "priceChange": world_state.current_price - world_state.initial_price,
                        "priceChangePct": ((world_state.current_price - world_state.initial_price) / world_state.initial_price) * 100,
                        "priceHistory": [
                            {
                                "time": h["time"],
                                "historical": h["price"],
                                "simulated": None,
                                "volume": 50000,
                            } for h in world_state.real_price_history
                        ] + [
                            {
                                "time": f"+{t.tick}m",
                                "historical": None,
                                "simulated": t.close_price,
                                "bull": t.close_price * 1.05,
                                "bear": t.close_price * 0.95,
                                "volume": 10000,
                            } for t in world_state.price_history
                        ],
                        "circuitBreaker": getattr(world_state, "circuit_breaker_active", False),
                        "sentiment": {
                            "bullish": sum(1 for a in agents if a.sentiment > 0.3),
                            "neutral": sum(1 for a in agents if -0.3 <= a.sentiment <= 0.3),
                            "bearish": sum(1 for a in agents if a.sentiment < -0.3),
                        },
                        "predictions": {
                            "bullProbability": round((sum(1 for a in agents if a.sentiment > 0.3) / len(agents)) * 100, 1) if agents else 33.3,
                            "neutralProbability": round((sum(1 for a in agents if -0.3 <= a.sentiment <= 0.3) / len(agents)) * 100, 1) if agents else 33.4,
                            "bearProbability": round((sum(1 for a in agents if a.sentiment < -0.3) / len(agents)) * 100, 1) if agents else 33.3,
                            "predictedHigh": round(world_state.current_price * (1 + world_state.volatility), 2),
                            "predictedLow": round(world_state.current_price * (1 - world_state.volatility), 2),
                            "confidenceScore": round(80 + (world_state.current_tick / max_ticks) * 15, 1),
                        },
                        "totalAgents": len(agents),
                    }
                    await self.broadcast_callback(sim_id, payload)
                
                # Small delay to prevent CPU spinning
                await asyncio.sleep(0.01)
        
        except Exception as e:
            print(f"[SimulationEngine] Error in tick loop: {e}")
            sim["status"] = SimulationStatus.ERROR
        finally:
            if sim["status"] != SimulationStatus.ERROR:
                sim["status"] = SimulationStatus.COMPLETED
    
    def pause_simulation(self, sim_id: str) -> None:
        """Pause simulation."""
        if sim_id in self.simulations:
            self.simulations[sim_id]["paused"] = True
            self.simulations[sim_id]["status"] = SimulationStatus.PAUSED
    
    def resume_simulation(self, sim_id: str) -> None:
        """Resume simulation."""
        if sim_id in self.simulations:
            self.simulations[sim_id]["paused"] = False
            self.simulations[sim_id]["status"] = SimulationStatus.RUNNING
    
    def get_simulation_status(self, sim_id: str) -> Dict[str, Any]:
        """Get simulation status."""
        if sim_id not in self.simulations:
            return {"error": "Simulation not found"}
        
        sim = self.simulations[sim_id]
        world_state = sim["world_state"]
        
        return {
            "simulation_id": sim_id,
            "status": sim["status"].value,
            "current_tick": world_state.current_tick,
            "max_ticks": sim.get("max_ticks", MAX_TICKS),
            "current_price": world_state.current_price,
            "volatility": world_state.volatility,
            "sentiment": world_state.sentiment.value,
            "total_agents": len(sim["agents"]),
        }
