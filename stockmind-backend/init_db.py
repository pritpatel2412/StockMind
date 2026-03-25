"""Database initialization and migration script."""

import asyncio
import sys
from datetime import datetime
from database import init_db, engine, async_session_maker
from models.database_models import User, Simulation, SimulationTick, AgentAction, MarketData, NewsFeed, TokenBlacklist
from utils.auth_jwt import hash_password
import uuid


async def seed_demo_data():
    """Create demo user and sample data."""
    async with async_session_maker() as session:
        # Create demo user
        demo_user = User(
            id=str(uuid.uuid4()),
            email="demo@stockmind.ai",
            password_hash=hash_password("demo123456"),
            full_name="Demo User",
            is_active=True,
        )
        session.add(demo_user)
        await session.commit()
        print(f"[Seed] Created demo user: demo@stockmind.ai / demo123456")

        # Create sample simulation
        sample_sim = Simulation(
            id=str(uuid.uuid4()),
            user_id=demo_user.id,
            name="Demo Simulation - AAPL Bullish",
            ticker="AAPL",
            scenario="bullish",
            agent_count=500,
            time_horizon="1w",
            status="completed",
            start_price=150.0,
            end_price=155.0,
            min_price=149.5,
            max_price=156.0,
            total_ticks=100,
            created_at=datetime.utcnow(),
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            final_sentiment={"bullish": 0.65, "bearish": 0.15, "neutral": 0.20},
        )
        session.add(sample_sim)
        await session.commit()
        print(f"[Seed] Created sample simulation: {sample_sim.name}")


async def main():
    """Run database initialization."""
    print("[Database] Initializing StockMind database schema...")
    
    try:
        # Create all tables
        await init_db()
        print("[Database] Schema created successfully")
        
        # Seed demo data
        print("[Database] Seeding demo data...")
        await seed_demo_data()
        
        print("[Database] Database initialization complete!")
        print("[Database] Test credentials:")
        print("  Email: demo@stockmind.ai")
        print("  Password: demo123456")
        
    except Exception as e:
        print(f"[Error] Database initialization failed: {e}")
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
