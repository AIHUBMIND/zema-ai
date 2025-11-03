# API Module Documentation

## Purpose
The `src/api/` folder contains the FastAPI web server, REST API routes, WebSocket endpoints, and dashboard for managing and interacting with Zema AI.

## Files in This Folder

### `server.py`
FastAPI server setup. Initializes FastAPI app, registers routes, sets up WebSocket endpoints, serves dashboard.

### `routes/`
API route handlers:
- `config.py` - Configuration endpoints (GET/POST `/api/config`, GET `/api/config/user-facing`, POST `/api/config/bulk`)
- `system.py` - System status endpoint (GET `/api/status`)
- `logs.py` - Logs viewer endpoints (GET `/api/logs`, GET `/api/logs/stream`, GET `/api/logs/stats`, DELETE `/api/logs/clear`)
- `users.py` - User management endpoints (GET/POST `/api/users`)
- `conversations.py` - Conversation history endpoint (GET `/api/conversations`)
- `voice.py` - Voice interaction endpoints (POST `/api/voice/start`, POST `/api/voice/stop`, WS `/ws/voice`)
- `vision.py` - Vision endpoints (POST `/api/vision/screenshot`, POST `/api/vision/camera`)

### `static/`
Static files for web dashboard:
- `index.html` - Dashboard HTML
- `css/style.css` - Dashboard styles
- `js/app.js` - Dashboard JavaScript

## API Endpoints
- `GET /api/config` - Get current configuration (all settings or user-facing only)
- `GET /api/config/user-facing` - Get only user-facing configuration settings
- `POST /api/config` - Update a single configuration setting
- `POST /api/config/bulk` - Update multiple configuration settings at once
- `GET /api/status` - Get system status
- `GET /api/logs` - Get log entries (supports filtering by level, search, limit)
- `GET /api/logs/stream` - Stream logs in real-time via SSE
- `GET /api/logs/stats` - Get log file statistics
- `DELETE /api/logs/clear` - Clear log file
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/conversations` - Get conversation history
- `POST /api/voice/start` - Start voice interaction
- `POST /api/voice/stop` - Stop voice interaction
- `WS /ws` - WebSocket for real-time updates
- `WS /ws/voice` - WebSocket for voice streaming

## Dashboard
Accessible at `http://localhost:8000` (or configured port). Provides web interface for:
- Viewing system status
- **Managing configuration via Settings page** (NEW in v0.1.3)
- Viewing application logs
- Voice Mode interaction
- Viewing conversation history
- Monitoring system health

## Key Features
- RESTful API
- WebSocket support
- Dashboard UI with Settings page (v0.1.3)
- Configuration management via web UI
- Log viewing and filtering (v0.1.1)
- Real-time log streaming (v0.1.1)
- Voice Mode UI (v0.1.2)
- User management
- Conversation history

