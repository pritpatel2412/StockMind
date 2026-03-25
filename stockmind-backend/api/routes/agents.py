"""
Agents API Routes
/api/agents/* endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

# Reference to global engine
engine = None


def set_engine(sim_engine):
    """Set the simulation engine reference."""
    global engine
    engine = sim_engine


@router.get("/{simulation_id}")
async def list_agents(simulation_id: str):
    """
    List all agents in simulation.
    
    Args:
        simulation_id: Simulation ID
        
    Returns:
        List of agents with their states
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    sim = engine.simulations[simulation_id]
    world_state = sim["world_state"]
    
    return {
        "simulation_id": simulation_id,
        "total_agents": len(sim["agents"]),
        "agents": [
            {
                "agent_id": agent.agent_id,
                "agent_type": agent.agent_type,
                "personality": agent.personality.model_dump(),
                "state": agent.to_state(world_state.current_price).model_dump(),
            }
            for agent in sim["agents"]
        ],
    }


@router.get("/{simulation_id}/{agent_id}")
async def get_agent_detail(simulation_id: str, agent_id: str):
    """
    Get detailed agent information.
    
    Args:
        simulation_id: Simulation ID
        agent_id: Agent ID
        
    Returns:
        Detailed agent state and history
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    sim = engine.simulations[simulation_id]
    world_state = sim["world_state"]
    
    agent = None
    for a in sim["agents"]:
        if a.agent_id == agent_id:
            agent = a
            break
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "agent_id": agent.agent_id,
        "agent_type": agent.agent_type,
        "personality": agent.personality.model_dump(),
        "state": agent.to_state(world_state.current_price).model_dump(),
        "memory": agent.observation_memory[-5:],
        "trades": [
            {
                "timestamp": t.timestamp.isoformat(),
                "action": t.action.value,
                "size": t.size,
                "price": t.price,
                "reasoning": t.reasoning,
            }
            for t in agent.trades[-20:]
        ],
    }


@router.get("/{simulation_id}/portfolio/summary")
async def get_portfolio_summary(simulation_id: str):
    """Get aggregate portfolio metrics."""
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    sim = engine.simulations[simulation_id]
    world_state = sim["world_state"]
    
    total_portfolio_value = 0
    total_realized_pnl = 0
    
    for agent in sim["agents"]:
        total_portfolio_value += agent.get_portfolio_value(world_state.current_price)
        total_realized_pnl += agent.realized_pnl
    
    return {
        "simulation_id": simulation_id,
        "total_agents": len(sim["agents"]),
        "aggregate_portfolio_value": total_portfolio_value,
        "aggregate_realized_pnl": total_realized_pnl,
        "price_change_percent": (
            (world_state.current_price - 100) / 100 * 100
        ),
    }
