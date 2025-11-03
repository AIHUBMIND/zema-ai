# Docker Deployment Guide for Zema Dashboard

## Quick Start

### Development Mode (Hot Reload - Recommended for UI Testing)

**Best for iterative UI development** - Changes reflect automatically without rebuild!

```bash
# Start development container with hot reload
docker-compose -f docker/docker-compose.dev.yml up

# Make changes to src/api/static/* files
# Save → automatically reloads
# Refresh browser → see changes immediately!
```

**Access:** `http://localhost:8000`

### Production Mode

```bash
# Build and start production container
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop
docker-compose -f docker/docker-compose.yml down
```

---

## Workflow for UI Testing

### Step 1: Start Development Container
```bash
cd C:\AI_Cloude_Files\ZEMA-AI
docker-compose -f docker/docker-compose.dev.yml up
```

### Step 2: Iterative Testing
1. Edit files in `src/api/static/`:
   - `src/api/static/index.html`
   - `src/api/static/css/style.css`
   - `src/api/static/js/app.js`

2. **Save the file** → Docker auto-reloads (if using dev mode)

3. **Refresh browser** (`http://localhost:8000`) → See changes!

4. **Repeat** until satisfied

### Step 3: View Logs
```bash
# In another terminal
docker-compose -f docker/docker-compose.dev.yml logs -f
```

### Step 4: Stop When Done
```bash
docker-compose -f docker/docker-compose.dev.yml down
```

---

## File Structure

```
docker/
├── Dockerfile              # Production Dockerfile
├── Dockerfile.dev          # Development Dockerfile (hot reload)
├── docker-compose.yml      # Production compose
├── docker-compose.dev.yml  # Development compose (hot reload)
├── .dockerignore           # Files to exclude from build
└── README.md               # This file
```

---

## Commands Reference

### Development (Hot Reload)
```bash
# Start with hot reload
docker-compose -f docker/docker-compose.dev.yml up

# Start in background
docker-compose -f docker/docker-compose.dev.yml up -d

# View logs
docker-compose -f docker/docker-compose.dev.yml logs -f

# Stop
docker-compose -f docker/docker-compose.dev.yml down

# Rebuild (if needed)
docker-compose -f docker/docker-compose.dev.yml up -d --build
```

### Production
```bash
# Build and start
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop
docker-compose -f docker/docker-compose.yml down

# Rebuild
docker-compose -f docker/docker-compose.yml up -d --build
```

### General Docker Commands
```bash
# List running containers
docker ps

# Execute commands in container
docker exec -it zema-dashboard-dev bash

# Check container logs
docker logs -f zema-dashboard-dev

# Remove everything
docker-compose -f docker/docker-compose.dev.yml down -v
docker rmi zema-ai-zema-dashboard-dev
```

---

## Troubleshooting

### Port Already in Use
```bash
# Edit docker-compose.dev.yml and change port:
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

### Changes Not Reflecting
- Make sure you're using `docker-compose.dev.yml` (not `docker-compose.yml`)
- Check that volumes are mounted correctly
- Verify uvicorn is running with `--reload` flag

### Permission Errors (Linux/Mac)
```bash
sudo chown -R $USER:$USER ../data/
```

### Container Won't Start
```bash
# Check logs
docker-compose -f docker/docker-compose.dev.yml logs

# Rebuild from scratch
docker-compose -f docker/docker-compose.dev.yml down -v
docker-compose -f docker/docker-compose.dev.yml up --build
```

---

## Environment Variables

You can customize via `.env` file or environment variables:

```bash
ENVIRONMENT=development
LOG_LEVEL=DEBUG
DASHBOARD_HOST=0.0.0.0
DASHBOARD_PORT=8000
```

---

## Benefits

- ✅ **Hot Reload**: Changes reflect automatically without rebuild
- ✅ **Ubuntu Environment**: Matches your production hardware (Ubuntu 22.04)
- ✅ **Isolated**: No conflicts with host system
- ✅ **Fast Iteration**: Save → Refresh → See changes
- ✅ **Consistent**: Same environment every time

---

## Next Steps

1. Start development container: `docker-compose -f docker/docker-compose.dev.yml up`
2. Make UI changes in `src/api/static/`
3. Save → Auto-reload → Refresh browser
4. Iterate until satisfied!

