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
        try:
            print("\n[Wake] WAKE WORD TRIGGERED - Recording user input...")
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
        except Exception as e:
            print(f"[Wake] Error in on_wake callback: {e}")
            import traceback
            traceback.print_exc()

    ww_cfg = WakeWordConfig(
        model_names=wake_models,
        threshold=0.1,
        smoothing_window=5,
    )
    
    print(f"[Wake] Initializing detector with models: {wake_models}")
    detector = WakeWordDetector(ww_cfg)
    print(f"[Wake] Detector ready. Target models: {detector.target_model_names}")
    
    try:
        detector.run(on_detect=on_wake)
    except KeyboardInterrupt:
        print("\n[Wake] Exiting wake-word mode.")
    except SystemExit:
        raise
    except Exception as e:
        print(f"[Wake] Error in detector: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    if should_exit:
        raise SystemExit
