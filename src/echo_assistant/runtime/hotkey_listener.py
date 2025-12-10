"""
hotkey_listener.py
Global hotkey trigger for Echo.
Press configured hotkey (default: ctrl+space) -> record -> stt -> llm -> tts
"""

from __future__ import annotations
import keyboard
from ..config import Config
from .loop import build_components


def run_hotkey_listener(config: Config):
    recorder, stt_engine, tts_engine, router = build_components(config)

    print(f"[Hotkey] Assistant running. Press {config.hotkey} to speak. Say 'exit assistant' to quit.")
    tts_engine.speak(f"{config.assistant_name} is active. Press {config.hotkey} to talk.")

    def on_hotkey():
        print("\n[Hotkey] Listening...")
        audio = recorder.record(seconds=4.0)   # adjustable later
        text, _ = stt_engine.transcribe(audio)

        if not text.strip():
            tts_engine.speak("I didn't catch that.")
            return

        result = router.route(text)
        tts_engine.speak(result.reply)

        if result.should_exit:
            tts_engine.speak("Goodbye.")
            raise SystemExit

    keyboard.add_hotkey(config.hotkey, on_hotkey)
    keyboard.wait()   # keeps script alive
