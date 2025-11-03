# API Module Documentation

## Purpose
The `src/api/` folder contains the FastAPI web server, REST API routes, WebSocket endpoints, and dashboard for managing and interacting with Zema AI.

## Files in This Folder

### `server.py`
FastAPI server setup. Initializes FastAPI app, registers routes, sets up WebSocket endpoints, serves dashboard.

### `routes/`
API route handlers:
- `config.py` - Configuration endpoints (GET/POST `/api/config`)
- `system.py` - System status endpoint (GET `/api/status`)
- `logs.py` - Logs viewer endpoints (GET `/api/logs`, GET `/api/logs/stream`, GET `/api/logs/stats`, DELETE `/api/logs/clear`)
- `users.py` - User management endpoints (GET/POST `/api/users`)
- `conversations.py` - Conversation history endpoint (GET `/api/conversations`)

### `static/`
Static files for web dashboard:
- `index.html` - Dashboard HTML
- `css/style.css` - Dashboard styles
- `js/app.js` - Dashboard JavaScript

## API Endpoints
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `GET /api/status` - Get system status
- `GET /api/logs` - Get log entries (supports filtering by level, search, limit)
- `GET /api/logs/stream` - Stream logs in real-time via SSE
- `GET /api/logs/stats` - Get log file statistics
- `DELETE /api/logs/clear` - Clear log file
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/conversations` - Get conversation history
- `WS /ws` - WebSocket for real-time updates

## Dashboard
Accessible at `http://localhost:8000` (or configured port). Provides web interface for:
- Viewing system status
- Managing configuration
- **Viewing application logs** (NEW in v0.1.1)
- Viewing conversation history
- Monitoring system health

## Key Features
- RESTful API
- WebSocket support
- Dashboard UI with Logs viewer
- Configuration management
- Log viewing and filtering (v0.1.1)
- Real-time log streaming (v0.1.1)
- User management
- Conversation history

