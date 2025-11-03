# AI Module Documentation

## Purpose
The `src/ai/` folder handles all AI/LLM-related functionality: LLM client for Ollama, context management, response parsing, and system prompts.

## Files in This Folder

### `llm_client.py`
LLM client for Ollama. Handles communication with local Ollama server, sends prompts, receives responses, manages conversation history.

### `context_manager.py`
Manages conversation context and multi-turn conversations. Builds context dictionaries for LLM, handles conversation history, extracts key information.

### `response_parser.py`
Parses LLM responses and extracts structured data: tool calls, actions, intents. Uses regex patterns to identify and extract tool call syntax.

### `system_prompts.py`
Pre-defined system prompts for different contexts: main assistant prompt, vision prompt, tool prompt, Ethiopian context prompt.

## AI Flow
```
User Input → Context Manager → Build Context → LLM Client → Ollama → Response
                                                                    ↓
                                            Response Parser → Tool Calls / Actions
```

## Key Features
- Local LLM inference (100% offline)
- Multi-turn conversations
- Context-aware responses
- Tool call parsing
- Multi-language support (English, Amharic)
- Ethiopian cultural context

