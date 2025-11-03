"""
Logs API Routes
Provides endpoints for viewing application logs
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any, Optional, AsyncGenerator
from pathlib import Path
import json
import asyncio
from datetime import datetime

router = APIRouter()

LOG_FILE = Path("data/logs/zema.log")


def parse_log_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a JSON log line into a dictionary"""
    try:
        if line.strip():
            return json.loads(line.strip())
    except json.JSONDecodeError:
        # If line is not valid JSON, return None
        return None
    return None


@router.get("/api/logs")
async def get_logs(
    limit: int = Query(default=100, ge=1, le=1000, description="Number of log entries to return"),
    level: Optional[str] = Query(default=None, description="Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"),
    search: Optional[str] = Query(default=None, description="Search term in log messages"),
    tail: bool = Query(default=True, description="Get logs from end of file (tail)")
) -> Dict[str, Any]:
    """
    Get log entries from log file
    
    Args:
        limit: Maximum number of log entries to return (1-1000)
        level: Filter by log level (optional)
        search: Search term in log messages (optional)
        tail: If True, get logs from end of file (default: True)
    
    Returns:
        Dictionary with log entries and metadata
    """
    if not LOG_FILE.exists():
        return {
            "logs": [],
            "total": 0,
            "message": "Log file not found"
        }
    
    try:
        # Read log file
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse log lines
        log_entries = []
        for line in lines:
            log_entry = parse_log_line(line)
            if log_entry:
                log_entries.append(log_entry)
        
        # Apply filters
        filtered_logs = log_entries
        
        # Filter by level if specified
        if level:
            level_upper = level.upper()
            filtered_logs = [log for log in filtered_logs if log.get('level') == level_upper]
        
        # Filter by search term if specified
        if search:
            search_lower = search.lower()
            filtered_logs = [
                log for log in filtered_logs
                if search_lower in log.get('message', '').lower() or
                   search_lower in log.get('logger', '').lower() or
                   search_lower in log.get('module', '').lower()
            ]
        
        # Get tail or head
        if tail:
            filtered_logs = filtered_logs[-limit:]
        else:
            filtered_logs = filtered_logs[:limit]
        
        return {
            "logs": filtered_logs,
            "total": len(filtered_logs),
            "file_size": LOG_FILE.stat().st_size,
            "file_path": str(LOG_FILE),
            "filters": {
                "level": level,
                "search": search,
                "limit": limit
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")


@router.get("/api/logs/stream")
async def stream_logs() -> StreamingResponse:
    """
    Stream logs in real-time via Server-Sent Events (SSE)
    
    Returns:
        StreamingResponse with log entries as they're written
    """
    async def log_generator() -> AsyncGenerator[str, None]:
        """Generate log entries as they're written"""
        # Read existing logs first
        if LOG_FILE.exists():
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-50:]:  # Last 50 lines
                    log_entry = parse_log_line(line)
                    if log_entry:
                        yield f"data: {json.dumps(log_entry)}\n\n"
        
        # Monitor file for new entries
        last_position = LOG_FILE.stat().st_size if LOG_FILE.exists() else 0
        
        while True:
            try:
                if LOG_FILE.exists():
                    with open(LOG_FILE, 'r', encoding='utf-8') as f:
                        f.seek(last_position)
                        new_lines = f.readlines()
                        
                        for line in new_lines:
                            log_entry = parse_log_line(line)
                            if log_entry:
                                yield f"data: {json.dumps(log_entry)}\n\n"
                        
                        last_position = f.tell()
                
                await asyncio.sleep(0.5)  # Check every 500ms
                
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                await asyncio.sleep(1)
    
    return StreamingResponse(
        log_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/api/logs/stats")
async def get_log_stats() -> Dict[str, Any]:
    """Get statistics about log file"""
    if not LOG_FILE.exists():
        return {
            "exists": False,
            "message": "Log file not found"
        }
    
    try:
        # Read log file and count by level
        level_counts = {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 0,
            "ERROR": 0,
            "CRITICAL": 0
        }
        
        total_lines = 0
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                total_lines += 1
                log_entry = parse_log_line(line)
                if log_entry and 'level' in log_entry:
                    level = log_entry['level']
                    if level in level_counts:
                        level_counts[level] += 1
        
        file_stat = LOG_FILE.stat()
        
        return {
            "exists": True,
            "file_path": str(LOG_FILE),
            "file_size": file_stat.st_size,
            "file_size_mb": round(file_stat.st_size / (1024 * 1024), 2),
            "total_lines": total_lines,
            "level_counts": level_counts,
            "last_modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting log stats: {str(e)}")


@router.delete("/api/logs/clear")
async def clear_logs() -> Dict[str, Any]:
    """Clear log file (admin only - should have authentication in production)"""
    try:
        if LOG_FILE.exists():
            LOG_FILE.unlink()
            # Create empty log file
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            LOG_FILE.touch()
        
        return {
            "success": True,
            "message": "Log file cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing logs: {str(e)}")

