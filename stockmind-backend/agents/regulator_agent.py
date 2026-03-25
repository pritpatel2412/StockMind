"""
Regulator Agent
Circuit breaker enforcement and trading halt logic
"""

from typing import Dict, Any, Optional

from agents.base_agent import BaseAgent
from models.schemas import AgentPersonality, AgentActionType
from models.simulation_state import WorldState
from config import DEFAULT_PERSONALITIES


class RegulatorAgent(BaseAgent):
    """Regulator agent: circuit breaker, trading halts, no trading."""
    
    def __init__(self, initial_cash: float = 0.0):
        """Initialize regulator agent."""
        personality = DEFAULT_PERSONALITIES["regulator"]
        super().__init__(
            agent_type="regulator",
            personality=AgentPersonality(**personality),
            initial_cash=initial_cash,
        )
        self.circuit_breaker_threshold = 0.20  # 20% move
        self.halt_duration = 5  # ticks
    
    async def observe(self, world_state: WorldState) -> Dict[str, Any]:
        """Monitor for circuit breaker conditions."""
        self.remember(f"Volatility: {world_state.volatility:.2%}, Halted: {world_state.is_halted}")
        
        return {
            "is_halted": world_state.is_halted,
            "current_price": world_state.current_price,
            "volatility": world_state.volatility,
            "tick": world_state.current_tick,
        }
    
    async def decide(
        self,
        observations: Dict[str, Any],
        world_state: WorldState,
    ) -> Dict[str, Any]:
        """Determine if circuit breaker should trigger."""
        if world_state.is_circuit_breaker_triggered(self.circuit_breaker_threshold):
            return {
                "action": "halt",
                "reason": f"Price move > {self.circuit_breaker_threshold:.0%}",
            }
        
        return {"action": "allow", "reason": "Normal trading"}
    
    async def act(
        self,
        decision: Dict[str, Any],
        world_state: WorldState,
    ) -> Optional[Dict[str, Any]]:
        """Execute regulatory decision."""
        if decision.get("action") == "halt" and not world_state.is_halted:
            world_state.is_halted = True
            world_state.halt_reason = decision.get("reason", "Circuit breaker triggered")
            world_state.halt_end_tick = world_state.current_tick + self.halt_duration
            
            return {
                "type": "halt",
                "reason": world_state.halt_reason,
                "duration_ticks": self.halt_duration,
            }
        
        return None
    
    async def check_halt_expiration(self, world_state: WorldState) -> bool:
        """Check if halt should be lifted."""
        if world_state.is_halted and world_state.halt_end_tick:
            if world_state.current_tick >= world_state.halt_end_tick:
                world_state.is_halted = False
                world_state.halt_reason = None
                world_state.halt_end_tick = None
                return True
        return False
