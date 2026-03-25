"""
FastAPI Main Application
Entry point for StockMind Backend API
"""

from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

from simulation.engine import SimulationEngine
from config import API_HOST, API_PORT, DEBUG
from database import init_db, close_db, get_session
from api.routes import simulation, agents, news, auth
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# Global simulation engine
engine: SimulationEngine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager."""
    global engine
    
    # Startup
    print("[Server] Initializing database...")
    await init_db()
    
    engine = SimulationEngine()
    await engine.initialize()
    
    # Inject WebSocket broadcast capability
    engine.broadcast_callback = manager.broadcast
    
    # Set engine reference in route modules
    simulation.set_engine(engine)
    agents.set_engine(engine)
    news.set_engine(engine)
    
    print("[Server] Simulation engine initialized")
    
    yield
    
    # Shutdown
    await engine.shutdown()
    await close_db()
    print("[Server] Simulation engine shutdown")


# Create FastAPI app
app = FastAPI(
    title="StockMind Backend",
    description="AI-powered market sentiment simulation engine",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(news.router, prefix="/api/news", tags=["News"])


# ============================================================================
# HEALTH ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "engine_ready": engine is not None,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "StockMind Backend",
        "description": "AI-powered market sentiment simulation",
        "docs": "/docs",
    }


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

class ConnectionManager:
    """WebSocket connection manager."""
    
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, simulation_id: str, websocket: WebSocket):
        """Connect to simulation updates."""
        await websocket.accept()
        if simulation_id not in self.active_connections:
            self.active_connections[simulation_id] = []
        self.active_connections[simulation_id].append(websocket)
    
    def disconnect(self, simulation_id: str, websocket: WebSocket):
        """Disconnect from simulation safely."""
        if simulation_id in self.active_connections:
            if websocket in self.active_connections[simulation_id]:
                self.active_connections[simulation_id].remove(websocket)
            # Cleanup empty simulation lists
            if not self.active_connections[simulation_id]:
                del self.active_connections[simulation_id]
    
    async def broadcast(self, simulation_id: str, message: dict):
        """Broadcast message to all clients associated with a simulation."""
        if simulation_id not in self.active_connections:
            return
            
        # Iterate over a copy of the list to allow removal during iteration
        for connection in list(self.active_connections[simulation_id]):
            try:
                await connection.send_json(message)
            except Exception as e:
                # Silently handle disconnected clients during broadcast
                if simulation_id in self.active_connections and connection in self.active_connections[simulation_id]:
                    self.active_connections[simulation_id].remove(connection)
                print(f"[WebSocket] Removed dead connection from {simulation_id}: {e}")


manager = ConnectionManager()


@app.websocket("/ws/{simulation_id}")
async def websocket_endpoint(websocket: WebSocket, simulation_id: str):
    """WebSocket endpoint for real-time simulation updates."""
    await manager.connect(simulation_id, websocket)
    
    try:
        while True:
            # Keep connection alive and listen for messages
            data = await websocket.receive_text()
            # Echo back for now, could implement client commands
            await websocket.send_json({"type": "ack", "data": data})
    
    except WebSocketDisconnect:
        manager.disconnect(simulation_id, websocket)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info" if not DEBUG else "debug",
    )
