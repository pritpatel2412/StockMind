"""Simulation data persistence and retrieval service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from typing import Optional, List
from models.database_models import Simulation, SimulationTick, AgentAction, User
from models.schemas import SimulationData, SimulationMetadata
from datetime import datetime
import uuid
import json


class SimulationDataService:
    """Handle simulation data persistence."""

    @staticmethod
    async def create_simulation(
        user_id: str,
        name: str,
        ticker: str,
        scenario: str,
        agent_count: int,
        time_horizon: str,
        config: dict,
        start_price: float,
        session: AsyncSession,
    ) -> Simulation:
        """Create new simulation record."""
        simulation = Simulation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            name=name,
            ticker=ticker,
            scenario=scenario,
            agent_count=agent_count,
            time_horizon=time_horizon,
            status="running",
            start_price=start_price,
            config=config,
            started_at=datetime.utcnow(),
        )
        session.add(simulation)
        await session.commit()
        await session.refresh(simulation)
        return simulation

    @staticmethod
    async def save_tick(
        simulation_id: str,
        tick_number: int,
        price: float,
        volume: float,
        sentiment: dict,
        session: AsyncSession,
    ) -> SimulationTick:
        """Save tick data."""
        tick = SimulationTick(
            id=str(uuid.uuid4()),
            simulation_id=simulation_id,
            tick_number=tick_number,
            price=price,
            volume=volume,
            sentiment_bullish=sentiment.get("bullish", 0),
            sentiment_bearish=sentiment.get("bearish", 0),
            sentiment_neutral=sentiment.get("neutral", 0),
            timestamp=datetime.utcnow(),
        )
        session.add(tick)
        await session.commit()
        await session.refresh(tick)
        return tick

    @staticmethod
    async def save_agent_action(
        simulation_id: str,
        tick_id: Optional[str],
        agent_id: str,
        agent_type: str,
        action: str,
        quantity: int,
        price: float,
        reasoning: Optional[str],
        sentiment_input: dict,
        session: AsyncSession,
    ) -> AgentAction:
        """Save agent action."""
        agent_action = AgentAction(
            id=str(uuid.uuid4()),
            simulation_id=simulation_id,
            tick_id=tick_id,
            agent_id=agent_id,
            agent_type=agent_type,
            action=action,
            quantity=quantity,
            price=price,
            reasoning=reasoning,
            sentiment_input=sentiment_input,
            timestamp=datetime.utcnow(),
        )
        session.add(agent_action)
        await session.commit()
        return agent_action

    @staticmethod
    async def update_simulation_status(
        simulation_id: str,
        status: str,
        end_price: Optional[float] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        final_sentiment: Optional[dict] = None,
        total_ticks: int = 0,
        session: AsyncSession = None,
    ) -> Optional[Simulation]:
        """Update simulation status and final data."""
        if not session:
            return None

        result = await session.execute(select(Simulation).where(Simulation.id == simulation_id))
        simulation = result.scalar_one_or_none()

        if not simulation:
            return None

        simulation.status = status
        if end_price is not None:
            simulation.end_price = end_price
        if min_price is not None:
            simulation.min_price = min_price
        if max_price is not None:
            simulation.max_price = max_price
        if final_sentiment is not None:
            simulation.final_sentiment = final_sentiment
        if total_ticks > 0:
            simulation.total_ticks = total_ticks
        if status == "completed":
            simulation.completed_at = datetime.utcnow()

        await session.commit()
        await session.refresh(simulation)
        return simulation

    @staticmethod
    async def get_simulation_by_id(
        simulation_id: str,
        user_id: str,
        session: AsyncSession,
    ) -> Optional[Simulation]:
        """Get simulation by ID (user-scoped)."""
        result = await session.execute(
            select(Simulation).where(
                Simulation.id == simulation_id,
                Simulation.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_simulations(
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        session: AsyncSession = None,
    ) -> List[Simulation]:
        """Get all simulations for a user."""
        if not session:
            return []

        result = await session.execute(
            select(Simulation)
            .where(Simulation.user_id == user_id)
            .order_by(desc(Simulation.created_at))
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    @staticmethod
    async def get_simulation_history(
        simulation_id: str,
        user_id: str,
        limit: int = 1000,
        session: AsyncSession = None,
    ) -> List[SimulationTick]:
        """Get tick history for simulation."""
        if not session:
            return []

        # First verify user owns simulation
        result = await session.execute(
            select(Simulation).where(
                Simulation.id == simulation_id,
                Simulation.user_id == user_id,
            )
        )
        if not result.scalar_one_or_none():
            return []

        # Get ticks
        result = await session.execute(
            select(SimulationTick)
            .where(SimulationTick.simulation_id == simulation_id)
            .order_by(SimulationTick.tick_number)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def get_agent_actions(
        simulation_id: str,
        user_id: str,
        agent_type: Optional[str] = None,
        limit: int = 1000,
        session: AsyncSession = None,
    ) -> List[AgentAction]:
        """Get agent actions from simulation."""
        if not session:
            return []

        # First verify user owns simulation
        result = await session.execute(
            select(Simulation).where(
                Simulation.id == simulation_id,
                Simulation.user_id == user_id,
            )
        )
        if not result.scalar_one_or_none():
            return []

        # Build query
        query = select(AgentAction).where(AgentAction.simulation_id == simulation_id)

        if agent_type:
            query = query.where(AgentAction.agent_type == agent_type)

        query = query.limit(limit)

        result = await session.execute(query)
        return result.scalars().all()
