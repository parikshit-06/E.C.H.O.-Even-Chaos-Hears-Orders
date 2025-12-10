"""
audio.py
Low-level audio recording utilities for Echo Assistant.

Responsibilities:
- Interact with the system microphone
- Record short clips of audio
- Return audio as numpy arrays (float32, mono)
- (Optional) Save audio to .wav for debugging
"""

from __future__ import annotations

import wave
from dataclasses import dataclass
from typing import Optional

import numpy as np
import sounddevice as sd


@dataclass
class AudioConfig:
    sample_rate: int = 16_000   # 16 kHz, good for speech + Whisper later
    channels: int = 1           # mono is enough for voice
    device: Optional[int] = None  # can be index or None for default


class AudioRecorder:
    def __init__(self, config: Optional[AudioConfig] = None) -> None:
        self.config = config or AudioConfig()

    def record(self, seconds: float) -> np.ndarray:
        """
        Record audio from the default input device for `seconds` seconds.

        Returns:
            np.ndarray of shape (num_samples,) with dtype float32, mono.
        """
        sr = self.config.sample_rate
        ch = self.config.channels

        print(f"[Audio] Recording {seconds:.2f}s at {sr} Hz, channels={ch} ...")

        audio = sd.rec(
            int(seconds * sr),
            samplerate=sr,
            channels=ch,
            dtype="float32",
            device=self.config.device,
        )
        sd.wait()  # block until finished

        # audio shape: (num_samples, channels); we force mono 1D
        audio = audio.squeeze()
        print(f"[Audio] Recorded shape: {audio.shape}, dtype: {audio.dtype}")

        return audio

    @staticmethod
    def save_wav(path: str, audio: np.ndarray, sample_rate: int) -> None:
        """
        Save mono float32 audio in range [-1, 1] as 16-bit PCM WAV.
        """
        # clip to [-1, 1] then scale to int16
        audio_clipped = np.clip(audio, -1.0, 1.0)
        pcm16 = (audio_clipped * 32767).astype(np.int16)

        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(sample_rate)
            wf.writeframes(pcm16.tobytes())

        print(f"[Audio] Saved WAV to {path}")


def _demo_record_and_save():
    """
    Small demo: record 3 seconds and save to 'test_recording.wav'.
    Run with:
        python -m echo_assistant.core.audio
    """
    cfg = AudioConfig(sample_rate=16_000, channels=1)
    recorder = AudioRecorder(cfg)

    audio = recorder.record(seconds=3.0)
    AudioRecorder.save_wav("test_recording.wav", audio, cfg.sample_rate)
    print("[Audio Demo] Done. Check 'test_recording.wav' in your current directory.")


if __name__ == "__main__":
    _demo_record_and_save()
