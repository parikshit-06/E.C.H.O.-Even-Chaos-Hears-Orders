"""
wake_listener.py
Always-on wake-word listener that triggers the voice assistant pipeline.
"""

from __future__ import annotations

from ..config import Config
from .loop import build_components
# src/echo_assistant/runtime/wake_listener.py

from ..core.wakeword import WakeWordConfig, WakeWordDetector

def run_wake_listener(config: Config) -> None:
    recorder, stt_engine, tts_engine, router = build_components(config)

    # Use actual openWakeWord model names without version suffix
    # Available models: "hey jarvis", "alexa", "computer", "jarvis", etc.
    wake_models = ["hey jarvis"]

    tts_engine.speak(
        f"{config.assistant_name} wake-word mode enabled. "
        f"Say 'hey Jarvis' to talk to me."
    )

    should_exit = False

    def on_wake():
        nonlocal should_exit
        print("\n[Wake] ⭐ WAKE WORD TRIGGERED - Recording user input...")
        audio = recorder.record(seconds=4.0)
        text, _ = stt_engine.transcribe(audio)

        if not text.strip():
            tts_engine.speak("I didn't catch that. Please try again.")
            return

        print(f"[Wake] You said: {text!r}")
        result = router.route(text)
        print(f"[Wake] Assistant reply: {result.reply!r}")
        tts_engine.speak(result.reply)

        if result.should_exit:
            tts_engine.speak("Shutting down wake-word mode. Goodbye.")
            should_exit = True

    ww_cfg = WakeWordConfig(
        model_names=wake_models,
        threshold=0.1,  # With peak detection, this is effective
        smoothing_window=5,
    )
    detector = WakeWordDetector(ww_cfg)
    
    try:
        detector.run(on_detect=on_wake)
    except KeyboardInterrupt:
        print("\n[Wake] Exiting wake-word mode.")
    except SystemExit:
        raise
    
    if should_exit:
        raise SystemExit
