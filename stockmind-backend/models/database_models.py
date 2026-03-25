"""SQLAlchemy ORM models for database persistence."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, JSON, Index, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """User account model."""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    simulations = relationship("Simulation", back_populates="user", cascade="all, delete-orphan")
    token_blacklist = relationship("TokenBlacklist", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_email_active", "email", "is_active"),
    )


class Simulation(Base):
    """Simulation run model."""
    __tablename__ = "simulations"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    ticker = Column(String, nullable=False, index=True)
    scenario = Column(String, nullable=False)  # "bullish", "bearish", "neutral", "crash"
    agent_count = Column(Integer, default=100, nullable=False)
    time_horizon = Column(String, default="1d", nullable=False)  # "1d", "1w", "1m", "3m"
    status = Column(String, default="completed", nullable=False, index=True)  # "running", "paused", "completed", "failed"
    total_ticks = Column(Integer, default=0, nullable=False)
    current_tick = Column(Integer, default=0, nullable=False)
    start_price = Column(Float, nullable=False)
    end_price = Column(Float, nullable=True)
    min_price = Column(Float, nullable=True)
    max_price = Column(Float, nullable=True)
    final_sentiment = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    config = Column(JSON, default={}, nullable=False)

    # Relationships
    user = relationship("User", back_populates="simulations")
    ticks = relationship("SimulationTick", back_populates="simulation", cascade="all, delete-orphan")
    actions = relationship("AgentAction", back_populates="simulation", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_simulation_user_created", "user_id", "created_at"),
        Index("idx_simulation_status", "status"),
    )


class SimulationTick(Base):
    """Tick-by-tick simulation data."""
    __tablename__ = "simulation_ticks"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    simulation_id = Column(String, ForeignKey("simulations.id"), nullable=False, index=True)
    tick_number = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=True)
    sentiment_bullish = Column(Float, nullable=False)
    sentiment_bearish = Column(Float, nullable=False)
    sentiment_neutral = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    simulation = relationship("Simulation", back_populates="ticks")
    actions = relationship("AgentAction", back_populates="tick")

    __table_args__ = (
        Index("idx_tick_simulation", "simulation_id", "tick_number"),
    )


class AgentAction(Base):
    """Agent trading actions."""
    __tablename__ = "agent_actions"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    simulation_id = Column(String, ForeignKey("simulations.id"), nullable=False, index=True)
    tick_id = Column(String, ForeignKey("simulation_ticks.id"), nullable=True)
    agent_id = Column(String, nullable=False, index=True)
    agent_type = Column(String, nullable=False)  # "hedge_fund", "retail", "news", "regulator", "market_maker"
    action = Column(String, nullable=False)  # "buy", "sell", "hold", "broadcast", "regulate"
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    reasoning = Column(Text, nullable=True)
    sentiment_input = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    simulation = relationship("Simulation", back_populates="actions")
    tick = relationship("SimulationTick", back_populates="actions")

    __table_args__ = (
        Index("idx_action_simulation", "simulation_id", "agent_type"),
    )


class MarketData(Base):
    """Historical market data cache."""
    __tablename__ = "market_data"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    ticker = Column(String, nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_market_data_ticker_date", "ticker", "date"),
    )


class NewsFeed(Base):
    """News articles and sentiment."""
    __tablename__ = "news_feed"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    ticker = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)  # "positive", "negative", "neutral"
    sentiment_score = Column(Float, nullable=False)
    published_at = Column(DateTime, nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    url = Column(String, nullable=True)

    __table_args__ = (
        Index("idx_news_ticker_sentiment", "ticker", "sentiment"),
    )


class TokenBlacklist(Base):
    """Blacklisted JWT tokens (for logout)."""
    __tablename__ = "token_blacklist"

    id = Column(String, primary_key=True, default=lambda: str(__import__('uuid').uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    token_jti = Column(String, unique=True, nullable=False, index=True)
    blacklisted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    user = relationship("User", back_populates="token_blacklist")

    __table_args__ = (
        Index("idx_blacklist_user", "user_id"),
    )
