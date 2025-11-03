"""
Model Management API Routes
Provides endpoints for managing Ollama models (list, download, check status)
"""

import subprocess
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
import json
import sys
from pathlib import Path

router = APIRouter()

# Available models with metadata
AVAILABLE_MODELS = {
    "llama2:13b": {
        "name": "Llama 2 13B",
        "size_gb": 7.3,
        "languages": ["English"],
        "strength": "Good for English conversations",
        "recommended": False
    },
    "llama3.2:3b": {
        "name": "Llama 3.2 3B",
        "size_gb": 2.0,
        "languages": ["English"],
        "strength": "Fast, lightweight",
        "recommended": False
    },
    "llama3.2:13b": {
        "name": "Llama 3.2 13B",
        "size_gb": 7.3,
        "languages": ["English"],
        "strength": "Better quality than Llama 2",
        "recommended": False
    },
    "llama3.1:8b": {
        "name": "Llama 3.1 8B",
        "size_gb": 4.7,
        "languages": ["English", "Multilingual (moderate)"],
        "strength": "Improved multilingual support",
        "recommended": False
    },
    "qwen2.5:3b": {
        "name": "Qwen 2.5 3B",
        "size_gb": 2.0,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "Fast multilingual & translation",
        "recommended": True
    },
    "qwen2.5:7b": {
        "name": "Qwen 2.5 7B",
        "size_gb": 4.7,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "Best balance - multilingual & translation",
        "recommended": True
    },
    "qwen2.5:14b": {
        "name": "Qwen 2.5 14B",
        "size_gb": 8.5,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "High quality multilingual",
        "recommended": False
    },
    "qwen2.5:72b": {
        "name": "Qwen 2.5 72B",
        "size_gb": 40.0,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "Best quality multilingual",
        "recommended": False
    },
    "aya:8b": {
        "name": "Aya 8B",
        "size_gb": 4.7,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "Translation specialist - best for translation tasks",
        "recommended": True
    },
    "aya:35b": {
        "name": "Aya 35B",
        "size_gb": 20.0,
        "languages": ["100+ languages including Amharic, Tigrinya, Oromo, Somali"],
        "strength": "Best translation quality",
        "recommended": False
    },
    "mistral:7b": {
        "name": "Mistral 7B",
        "size_gb": 4.1,
        "languages": ["English", "Multilingual (good)"],
        "strength": "Fast multilingual",
        "recommended": False
    },
    "mixtral:8x7b": {
        "name": "Mixtral 8x7B",
        "size_gb": 26.0,
        "languages": ["English", "Multilingual (good)"],
        "strength": "High quality multilingual",
        "recommended": False
    }
}

async def run_ollama_command(command: List[str]) -> Dict[str, Any]:
    """
    Run Ollama command asynchronously
    
    Args:
        command: List of command arguments
        
    Returns:
        Dictionary with success status and output
    """
    try:
        process = await asyncio.create_subprocess_exec(
            "ollama",
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "success": process.returncode == 0,
            "exit_code": process.returncode,
            "stdout": stdout.decode('utf-8', errors='replace'),
            "stderr": stderr.decode('utf-8', errors='replace')
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "Ollama not found. Please install Ollama first.",
            "output": "Install from: https://ollama.ai"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "output": f"Error running command: {str(e)}"
        }

@router.get("/api/models/list")
async def list_installed_models() -> Dict[str, Any]:
    """
    List all installed Ollama models
    """
    result = await run_ollama_command(["list"])
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result.get("error", "Failed to list models"))
    
    # Parse Ollama list output
    lines = result["stdout"].strip().split('\n')
    models = []
    
    # Skip header line if present
    for line in lines[1:] if len(lines) > 1 else lines:
        if line.strip():
            parts = line.split()
            if parts:
                model_name = parts[0]
                # Get metadata if available
                metadata = AVAILABLE_MODELS.get(model_name, {
                    "name": model_name,
                    "size_gb": None,
                    "languages": ["Unknown"],
                    "strength": "No metadata available",
                    "recommended": False
                })
                metadata["installed"] = True
                models.append({
                    "name": model_name,
                    **metadata
                })
    
    return {
        "status": "success",
        "models": models,
        "count": len(models)
    }

@router.get("/api/models/available")
async def list_available_models() -> Dict[str, Any]:
    """
    List all available models with metadata
    """
    # Check which are installed
    installed_result = await run_ollama_command(["list"])
    installed_models = set()
    
    if installed_result["success"]:
        lines = installed_result["stdout"].strip().split('\n')
        for line in lines[1:] if len(lines) > 1 else lines:
            if line.strip():
                parts = line.split()
                if parts:
                    installed_models.add(parts[0])
    
    # Build response with install status
    models = []
    for model_id, metadata in AVAILABLE_MODELS.items():
        models.append({
            "id": model_id,
            "installed": model_id in installed_models,
            **metadata
        })
    
    return {
        "status": "success",
        "models": models,
        "count": len(models)
    }

@router.post("/api/models/download/{model_name}")
async def download_model(model_name: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Download an Ollama model
    
    Args:
        model_name: Model name (e.g., "qwen2.5:7b")
    """
    # Validate model name
    if model_name not in AVAILABLE_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model: {model_name}. Available models: {list(AVAILABLE_MODELS.keys())}"
        )
    
    # Check if already installed
    installed_result = await run_ollama_command(["list"])
    if installed_result["success"]:
        if model_name in installed_result["stdout"]:
            return {
                "status": "already_installed",
                "model": model_name,
                "message": f"Model {model_name} is already installed"
            }
    
    # Start download in background
    async def download_task():
        result = await run_ollama_command(["pull", model_name])
        return result
    
    # Run download
    result = await download_task()
    
    if result["success"]:
        return {
            "status": "success",
            "model": model_name,
            "message": f"Model {model_name} downloaded successfully",
            "output": result["stdout"]
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to download model: {result.get('error', result.get('stderr', 'Unknown error'))}"
        )

@router.delete("/api/models/{model_name}")
async def delete_model(model_name: str) -> Dict[str, Any]:
    """
    Delete an Ollama model
    
    Args:
        model_name: Model name to delete
    """
    result = await run_ollama_command(["rm", model_name])
    
    if result["success"]:
        return {
            "status": "success",
            "model": model_name,
            "message": f"Model {model_name} deleted successfully"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete model: {result.get('error', result.get('stderr', 'Unknown error'))}"
        )

@router.get("/api/models/{model_name}/status")
async def get_model_status(model_name: str) -> Dict[str, Any]:
    """
    Get status of a specific model
    
    Args:
        model_name: Model name to check
    """
    installed_result = await run_ollama_command(["list"])
    
    if not installed_result["success"]:
        raise HTTPException(status_code=500, detail="Failed to check model status")
    
    is_installed = model_name in installed_result["stdout"]
    metadata = AVAILABLE_MODELS.get(model_name, {})
    
    return {
        "model": model_name,
        "installed": is_installed,
        "metadata": metadata
    }

@router.post("/api/models/download-recommended")
async def download_recommended_models() -> Dict[str, Any]:
    """
    Download recommended models for multilingual support
    Downloads: qwen2.5:7b and aya:8b
    """
    recommended = ["qwen2.5:7b", "aya:8b"]
    results = {}
    
    for model_name in recommended:
        try:
            result = await download_model(model_name, BackgroundTasks())
            results[model_name] = result
        except HTTPException as e:
            results[model_name] = {
                "status": "error",
                "error": e.detail
            }
    
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    
    return {
        "status": "partial" if success_count < len(recommended) else "success",
        "results": results,
        "downloaded": success_count,
        "total": len(recommended)
    }

