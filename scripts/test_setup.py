#!/usr/bin/env python3
"""Test script to verify project setup."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from config.settings import Settings, settings
    
    print("✓ Successfully imported Settings")
    print(f"✓ App Name: {settings.app_name}")
    print(f"✓ App Version: {settings.app_version}")
    print(f"✓ API Host: {settings.api_host}")
    print(f"✓ API Port: {settings.api_port}")
    print(f"✓ Ollama Model: {settings.ollama_model}")
    print(f"✓ Database URL: {settings.database_url}")
    print("\n✅ All imports successful! Project setup is correct.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

