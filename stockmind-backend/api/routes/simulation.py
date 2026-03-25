"""
Simulation API Routes
/api/simulation/* endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Optional, Dict

from models.schemas import (
    StartSimulationRequest, SimulationStatusResponse, DetailedSimulationState
)

router = APIRouter()

# Reference to global engine (injected at runtime)
engine = None


def set_engine(sim_engine):
    """Set the simulation engine reference."""
    global engine
    engine = sim_engine


@router.post("/start")
async def start_simulation(
    request: StartSimulationRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start a new simulation.
    
    Args:
        request: Simulation configuration
        background_tasks: FastAPI background tasks
        
    Returns:
        Simulation ID and initial status
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    try:
        sim_id = await engine.create_simulation(
            scenario=request.scenario,
            ticker=request.ticker,
            agent_count=request.agent_count,
            agent_distribution=request.agent_distribution,
            custom_volatility=request.custom_volatility,
        )
        
        # Start simulation in background
        background_tasks.add_task(
            engine.start_simulation,
            sim_id,
            max_ticks=1000,
        )
        
        return {
            "simulation_id": sim_id,
            "status": "running",
            "message": f"Simulation {sim_id} started",
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status/{simulation_id}")
async def get_status(simulation_id: str) -> SimulationStatusResponse:
    """
    Get current simulation status.
    
    Args:
        simulation_id: Simulation ID
        
    Returns:
        Current status snapshot
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    status = engine.get_simulation_status(simulation_id)
    
    if "error" in status:
        raise HTTPException(status_code=404, detail=status["error"])
    
    return SimulationStatusResponse(**status)


@router.get("/details/{simulation_id}")
async def get_details(simulation_id: str):
    """
    Get detailed simulation state with all agent data.
    
    Args:
        simulation_id: Simulation ID
        
    Returns:
        Full simulation state
    """
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    sim = engine.simulations[simulation_id]
    world_state = sim["world_state"]
    
    # Convert to response model
    return {
        "simulation_id": simulation_id,
        "status": sim["status"].value,
        "current_tick": world_state.current_tick,
        "current_price": world_state.current_price,
        "volatility": world_state.volatility,
        "sentiment": world_state.sentiment.value,
        "agents": [
            agent.to_state(world_state.current_price).model_dump()
            for agent in sim["agents"]
        ],
        "recent_news": [
            news.model_dump()
            for news in world_state.recent_news[:10]
        ],
        "total_volume": world_state.cumulative_volume,
    }


@router.post("/pause/{simulation_id}")
async def pause_simulation(simulation_id: str):
    """Pause simulation."""
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    engine.pause_simulation(simulation_id)
    return {"status": "paused", "simulation_id": simulation_id}


@router.post("/resume/{simulation_id}")
async def resume_simulation(simulation_id: str):
    """Resume simulation."""
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    engine.resume_simulation(simulation_id)
    return {"status": "running", "simulation_id": simulation_id}


@router.get("/history/{simulation_id}")
async def get_price_history(simulation_id: str):
    """Get price history for simulation."""
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    if simulation_id not in engine.simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    world_state = engine.simulations[simulation_id]["world_state"]
    
    return {
        "simulation_id": simulation_id,
        "prices": [
            {
                "tick": tick.tick,
                "price": tick.close_price,
                "volume": sum(
                    len([a for a in engine.simulations[simulation_id]["tick_results"][tick.tick].get("actions", [])
                    if a.get("action") in ["buy", "sell"]])
                ) if tick.tick < len(engine.simulations[simulation_id]["tick_results"]) else 0,
            }
            for tick in world_state.price_history
        ],
    }
