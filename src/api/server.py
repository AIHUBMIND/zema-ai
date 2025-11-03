"""
Web Dashboard Server
FastAPI server for Zema dashboard
"""

import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from pathlib import Path
from src.config.settings import Settings
from src.api.routes import logs, system, config, users, conversations, voice, vision, hardware, models

logger = logging.getLogger(__name__)

app = FastAPI(title="Zema Dashboard", version="1.0.0")

# Register API routes
app.include_router(logs.router)
app.include_router(system.router)
app.include_router(config.router)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(voice.router)
app.include_router(vision.router)
app.include_router(hardware.router)
app.include_router(models.router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path("src/api/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# WebSocket connections
websocket_connections = []

@app.on_event("startup")
async def startup() -> None:
    """Startup event"""
    logger.info("Dashboard server starting...")

@app.on_event("shutdown")
async def shutdown() -> None:
    """Shutdown event"""
    logger.info("Dashboard server shutting down...")

@app.get("/", response_class=HTMLResponse)
async def dashboard() -> HTMLResponse:
    """Serve main dashboard page"""
    html_path = static_dir / "index.html"
    if html_path.exists():
        return html_path.read_text()
    return "<h1>Dashboard not found</h1>"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket for real-time updates"""
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        while True:
            # Get real status using shared function
            try:
                status = system.get_system_status()
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                # Fallback status
                status = {
                    "listening": False,
                    "cpu_percent": 0,
                    "memory_percent": 0,
                    "uptime": 0
                }
            
            # Send status updates
            await websocket.send_json({
                "type": "status",
                "data": status
            })
            await asyncio.sleep(2)  # Update every 2 seconds
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in websocket_connections:
            websocket_connections.remove(websocket)

async def start_dashboard(settings: Settings) -> None:
    """Start dashboard server"""
    config = uvicorn.Config(
        app,
        host=settings.dashboard_host,
        port=settings.dashboard_port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

