# Core Module Documentation

## Purpose
The `src/core/` folder contains the core system components that orchestrate and coordinate all other modules. These are the foundation of the Zema AI system.

## Files in This Folder

### `orchestrator.py`
Main orchestrator that coordinates all system components. Starts and stops the entire system, manages component lifecycle.

### `state.py`
State management for application state, conversation history, and system state.

### `event_bus.py`
Pub/sub event system for component communication. Allows components to publish events and subscribe to events without tight coupling.

## How They Work Together
1. **Orchestrator** initializes all components
2. **Event Bus** enables loose coupling between components
3. **State** maintains application state across components

## Key Concepts
- **Orchestrator Pattern**: Central coordinator for all components
- **Event-Driven Architecture**: Components communicate via events
- **State Management**: Centralized state for consistency

