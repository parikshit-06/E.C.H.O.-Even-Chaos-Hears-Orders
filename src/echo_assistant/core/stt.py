"""
stt.py
Speech-to-text interface for Echo Assistant.

Responsibilities:
- Wrap the chosen STT backend (initially: local Whisper via faster-whisper)
- Provide a simple function: transcribe(audio: np.ndarray) -> str
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from faster_whisper import WhisperModel


@dataclass
class STTConfig:
    model_name: str = "small"    # "tiny", "base", "small", "medium", etc.
    device: str = "cpu"          # "cpu" or "cuda"
    compute_type: str = "int8"   # "int8" / "int8_float32" / "float16" / "float32"
    language: str = "en"         # Forcing language speeds things up.


class STTEngine:
    def __init__(self, config: Optional[STTConfig] = None) -> None:
        self.config = config or STTConfig()
        print(f"[STT] Loading Whisper model '{self.config.model_name}' on {self.config.device}...")
        self.model = WhisperModel(
            self.config.model_name,
            device=self.config.device,
            compute_type=self.config.compute_type,
        )
        print("[STT] Model loaded.")

    def transcribe(self, audio: np.ndarray) -> Tuple[str, float]:
        """
        Transcribe a mono 16kHz float32 numpy array.

        Returns:
            text (str), avg_logprob (float or NaN if not available)
        """
        # faster-whisper expects either a path or a numpy array (float32, mono)
        segments, info = self.model.transcribe(
            audio,
            language=self.config.language,
            beam_size=5,
            vad_filter=True,  # helps ignore silence
        )

        texts = []
        for seg in segments:
            texts.append(seg.text)

        full_text = " ".join(t.strip() for t in texts).strip()

        avg_logprob = getattr(info, "avg_logprob", float("nan"))
        print(f"[STT] Transcription: '{full_text}'")
        print(f"[STT] Avg logprob: {avg_logprob}")

        return full_text, avg_logprob


def _demo_record_and_transcribe():
    """
    Demo: record audio using AudioRecorder, then transcribe with Whisper.
    Run with:
        python -m echo_assistant.core.stt
    """
    from .audio import AudioConfig, AudioRecorder  # local import to avoid circular deps

    # 1. Record
    audio_cfg = AudioConfig(sample_rate=16_000, channels=1)
    recorder = AudioRecorder(audio_cfg)

    print("[Demo] Recording 4 seconds. Speak clearly...")
    audio = recorder.record(seconds=4.0)

    # 2. STT
    stt_cfg = STTConfig(
        model_name="small",   # use "tiny" if your laptop is weak
        device="cpu",         # "cuda" if you have a GPU + CUDA set up
        compute_type="int8",  # int8 is lighter on CPU
        language="en",
    )
    engine = STTEngine(stt_cfg)
    text, score = engine.transcribe(audio)

    print("[Demo] Final text:", repr(text))


if __name__ == "__main__":
    _demo_record_and_transcribe()
