# Tools Module Documentation

## Purpose
The `src/tools/` folder contains personal assistant tools that extend the AI's capabilities. These tools can be called by the LLM to perform actions.

## Files in This Folder

### `base.py`
Base class for all tools. Defines the interface that all tools must implement.

### `tasks.py`
Task manager for reminders, calendar events, and recurring tasks. Creates, lists, and manages tasks.

### `notes.py`
Note-taking system for voice notes and memos. Saves, searches, exports, and categorizes notes.

### `knowledge.py`
Knowledge base for storing and retrieving information locally. Semantic search, context-aware retrieval.

### `web_search.py`
Web search integration (privacy mode dependent). Searches web, summarizes results, cites sources. Disabled in local privacy mode.

### `system_config.py`
System configuration tool for voice-based configuration commands. Allows changing settings via voice commands.

## Tool Execution Flow
```
LLM Response → Response Parser → Tool Call → Tool.execute() → Result → LLM → Response
```

## Key Features
- Extensible tool system
- Privacy-aware (web search disabled in local mode)
- Voice-based configuration
- Local knowledge storage
- Task and note management

## Tool Interface
All tools inherit from `Tool` base class and implement:
- `execute(action, parameters)` - Execute tool action
- `get_description()` - Get tool description for LLM

