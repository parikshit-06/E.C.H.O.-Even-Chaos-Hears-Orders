"""
loop.py
Main voice interaction loop for Echo Assistant.

Orchestration only:
- record from mic
- STT -> text
- Router -> reply / exit
- TTS -> speak reply
"""

from __future__ import annotations

from typing import Optional

from ..config import Config
from ..ui.notify import show_popup
from ..core.audio import AudioConfig, AudioRecorder
from ..core.stt import STTConfig, STTEngine
from ..core.tts import TTSConfig, TTSEngine
from ..core.brain import Brain, BrainConfig
from ..core.router import Router


def build_components(config: Config):
    """
    Construct all core components from the config.
    """
    # Audio
    audio_cfg = AudioConfig(
        sample_rate=config.sample_rate,
        channels=config.audio_channels,
    )
    recorder = AudioRecorder(audio_cfg)

    # STT
    stt_cfg = STTConfig(
        model_name=config.stt_model_name,
        device=config.stt_device,
        compute_type=config.stt_compute_type,
        language=config.language,
    )
    stt_engine = STTEngine(stt_cfg)

    # TTS
    tts_cfg = TTSConfig()
    tts_engine = TTSEngine(tts_cfg)

    # Brain + Router
    brain_cfg = BrainConfig(
        backend=config.llm_backend,
        assistant_name=config.assistant_name,
    )
    brain = Brain(brain_cfg)
    router = Router(brain)

    return recorder, stt_engine, tts_engine, router


def run_basic_voice_loop(config: Optional[Config] = None) -> None:
    """
    Simple blocking loop:
    - Records fixed-length chunks
    - Transcribes
    - Routes to brain
    - Speaks reply
    - Stop when user says 'exit assistant' (or similar)
    """
    from ..config import load_config

    cfg = config or load_config()
    recorder, stt_engine, tts_engine, router = build_components(cfg)

    intro = (
        f"{cfg.assistant_name} voice loop started. "
        "Say something after the tone. Say 'exit assistant' to stop."
    )
    if cfg.response_mode.lower() == "popup":
        show_popup("E.C.H.O.", intro)
    else:
        tts_engine.speak(intro)

    while True:
        print("\n[Loop] Recording 4 seconds. Speak now...")
        audio = recorder.record(seconds=4.0)

        text, _score = stt_engine.transcribe(audio)
        if not text.strip():
            print("[Loop] No speech detected.")
            if cfg.response_mode.lower() == "popup":
                show_popup("E.C.H.O.", "I did not catch that. Please try again.")
            else:
                tts_engine.speak("I did not catch that. Please try again.")
            continue

        print(f"[Loop] You said: {text!r}")

        result = router.route(text)
        print(f"[Loop] Assistant reply: {result.reply!r}")

        if result.kind == "chat":
            if cfg.response_mode.lower() == "popup":
                show_popup("E.C.H.O.", result.reply)
            else:
                tts_engine.speak(result.reply)
        else:
            # control commands: silent
            pass

        if result.should_exit:
            if cfg.response_mode.lower() == "popup":
                show_popup("E.C.H.O.", "Goodbye.")
            else:
                tts_engine.speak("Goodbye.")
            break

    print("[Loop] Exiting voice loop.")
