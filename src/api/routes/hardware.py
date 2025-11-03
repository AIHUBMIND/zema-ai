"""
Hardware Verification API Routes
Provides on-demand hardware verification endpoints
"""

import subprocess
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from typing import Dict, Any, Optional
from pathlib import Path
import json
import sys

router = APIRouter()

async def run_script(script_path: str) -> Dict[str, Any]:
    """
    Run a verification script asynchronously
    
    Args:
        script_path: Path to the script
        
    Returns:
        Dictionary with success status and output
    """
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=Path(__file__).parent.parent.parent
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "success": process.returncode == 0,
            "exit_code": process.returncode,
            "stdout": stdout.decode('utf-8', errors='replace'),
            "stderr": stderr.decode('utf-8', errors='replace'),
            "output": stdout.decode('utf-8', errors='replace')
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": f"Error running script: {str(e)}"
        }

@router.post("/api/hardware/verify/camera")
async def verify_camera() -> Dict[str, Any]:
    """
    Run camera verification test on-demand
    """
    script_path = Path(__file__).parent.parent.parent / "scripts" / "verify_hardware.py"
    
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Camera verification script not found")
    
    result = await run_script(str(script_path))
    
    return {
        "status": "success" if result["success"] else "failed",
        "test": "camera",
        "result": result
    }

@router.post("/api/hardware/verify/audio")
async def verify_audio() -> Dict[str, Any]:
    """
    Run audio verification test on-demand
    """
    script_path = Path(__file__).parent.parent.parent / "scripts" / "verify_audio.py"
    
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Audio verification script not found")
    
    result = await run_script(str(script_path))
    
    return {
        "status": "success" if result["success"] else "failed",
        "test": "audio",
        "result": result
    }

@router.post("/api/hardware/verify/ollama")
async def verify_ollama() -> Dict[str, Any]:
    """
    Run Ollama verification test on-demand
    """
    script_path = Path(__file__).parent.parent.parent / "scripts" / "verify_ollama.py"
    
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Ollama verification script not found")
    
    result = await run_script(str(script_path))
    
    return {
        "status": "success" if result["success"] else "failed",
        "test": "ollama",
        "result": result
    }

@router.post("/api/hardware/verify/all")
async def verify_all() -> Dict[str, Any]:
    """
    Run all hardware verification tests
    """
    results = {}
    
    # Run all tests concurrently
    camera_task = verify_camera()
    audio_task = verify_audio()
    ollama_task = verify_ollama()
    
    results["camera"] = await camera_task
    results["audio"] = await audio_task
    results["ollama"] = await ollama_task
    
    all_success = all(r["status"] == "success" for r in results.values())
    
    return {
        "status": "success" if all_success else "partial",
        "tests": results,
        "summary": {
            "passed": sum(1 for r in results.values() if r["status"] == "success"),
            "failed": sum(1 for r in results.values() if r["status"] == "failed"),
            "total": len(results)
        }
    }

@router.get("/api/hardware/status")
async def get_hardware_status() -> Dict[str, Any]:
    """
    Get current hardware status (last verification results)
    """
    # TODO: Implement caching of last verification results
    # For now, return placeholder
    return {
        "camera": {"status": "unknown", "last_checked": None},
        "audio": {"status": "unknown", "last_checked": None},
        "ollama": {"status": "unknown", "last_checked": None}
    }

