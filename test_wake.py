#!/usr/bin/env python
"""Test wake-word detection directly"""
import sys
sys.path.insert(0, 'src')

from echo_assistant.config import load_config
from echo_assistant.runtime.wake_listener import run_wake_listener

if __name__ == "__main__":
    config = load_config()
    print(f"[Test] Config: backend={config.llm_backend}, hotkey={config.hotkey}")
    print("[Test] Starting wake-word listener...")
    print("[Test] Try saying 'hey Jarvis' near your microphone...")
    run_wake_listener(config)
