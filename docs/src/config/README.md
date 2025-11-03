# Config Module Documentation

## Purpose
The `src/config/` folder handles all configuration management. Uses Pydantic for type-safe configuration with validation.

## Files in This Folder

### `settings.py`
Main settings class using Pydantic. Loads configuration from environment variables and `.env` file. Provides type-safe access to all configuration values.

### `config_manager.py`
Configuration manager for runtime configuration updates. Handles saving/loading configuration changes, validates updates, and notifies components of changes.

## Configuration Sources
1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

## Key Features
- Type validation
- Environment variable support
- Default values
- Runtime updates (via config_manager)

