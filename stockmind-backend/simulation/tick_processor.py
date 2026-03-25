"""
Tick Processor
Per-tick simulation logic: observe → decide → act → price update
"""

from typing import List, Dict, Any, Optional
import asyncio

from agents.base_agent import BaseAgent
from models.simulation_state import WorldState
from data.market_fetcher import MarketFetcher


class TickProcessor:
    """Processes single tick of simulation with all agents."""
    
    def __init__(self, market_fetcher: MarketFetcher):
        """
        Initialize tick processor.
        
        Args:
            market_fetcher: Market data provider
        """
        self.market_fetcher = market_fetcher
    
    async def process_tick(
        self,
        world_state: WorldState,
        agents: List[BaseAgent],
        regulator_agent: Optional[BaseAgent] = None,
    ) -> Dict[str, Any]:
        """
        Process single tick: news → observe → decide → act → price update.
        
        Args:
            world_state: Current simulation state
            agents: List of trading agents
            regulator_agent: Optional regulator for circuit breakers
            
        Returns:
            Tick results with actions and metrics
        """
        tick_result = {
            "tick": world_state.current_tick,
            "actions": [],
            "news_items": [],
            "halt_triggered": False,
            "errors": [],
        }
        
        # Check for halt expiration
        if regulator_agent and hasattr(regulator_agent, 'check_halt_expiration'):
            halt_expired = await regulator_agent.check_halt_expiration(world_state)
            if halt_expired:
                tick_result["halt_expired"] = True
        
        # If halted, skip trading but update price slightly
        if world_state.is_halted:
            tick_result["halted"] = True
            await self._update_price_idle(world_state)
            return tick_result
        
        # Phase 1: Observe - all agents gather information
        try:
            observations = await asyncio.gather(*[
                agent.observe(world_state)
                for agent in agents
            ])
        except Exception as e:
            tick_result["errors"].append(f"Observe phase error: {str(e)}")
            observations = [{} for _ in agents]
        
        # Phase 2: Decide - all agents make decisions (uses LLM)
        try:
            decisions = await asyncio.gather(*[
                agent.decide(obs, world_state)
                for agent, obs in zip(agents, observations)
            ])
        except Exception as e:
            tick_result["errors"].append(f"Decide phase error: {str(e)}")
            decisions = [{"action": "hold", "size": 0} for _ in agents]
        
        # Phase 3: Act - execute trades
        tick_actions = []
        for agent, decision in zip(agents, decisions):
            try:
                # Update agent sentiment tracker
                action_str = str(decision.get("action", "hold")).lower()
                if action_str == "buy":
                    agent.sentiment = 0.5
                elif action_str == "sell":
                    agent.sentiment = -0.5
                else:
                    agent.sentiment = 0.0

                action = await agent.act(decision, world_state)
                if action:
                    tick_actions.append(action)
                    tick_result["actions"].append({
                        "agent_id": agent.agent_id,
                        "agent_type": agent.agent_type,
                        "action": action.action.value,
                        "size": action.size,
                        "price": action.price,
                    })
            except Exception as e:
                tick_result["errors"].append(
                    f"Agent {agent.agent_id} act error: {str(e)}"
                )
        
        # Phase 4: Regulatory check (circuit breaker)
        if regulator_agent:
            try:
                reg_observations = await regulator_agent.observe(world_state)
                reg_decision = await regulator_agent.decide(reg_observations, world_state)
                reg_action = await regulator_agent.act(reg_decision, world_state)
                
                if reg_action and reg_action.get("type") == "halt":
                    tick_result["halt_triggered"] = True
                    tick_result["halt_reason"] = reg_action.get("reason")
            except Exception as e:
                tick_result["errors"].append(f"Regulator error: {str(e)}")
        
        # Phase 5: Price update based on order flow
        await self._update_price(world_state, tick_actions)
        
        # Phase 6: Update tick metrics
        world_state.current_tick += 1
        world_state.current_tick_volume = 0
        world_state.total_trades += len(tick_actions)
        
        return tick_result
    
    async def _update_price(
        self,
        world_state: WorldState,
        actions: List[Any],
    ) -> None:
        """
        Update price based on agent actions (order flow).
        
        Args:
            world_state: State to update
            actions: Agent actions this tick
        """
        if not actions:
            # Random walk if no trades
            import random
            shock = random.gauss(0, world_state.volatility)
            new_price = world_state.current_price * (1 + shock)
            world_state.update_price(new_price, 0)
            return
        
        # Calculate volume-weighted price from trades
        total_value = 0
        total_volume = 0
        
        for action in actions:
            volume = action.size
            price = action.price
            
            total_value += price * volume
            total_volume += volume
        
        # New price = VWAP of trades
        if total_volume > 0:
            new_price = total_value / total_volume
            world_state.update_price(new_price, total_volume)
    
    async def _update_price_idle(self, world_state: WorldState) -> None:
        """Update price slightly during halt."""
        import random
        shock = random.gauss(0, world_state.volatility * 0.1)  # Reduced vol
        new_price = world_state.current_price * (1 + shock)
        world_state.update_price(new_price, 0)
