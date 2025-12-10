"""
tts.py
Text-to-speech interface for Echo Assistant.

Responsibilities:
- Wrap the chosen TTS backend (initially: pyttsx3)
- Provide a simple function: speak(text: str) -> None
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pyttsx3


@dataclass
class TTSConfig:
    voice_name: Optional[str] = None   # e.g. "Microsoft Zira Desktop" (optional)
    rate: int = 180                    # words per minute
    volume: float = 1.0                # 0.0 to 1.0


class TTSEngine:
    def __init__(self, config: Optional[TTSConfig] = None) -> None:
        self.config = config or TTSConfig()
        self.engine = pyttsx3.init()

        # Apply basic settings
        self.engine.setProperty("rate", self.config.rate)
        self.engine.setProperty("volume", self.config.volume)

        if self.config.voice_name:
            for v in self.engine.getProperty("voices"):
                if self.config.voice_name.lower() in v.name.lower():
                    self.engine.setProperty("voice", v.id)
                    break

    def speak(self, text: str) -> None:
        if not text:
            return
        print(f"[TTS] Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()


def _demo_speak():
    """
    Demo 1: just speak a fixed line.
    Run with:
        python -m echo_assistant.core.tts
    """
    tts = TTSEngine()
    tts.speak("Hello. I am ECHO, your voice assistant.")


def _demo_roundtrip():
    """
    Demo 2: record -> STT -> TTS (echo back what you said).

    Run with:
        python -m echo_assistant.core.tts roundtrip
    """
    import sys
    from .audio import AudioConfig, AudioRecorder
    from .stt import STTConfig, STTEngine

    # 1. Setup components
    audio_cfg = AudioConfig(sample_rate=16_000, channels=1)
    recorder = AudioRecorder(audio_cfg)

    stt_cfg = STTConfig(
        model_name="small",   # change to "tiny" if your machine is weak
        device="cpu",
        compute_type="int8",
        language="en",
    )
    stt_engine = STTEngine(stt_cfg)

    tts_engine = TTSEngine()

    # 2. Record
    print("[Roundtrip Demo] Recording 4 seconds. Say something...")
    audio = recorder.record(seconds=4.0)

    # 3. STT
    text, _score = stt_engine.transcribe(audio)
    if not text:
        print("[Roundtrip Demo] No text recognized.")
        tts_engine.speak("I did not catch that.")
        sys.exit(0)

    print("[Roundtrip Demo] You said:", repr(text))

    # 4. TTS
    tts_engine.speak(f"You said: {text}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "roundtrip":
        _demo_roundtrip()
    else:
        _demo_speak()
