# E.C.H.O Assistant

A voice-activated AI assistant with modular architecture.

## Features

- Voice interaction with hotkey activation
- Speech-to-text and text-to-speech
- LLM integration for intelligent responses
- Extensible skills system
- System control capabilities

## Setup

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Copy `.env.example` to `.env` and configure your API keys

3. Run the assistant:
   ```bash
   python -m echo_assistant.main
   ```

## Project Structure

- `core/` - Core engine components (audio, STT, TTS, LLM)
- `runtime/` - Orchestration and event loop
- `skills/` - Action handlers and capabilities
- `ui/` - User interface components
