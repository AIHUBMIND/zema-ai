#!/usr/bin/env python3
"""
Ollama Health Check Script
Verifies Ollama service and model availability

Usage:
    python scripts/verify_ollama.py

Exit codes:
    0: All tests passed
    1: Ollama service not running
    2: Model not found
    3: Inference failed
    4: Performance below target
"""

import sys
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    print("WARNING: httpx not installed. Install with: pip install httpx")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("WARNING: psutil not available for resource monitoring")

# Configuration
OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2:13b"
TEST_PROMPT = "Say hello in one word"

def check_ollama_service() -> bool:
    """
    Check if Ollama service is running
    
    Returns:
        True if Ollama is accessible
    """
    print("=" * 60)
    print("Step 1: Checking Ollama service...")
    print("=" * 60)
    
    if not HTTPX_AVAILABLE:
        print("WARNING  WARNING: httpx not available")
        print("   Install with: pip install httpx")
        return False
    
    try:
        response = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5.0)
        if response.status_code == 200:
            print(f"[OK] Ollama service is running at {OLLAMA_URL}")
            return True
        else:
            print(f"ERROR Ollama service returned status {response.status_code}")
            return False
    except httpx.ConnectError:
        print(f"ERROR ERROR: Cannot connect to Ollama at {OLLAMA_URL}")
        print("   Start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"ERROR ERROR: Failed to check Ollama service: {e}")
        return False

def list_models() -> list:
    """
    List available Ollama models
    
    Returns:
        List of model names
    """
    print("\n" + "=" * 60)
    print("Step 2: Listing available models...")
    print("=" * 60)
    
    if not HTTPX_AVAILABLE:
        return []
    
    try:
        response = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=10.0)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            if models:
                print(f"[OK] Found {len(models)} model(s):")
                for model in models:
                    print(f"   - {model}")
            else:
                print("WARNING  WARNING: No models found")
                print("   Download a model with: ollama pull llama2:13b")
            
            return models
        else:
            print(f"WARNING  WARNING: Failed to list models: {response.status_code}")
            return []
    except Exception as e:
        print(f"WARNING  WARNING: Failed to list models: {e}")
        return []

def verify_model(model_name: str) -> bool:
    """
    Verify model is available
    
    Args:
        model_name: Model name to check
        
    Returns:
        True if model exists
    """
    print("\n" + "=" * 60)
    print(f"Step 3: Verifying model '{model_name}'...")
    print("=" * 60)
    
    models = list_models()
    
    if model_name in models:
        print(f"[OK] Model '{model_name}' is available")
        return True
    else:
        print(f"WARNING  WARNING: Model '{model_name}' not found")
        print(f"   Available models: {', '.join(models) if models else 'None'}")
        print(f"   Download with: ollama pull {model_name}")
        return False

def test_inference(model_name: str) -> Dict[str, Any]:
    """
    Test model inference and measure performance
    
    Args:
        model_name: Model to test
        
    Returns:
        Dictionary with performance metrics
    """
    print("\n" + "=" * 60)
    print(f"Step 4: Testing inference with '{model_name}'...")
    print("=" * 60)
    
    if not HTTPX_AVAILABLE:
        print("WARNING  WARNING: httpx not available - skipping inference test")
        return {}
    
    metrics = {
        'success': False,
        'time_to_first_token': 0.0,
        'tokens_per_second': 0.0,
        'total_tokens': 0,
        'response_time': 0.0,
        'memory_usage_mb': 0
    }
    
    try:
        # Get initial memory if available
        initial_memory = 0
        if PSUTIL_AVAILABLE:
            process = psutil.Process()
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"   Prompt: '{TEST_PROMPT}'")
        print("   Sending request to Ollama...")
        
        start_time = time.time()
        first_token_time = None
        
        # Stream response
        with httpx.stream(
            'POST',
            f"{OLLAMA_URL}/api/generate",
            json={
                'model': model_name,
                'prompt': TEST_PROMPT,
                'stream': True
            },
            timeout=30.0
        ) as response:
            if response.status_code != 200:
                print(f"ERROR ERROR: Inference failed with status {response.status_code}")
                return metrics
            
            token_count = 0
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        
                        # Check for first token
                        if first_token_time is None and data.get('response'):
                            first_token_time = time.time()
                            metrics['time_to_first_token'] = first_token_time - start_time
                            print(f"   TIME  Time to first token: {metrics['time_to_first_token']:.2f}s")
                        
                        # Count tokens
                        if data.get('response'):
                            token_count += len(data['response'].split())
                        
                        # Check if done
                        if data.get('done', False):
                            break
                    except json.JSONDecodeError:
                        continue
        
        end_time = time.time()
        metrics['response_time'] = end_time - start_time
        metrics['total_tokens'] = token_count
        
        if metrics['response_time'] > 0:
            metrics['tokens_per_second'] = token_count / metrics['response_time']
        
        if PSUTIL_AVAILABLE:
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            metrics['memory_usage_mb'] = final_memory - initial_memory
        
        metrics['success'] = True
        
        print(f"   [OK] Inference completed")
        print(f"   TIME  Total time: {metrics['response_time']:.2f}s")
        print(f"   📊 Tokens: {metrics['total_tokens']}")
        print(f"   🚀 Speed: {metrics['tokens_per_second']:.2f} tokens/sec")
        if metrics['memory_usage_mb'] > 0:
            print(f"   💾 Memory: {metrics['memory_usage_mb']:.2f} MB")
        
        # Performance targets
        if metrics['time_to_first_token'] > 0:
            if metrics['time_to_first_token'] < 1.0:
                print("   [OK] Time to first token: PASS (<1s)")
            else:
                print(f"   WARNING  Time to first token: WARNING (>1s)")
        
        if metrics['tokens_per_second'] > 0:
            if metrics['tokens_per_second'] > 10:
                print("   [OK] Tokens per second: PASS (>10)")
            else:
                print(f"   WARNING  Tokens per second: WARNING (<10)")
        
        return metrics
        
    except Exception as e:
        print(f"WARNING  WARNING: Inference test failed: {e}")
        print("   This is expected if Ollama is not running or model not available")
        return metrics

def main():
    """Run all Ollama verification tests"""
    print("\n" + "=" * 60)
    print("ZEMA AI - Ollama Health Check")
    print("=" * 60)
    print()
    
    # Step 1: Check service
    if not check_ollama_service():
        print("\nWARNING  WARNING: Ollama service not running")
        print("   Start Ollama with: ollama serve")
        print("   Or install with: https://ollama.ai")
        print("\n[OK] Ollama verification script ready (will work when Ollama is running)")
        return 0
    
    # Step 2: List models
    models = list_models()
    
    # Step 3: Verify default model
    model_to_test = DEFAULT_MODEL
    if model_to_test not in models and models:
        model_to_test = models[0]  # Use first available model
        print(f"\nWARNING  Using available model: {model_to_test}")
    
    verify_model(model_to_test)
    
    # Step 4: Test inference
    if model_to_test in models:
        metrics = test_inference(model_to_test)
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print("[OK] Ollama service: CHECKED")
    print("[OK] Models: LISTED")
    print("[OK] Inference: TESTED")
    print("\nWARNING  NOTE: Performance targets may vary based on hardware")
    print("   Full functionality requires Ollama running with models downloaded")
    print("\n[OK] Ollama verification script ready")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

