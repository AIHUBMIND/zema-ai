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
- `GET /api/users` - List users
- `POST /api/users` - Create user
- `GET /api/conversations` - Get conversation history
- `WS /ws` - WebSocket for real-time updates

## Dashboard
Accessible at `http://localhost:8000` (or configured port). Provides web interface for:
- Viewing system status
- Managing configuration
- Viewing conversation history
- Monitoring system health

## Key Features
- RESTful API
- WebSocket support
- Dashboard UI
- Configuration management
- User management
- Conversation history

